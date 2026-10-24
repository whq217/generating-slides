#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_patches — 由「基座 + 负样本全文」重算 samples/patches.json（纯标准库，零依赖）

何时用：改了基座（samples/good/chassis.html）或改了某份负样本之后，行级补丁会错位/过期。
流程：先 python samples/build_samples.py --out <临时目录> 取出当前样本 → 改你想改的 →
      python samples/gen_patches.py --from <临时目录> 重算补丁。

安全闸：重算前先核对基座 sha256 与旧 patches.json 是否一致；不一致且未加 --force-base
       时中止，避免在基座已变、样本还是旧基座派生的情况下把错误固化成新基线。

用法：
  python samples/gen_patches.py --from <样本目录>
  python samples/gen_patches.py --from <样本目录> --base samples/good/chassis.html
  python samples/gen_patches.py --from <样本目录> --force-base
"""
import argparse
import difflib
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "patches.json")


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description="重算 samples/patches.json")
    ap.add_argument("--from", dest="src", required=True, help="负样本全文所在目录")
    ap.add_argument("--base", default=os.path.join(HERE, "good", "chassis.html"), help="基座路径")
    ap.add_argument("--force-base", action="store_true", help="基座 sha 变了也继续（会重置基线）")
    a = ap.parse_args(argv)

    if not os.path.isdir(a.src):
        raise SystemExit("[FAIL] 样本目录不存在: %s" % a.src)
    if not os.path.isfile(a.base):
        raise SystemExit("[FAIL] 基座不存在: %s" % a.base)

    with open(a.base, "rb") as fh:
        base_raw = fh.read()
    base_lines = base_raw.decode("utf-8").splitlines(keepends=True)

    old = None
    if os.path.isfile(MANIFEST):
        with open(MANIFEST, encoding="utf-8") as fh:
            old = json.load(fh)
        if old["base"]["sha256"] != _sha(base_raw) and not a.force_base:
            raise SystemExit(
                "[FAIL] 基座 sha256 与现有 patches.json 记录不符。\n"
                "  现在用旧样本重算，等于把「旧基座派生」的样本贴到新基座上，缺陷会错位。\n"
                "  确认无误再加 --force-base；否则先用当前基座重建样本再改。"
            )

    names = sorted(f for f in os.listdir(a.src) if f.endswith(".html"))
    if not names:
        raise SystemExit("[FAIL] %s 下没有 .html" % a.src)

    cases = []
    for name in names:
        with open(os.path.join(a.src, name), "rb") as fh:
            tgt = fh.read()
        tgt_lines = tgt.decode("utf-8").splitlines(keepends=True)
        if len(tgt_lines) < len(base_lines) * 0.8:
            cases.append({"file": name, "mode": "copy", "from": name,
                          "sha256": _sha(tgt), "bytes": len(tgt)})
            continue
        sm = difflib.SequenceMatcher(None, base_lines, tgt_lines, autojunk=False)
        edits = [{"at": i1, "del": i2 - i1, "ins": tgt_lines[j1:j2]}
                 for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]
        cases.append({"file": name, "mode": "patch", "edits": edits,
                      "sha256": _sha(tgt), "bytes": len(tgt)})

    man = {
        "base": {"path": os.path.relpath(a.base, HERE).replace("\\", "/"),
                 "sha256": _sha(base_raw), "bytes": len(base_raw), "lines": len(base_lines)},
        "note": "samples/bad 下的负样本由 build_samples.py 依据本文件现场生成，不随包分发全文；"
                "改基座后必须重跑 gen_patches.py 重算",
        "cases": cases,
    }
    with open(MANIFEST, "w", encoding="utf-8", newline="") as fh:
        json.dump(man, fh, ensure_ascii=False)

    copies = [c for c in cases if c["mode"] == "copy"]
    os.makedirs(os.path.join(HERE, "_base"), exist_ok=True)
    for c in copies:
        with open(os.path.join(a.src, c["file"]), "rb") as fh:
            data = fh.read()
        with open(os.path.join(HERE, "_base", c["from"]), "wb") as fh:
            fh.write(data)

    print("[OK] patches.json 重算完成：%d 例（patch %d / copy %d），%.1f KB"
          % (len(cases), len(cases) - len(copies), len(copies),
             os.path.getsize(MANIFEST) / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
