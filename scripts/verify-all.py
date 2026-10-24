# -*- coding: utf-8 -*-
"""verify-all — 机验门禁总入口（2026-10-23 M6 立，P0 版四步；gen/spec-audit 属后续批次）
用法: python scripts/verify-all.py
步骤: [1/4] build 重建逐字节一致（node build-chassis.mjs；无 node 时 SKIP 不判败）
      [2/4] 正样本全绿（samples/good，双脚本 exit 0）
      [3/4] 负样本全红且命中标记（由 samples/patches.json 现场生成 → expected.json 逐条比对，含单引号 .sq 双写法）
      [4/4] 旧术语零命中（硬门禁/命中即 FAIL/字号白名单——F4 回归锚点）
任何一步失败 → 总 exit 1。绿色必须能被证明是「看见了没事」，不是「没看见」。
expected.json 每项: {"check-deck.py"|"verify-consistency.py": {"exit": 0|1, "any": [输出须含的关键词]}}。"""
import json, os, re, shutil, subprocess, sys, tempfile

sys.stdout.reconfigure(encoding="utf-8")
PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(PKG, "samples")
results, n_fail = [], 0


def step(name, ok, detail=""):
    global n_fail
    if not ok:
        n_fail += 1
    results.append(("[PASS]" if ok else "[FAIL]") + " " + name + ((" — " + detail) if detail else ""))


# ── [1/4] build 重建逐字节一致 ──
chassis = os.path.join(PKG, "assets", "chassis-v2.html")
if shutil.which("node"):
    before = open(chassis, "rb").read()
    r = subprocess.run(["node", os.path.join(PKG, "scripts", "build-chassis.mjs")],
                       capture_output=True, text=True, shell=False)
    after = open(chassis, "rb").read()
    if before != after:   # 无论如何恢复现场，差异已在比对中暴露
        open(chassis, "wb").write(before)
    step("build 重建逐字节一致", r.returncode == 0 and before == after,
        "" if (r.returncode == 0 and before == after) else "build exit %d / 一致 %s / %s"
        % (r.returncode, before == after, (r.stdout or r.stderr or "")[-120:]))
else:
    step("build 重建逐字节一致", True, "SKIP（本机无 node）")

# ── [2/4] 正样本全绿 ──
goods = sorted(f for f in os.listdir(os.path.join(SAMPLES, "good")) if f.endswith(".html"))
for f in goods:
    for sc in ("verify-consistency.py", "check-deck.py"):
        r = subprocess.run([sys.executable, os.path.join(PKG, "scripts", sc),
                            os.path.join(SAMPLES, "good", f)], capture_output=True, text=True)
        step("good/%s × %s 全绿" % (f, sc.split(".")[0]), r.returncode == 0,
             "exit %d" % r.returncode if r.returncode else "")

# ── [3/4] 负样本按 expected 逐条比对 ──
# 负样本不随包分发全文：由基座 + samples/patches.json 现场生成到临时目录（逐份 sha256 自证），
# 生成物不写包目录；基座与补丁不符时 build 会主动中止，这里如实记红。
exp = json.load(open(os.path.join(SAMPLES, "expected.json"), encoding="utf-8"))
bad_dir = None
try:
    sys.path.insert(0, SAMPLES)
    import build_samples
    bad_dir = build_samples.build(tempfile.mkdtemp(prefix="deck-samples-"))
except (SystemExit, Exception) as e:
    step("负样本现场生成（基座 + patches.json）", False, str(e).replace("\n", " ")[:140])
for f, wants in (sorted(exp.items()) if bad_dir else []):
    p = os.path.join(bad_dir, f)
    if not os.path.exists(p):
        step("bad/%s 存在" % f, False, "文件缺失")
        continue
    for sc, want in wants.items():
        r = subprocess.run([sys.executable, os.path.join(PKG, "scripts", sc), p],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = (r.stdout or "") + (r.stderr or "")
        ok = r.returncode == want.get("exit", 1)
        miss = [k for k in want.get("any", []) if k not in out]
        if miss:
            ok = False
        step("bad/%s × %s（exit %d%s）" % (f, sc.split(".")[0], want.get("exit", 1),
             " 含「%s」" % "／".join(want.get("any", [])) if want.get("any") else ""),
             ok, "" if ok else "实际 exit %d / 漏「%s」/ %s" % (r.returncode, "、".join(miss), out.strip().splitlines()[-1][:80] if out.strip() else ""))

# ── [4/4] 旧术语零命中（F4 回归锚点）──
pat = re.compile(r"硬门禁|命中即 FAIL|字号白名单")
hits = []
for root, _d, files in os.walk(PKG):
    if "samples" in root or "node_modules" in root:
        continue
    for f in files:
        if f.endswith((".md",)):
            for i, line in enumerate(open(os.path.join(root, f), encoding="utf-8", errors="replace"), 1):
                if pat.search(line):
                    hits.append("%s:%d" % (os.path.relpath(os.path.join(root, f), PKG), i))
step("旧术语零命中（硬门禁/命中即 FAIL/字号白名单）", not hits, "、".join(hits[:4]) if hits else "")

if bad_dir:
    shutil.rmtree(bad_dir, ignore_errors=True)   # 现场生成的负样本用完即弃，不留痕迹

print("=" * 78)
print("\n".join(results))
print("=" * 78)
total = len(results)
print("verify-all：%d/%d 步通过 → %s" % (total - n_fail, total, "PASS" if n_fail == 0 else "FAIL（%d 步红）" % n_fail))
sys.exit(1 if n_fail else 0)
