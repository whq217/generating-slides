#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从本仓库（唯一真源）派生「技能市场」分发包。

本仓库是 generating-slides 的唯一真源。技能市场（SkillHub）对包的要求与 GitHub
有 4 处硬差异，手工维护两份必然漂移，故用本脚本按规则单向派生：

  GitHub 侧独有 / 平台侧不允许      → 派生时处理
  ─────────────────────────────────────────────────────────────
  LICENSE（平台拒收该文件类型）      → 不打包；MIT 声明由 SKILL.md《来源与许可》承担
  NOTICE（署名与第三方声明）         → 不打包；内容已在 SKILL.md 与 README 致谢
  .gitattributes（换行锁 LF）        → 不打包；平台以 zip 分发，不经 git 转换
  .gitignore                        → 不打包
  README_en.md（英文说明）           → 不打包；中文 README 里那条语言切换行一并去掉
  tools/（发布辅助脚本）             → 不打包；属仓库基建，不是技能内容

  README 中随渠道变化的两节          → 按下面的模板重写
  「## 安装」                        → 平台版（复制目录 / 市场安装），去掉 git clone 步骤
  「## 许可证」                      → 指向 SKILL.md 文末，不引用 LICENSE / NOTICE

其余一律原样搬运，不做任何改写——所以两边不会漂移：改真源，重跑脚本即可。

用法：
  python tools/build_platform_pkg.py                     # 派生到 ../pkg-<version>/
  python tools/build_platform_pkg.py --out <输出目录>
  python tools/build_platform_pkg.py --verify            # 派生后跑 scripts/verify-all.py
  python tools/build_platform_pkg.py --check-only <目录> # 只体检已派生的包，不重建

体检项（任一不过即 exit 1）：
  1. 无 GitHub 专属文件残留
  2. README 无失效相对链接
  3. README/SKILL 无指向已剥离文件的引用
  4. 无已删除功能的残余说明（N 键提词面板）
  5. 目录树无 tools/ 及其子项
  6. SKILL.md 含 MIT 声明（LICENSE 不随包时的唯一载体）
"""

import argparse
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)  # 仓库根 = 真源

# ── 不进入平台包的文件 / 目录（相对仓库根的 POSIX 路径或文件名）─────────────
EXCLUDE_FILES = {
    "LICENSE",           # 平台拒收该文件类型
    "NOTICE",            # 署名声明已在 SKILL.md / README
    ".gitattributes",    # 平台 zip 分发，不经 git 换行转换
    ".gitignore",
    "README_en.md",      # 英文说明只服务 GitHub 访客, "CHANGELOG.md"}
EXCLUDE_DIRS = {".git", "tools", "bad", "samples", "__pycache__", ".idea", ".vscode", ".pytest_cache", ".backups"}
EXCLUDE_EXT = {".pyc", ".pyo", ".orig", ".rej", ".swp", ".tmp", ".log", ".bak"}
EXCLUDE_NAMES = {".DS_Store", "Thumbs.db"}

# ── README 两节按渠道重写的模板 ───────────────────────────────────────────
INSTALL_PLATFORM = """装到 Claude Code 的 skills 目录，**目录名必须是 `generating-slides`**（与 SKILL.md 的 `name` 一致）。

从技能市场安装无需手动操作；若拿到的是 ZIP，解压后整目录复制，确保文件夹名为 `generating-slides`：

```bash
cp -r generating-slides ~/.claude/skills/generating-slides
```

Windows PowerShell：

