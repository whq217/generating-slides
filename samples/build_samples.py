#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_samples — 由基座 + 行级补丁现场生成 samples/bad 下的负样本（纯标准库，零依赖）

为什么这么做：25 份负样本每份都是 ~1089 行底盘全文副本、仅注入一处（或几处）缺陷，
全文随包分发占包体九成。改为随包只带基座（good/chassis.html）+ patches.json，
运行时按行号补丁还原，逐份 sha256 自证——还原字节与原始样本完全一致。

生成产物属临时物：默认写系统临时目录，不写包目录，跑完即弃。

用法：
  python samples/build_samples.py                      生成到系统临时目录，打印路径
  python samples/build_samples.py --out <输出目录>      生成到指定目录
  python samples/build_samples.py --verify              只自证、不落盘
  python samples/build_samples.py --list                列出用例清单

被 scripts/verify-all.py 以 build(tmpdir) 形式调用，二者都不写包目录。
改基座或改样本后，跑 python samples/gen_patches.py --regen 重算 patches.json。
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "patches.json")


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def load_manifest(path=MANIFEST):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def build(out_dir, manifest=None):
    """按 manifest 还原全部负样本到 out_dir，返回 out_dir。逐份校验 sha256，不符即中止。"""
    m = manifest or load_manifest()
    base_path = os.path.join(HERE, m["base"]["path"])
    with open(base_path, "rb") as fh:
        raw = fh.read()
    if _sha(raw) != m["base"]["sha256"]:
        raise SystemExit(
            "[FAIL] 基座 sha256 与 patches.json 记录不符——基座被改过，补丁行号会错位。\n"
            "  期望 %s\n  实际 %s\n"
            "  处置：python samples/gen_patches.py --regen 重算补丁后再试。"
            % (m["base"]["sha256"], _sha(raw))
        )
    base_lines = raw.decode("utf-8").splitlines(keepends=True)
    os.makedirs(out_dir, exist_ok=True)
    for c in m["cases"]:
        name = c["file"]
        if c["mode"] == "copy":
            with open(os.path.join(HERE, "_base", c["from"]), "rb") as fh:
                data = fh.read()
        else:
            lines = list(base_lines)
            for e in sorted(c["edits"], key=lambda x: x["at"], reverse=True):
                lines[e["at"]:e["at"] + e["del"]] = e["ins"]
            data = "".join(lines).encode("utf-8")
        got = _sha(data)
        if got != c["sha256"]:
            raise SystemExit(
                "[FAIL] %s 还原后 sha256 不符（期望 %s… 实际 %s…）"
                % (name, c["sha256"][:12], got[:12])
            )
        with open(os.path.join(out_dir, name), "wb") as fh:
            fh.write(data)
    return out_dir


def main(argv=None):
    ap = argparse.ArgumentParser(description="由基座 + 补丁现场生成负样本")
    ap.add_argument("--out", help="输出目录（默认系统临时目录）")
    ap.add_argument("--verify", action="store_true", help="只自证还原结果，不保留文件")
    ap.add_argument("--list", action="store_true", help="列出用例清单")
    a = ap.parse_args(argv)

    m = load_manifest()
    if a.list:
        print("基座: %s（%d 行 / %d B）" % (m["base"]["path"], m["base"]["lines"], m["base"]["bytes"]))
        print("用例: %d 份（patch %d / copy %d）" % (
            len(m["cases"]),
            sum(1 for c in m["cases"] if c["mode"] == "patch"),
            sum(1 for c in m["cases"] if c["mode"] == "copy")))
        for c in m["cases"]:
            print("  %-6s %-34s %6d B" % (c["mode"], c["file"], c["bytes"]))
        return 0

    if a.verify:
        tmp = tempfile.mkdtemp(prefix="deck-samples-")
        try:
            build(tmp, m)
            print("[PASS] %d 份负样本还原自证通过（sha256 逐份一致）" % len(m["cases"]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        return 0

    out = a.out or tempfile.mkdtemp(prefix="deck-samples-")
    build(out, m)
    print("[OK] %d 份负样本已生成 → %s" % (len(m["cases"]), out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
