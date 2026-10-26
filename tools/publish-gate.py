# -*- coding: utf-8 -*-
"""发布门禁：一条命令跑完全部核对，全绿才准发 SkillHub。

用法：
  python tools/publish-gate.py --peer <安装位> --material <物料> --zip <生成/slides_版本.zip>

检查项（任一 FAIL 即整体不准发）：
  G1 check-version 四值同源（C1-C8 全过）
  G2 仓库 ↔ 安装位 内容零差异（samples/__pycache__ 等运行残留除外）
  G3 包内条目数与 zip 实际一致（防发旧包/错包）
  G4 禁入项扫描：CHANGELOG / samples / tools / .backups / .bak / 本机绝对路径
  G5 frontmatter 版本 == zip 文件名版本
输出：每项 PASS/FAIL + 最终一行「✅ 可发布」或「❌ 不准发：原因」
"""
import argparse, hashlib, os, re, subprocess, sys, zipfile

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESIDUE = {".backups"}

results = []


def add(ok, name, detail=""):
    results.append((ok, name, detail))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--peer", required=True, help="安装位目录")
    ap.add_argument("--material", required=True, help="发布物料 md")
    ap.add_argument("--zip", required=True, help="待发布的 zip 路径")
    a = ap.parse_args()

    # G1 check-version 四值同源
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "check-version.py"),
                        "--peer", a.peer, "--material", a.material, "--target", "both"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=ROOT, timeout=180)
    ok = "PASS（四值同源）" in (r.stdout or "")
    fails = [l.strip() for l in (r.stdout or "").splitlines() if "FAIL" in l]
    add(ok, "G1 版本四值同源（check-version）", "；".join(fails) if fails else "")

    # G2 仓库 ↔ 安装位 内容零差异
    diffs = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", ".backups", "__pycache__")]
        for f in files:
            rel = os.path.relpath(os.path.join(base, f), ROOT).replace("\\", "/")
            if rel.startswith("samples/") and f.endswith(".pyc"):
                continue
            p2 = os.path.join(a.peer, rel)
            if not os.path.isfile(p2):
                diffs.append("仅仓库有: " + rel)
            elif _h(os.path.join(base, f)) != _h(p2):
                diffs.append("内容不同: " + rel)
    for base, dirs, files in os.walk(a.peer):
        dirs[:] = [d for d in dirs if d not in (".git", ".backups", "__pycache__")]
        for f in files:
            rel = os.path.relpath(os.path.join(base, f), a.peer).replace("\\", "/")
            if rel.startswith("samples/") and f.endswith(".pyc"):
                continue
            if not os.path.isfile(os.path.join(ROOT, rel)):
                diffs.append("仅安装位有: " + rel)
    add(not diffs, "G2 仓库 ↔ 安装位 内容一致", "；".join(diffs[:6]) + ("…共 %d 处" % len(diffs) if len(diffs) > 6 else ""))

    # G5 版本号 == zip 文件名版本
    fm = open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
    m = re.search(r"^version:\s*(\S+)", fm, re.M)
    ver = m.group(1) if m else "?"
    zipname = "generating-slides_%s.zip" % ver
    add(os.path.basename(a.zip) == zipname, "G5 zip 文件名与版本匹配",
        "" if os.path.basename(a.zip) == zipname else "文件名 %s ≠ 预期 %s" % (os.path.basename(a.zip), zipname))

    if not os.path.isfile(a.zip):
        add(False, "G3/G4 包文件存在", "zip 不存在：%s" % a.zip)
        _report(ver, None)
        return
    z = zipfile.ZipFile(a.zip)
    names = z.namelist()

    # G3 条目数与包目录一致
    pkg = os.path.join(os.path.dirname(a.zip), "pkg-%s" % ver)
    n_pkg = 0
    for base, dirs, files in os.walk(pkg):
        dirs[:] = [d for d in dirs if d not in (".git", ".backups", "__pycache__")]
        n_pkg += len(files)
    add(len(names) == n_pkg, "G3 zip 条目数 == 派生目录文件数",
        "zip %d ≠ 派生 %d" % (len(names), n_pkg) if len(names) != n_pkg else "")

    # G4 禁入项扫描
    banned_prefix = ("samples/", "tools/", ".backups/", "__pycache__/")
    banned_name = ("CHANGELOG.md",)
    hits = []
    for n in names:
        if any(n.startswith(p) for p in banned_prefix) or os.path.basename(n) in banned_name:
            hits.append(n)
        if n.endswith((".bak", ".pyc", ".log")):
            hits.append(n)
        body = z.read(n)
        if b"D:\\CLAUDE" in body or b"D:/CLAUDE" in body or b"C:\\Users\\" in body:
            hits.append(n + " (含本机路径)")
    add(not hits, "G4 禁入项扫描（维护日志/样本/备份/本机路径）", "；".join(hits[:6]) + ("…共 %d" % len(hits) if len(hits) > 6 else ""))

    _report(ver, a.zip)


def _h(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def _report(ver, zip_path):
    print("=" * 60)
    for ok, name, detail in results:
        print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, ("　" + detail) if detail else ""))
    print("=" * 60)
    if zip_path and os.path.isfile(zip_path):
        b = open(zip_path, "rb").read()
        print("zip: %.1f KB / %s 条目 / MD5 %s" % (len(b) / 1024, len(zipfile.ZipFile(zip_path).namelist()),
                                                   hashlib.md5(b).hexdigest()))
    bad = [r for r in results if not r[0]]
    if bad:
        print("❌ 不准发：%d 项未过（见上）" % len(bad))
        sys.exit(1)
    print("✅ 可发布：版本 %s" % ver)


if __name__ == "__main__":
    main()