```powershell
Copy-Item -Recurse -Force .\\generating-slides "$env:USERPROFILE\\.claude\\skills\\generating-slides"
```
"""

LICENSE_PLATFORM = """MIT License。本包经技能市场分发，不随包附带许可文件；许可全文、上游版权声明与第三方署名见 [SKILL.md](SKILL.md) 文末《来源与许可》。
"""

# 目录树里需要整行（或整棵子树）去掉的条目
TREE_DROP_FILES = {"LICENSE", "NOTICE", ".gitattributes", ".gitignore", "README_en.md"}
TREE_DROP_DIRS = {"tools", "samples"}


def read_version(root):
    p = os.path.join(root, "SKILL.md")
    with open(p, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    fm = m.group(1)
    mm = re.search(r"^version:\s*(.+)$", fm, re.M)
    return mm.group(1).strip().strip('"\'') if mm else None


def _tree_prefix_len(line):
    """目录树行的前置框线宽度，用于判断层级。"""
    n = 0
    while n < len(line) and line[n] in " │├└─":
        n += 1
    return n


def _tree_name(line):
    """从目录树行里取出文件名/目录名（去注释、去斜杠）。"""
    body = line.lstrip(" │├└─").strip()
    body = body.split("#")[0].strip()
    return body.rstrip("/").strip()


def rewrite_readme(text):
    """把 GitHub 版 README 改写为平台版。返回 (新文本, 操作记录)。"""
    ops = []
    lines = text.splitlines()

    # 1) 去掉引用 README_en.md 的行（顶部语言切换）
    out = []
    for ln in lines:
        if "README_en.md" in ln and not ln.lstrip().startswith(("├", "└", "│")):
            ops.append("README: 去掉顶部语言切换行")
            continue
        out.append(ln)
    lines = out

    # 2) 目录树：去掉专属文件行与被排除的子树
    out = []
    in_fence = False
    drop_depth = None  # 正在丢弃的子树的前缀宽度
    for ln in lines:
        if ln.startswith("```"):
            in_fence = not in_fence
            out.append(ln)
            drop_depth = None
            continue
        if in_fence and re.search(r"[├└]", ln):
            plen = _tree_prefix_len(ln)
            if drop_depth is not None and plen > drop_depth:
                continue  # 子树内的行
            if drop_depth is not None and plen <= drop_depth:
                drop_depth = None
            name = _tree_name(ln)
            if name in TREE_DROP_FILES:
                ops.append("README 目录树: 去掉 %s" % name)
                continue
            if name in TREE_DROP_DIRS:
                ops.append("README 目录树: 去掉 %s/ 及其子项" % name)
                drop_depth = plen
                continue
            out.append(ln)
            continue
        out.append(ln)
    lines = out

    # 3) 目录树末项收口：只处理「顶层最后一个条目」，并把它下面的 │ 缩进改成空格
    in_fence = False
    top_idx = []  # 顶层条目行号（行首直接是 ├── 或 └──）
    for i, ln in enumerate(lines):
        if ln.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence and (ln.startswith("├── ") or ln.startswith("└── ")):
            top_idx.append(i)
    if top_idx:
        last = top_idx[-1]
        if lines[last].startswith("├── "):
            lines[last] = lines[last].replace("├──", "└──", 1)
            # 该条目的子级仍在用 │ 前缀，改成纯空格，避免出现「└── 后面还挂 │」的错树
            k = last + 1
            while k < len(lines) and not lines[k].startswith("```"):
                if lines[k].startswith("│   "):
                    lines[k] = "    " + lines[k][4:]
                k += 1
            ops.append("README 目录树: 末项收口改 └── 并对齐子级缩进")

    # 4) 去掉「GitHub 存档」引用块（指向本仓库标签）
    out = []
    skipping = False
    for ln in lines:
        if ln.startswith("> **GitHub 存档**"):
            skipping = True
            ops.append("README: 去掉「GitHub 存档」引用块")
            continue
        if skipping:
            if ln.startswith(">"):
                continue
            skipping = False
        out.append(ln)
    lines = out

    # 4b) 去掉「维护者与二次开发」整节（含机验 / 真源地图 / 包内结构三小节）
    #     平台包已剥离 samples/ 与 tools/，这三节引用的都是仓库侧资产，对终端用户无意义
    _blob = "\n".join(lines)
    _pat_maint = re.compile(r"^## 维护者与二次开发\s*$.*?(?=^## |\Z)", re.S | re.M)
    if _pat_maint.search(_blob):
        lines = _pat_maint.sub("", _blob, count=1).splitlines()
        ops.append("README: 去掉「维护者与二次开发」整节")

    # 4c) 去掉「与 v1 的关系」节
    #     平台侧从首版（1.0.0）起就是 v2 内核，用户从未见过 v1；该节的「不删除」说的是仓库标签行为，
    #     包内既无 v1 也无从验证——属跨载体残留，不随包分发
    _blob = "\n".join(lines)
    _pat_v1 = re.compile(r"^## 与 v1 的关系\s*$.*?(?=^## |\Z)", re.S | re.M)
    if _pat_v1.search(_blob):
        lines = _pat_v1.sub("", _blob, count=1).splitlines()
        ops.append("README: 去掉「与 v1 的关系」节（平台侧无 v1）")

    # 4d) 压缩「更新记录」节
    #     平台自带「版本历史」页，README 再列一遍是重复；且逐版条目全是维护者语言
    #     （DSH 必修 / samples 补丁化 / 字节数瘦身），对使用者无意义。
    #     只保留「仍在维护」这一个有用信号，且不写死版本号与日期，避免过期。
    _blob = "\n".join(lines)
    _pat_chg = re.compile(r"^## 更新记录\s*$.*?(?=^## |\Z)", re.S | re.M)
    if _pat_chg.search(_blob):
        _blob = _pat_chg.sub(
            "## 更新记录\n\n持续更新中。逐版明细见平台的「版本历史」页，或仓库的 `git log`。\n\n",
            _blob, count=1)
        lines = _blob.splitlines()
        ops.append("README: 压缩「更新记录」节（平台自带版本历史页）")

    # 5) 按节重写「安装」与「许可证」
    text = "\n".join(lines) + "\n"
    for title, body, key in (
        ("## 安装", INSTALL_PLATFORM, "安装"),
        ("## 许可证", LICENSE_PLATFORM, "许可证"),
    ):
        pat = re.compile(r"(" + re.escape(title) + r"\n)(.*?)(?=\n## |\n---\n|\Z)", re.S)
        if not pat.search(text):
            raise SystemExit("README 结构变动：找不到「%s」节，无法派生" % title)
        text = pat.sub(lambda m: m.group(1) + "\n" + body, text, count=1)
        ops.append("README: 重写「%s」节（平台版）" % key)

    # 6) 收掉改写后可能出现的连续空行
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, ops


def copy_tree(dst):
    copied = 0
    for dp, dn, fn in os.walk(SRC):
        rel_dir = os.path.relpath(dp, SRC).replace("\\", "/")
        if rel_dir == ".":
            rel_dir = ""
        dn[:] = [d for d in dn if d not in EXCLUDE_DIRS]
        for f in fn:
            if f in EXCLUDE_FILES or f in EXCLUDE_NAMES:
                continue
            if os.path.splitext(f)[1].lower() in EXCLUDE_EXT:
                continue
            rel = (rel_dir + "/" + f) if rel_dir else f
            target = os.path.join(dst, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy2(os.path.join(dp, f), target)
            copied += 1
    return copied


def check(root):
    """体检已派生的平台包。返回 (错误列表, 提示列表)。"""
    errs, warns = [], []

    # 1) GitHub 专属文件残留
    for f in EXCLUDE_FILES:
        if os.path.exists(os.path.join(root, f)):
            errs.append("残留 GitHub 专属文件: %s" % f)
    if os.path.exists(os.path.join(root, "tools")):
        errs.append("残留仓库基建目录: tools/")
    if os.path.exists(os.path.join(root, ".git")):
        errs.append("包内含 .git 目录")

    # 2)(3)(4)(5) README / SKILL 文本检查
    md_files = []
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f.endswith(".md"):
                md_files.append(os.path.join(dp, f))

    for p in md_files:
        rel = os.path.relpath(p, root).replace("\\", "/")
        txt = open(p, encoding="utf-8").read()
        # 失效相对链接
        for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", txt):
            tgt = m.group(1).split("#")[0].strip()
            if not tgt or tgt.startswith(("http://", "https://", "mailto:")):
                continue
            base_dir = os.path.dirname(p)
            if not os.path.exists(os.path.normpath(os.path.join(base_dir, tgt))):
                errs.append("%s: 失效相对链接 → %s" % (rel, tgt))
        for lineno, line in enumerate(txt.splitlines(), 1):
            # 「已移除 / 不接受 / 迁出」属正当的历史陈述与条件分支，不算残留
            excused = any(k in line for k in ("不接受", "已移除", "移除", "迁出", "已废"))
            if any(t in line for t in ("README_en.md", "NOTICE")):
                errs.append("%s:%d 仍引用已剥离文件（README_en.md / NOTICE）" % (rel, lineno))
            if re.search(r"\[LICENSE\]|`LICENSE`|\.gitattributes", line) and not excused:
                errs.append("%s:%d 仍引用 LICENSE / .gitattributes" % (rel, lineno))
            if re.search(r"提词面板|\*\*N\*\*", line) and not excused:
                errs.append("%s:%d 仍有已删除的 N 键提词面板说明" % (rel, lineno))
            if re.search(r"[├└]──\s*tools/", line):
                errs.append("%s:%d 目录树仍列 tools/" % (rel, lineno))

    # 6) SKILL.md 必须承担 MIT 声明
    skill = os.path.join(root, "SKILL.md")
    if not os.path.exists(skill):
        errs.append("缺 SKILL.md")
    else:
        st = open(skill, encoding="utf-8").read()
        if "MIT" not in st or "来源与许可" not in st:
            errs.append("SKILL.md 未承担 MIT 声明（LICENSE 不随包时的唯一载体）")

    return errs, warns


def main():
    ap = argparse.ArgumentParser(description="从本仓库派生技能市场分发包")
    ap.add_argument("--out", help="输出目录（默认 ../pkg-<version>/）")
    ap.add_argument("--verify", action="store_true", help="派生后跑 scripts/verify-all.py")
    ap.add_argument("--check-only", metavar="DIR", help="只体检指定目录，不重建")
    args = ap.parse_args()

    if args.check_only:
        errs, _ = check(os.path.abspath(args.check_only))
        print("体检目录:", args.check_only)
        if errs:
            print("FAIL（%d 项）:" % len(errs))
            for e in errs:
                print("  ✗", e)
            return 1
        print("体检通过 ✓")
        return 0

    version = read_version(SRC)
    if not version:
        print("读不到 SKILL.md 的 version", file=sys.stderr)
        return 1

    out = os.path.abspath(args.out or os.path.join(os.path.dirname(SRC), "pkg-%s" % version))
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)

    n = copy_tree(out)

    def count_src():
        """仓库内全部文件数（仅排除 .git 等版本控制目录），用于对比剥离了多少。"""
        c = 0
        for dp, dn, fn in os.walk(SRC):
            dn[:] = [d for d in dn if d not in (".git", "__pycache__")]
            c += len(fn)
        return c

    # README 改写
    src_readme = os.path.join(SRC, "README.md")
    dst_readme = os.path.join(out, "README.md")
    with open(src_readme, encoding="utf-8") as f:
        text = f.read()
    new_text, ops = rewrite_readme(text)
    with open(dst_readme, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_text)

    print("真源:", SRC)
    print("派生:", out)
    print("版本:", version)
    print("文件数:", n, "（源 %d，差值为剥离的 %d 个渠道专属文件）" % (count_src(), count_src() - n))
    print()
    print("派生时执行的处理:")
    for o in ops:
        print("  ·", o)
    for f in sorted(EXCLUDE_FILES):
        print("  · 不打包 %s" % f)
    print("  · 不打包 tools/（仓库基建）")

    # 体检
    print()
    errs, _ = check(out)
    if errs:
        print("体检 FAIL（%d 项）:" % len(errs))
        for e in errs:
            print("  ✗", e)
        return 1
    print("体检通过 ✓（专属文件零残留 / 链接零失效 / 无死引用 / 无旧功能说明）")

    if args.verify:
        print()
        print("跑包内自检 …")
        rc = subprocess.call([sys.executable, os.path.join(out, "scripts", "verify-all.py")])
        if rc != 0:
            print("自检未通过", file=sys.stderr)
            return rc

    print()
    print("发布命令（确认后再执行）:")
    print('  skillhub-publish publish "%s" --version %s --changelog "<更新说明>"' % (out, version))
    return 0


if __name__ == "__main__":
    sys.exit(main())
