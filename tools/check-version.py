#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-version — 发版前仓库级版本一致性检查（纯标准库，零依赖）

为什么单独成脚本：版本号散落在 SKILL.md frontmatter、README 更新记录、
README_en Changelog、git tag、发布物料、派生包/安装位六处，人工对一遍必漏；
漏了不会当场报错，会等到上架后才发现「对外说 1.0.0、包内写 1.6.1」。

用法:
  python tools/check-version.py                      # 检查脚本所在仓库
  python tools/check-version.py <技能包目录>          # 检查指定目录
  python tools/check-version.py --peer <另一副本>     # 追加对账安装位/派生包
  python tools/check-version.py --material <物料.md>  # 追加对账发布物料
  python tools/check-version.py --target openplatform # 追加开放平台必填字段

检查项:
  C1 frontmatter 可解析 + 必备字段齐全（--target openplatform 追加双语描述）
  C2 README「更新记录」最高版本 == frontmatter version（另比对最新日期条目）
  C3 README_en「Changelog」最高版本 == frontmatter version（文件存在时）
  C4 git tag 不得高于包内版本（有 .git 时；当前版本无 tag 只提示）
  C5 git 工作区干净（有 .git 时）
  C6 slug == name == 目录名（平台按目录名安装）
  C7 --peer 副本版本一致
  C8 --material 发布物料版本一致

