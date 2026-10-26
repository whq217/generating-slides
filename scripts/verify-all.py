# -*- coding: utf-8 -*-
"""verify-all — 机验门禁总入口（2026-10-23 M6 立，P0 版四步；2026-10-24 增第 5 步装配链）
用法: python scripts/verify-all.py（2026-10-26 增第 6 步行为探针）
步骤: [1/6] build 重建逐字节一致（node build-chassis.mjs；无 node 时 SKIP 不判败）
      [2/6] 正样本全绿（samples/good，双脚本 exit 0；含 .deco 装饰层正样本 deco-cover.html
            ——「装饰隐身」在回归集里的唯一覆盖）
      [3/6] 负样本全红且命中标记（由 samples/patches.json 现场生成 → expected.json 逐条比对，含单引号 .sq 双写法）
      [4/6] 旧术语零命中（硬门禁/命中即 FAIL/字号白名单——F4 回归锚点）
      [5/6] 样本内嵌 deco 参数 == modules/effects.css（样本 CSS 是手工同步的，改真源不跟即红
            ——与首轮底盘 S1 同构的装配链病根）
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


# ── [1/6] build 重建逐字节一致 ──
chassis = os.path.join(PKG, "assets", "chassis-v2.html")
if shutil.which("node"):
    before = open(chassis, "rb").read()
    r = subprocess.run(["node", os.path.join(PKG, "scripts", "build-chassis.mjs")],
                       capture_output=True, text=True, shell=False,
                       encoding="utf-8", errors="replace")
    after = open(chassis, "rb").read()
    if before != after:   # 无论如何恢复现场，差异已在比对中暴露
        open(chassis, "wb").write(before)
    step("build 重建逐字节一致", r.returncode == 0 and before == after,
        "" if (r.returncode == 0 and before == after) else "build exit %d / 一致 %s / %s"
        % (r.returncode, before == after, (r.stdout or r.stderr or "")[-120:]))
else:
    step("build 重建逐字节一致", True, "SKIP（本机无 node）")

# ── [2/6] 正样本全绿 ──
goods = sorted(f for f in os.listdir(os.path.join(SAMPLES, "good")) if f.endswith(".html"))
for f in goods:
    for sc in ("verify-consistency.py", "check-deck.py"):
        r = subprocess.run([sys.executable, os.path.join(PKG, "scripts", sc),
                            os.path.join(SAMPLES, "good", f)], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        step("good/%s × %s 全绿" % (f, sc.split(".")[0]), r.returncode == 0,
             "exit %d" % r.returncode if r.returncode else "")

# ── [3/6] 负样本按 expected 逐条比对 ──
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

# ── [4/6] 旧术语零命中（F4 回归锚点）──
pat = re.compile(r"硬门禁|命中即 FAIL|字号白名单")
hits = []
for root, _d, files in os.walk(PKG):
    if "samples" in root or "node_modules" in root or ".backups" in root:
        continue
    for f in files:
        if f.endswith((".md",)):
            for i, line in enumerate(open(os.path.join(root, f), encoding="utf-8", errors="replace"), 1):
                if pat.search(line):
                    hits.append("%s:%d" % (os.path.relpath(os.path.join(root, f), PKG), i))
step("旧术语零命中（硬门禁/命中即 FAIL/字号白名单）", not hits, "、".join(hits[:4]) if hits else "")

# ── [5/6] 样本内嵌 deco 参数 == modules/effects.css（2026-10-24 A1 装配链）──
#    样本 CSS 与底盘产物不同源（build-chassis 只喂 chassis-v2.html），属手工同步——
#    改 effects.css 参数后样本不跟，#15b 对参数漂移即失明（首轮 S1 底盘事故同构病根）。
#    抽三组关键参数钉死：.deco .grid 的 color-mix% / .deco .scan 的 % / .deco.dim .grid 的 opacity。
#    负样本在远端不以全文分发，故遍历根 = samples/good + 现场生成的 bad_dir（须在本步之后才清理）。
def _deco_params(css_text):
    out = {}
    for key, pat in (("grid_mix", r"\.deco\s+\.grid\s*\{([^}]*)\}"),
                     ("scan_mix", r"\.deco\s+\.scan\s*\{([^}]*)\}"),
                     ("dim_op", r"\.deco\.dim\s+\.grid\s*\{([^}]*)\}")):
        body = re.search(pat, css_text)
        if not body:
            out[key] = None
            continue
        vals = re.findall(r"color-mix\([^;]*?([\d.]+)\s*%", body.group(1)) if key != "dim_op" \
            else re.findall(r"opacity\s*:\s*([\d.]+)", body.group(1))
        out[key] = sorted(set(vals))
    return out

_fx = open(os.path.join(PKG, "assets", "modules", "effects.css"), encoding="utf-8").read()
_want = _deco_params(_fx)
_drift = []
for _root in ([os.path.join(SAMPLES, "good")] + ([bad_dir] if bad_dir else [])):
    for _f in sorted(f for f in os.listdir(_root) if f.endswith(".html")):
        _css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>",
                          open(os.path.join(_root, _f), encoding="utf-8", errors="replace").read(), re.S))
        _got = _deco_params(_css)
        if _got != _want:
            _drift.append("%s: grid%s/scan%s/dim%s" % (
                os.path.relpath(os.path.join(_root, _f), SAMPLES),
                _got["grid_mix"], _got["scan_mix"], _got["dim_op"]))
step("样本内嵌 deco 参数 == effects.css（grid %s / scan %s / dim %s）"
     % ("/".join(_want["grid_mix"] or ["?"]), "/".join(_want["scan_mix"] or ["?"]),
        "/".join(_want["dim_op"] or ["?"])),
     not _drift, ("漂移 %d 份: %s" % (len(_drift), "、".join(_drift[:3]))) if _drift else "")

if bad_dir:
    shutil.rmtree(bad_dir, ignore_errors=True)   # 现场生成的负样本用完即弃，不留痕迹

# ── [6/6] 行为级探针（2026-10-26 C3.1 增；环境在才跑，缺则 SKIP 不判红）──
#    measure-layout：正样本注入三步跑出 REPORT:: 即过，版率数值只打印不判红（阈值人判）——
#    覆盖「版面率第一红线」的口径失守（改底盘后探针崩了无人知）。
#    crowd-probe：正样本必须 0 问题（display 上下文排除修复后的探针自身回归锚点）。
def _find_chrome():
    for c in ("chrome",):
        w = shutil.which(c)
        if w:
            return w
    for p in (os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Google\Chrome\Application\chrome.exe"),
              r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
        if os.path.exists(p):
            return p
    return None

_good_chassis = os.path.abspath(os.path.join(SAMPLES, "good", "chassis.html"))
try:
    _js = open(os.path.join(PKG, "scripts", "measure-layout.js"), encoding="utf-8", errors="replace").read()
    _dk = open(_good_chassis, encoding="utf-8", errors="replace").read()
    _i = _dk.rfind("</body>")
    _chrome = _find_chrome()
    if _i < 0:
        step("measure-layout 行为探针（正样本出 REPORT）", False, "正样本无 </body>")
    elif not _chrome:
        step("measure-layout 行为探针（正样本出 REPORT）", True, "SKIP（未找到 Chrome，不判红）")
    else:
        with tempfile.TemporaryDirectory(prefix="verify-probe-") as _td:
            _pp = os.path.join(_td, "probe.html")
            with open(_pp, "w", encoding="utf-8", newline="") as _f:
                _f.write(_dk[:_i] + "<script>\n" + _js + "\n</script>\n" + _dk[_i:])
            try:
                _r = subprocess.run([_chrome, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                                     "--user-data-dir=" + os.path.join(_td, "prof"),
                                     "--virtual-time-budget=20000", "--dump-dom",
                                     "file:///" + _pp.replace("\\", "/")],
                                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                                    timeout=120)
                _lines = [l.strip()[:100] for l in (_r.stdout or "").splitlines() if "REPORT::" in l]
                step("measure-layout 行为探针（正样本出 REPORT，数值只打印）", len(_lines) > 0,
                     "" if _lines else "无 REPORT 输出（探针或注入链损坏）")
                if _lines:
                    print("    · " + "\n    · ".join(_lines[:3]))
            except subprocess.TimeoutExpired:
                step("measure-layout 行为探针（正样本出 REPORT）", False, "Chrome 渲染超时 120s")
except Exception as _e:
    step("measure-layout 行为探针（正样本出 REPORT）", False, "异常: %s" % str(_e)[:100])

try:
    _r2 = subprocess.run([sys.executable, os.path.join(PKG, "scripts", "crowd-probe.py"), _good_chassis],
                         capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
    _out2 = (_r2.stdout or "") + (_r2.stderr or "")
    if "[SKIP]" in _out2:
        step("crowd-probe 行为探针（正样本 0 问题）", True, "SKIP（无 playwright，不判红）")
    else:
        _ok6 = _r2.returncode == 0 and "0 处问题" in _out2
        step("crowd-probe 行为探针（正样本 0 问题）", _ok6, "" if _ok6 else _out2.strip()[-160:])
except Exception as _e:
    step("crowd-probe 行为探针（正样本 0 问题）", False, "异常: %s" % str(_e)[:100])

print("=" * 78)
print("\n".join(results))
print("=" * 78)
total = len(results)
print("verify-all：%d/%d 步通过 → %s" % (total - n_fail, total, "PASS" if n_fail == 0 else "FAIL（%d 步红）" % n_fail))
sys.exit(1 if n_fail else 0)