退出码：全过 0，任一 FAIL 1。
"""
import argparse
import os
import re
import subprocess
import sys

SEMVER = re.compile(r"(\d+)\.(\d+)\.(\d+)")
CORE_FIELDS = ["name", "slug", "displayName", "version", "author",
               "license", "summary", "description", "tags"]
OPEN_FIELDS = ["description_zh", "description_en"]
results = []


def add(level, name, detail=""):
    results.append((level, name, detail))


def unq(v):
    v = (v or "").strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v


def parse_frontmatter(path):
    if not os.path.isfile(path):
        return None
    text = open(path, encoding="utf-8", errors="replace").read()
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if mm:
            fm[mm.group(1)] = unq(mm.group(2))
    return fm


def slice_section(text, title):
    m = re.search(r"^##\s*" + re.escape(title) + r"\s*$(.*?)(?=^##\s|\Z)",
                  text, re.S | re.M)
    return m.group(1) if m else None


def max_ver(block):
    if not block:
        return None
    found = [tuple(int(x) for x in m.groups()) for m in SEMVER.finditer(block)]
    return max(found) if found else None


def ver(s):
    m = SEMVER.search(s or "")
    return tuple(int(x) for x in m.groups()) if m else None


def fmt(v):
    return "%d.%d.%d" % v if v else "—"


def git(root, *args):
    try:
        r = subprocess.run(["git", "-C", root] + list(args), capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except OSError:
        return 127, "", "git 不可用"


def readme_version(root, name="README.md", title="更新记录"):
    p = os.path.join(root, name)
    if not os.path.isfile(p):
        return None, False
    block = slice_section(open(p, encoding="utf-8", errors="replace").read(), title)
    return max_ver(block), block is not None


def main():
    ap = argparse.ArgumentParser(description="发版前仓库级版本一致性检查")
    ap.add_argument("path", nargs="?",
                    default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="技能包目录（默认脚本上一级）")
    ap.add_argument("--peer", help="另一副本目录（安装位/派生包），对账其版本")
    ap.add_argument("--material", help="发布物料 .md，对账其 version 字段")
    ap.add_argument("--target", choices=["skillhub", "openplatform", "both"],
                    default="skillhub", help="目标平台，决定追加校验哪些字段")
    a = ap.parse_args()

    root = os.path.abspath(a.path)
    print("技能包：%s" % root)
    print("目标平台：%s" % a.target)
    print()

    # ── C1 frontmatter ──
    fm = parse_frontmatter(os.path.join(root, "SKILL.md"))
    if not fm:
        add("FAIL", "C1 frontmatter 可解析", "SKILL.md 缺失或无 --- 块")
        fm = {}
    else:
        missing = [k for k in CORE_FIELDS if not fm.get(k)]
        add("FAIL" if missing else "PASS",
            "C1 frontmatter 必备字段（%d 项）" % len(CORE_FIELDS),
            "缺 %s" % "、".join(missing) if missing else "")
        if a.target in ("openplatform", "both"):
            miss2 = [k for k in OPEN_FIELDS if not fm.get(k)]
            add("FAIL" if miss2 else "PASS",
                "C1b 开放平台必填双语描述",
                "缺 %s（开放平台表单会空）" % "、".join(miss2) if miss2 else "")
        if not fm.get("copyright"):
            add("WARN", "C1c copyright 字段",
                "缺（署名分工要求 metadata.copyright = 版权人；当前由 LICENSE/NOTICE/SKILL.md 承担）")

    cur = ver(fm.get("version"))
    if not cur:
        add("FAIL", "C1d version 可解析", "读不到 X.Y.Z：%r" % fm.get("version"))

    # ── C2 README 更新记录 ──
    rv, has_sec = readme_version(root)
    if not has_sec:
        add("FAIL", "C2 README「更新记录」节存在", "找不到 ## 更新记录")
    elif not rv:
        add("FAIL", "C2 README 更新记录含版本号", "节内无 X.Y.Z")
    else:
        add("PASS" if rv == cur else "FAIL",
            "C2 README 更新记录最高版本 == frontmatter",
            "" if rv == cur else "README %s ≠ 包内 %s" % (fmt(rv), fmt(cur)))

    # ── C3 README_en Changelog ──
    ev, has_en = readme_version(root, "README_en.md", "Changelog")
    if not os.path.isfile(os.path.join(root, "README_en.md")):
        add("SKIP", "C3 README_en Changelog", "无该文件（平台包不含，正常）")
    elif not has_en:
        add("WARN", "C3 README_en Changelog", "有文件但无 ## Changelog 节")
    elif not ev:
        add("WARN", "C3 README_en Changelog", "节内无 X.Y.Z")
    else:
        add("PASS" if ev == cur else "FAIL",
            "C3 README_en Changelog 最高版本 == frontmatter",
            "" if ev == cur else "README_en %s ≠ 包内 %s（英文版落后）" % (fmt(ev), fmt(cur)))

    # ── C4 / C5 git ──
    has_git = os.path.isdir(os.path.join(root, ".git"))
    tag_max = None
    if not has_git:
        add("SKIP", "C4 git tag 不高于包内版本", "无 .git（安装位/派生包，正常）")
        add("SKIP", "C5 git 工作区干净", "无 .git")
    else:
        rc, out, _ = git(root, "tag", "-l")
        tags = [t for t in out.splitlines() if t.strip()]
        tvers = [(ver(t), t) for t in tags if ver(t)]
        if tvers:
            tag_max = max(tvers, key=lambda x: x[0])
        if not tags:
            add("WARN", "C4 git tag", "仓库无任何 tag，发版时补 v<version>")
        elif tag_max and cur and tag_max[0] > cur:
            add("FAIL", "C4 git tag 不高于包内版本",
                "tag %s 高于包内 %s（版本号回退）" % (tag_max[1], fmt(cur)))
        else:
            note = ""
            if cur and ("v" + fmt(cur)) not in tags:
                note = "当前版本尚无 tag（发版时补 v%s）" % fmt(cur)
            add("PASS", "C4 git tag 不高于包内版本",
                note if note else "最大 %s" % tag_max[1])
        rc, out, _ = git(root, "status", "--porcelain")
        add("PASS" if not out else "FAIL", "C5 git 工作区干净",
            "" if not out else "%d 项未提交（发版须可复现）" % len(out.splitlines()))

    # ── C6 命名一致 ──
    base = os.path.basename(root.rstrip("\\/"))
    name, slug = fm.get("name"), fm.get("slug")
    bad = [s for s, v in (("name", name), ("slug", slug)) if v and v != base]
    if name and slug and name != slug:
        bad.append("name≠slug")
    add("FAIL" if bad else "PASS", "C6 slug == name == 目录名",
        "不一致：%s（目录 %s）" % ("、".join(bad), base) if bad else "")

    # ── C7 peer ──
    pv = None
    if a.peer:
        pf = parse_frontmatter(os.path.join(os.path.abspath(a.peer), "SKILL.md"))
        pv = ver((pf or {}).get("version"))
        if not pf:
            add("FAIL", "C7 --peer 可读", "对账目录无 SKILL.md：%s" % a.peer)
        else:
            add("PASS" if pv == cur else "FAIL",
                "C7 --peer 版本一致",
                "" if pv == cur else "本包 %s ≠ 对账副本 %s" % (fmt(cur), fmt(pv)))

    # ── C8 material ──
    mv = None
    if a.material:
        mp = os.path.abspath(a.material)
        if not os.path.isfile(mp):
            add("FAIL", "C8 --material 可读", "文件不存在：%s" % a.material)
        else:
            mv = None
            for line in open(mp, encoding="utf-8", errors="replace"):
                if re.search(r"version", line, re.I):
                    mv = ver(line)
                    if mv:
                        break
            if not mv:
                add("FAIL", "C8 --material 含 version", "物料里找不到 X.Y.Z")
            else:
                add("PASS" if mv == cur else "FAIL", "C8 发布物料版本一致",
                    "" if mv == cur else "物料 %s ≠ 包内 %s" % (fmt(mv), fmt(cur)))

    # ── 注册表 ──
    print("版本注册表")
    rows = [("SKILL.md frontmatter", cur),
            ("README 更新记录", rv),
            ("README_en Changelog", ev),
            ("git tag 最大", tag_max[0] if tag_max else None),
            ("对账副本（peer）", pv),
            ("发布物料", mv)]
    for k, v in rows:
        print("  %-22s %s" % (k, fmt(v)))
    print()

    # ── 结论 ──
    order = {"FAIL": 0, "WARN": 1, "PASS": 2, "SKIP": 3}
    for lv, nm, dt in sorted(results, key=lambda r: order[r[0]]):
        print("[%s] %s%s" % (lv, nm, (" — " + dt) if dt else ""))
    nf = sum(1 for r in results if r[0] == "FAIL")
    nw = sum(1 for r in results if r[0] == "WARN")
    print()
    print("结论：%s%s" % ("PASS（四值同源）" if nf == 0 else "FAIL（%d 项需处理）" % nf,
                        "" if nw == 0 else "／%d 项提示" % nw))
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
