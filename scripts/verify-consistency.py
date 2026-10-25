# -*- coding: utf-8 -*-
r"""
verify-consistency.py — 静态一致性探针（不需要渲染，秒级）
用法: python verify-consistency.py <ppt.html> [--json]

检查项（都对应真实踩过的坑）。**单一报告制（2026-10-23 立）**：本脚本只出问题清单、不做交付裁决——
  出现问题 exit 1（=打回信号），干净 exit 0；[严重]/[提示] 仅为分级标签（严重=结构性事故指纹，提示=阈值/版式建议），
  逐项处理或说明理由后交付，决定权在生成端与使用者。
  ── 严重项（exit 1）──
  0. 扫描基数自证        解析基数为 0 报「解析异常」（M9：绿报告必须能证明「看见了没事」，单双引号通吃）
  1. 强调容器形态数      同层级"强调容器"用了几种（card/term-card/quote-bar/...），>6 即严重（4-6 只提示）
  2. 缺 hl 的卡片        class 含 card 但不含 hl 的个数，>5 即严重（1-5 只提示）
  3. 内联字号地板        style 里 font-size < 11.5px 的个数，>10 即严重（≤10 只提示）
  5. 页间竖间距          各页 .body-area（v2）/ .slide-body（v1 产物）内联 gap 的取值种类，>2 即严重（2 种只提示）；
                        仅当生成端写了内联 gap 时生效，否则显示「统一」
  6. 光晕配色 bug        .hl:hover 里还有 border-color…!important（把辅助色刷成主色），命中即严重
  9. 孤儿 class          骨架/组件类（cover-title 等）HTML 用了但 CSS 无规则 → 严重；非关键类只提示
 10. 悬空 CSS 变量       :root 声明但全文无 var() 引用；字号类即严重（其余只提示）
 11. 封面标题字号覆盖    检出 .cover-title 却无显式 font-size 规则即严重（防回落浏览器默认 h1 爆行）
 11a. token 对比度       --ink/--ink-dim/--line-struct 对 --bg 静态对比度过低（2026-10-23 补）
 11b. 压轴句存在性       内容页缺 .punch → 只提示（2026-10-23 补，留痕不拦截）
 12. 骨架完整性          10 条硬断言（v2 活断言 8 条 + 348/349 两条）：S1 .stage 锁 1920×1080 /
                        S2 页集与翻页状态机（section.slide + classList.active）/ S3 每页边注必备件
                        （folio+footmark，版率探针排除锚点）/ S4 :root token 齐全 / S5 翻页通道存在
                        且 go() 体内零动态 DOM / S6 舞台等比缩放 / S7 帧预印动画 + reduced-motion 豁免 /
                        S8 无 v1 残留；348 step 叙事时序与初见密度；349 数字排版三条。
                        **全部严重**——命中即骨架断裂或踩过的静默事故，不做阈值让步。
 13. 可视化规范          C-1 option 字号地板(<11.5) / C-2 图表页缺来源脚 / C-3 柱条 min 非 0 /
                        C-4 环形组件>5 / D-2 图示写死色值 → **严重**；
                        D-3 图示节点超上限（≤4/≤5 是经验阈值）→ 只提示。
 14. 口径自洽            文档宣称的「组数/判据数」vs 源码实数：实际值从源码算（组数=本 docstring
                        编号最大值、FAIL 面=源码失败追加次数），宣称值从 README/SKILL 抓，
                        不一致即 **严重** 并给 文件:行；0 处宣称跳过比对。
 15. 封面断言            a 视觉事件三证据取一（stamp 级数字 / .has-metrics+.cover-metrics /
                        .dv- 装置标记）全缺 = 平庸封面 → **严重**（纯大标题不算数）；
                        b 装饰隐身：grid/scan 有效对比度 <1.1:1 → **严重**。仅当 deck 实际用了
                        .deco 对应词条才判（2026-10-24 复查补使用前提——CSS 里留着旧参数词条规则
                        ≠ 页面用了它，不设前提会把「不用装饰的合法 deck」与存量旧稿永久判红；
                        dim 档有效覆盖按 base_op×dim_op 连乘取保守值——新 CSS 基础规则无
                        opacity、连乘与覆盖两读法等价；旧值实测 base 5%×.55=2.75%→1.06:1、
                        dim 5%×.3=1.5%→1.03:1）；
                        c .deco 直接子元素 >2 → **严重**；d stamp/标题字号让位比 <1.3、
                        e 巨数缺口径注 → 只提示。
  ── 提示（不影响退出码，只打在报告里供人判断）──
  4. 内联硬编码颜色       style 里出现 #rrggbb 的个数（与预设示例教学重叠，误报高）
  7. 辅助色未声明 tone    疑似辅助色元素缺 tone 声明
  8. 单列纵排逃逸        单个列表 ≥4 条且祖先链无分栏信号（版式建议，随页型变化）
  12/13 中的阈值项       强调形态 4-6 种、缺 hl 1-5 个、内联小字 ≤10 处、D-3 节点上限
  ── 撤销说明 ──（#14 口径自洽已于 2026-10-24 归位严重区）
  旧版对 #12/#13 采用「只报警不拦截 + 攒够 10 份不同稿件/两周再议转正 + 误报率>10% 退回」机制；
  该机制对**对外发布**的技能包不成立（样本记录只落在使用者的本机，维护者收不到汇总），等于让
  结构性事故永久不设防。故整体撤销：结构性断言直接 FAIL，阈值类断言降为提示；配套的样本计数
  文件与命令行开关一并删除，本脚本不写任何外部文件。
  2026-10-23 演进（本包定稿）：FAIL/HINT 两级从裁决机制降为信息分级——脚本只出报告，
  exit 1 = 打回信号（重修），不写「命中即不许交付」；处理决定权在使用方。
"""
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

CONTAINERS = [
    "card", "term-card", "quote-bar", "quote-box", "highlight-box",
    "asset-cell", "suggest-card", "tl-node", "rank-item", "cmp-table",
]


def load(path):
    return open(path, encoding="utf-8", errors="replace").read()


def css_and_body(html):
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    body = html
    m = re.search(r"</head>\s*<body[^>]*>", html, re.S)   # 锚 </head>：core.css 注释里有字面量 <body>（2026-10-23 修）
    if m:
        body = html[m.end():]
    elif "<body" in html:
        body = html.split("<body", 1)[1]
    body = re.split(r"<script\b", body, maxsplit=1)[0]
    return css, body


def norm_attrs(body):
    """属性预处理视图（不改原文件）：单引号属性值统一双引号、属性名转小写。
    只对切掉 <script> 之后的 body 做（2026-10-23 M8：单引号 HTML 是合法产物写法，
    解析层对它失明曾让含真故障的产物全绿）；JS 字符串里的引号不受影响。"""
    return re.sub(
        r"([A-Za-z-]+)\s*=\s*'([^'\n]*)'",
        lambda m: m.group(1).lower() + '="' + m.group(2) + '"',
        body,
    )


def tags(body):
    """扫出所有开始标签的 (tagname, attrs dict)"""
    out = []
    for m in re.finditer(r"<([a-zA-Z][\w-]*)((?:\s+[^<>]*?)?)\s*/?>", body):
        raw = m.group(2) or ""
        attrs = {}
        for am in re.finditer(r"([\w:-]+)\s*=\s*([\"'])(.*?)\2", raw, re.S):
            attrs[am.group(1).lower()] = am.group(3)
        out.append((m.group(1).lower(), attrs))
    return out


def chassis_registry():
    """类名注册表（2026-10-23 M1）：从底盘 chassis-v2.html 的 CSS 里自动提取，禁手抄名单。
    两源：① 行内标记（定义块体首 @critical/@hook/@svg-text，归属=选择器最右分段的类名）
          ② 集中声明行（@critical-declared/@hook-declared，收纳无 CSS 定义的纯 JS 钩子与
             v1 遗留豁免）——加组件类在底盘 CSS 打标即自动跟，本脚本零改动。"""
    reg = {"critical": set(), "hook": set(), "svg_text": set()}
    try:
        src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "assets", "chassis-v2.html"),
                   encoding="utf-8", errors="replace").read()
    except OSError:
        return reg
    css_all = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S))
    for kind in ("critical", "hook", "svg-text"):
        m = re.search(r"@%s-declared\s*:\s*([^*]+)" % kind.replace("-", r"\-"), css_all)
        if m:
            reg[kind.replace("-", "_")].update(m.group(1).strip().split())
    for sel, bd, _s, _e in brace_blocks(css_all):
        m = re.match(r"\s*/\*\s*@(critical|hook|svg-text)\s*\*/", bd)
        if not m:
            continue
        kind = m.group(1).replace("-", "_")
        for part in sel.split(","):
            part = re.sub(r"::?[a-zA-Z-]+(\([^)]*\))?", "", part.strip())
            segs = part.split()
            if segs:
                reg[kind].update(re.findall(r"\.(-?[_a-zA-Z][\w-]*)", segs[-1]))
    return reg


def brace_blocks(css):
    """返回 [(selector, body, start, end)]，支持一层嵌套（@media）"""
    blocks, i, n, depth_stack = [], 0, len(css), []
    cur_start = 0
    while i < n:
        ch = css[i]
        if ch == "{":
            sel = css[cur_start:i].strip()
            # 找匹配的 }
            d, j = 1, i + 1
            while j < n and d:
                if css[j] == "{":
                    d += 1
                elif css[j] == "}":
                    d -= 1
                j += 1
            blocks.append((sel, css[i + 1:j - 1], cur_start, j))
            cur_start = j
            i = j
            continue
        i += 1
    return blocks


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    path = os.path.abspath(sys.argv[1])
    as_json = "--json" in sys.argv
    html = load(path)
    css, body = css_and_body(html)
    body = norm_attrs(body)

    result = {"file": path}
    fails, hints = [], []

    # 0. 扫描基数自证（2026-10-23 M9）：基数为 0 不得报绿——「没解析到」≠「看见了没事」。
    #    单引号整稿曾让 class/style 全数失明、报告仍「干净」，此闸兜住解析层整体失效。
    scan = {
        "section": len(re.findall(r"<section\b", body, re.I)),
        "class_attr": len(re.findall(r"\bclass\s*=", body, re.I)),
        "inline_style": len(re.findall(r"\bstyle\s*=", body, re.I)),
        "svg": len(re.findall(r"<svg\b", body, re.I)),
        "css_rule": len(brace_blocks(css)),
    }
    result["scan_base"] = scan
    if len(html) > 10240 and (scan["section"] == 0 or scan["class_attr"] == 0):
        fails.append("解析异常：未解析到 section/class（基数 %s）→ 先查属性引号与解析器，勿当通过" % scan)

    # 1. 容器形态
    counts = Counter()
    for name, attrs in tags(body):
        cls = attrs.get("class", "").split()
        for c in CONTAINERS:
            if c in cls:
                counts[c] += 1
    shapes = [c for c in counts if c in
              ("term-card", "quote-bar", "quote-box", "highlight-box",
               "asset-cell", "suggest-card", "card")]
    result["containers"] = dict(counts.most_common())
    result["emphasis_containers"] = len(shapes)
    if len(shapes) > 6:
        fails.append("强调容器形态 %d 种（>6）: %s" % (len(shapes), shapes))
    elif len(shapes) > 4:
        hints.append("强调容器形态 %d 种（>4）: %s" % (len(shapes), shapes))

    # 2. 缺 hl
    no_hl = [a.get("class", "") for t, a in tags(body)
             if "card" in a.get("class", "").split() and "hl" not in a.get("class", "").split()]
    result["cards_missing_hl"] = len(no_hl)
    if len(no_hl) > 5:
        fails.append("缺 hl 的卡片 %d 个（>5）" % len(no_hl))
    elif no_hl:
        hints.append("缺 hl 的卡片 %d 个" % len(no_hl))

    # 3. 内联字号（em 是相对父级，不算越界；只查 rem / px）
    #    同时给两套口径：uniform=统一 11.5px（更严）；skill=技能现役双轨（正文/td/li <11.5，其他 <10.5）
    floor_uniform, floor_skill = [], []
    inline_sizes = 0
    for tag, attrs in tags(body):
        st = attrs.get("style", "")
        m = re.search(r"font-size:\s*([0-9.]+)\s*(rem|px)", st, re.I)
        if not m:
            continue
        inline_sizes += 1
        v, u = float(m.group(1)), m.group(2)
        px = v * 16 if u.lower() == "rem" else v
        if px < 11.5:
            floor_uniform.append("%s:%s%s" % (tag, v, u))
        lim = 11.5 if tag in ("p", "td", "li") else 10.5
        if px < lim:
            floor_skill.append("%s:%s%s" % (tag, v, u))
    result["inline_fontsize"] = inline_sizes
    result["inline_fontsize_below_floor_uniform"] = len(floor_uniform)
    result["inline_fontsize_below_floor_skill"] = len(floor_skill)
    result["inline_fontsize_below_floor"] = len(floor_skill)  # 兼容旧字段，取技能口径
    if len(floor_uniform) > 10:
        fails.append("内联字号 <11.5px（统一口径）%d 处（>10）" % len(floor_uniform))
    elif floor_uniform:
        hints.append("内联字号 <11.5px（统一口径）%d 处" % len(floor_uniform))
    if floor_skill:
        hints.append("内联字号低于技能双轨地板 %d 处（正文<11.5 / 其他<10.5）" % len(floor_skill))

    # 4. 内联颜色
    # ⚠️ 口径说明（2026-10-19）：style-presets.md 的组件示例本身含内联十六进制色
    # （边框/装饰演示），该项与预设教学有重叠，因此只作 WARN 提示、不判 FAIL。
    # 语义色（正负/主辅）应走底盘 CSS 变量（--accent 系），不硬编码
    hexes = re.findall(r'style\s*=\s*"[^"]*#([0-9a-fA-F]{3,8})', body, re.I)
    result["inline_hex_colors"] = len(hexes)
    if hexes:
        hints.append("内联硬编码颜色 %d 处（与 style-presets 示例教学有重叠，仅提示；语义色建议走变量+tone-alt）" % len(hexes))

    # 5. gap 种类
    gaps = re.findall(r'class="[^"]*(?:body-area|slide-body)[^"]*"[^>]*style="[^"]*gap:\s*([0-9]+px)', body)
    result["gap_values"] = sorted(set(gaps), key=lambda x: int(x[:-2]))
    if len(set(gaps)) > 2:
        fails.append("页间竖间距取值 %d 种（>2）: %s" % (len(set(gaps)), result["gap_values"]))
    elif len(set(gaps)) > 1:
        hints.append("页间竖间距取值 %d 种: %s" % (len(set(gaps)), result["gap_values"]))

    # 6. 光晕 bug
    buggy = []
    for sel, bd, s, e in brace_blocks(css):
        if ".hl" in sel and "hover" in sel and "border-color" in bd and "important" in bd:
            buggy.append(re.sub(r"\s+", " ", sel)[:80])
    result["glow_border_important"] = buggy
    if buggy:
        fails.append("光晕配色 bug：.hl:hover 仍用 border-color…!important 刷主色（%d 条规则）" % len(buggy))

    # 7. 辅助色未声明 tone
    ALT_KEYS = ("rgba(255,0,170", "rgba(244,63,94", "rgba(255, 0, 170", "rgba(244, 63, 94")
    undecided = []
    for t, a in tags(body):
        cls = a.get("class", "")
        style = a.get("style", "")
        looks_alt = any(k in style for k in ALT_KEYS) or re.search(r"\b(card\s+mag|mag\b|neg-line)", cls)
        declared = "tone-alt" in cls or "hl--alt" in cls or 'data-tone="alt"' in str(a)
        if looks_alt and not declared:
            undecided.append(cls[:60])
    result["alt_without_tone"] = len(undecided)
    if undecided:
        hints.append("疑似辅助色元素 %d 个未声明 tone（修补后靠组件名映射可兜住，新页面建议显式加 tone-alt）" % len(undecided))

    # 8. 单列纵排逃逸（单个列表块 ≥4 条 li + 该块祖先链上无分栏信号）
    #    判据演进（2026-10-19 v2）：原「整页有 card/grid 类即豁免」在真实产物上几乎页页命中
    #    （FDE 13/15 页、WB 13/14 页），实测 li≥4 的页全部被整页豁免，其中 FDE 内容页3 是
    #    裸 ul.styled-list 直挂 slide-body 的真单列 → 结构性漏判。
    #    现改为：豁免下沉到「该列表的祖先链」，信号源 = class ∪ inline style；
    #    card 不算豁免（外框不改变内部是否单列）。
    #    口径：只判 WARN 不判 FAIL——静态正则拿不到几何，自定义 class 仍会假阴性；
    #    闸门在 SKILL.md 6.5 清单（WARN 必须处理不得放行），两者分工不可合并。
    #    页码口径：N 为「内容页序号」（封面无 body-area），对应全 deck 的 P{N+1}。
    #    2026-10-24 补：底盘自带的 .duo/.col 双栏组件此前不在信号表里——真产物用它排两栏，
    #    仍被判「单列纵排逃逸」（FDE SOP 实测 5 处误报）。分栏信号必须认自家组件。
    LAYOUT_CLS = re.compile(r'(^|[\s-])(grid|grid-\d|cols|col|col-\d|duo|two-col|split|rank-item|asset-cell|flex|row)([\s-]|$)')
    LAYOUT_STY = re.compile(r'(display\s*:\s*(flex|grid)|grid-template-columns|flex-direction\s*:\s*row)')
    VOID_TAGS = {'br', 'img', 'input', 'hr', 'meta', 'link', 'path', 'circle', 'rect', 'line', 'use'}

    def _ancestors(seg, pos):
        stack = []
        for t in re.finditer(r'<(/?)([a-zA-Z][\w-]*)([^>]*)>', seg[:pos]):
            closing, name, attrs = t.group(1), t.group(2).lower(), t.group(3)
            if name in VOID_TAGS:
                continue
            if closing:
                if stack and stack[-1][0] == name:
                    stack.pop()
                continue
            stack.append((name, attrs))
        return stack

    def _layout_signal(chain):
        for name, attrs in chain:
            cl = re.search(r'class="([^"]*)"', attrs)
            if cl and LAYOUT_CLS.search(cl.group(1)):
                return 'class:' + LAYOUT_CLS.search(cl.group(1)).group(0).strip()
            st = re.search(r'style="([^"]*)"', attrs)
            if st and LAYOUT_STY.search(st.group(1)):
                return 'inline:' + LAYOUT_STY.search(st.group(1)).group(0)
        return ''

    escape = []
    for page_no, m in enumerate(re.finditer(r'class="[^"]*(?:body-area|slide-body)[^"]*"', body), 1):
        seg = re.split(r"</section>", body[m.end():], maxsplit=1)[0]
        for ul in re.finditer(r'<(ul|ol)\b([^>]*)>(.*?)</\1>', seg, flags=re.S):
            n_li = len(re.findall(r'<li\b', ul.group(3)))
            if n_li < 4:
                continue
            if _layout_signal(_ancestors(seg, ul.start())):
                continue
            escape.append({"page": page_no, "items": n_li})
    result["single_column_escape"] = escape
    if escape:
        hints.append("单列纵排逃逸：内容页 %s（单个列表 ≥4 条且祖先链无分栏信号）→ 改 L-1/L-2/D-2"
                     % [(e["page"], e["items"]) for e in escape])

    # 9. 孤儿 class（2026-10-19 立）
    #    真实事故：产物抄了 boilerplate 的 :root 变量，却漏搬「封面元素」整段 CSS，
    #    h1.cover-title 无任何规则 → 落到 Reveal 主题默认 2.5em=105px，封面标题折成 3 行、
    #    占画布 54%。三道既有闸门全放行：verify-layout 把封面当「无骨架」整页跳过、
    #    本脚本原 8 项不查未定义 class、verify-input 只测翻页 —— 属闸门真空，故新增本项。
    #    口径：JS/动画钩子与 Font Awesome 图标字体本就无 CSS 规则，不算孤儿；
    #    critical 是「缺样式必出事」的骨架/组件类 → FAIL，其余只提示（hints）。
    #    名单来源 = 底盘 CSS 注册表自动提取（M1，2026-10-23）——原两份手抄名单
    #    （CRITICAL_ORPHANS 14 / HOOK_CLASSES 31）已删，加组件类在底盘打标即自动跟。
    css_nc = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    _reg = chassis_registry()
    if len(_reg["critical"]) < 10 or len(_reg["hook"]) < 20:
        fails.append("注册表提取异常：critical %d / hook %d（阈值 10/20）→ 底盘标记或"
                     " chassis-v2.html 损坏，检查器失明，勿当通过"
                     % (len(_reg["critical"]), len(_reg["hook"])))
    CRITICAL_ORPHANS = _reg["critical"]
    HOOK_CLASSES = _reg["hook"]
    ICON_FONT = {"fa", "fas", "far", "fab", "fal", "fad", "fat"}
    used_cls = set()
    for _t, a in tags(body):
        for c in (a.get("class") or "").split():
            used_cls.add(c)
    defined_cls = set()
    for sel, _bd, _s, _e in brace_blocks(css_nc):
        for m in re.finditer(r"\.(-?[_a-zA-Z][\w-]*)", sel):
            defined_cls.add(m.group(1))
    orphans = sorted(
        c for c in used_cls
        if c not in defined_cls
        and c not in HOOK_CLASSES
        and c not in ICON_FONT
        and not c.startswith("fa-")
        and not c.startswith(("js-", "is-"))
    )
    critical_orphans = [c for c in orphans if c in CRITICAL_ORPHANS]
    result["orphan_classes"] = orphans
    result["orphan_classes_critical"] = critical_orphans
    if critical_orphans:
        fails.append("孤儿组件类（HTML 用到、CSS 无规则）: %s → 该段 CSS 漏搬，照 chassis-v2（core.css）补齐"
                     % ", ".join("." + c for c in critical_orphans))
    if orphans:
        hints.append("孤儿 class %d 个（HTML 用到、CSS 未定义）: %s"
                     % (len(orphans), ", ".join("." + c for c in orphans[:8])))

    # 10. 悬空 CSS 变量（2026-10-19 立）
    #    「变量在、规则没搬」的指纹：本次 --cover-title-size 声明了，但全文没有一处 var() 引用它。
    #    口径：只认 :root 块内的声明，扫全文（含内联 style 与 JS 字符串）。
    #    只有「字号类」悬空才判 FAIL（字号一定有对应规则，悬空 100% 是规则漏搬）；
    #    其余（--canvas-h/--nav-h 这类布局量）可能只是历史残留，只提示（hints）。
    root_decl = []
    for sel, bd, _s, _e in brace_blocks(css_nc):
        if ":root" in sel:
            root_decl += re.findall(r"(--[\w-]+)\s*:", bd)
    dangling = sorted({v for v in root_decl if ("var(%s" % v) not in html})
    result["dangling_vars"] = dangling
    # 判据=字号 token 前缀白名单（2026-10-23 F1 修）：原「"size" in v」子串匹配把装饰
    # token（--deco-size 光斑尺寸）误判成字号类，--no-effects 简装底盘合法产物被判 exit 1。
    # 底盘字号 token 全走 --fs- 前缀；--num- 为数字排版预留。
    size_dangling = [v for v in dangling if v.startswith(("--fs-", "--num-"))]
    result["dangling_vars_size"] = size_dangling
    if size_dangling:
        fails.append("字号类 CSS 变量悬空（:root 声明但全文无 var() 引用）: %s → 对应字号规则段漏搬"
                     % ", ".join(size_dangling))
    other_dangling = [v for v in dangling if v not in size_dangling]
    if other_dangling:
        hints.append("悬空 CSS 变量 %d 个（多为历史残留）: %s"
                     % (len(other_dangling), ", ".join(other_dangling)))

    # 11a. token 对比度（2026-10-23 补）：--ink/--ink-dim/--line-struct 对 --bg 静态对比度。
    #     只算 :root 直接色值（hex/rgba），color-mix 派生与 body 挂 palette 的覆盖场景跳过（静态局限，防误报）。
    #     硬线（低于即 FAIL）：ink<3.0 不可读；dim/struct<2.0 极端弱。弱线（提示）：ink<4.5 / dim与struct<3.0。
    def _to_rgb(v):
        v = v.strip()
        m = re.match(r'^#([0-9a-fA-F]{6})$', v)
        if m:
            return tuple(int(m.group(1)[i:i + 2], 16) for i in (0, 2, 4)) + (1.0,)
        m = re.match(r'^#([0-9a-fA-F]{3})$', v)
        if m:
            return tuple(int(c * 2, 16) for c in m.group(1)) + (1.0,)
        m = re.match(r'^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+))?', v)
        if m:
            a = m.group(4)
            alpha = 1.0 if not a else (float(a.rstrip('%')) / 100 if a.endswith('%') else float(a))
            return (float(m.group(1)), float(m.group(2)), float(m.group(3)), alpha)
        return None

    def _lum(rgb, bgc):
        r, g, b, a = rgb
        r = r * a + bgc[0] * (1 - a)
        g = g * a + bgc[1] * (1 - a)
        b = b * a + bgc[2] * (1 - a)
        def f(c):
            c /= 255.0
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

    def _ratio(c1, bgc):
        l1, l2 = _lum(c1, bgc), _lum(bgc, bgc)
        hi, lo = max(l1, l2), min(l1, l2)
        return (hi + 0.05) / (lo + 0.05)

    root_css = next((bd for sel, bd, _s, _e in brace_blocks(css_nc) if ":root" in sel), "")
    def _tok(name):
        m = re.search(r'%s\s*:\s*([^;]+)' % name, root_css)
        return _to_rgb(m.group(1)) if m else None
    bgc = _tok('--bg')
    contrast_rows = []
    if bgc:
        for name, hard, soft in (('--ink', 3.0, 4.5), ('--ink-dim', 2.0, 3.0), ('--line-struct', 2.0, 3.0)):
            c = _tok(name)
            if not c:
                continue
            r = round(_ratio(c, bgc), 2)
            if r < hard:
                fails.append("token 对比度 %.2f:1（%s on --bg，硬线 %.1f:1）→ 正文/结构线投影不可读" % (r, name, hard))
            elif r < soft:
                hints.append("token 对比度偏弱 %.2f:1（%s on --bg，建议 ≥%.1f:1）" % (r, name, soft))
            contrast_rows.append((name, r))
    result["contrast"] = contrast_rows

    # 11b. 压轴句存在性（2026-10-23 补，提示级）：内容页（含 .head 或 <h2>）缺 .punch → 留痕。
    #     「一页一收束」；封面/仪式页不计。提示不拦截——无收束句可能是有意（引文页/过渡页）。
    slide_segs = re.split(r'<section[^>]*class="slide', body)[1:]
    no_punch = []
    for i, seg in enumerate(slide_segs, 1):
        seg_head = seg.split('</section>', 1)[0]
        if re.search(r'class="head"|<h2', seg_head) and 'punch' not in seg_head:
            no_punch.append(i)
    if no_punch:
        hints.append("内容页缺压轴句（.punch）: 第 %s 页 → 「一页一收束」，确认是否有意" % ",".join(map(str, no_punch[:6])))
    result["pages_without_punch"] = no_punch

    # 11. 封面标题字号覆盖（2026-10-19 立；2026-10-21 v2 化：Reveal 主题压色场景已随 v1 退役，
    #     判据收敛为「检出 .cover-title → 必须有显式 font-size 规则 + 禁 inline 覆盖」）
    #     v2 口径：底盘 core.css `.cover-title{font-size:140px…}`（仪式位 110-140px 档）；
    #     漏搬该段 = 标题回落浏览器默认 h1 样式，爆行风险同 v1 事故。
    used_cover_title = any("cover-title" in (a.get("class") or "") for _t, a in tags(body))
    result["cover_title_detected"] = used_cover_title
    if used_cover_title:
        override_ok = False
        for sel, bd, _s, _e in brace_blocks(css_nc):
            if "cover-title" in sel and re.search(r"font-size\s*:", bd):
                override_ok = True
                break
        result["cover_title_size_override"] = override_ok
        if not override_ok:
            fails.append("封面标题字号未覆盖：检出 .cover-title 但 CSS 里没有显式 font-size 规则"
                         " → 回落浏览器默认 h1 样式有爆行风险。"
                         "照 chassis-v2（core.css）补 `.cover-title{font-size:140px…}`（仪式位 110-140px 档）")
        inline_fs = [(_t, a.get("style")) for _t, a in tags(body)
                     if "cover-title" in (a.get("class") or "")
                     and a.get("style") and re.search(r"font-size", a["style"], re.I)]
        if inline_fs:
            fails.append("封面标题 inline font-size（%s…）→ 封面字号禁 inline 覆盖，只走 CSS 规则档"
                         % (inline_fs[0][1] or "")[:60])

    # 12. 骨架完整性（2026-10-20 收敛 21→10 条；2026-10-22 第七十一轮起全部为严重级 FAIL）
    #    收敛依据（维护者拍板）：旧 21 条里 ~11 条是 v1 能力指纹（编辑模式 / 演讲者视图 / 封面动画双轨 /
    #    Reveal 初始化标记 / 两段式骨架 / 封面槽位封闭 / CDN 白名单），v2 底盘根本没有这些能力——断言
    #    对象不存在，随 v1 注销、不重写；~8 条在 v2 有等价物
    #    且防退化价值真实 → 重写为 v2 骨架指纹；348/349 两条不动（管的是 fragment 时序与数字排版，
    #    与骨架版本无关）。
    #    原「只报警不拦截 + ≥10 份稿件出口」机制已于第七十一轮撤销：对外发布的包里样本记录只落
    #    在使用者本机、维护者收不到汇总，等于让结构性事故永久不设防。现为严重级：命中即 FAIL，
    #    每条附「位置 + 修复指引」。
    #    指纹全部 grep 自 assets/chassis-v2.html 实测（类名 / 函数名 / 规则形态），非文档口径；
    #    JS 侧检测用全文 html（body 在 <script 处截断）。
    #    页口径：最内层 <section> = 一页（_pages 栈式配对），封面/结束页同为页级处理，不单独豁免。
    def _line_no(offset_html, pos):
        return html[:pos].count("\n") + 1

    def _pages(body_str):
        """栈式配对，返回最内层（无嵌套子 section）的 [(attrs, inner)]——即「页」。
        v2 底盘是 flat 结构（.stage 下平铺 section.slide），外层再包一层也照此处理。"""
        out, stack = [], []
        for m in re.finditer(r"<section\b([^>]*)>|</section>", body_str):
            if m.group(0).startswith("</"):
                if stack:
                    attrs, start = stack.pop()
                    inner = body_str[start:m.start()]
                    if "<section" not in inner:
                        out.append((attrs, inner))
            else:
                stack.append((m.group(1) or "", m.end()))
        return out

    js_all = html  # JS 检测全文（body 在 <script 处被截断，JS 必须扫全文）
    pages = _pages(body)
    sk_hits = []  # (标签, 消息)

    def _has_css_rule(sel_pat, decl_pat):
        return any(re.search(sel_pat, sel) and re.search(decl_pat, bd, re.I)
                   for sel, bd, _s, _e in brace_blocks(css_nc))

    # ---- S1 底盘存在：.stage 锁 1920×1080（舞台尺寸是版率口径的分母）----
    _has_stage = bool(re.search(r'class\s*=\s*["\'][^"\']*\bstage\b', body)
                      or re.search(r'id\s*=\s*["\']stage["\']', body))
    _stage_decl = "\n".join(bd for sel, bd, _s, _e in brace_blocks(css_nc) if re.search(r"\.stage\b", sel))
    if not _has_stage:
        sk_hits.append(("S1", "缺 `.stage` 舞台容器（v2 底盘唯一根：1920×1080 固定舞台 + 等比缩放）"
                              " → 复制 assets/chassis-v2.html 作起点，别自造骨架"))
    elif not (re.search(r"width\s*:\s*1920px", _stage_decl)
              and re.search(r"height\s*:\s*1080px", _stage_decl)):
        sk_hits.append(("S1", "`.stage` 未锁 1920×1080（width:1920px / height:1080px 缺一）"
                              " → 舞台尺寸是版率阈值与本脚本所有几何判据的分母，改了就全线失效"))

    # ---- S2 页集与翻页状态机：section.slide + classList 切 .active ----
    _n_slides = len(re.findall(r'<section\b[^>]*class\s*=\s*["\'][^"\']*\bslide\b', body))
    if not _n_slides:
        sk_hits.append(("S2", "没有任何 `section.slide` 页容器 → 底盘页骨架未落地（chassis 的 .slide 带"
                              " position:absolute/inset:0 与 .active 显隐）"))
    else:
        if not re.search(r"querySelectorAll\(\s*['\"]\.slide['\"]", js_all):
            sk_hits.append(("S2", "翻页 JS 未用 `querySelectorAll('.slide')` 收集页 —— 页集合与 DOM 脱钩，"
                                  "加页即漏翻（chassis 用 slides 数组 + go(n)）"))
        if not re.search(r"classList\.(?:add|toggle)\(\s*['\"]active['\"]", js_all):
            sk_hits.append(("S2", "翻页未通过 `classList.add('active')` 切页 —— chassis 靠 .slide.active 控制"
                                  "显示，另立一套显隐机制会与 CSS 打架（两页同显或全黑）"))

    # ---- S3 每页边注必备件（folio 页码位 + footmark 落款位）----
    #    这两件是版率探针的排除锚点（量版率时剔除边注），缺了会被当正文算进版面率
    _miss_marg = []
    for _pi, (_pa, _pinner) in enumerate(pages, 1):
        _miss = [c for c in ("folio", "footmark")
                 if not re.search(r'class\s*=\s*["\'][^"\']*\b%s\b' % c, _pinner)]
        if _miss:
            _miss_marg.append("P%d 缺 %s" % (_pi, "/".join(_miss)))
    if _miss_marg:
        _shown = "; ".join(_miss_marg[:3]) + ("（共 %d 页）" % len(_miss_marg) if len(_miss_marg) > 3 else "")
        sk_hits.append(("S3", "边注必备件不全：%s → 每页保留 folio（页码）+ footmark（落款），"
                              "corner-note/hint 按需；这两件是版率探针的排除锚点，缺了量测会把边注算进正文"
                              % _shown))

    # ---- S4 :root token 齐全（token 是三层红线的唯一落点）----
    _TOKENS = ("--bg", "--ink", "--ink-dim", "--accent", "--hairline",
               "--fs-title", "--fs-quote", "--fs-body", "--fs-punch", "--fs-meta", "--fs-marg",
               "--s-in", "--s-mid", "--s-out", "--pad-v", "--pad-h")
    _root_decl = "\n".join(bd for sel, bd, _s, _e in brace_blocks(css_nc) if ":root" in sel)
    _miss_tok = [t for t in _TOKENS if not re.search(r"%s\s*:" % re.escape(t), _root_decl)]
    if not _root_decl:
        sk_hits.append(("S4", "整份产物无 `:root` token 段 → 字号/间距/颜色全靠生成端自由填，三层红线无处落地"
                              " → 照 chassis-v2 的 :root 段整段复制"))
    elif _miss_tok:
        sk_hits.append(("S4", ":root 缺 token %d 个（%s）→ 缺一个就有一个值可以乱填，红线随之失效"
                              % (len(_miss_tok), " ".join(_miss_tok))))

    # ---- S5 翻页通道存在，且翻页函数体内零动态 DOM（翻页事故的机验化）----
    # 2026-10-22 结账重设计：判据收窄为「function go() 体内零 DOM 增删」——底盘有四个合法动态点
    # （提词面板渲染 paint / Preview-only 条件注入 / 演讲者独立窗口 / typewriter 逐字动画件），
    # 全不在翻页路径；「全文档扫 DOM API + 逐点豁免」当日连修四点仍误报，按立意精确化到翻页函数体。
    _go = re.search(r"function\s+go\s*\([^)]*\)\s*\{", js_all)
    _go_body = ""
    if _go:
        _depth = 0
        _end = len(js_all)
        for _i in range(_go.end() - 1, len(js_all)):
            _ch = js_all[_i]
            if _ch == "{":
                _depth += 1
            elif _ch == "}":
                _depth -= 1
                if _depth == 0:
                    _end = _i
                    break
        _go_body = js_all[_go.end():_end]
    if not _go_body.strip():
        sk_hits.append(("S5", "未找到翻页函数 `function go(n)`——chassis 标准翻页入口缺失（翻页只切 class 的前提是入口存在）"))
    elif re.search(r"\.(?:createElement|insertAdjacentHTML|write)\s*\(|innerHTML\s*=", _go_body):
        sk_hits.append(("S5", "翻页函数 go() 体内有动态 DOM 操作——翻页事故：切页时动态增删节点会与动画时序互抢"
                              "（一次点击翻两页 / 动画不重播）→ 翻页只切 class，节点一律静态预印（动画件在页内自理，不进翻页路径）"))
    if not re.search(r"addEventListener\(\s*['\"]key(?:down|up)", js_all):
        sk_hits.append(("S5", "缺键盘翻页监听（keydown → 上一页/下一页）→ 投影现场没有鼠标或遥控失灵时的唯一通道"))
    if not re.search(r"addEventListener\(\s*['\"]click", js_all):
        sk_hits.append(("S5", "缺点击翻页监听（chassis 标准做法：click 按 clientX 分左右半屏）"))

    # ---- S6 舞台等比缩放（1920 舞台在 1080p 以下的屏上不裁边）----
    if _has_stage and not re.search(r"Math\.min\([^)]*1920", js_all):
        sk_hits.append(("S6", "缺舞台等比缩放（`Math.min(innerWidth/1920, innerHeight/1080)` + `transform:scale`）"
                              " → 不缩放时 1920 舞台在 1440/1366 屏上被裁掉两侧内容"))

    # ---- S7 帧预印动画 + 无障碍豁免 ----
    if not (_has_css_rule(r"\.rv\b", r"opacity\s*:\s*0") and re.search(r"@keyframes\s+[\w-]+", css_nc)):
        sk_hits.append(("S7", "入场动画缺帧预印（`.rv{opacity:0}` + `@keyframes`）→ chassis 的纪律是 frame "
                              "pre-printed（帧先印好、内容后到），缺了就变「生成时可见、放映时乱跳」"))
    if not re.search(r"prefers-reduced-motion", css_nc):
        sk_hits.append(("S7", "缺 `@media (prefers-reduced-motion: reduce)` 豁免块 → 无障碍红线："
                              "系统开了减弱动效必须关动画"))

    # ---- S8 无 v1 残留（套旧模板一锤定音）----
    _V1_PATTERNS = (
        (r"Reveal\s*\.\s*(?:initialize|slide|getCurrentSlide)", "Reveal.js 初始化/翻页 API"),
        (r'class\s*=\s*["\'][^"\']*\breveal\b', 'Reveal.js 根容器 class="reveal"'),
        (r'data-state\s*=\s*["\'](?:cover|end)["\']', "v1 封面/结束页标记 data-state"),
        (r'class\s*=\s*["\'][^"\']*\b(?:slide-title|slide-head|slide-body|cover-subtitle|speaker-notes|edit-mode)\b',
         "v1 两段式骨架 / 编辑模式 / 演讲者类名"),
        (r'function\s+autoPositionImages\b', "v1 图片自动定位函数"),
        (r"\bboilerplate\b", "v1 骨架引用（boilerplate）"),
    )
    _v1_hits = []
    for _pat, _label in _V1_PATTERNS:
        _ms = list(re.finditer(_pat, html))
        if _ms:
            _v1_hits.append("%s（line %d%s）"
                            % (_label, _line_no(html, _ms[0].start()),
                               "" if len(_ms) == 1 else " 等 %d 处" % len(_ms)))
    if _v1_hits:
        _v1_deck = (not _has_stage) and bool(re.search(r"\breveal\b", html, re.I))
        sk_hits.append(("S8", "%s：%s → %s"
                        % ("整稿仍是 v1 骨架（Reveal.js 时代）" if _v1_deck else "v2 底盘混入 v1 残留",
                           "；".join(_v1_hits),
                           "v2 范式已换代，存量 v1 稿只作归档；要交付须按 assets/chassis-v2.html 重制"
                           if _v1_deck else
                           "清掉这些残留——v2 底盘不需要 Reveal / 两段式骨架 / 编辑模式 / 图片定位函数")))
    # 348 step 叙事时序与初见密度（2026-10-20 立 fragment 版：「附近」页事故；
    #     2026-10-22 结账 .step 化——v2 用 .step 逐条揭示，收尾金句=压轴行 .punch，正文组=.row/.card）
    for _pi, (_pa, _pinner) in enumerate(pages, 1):
        if not re.search(r'class\s*=\s*["\'][^"\']*\bstep\b', _pinner):
            continue
        _m = re.search(r'class\s*=\s*(["\'])([^"\']*\bpunch\b[^"\']*)\1', _pinner)
        if _m and 'step' not in _m.group(2):
            sk_hits.append(("348", "P%d 收尾压轴行 `.punch` 未挂 step——时序倒挂（结论先亮、论据逐条后出，"
                                   "初见只剩一句显空）→ 压轴行挂 step 并排 step 序列最后（核心原则 8："
                                   "过程型结论压轴）" % _pi))
        for _cls in ('row', 'card'):
            _cls_insts = [c for _q, c in re.findall(r'class\s*=\s*(["\'])([^"\']*)\1', _pinner)
                          if _cls in c.split()]
            if len(_cls_insts) >= 2 and all('step' in c for c in _cls_insts):
                sk_hits.append(("348", "P%d 的 %d 个 `.%s` 全挂 step——初见零正文（翻到即空页）"
                                       " → 首条去 step 保底可见，其余逐条（animation-routing §四 step 叙事纪律）"
                                       % (_pi, len(_cls_insts), _cls)))
                break

    # 349 数字排版（2026-10-20 立：「抗AI页」事故——2 个数字条 flex:1 铺满
    #     与下方 3 卡强行同幅 + 数字装色块；真源 references/number-typography.md）
    # a) 数字条子项 flex:1 铺满（宽度应按内容收缩，数量不匹配禁强行同幅）
    for _sel, _bd, _s1, _e1 in brace_blocks(css):
        if re.search(r'(metric-strip|stat-strip|kpi-strip|num-strip|data-strip)', _sel) \
                and re.search(r'flex\s*:\s*1\b', _bd):
            sk_hits.append(("349", "数字条 `%s` 子项 flex:1 铺满整行——与卡片组强行同幅（数字少被拉宽）"
                                   " → 子项改 flex:0 0 auto 按内容收缩（number-typography §1 宽度纪律）"
                                   % re.sub(r'\s+', ' ', _sel)[:60]))
    # b) 多数字并列缺 tabular-nums（≥2 个数字容器类且全文档无等宽数字设置）
    _num_cls_insts = [c for _q, c in re.findall(r'class\s*=\s*(["\'])([^"\']*)\1', body)
                      if any(k in c.split() for k in ('metric-val', 'stat-number', 'data-big', 'data-num'))]
    if len(_num_cls_insts) >= 2 and 'tabular-nums' not in css:
        sk_hits.append(("349", "%d 个数字容器（metric-val/stat-number/data-big）但 CSS 无 `font-variant-numeric:"
                               " tabular-nums`——多数字并列纵向参差 → 数字类补等宽数字"
                               "（number-typography §1 铁律 2）" % len(_num_cls_insts)))
    # c) 数字直接装色块（chip/badge/pill 类块有背景且直系文本以数字开头；角条/淡染是合法替代）
    for _sel, _bd, _s2, _e2 in brace_blocks(css):
        if not re.search(r'background(?!-)', _bd) or re.search(r'background\s*:\s*(none|transparent)', _bd):
            continue
        for _clsname in re.findall(r'\.((?:[\w-]*)(?:chip|badge|pill|num-box|stat-box|metric-box)[\w-]*)', _sel):
            for _m2 in re.finditer(r'class\s*=\s*(["\'])[^"\']*\b%s\b[^"\']*\1\s*>\s*([^<]{0,20})'
                                   % re.escape(_clsname), body):
                if re.match(r'\s*\d', _m2.group(2)):
                    sk_hits.append(("349", "数字「%s」直接装在色块 .%s 上——盒边界与文本基线两套对齐打架"
                                           " → 数字去色块，强调改角条/下划线/淡染三选一"
                                           "（number-typography §1 铁律 1）"
                                           % (_m2.group(2).strip()[:10], _clsname)))
                    break

    _sk_tags_hit = sorted({t for t, _m in sk_hits})
    result["skeleton_checks_total"] = 10
    result["skeleton_checks_hit"] = _sk_tags_hit
    result["skeleton_hits_detail"] = ["[%s] %s" % (t, m) for t, m in sk_hits]
    for t, m in sk_hits:
        fails.append("[骨架#12·%s] %s" % (t, m))

    # ===== 13. 可视化规范（图表 C-1~C-4 + 图示 D-2/D-3）：C-1~C-4/D-2 = FAIL，D-3 = 提示 =====
    vis_hits = []
    _js_scripts = re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.S)
    _chart_js = "\n".join(s for s in _js_scripts if "echarts" in s or "chartConfigs" in s)

    # C-1 图内字号地板（ECharts 渲到 canvas，DOM 字号探针量不到，只能扫源码）
    if _chart_js:
        _small_fs = sorted({v for v in re.findall(r"fontSize\s*:\s*([\d.]+)", _chart_js)
                            if float(v) < 11.5})
        if _small_fs:
            vis_hits.append(("C-1", "图表 option 里 fontSize %s（<11.5 不合格）"
                                   " → 轴标签/图内文字统一 ≥12（chart-recipes §4）" % "/".join(_small_fs)))

    # C-2 图表页缺来源脚（图表数字绕过红线①锚定；2026-10-22 结账对齐 v2：来源脚落角落位 footmark/corner-note 或"来源"字样，v1 .source 类已死）
    _chart_nosrc = ["P%d" % pi for pi, (_a, inner) in enumerate(pages, 1)
                    if (re.search(r'id\s*=\s*["\']chart', inner)
                        or re.search(r'class\s*=\s*["\'][^"\']*\bchart\b', inner))
                    and not (re.search(r'class\s*=\s*["\'][^"\']*\b(?:footmark|corner-note)\b', inner)
                             or '来源' in inner)]
    if _chart_nosrc:
        vis_hits.append(("C-2", "图表页 %s 缺来源脚 → 角落位补来源（footmark/corner-note 或含「来源」字样：机构/文献，日期）"
                               % ", ".join(_chart_nosrc)))

    # C-3 柱/条 Y 轴显式非 0 min（只报显式正例，"没写 min"默认多为 0 不报——防误报）
    if re.search(r"type\s*:\s*['\"]bar['\"]", _chart_js):
        _bad_min = [v for v in re.findall(r"\bmin\s*:\s*([\d.]+)", _chart_js) if float(v) != 0]
        if _bad_min:
            vis_hits.append(("C-3", "柱/条图 Y 轴 min=%s 非 0 起（截断轴放大差异误导，FT 铁律）"
                                   " → 删掉 min 或改 min:0" % "/".join(_bad_min)))

    # C-4 环形/饼组件 >5
    if re.search(r"type\s*:\s*['\"]pie['\"]", _chart_js):
        for m in re.finditer(r"type\s*:\s*['\"]pie['\"]", _chart_js):
            dm = re.search(r"data\s*:\s*\[([^\]]*)\]", _chart_js[m.start():m.start() + 900])
            if dm:
                n_items = len(re.findall(r"value\s*:", dm.group(1))) or \
                          len(re.findall(r"\d+", dm.group(1).split(",")[0]))
                if n_items > 5:
                    vis_hits.append(("C-4", "环形/饼图组件 %d 项（>5 投影距离下不可读）→ 改堆叠条形"
                                           "（chart-recipes §1 占比构成备用档）" % n_items))
                    break

    # D-2 图示 CSS 写死色值（只扫 .g-* 选择器块，:root 定义区豁免）
    _g_hex = []
    for sel, bd, _s, _e in brace_blocks(css_nc):
        if ":root" in sel or not re.search(r"\.g-", sel):
            continue
        _g_hex += [h for h in re.findall(r"#[0-9a-fA-F]{3,8}\b", bd)]
    if _g_hex:
        vis_hits.append(("D-2", "图示 CSS 写死色值 %d 处 → 一律 var(--g-tone-*) / var(--accent*)，"
                               "换主题图不翻车（diagram-patterns §4）" % len(_g_hex)))

    # D-3 图示节点超上限（口径=整页计数，一页一主图为主场景；pipeline/timeline ≤5、radial/funnel/matrix ≤4）
    _NODE_CAP = {"g--pipeline": 5, "g--timeline": 5, "g--radial": 4, "g--funnel": 4, "g--matrix": 4}
    for pi, (_a, inner) in enumerate(pages, 1):
        _modes = [mo for mo in _NODE_CAP if re.search(r'class\s*=\s*["\'][^"\']*\b%s\b' % mo, inner)]
        if not _modes:
            continue
        n_nodes = len(re.findall(r'class\s*=\s*["\'][^"\']*\bg-node\b', inner))
        if n_nodes > min(_NODE_CAP[mo] for mo in _modes):
            vis_hits.append(("D-3", "P%d 图示 %s 共 %d 节点超上限（≤%d，整页计数口径）"
                                   " → 拆页或砍节点（diagram-patterns §4）"
                                   % (pi, "+".join(_modes), n_nodes, min(_NODE_CAP[mo] for mo in _modes))))

    _vis_tags_hit = sorted({t for t, _m in vis_hits})
    result["vis_checks_total"] = 6
    result["vis_checks_hit"] = _vis_tags_hit
    result["vis_hits_detail"] = ["[%s] %s" % (t, m) for t, m in vis_hits]
    for t, m in vis_hits:
        if t == "D-3":   # 节点上限是经验阈值（≤4/≤5），只提示不拦交付
            hints.append("[可视化#13·%s] %s" % (t, m))
        else:
            fails.append("[可视化#13·%s] %s" % (t, m))

    # ===== 14. 口径自洽（2026-10-20 重构第二批 T8；计入 FAIL 面）=====
    #    起因：同一口径写在多处（脚本 docstring / README / SKILL），改一处必漂。
    #    本批实测到的三处漂移：SKILL 曾写「八项判据 / 十项 FAIL / 12 组检查」、README 写
    #    「九项判据 / 14 组检查」、verify-layout docstring 又写「八项判据」而它自己列到判据 9。
    #    做法：实际值一律从源码算（禁写死），宣称值从文档抓，不一致即 FAIL 并给 文件:行，
    #    逼改的人当场决定「改文档还是改脚本」。
    #    本项自始不设阈值缓冲：断言对象是文档与源码，不扫产物、不依赖稿件形态。
    #    0 处宣称不判 FAIL：文档把数字删干净正是新口径的目标态，不能反过来变成失败。
    _ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

    def _read_rel(name):
        try:
            with open(os.path.join(_ROOT, name), encoding="utf-8", errors="replace") as fh:
                return fh.read()
        except OSError:
            return ""

    _layout_doc = ""  # 2026-10-22：verify-layout.py 已退役（v1 件），判据数维度随之作废，仅保留组数/FAIL 面比对

    _CN_DIG = "零一二三四五六七八九"

    def _cn2int(tok):
        if tok.isdigit():
            return int(tok)
        total, cur = 0, 0
        for ch in tok:
            if ch == "十":
                total += (cur or 1) * 10
                cur = 0
            else:
                i = _CN_DIG.find(ch)
                if i < 0:
                    return None
                cur = i
        return total + cur

    # 组数 = 本文件 docstring 编号最大值（判据数维度已随 verify-layout 退役）
    _src_groups = max([int(x) for x in re.findall(r"^\s+(\d+)\.\s", __doc__ or "", re.M)] or [0])
    _src_criteria = 0
    # FAIL 面 = 源码中失败追加调用的次数；needle 用拼接构造，避免「字面量自命中」多算一次
    _src_fails = load(os.path.abspath(__file__)).count("fails" + ".append(")

    _DECL_PATTERNS = (
        ("group", re.compile(r"(\d+)\s*组检查")),
        ("group", re.compile(r"观感\s*(\d+)\s*项")),
        ("group", re.compile(r"(\d+)\s*check groups", re.I)),
        ("criteria", re.compile(r"([一二三四五六七八九十]+|\d+)\s*项判据")),
        ("criteria", re.compile(r"(\d+)\s*criteria", re.I)),
    )
    _drifts, _decl_n = [], 0
    for _name in ("README.md", "SKILL.md"):   # README_en.md 不存在（若将来补英文版再挂回）
        for _li, _line in enumerate(_read_rel(_name).splitlines(), 1):
            for _kind, _pat in _DECL_PATTERNS:
                for _m in _pat.finditer(_line):
                    _val = _cn2int(_m.group(1))
                    if _val is None:
                        continue
                    _decl_n += 1
                    _actual = _src_groups if _kind == "group" else _src_criteria
                    _unit = "组" if _kind == "group" else "项判据"
                    if _val != _actual:
                        _drifts.append(
                            "口径漂移：%s:%d 宣称 %d %s，脚本实为 %d %s → 改文档或改脚本，二者必须一致"
                            % (_name, _li, _val, _unit, _actual, _unit))

    result["src_groups"] = _src_groups
    result["src_fails"] = _src_fails
    result["src_criteria"] = _src_criteria
    result["decl_count"] = _decl_n
    result["consistency_drifts"] = _drifts
    if _drifts:
        fails.append("；".join(_drifts))

    # ===== 15. 封面断言（2026-10-24 立，真源 decoration-vocab §五封面构图总纲） =====
    #     治「平庸封面交卷」（AI投毒首版病历：徽标+两行标题+一条线+副题，无视觉事件，权限全开也没用）。
    #     a) 视觉事件三证据（FAIL）：封面（第一个 section.slide）占其一即过——stamp 级语义数字
    #        （.stamp-num/.cm-v）/ .has-metrics+.cover-metrics / .dv- 装置标记（类名前缀或 data-device）。
    #        全缺 = 平庸封面。纯大标题不算数（标题字号再大不构成视觉事件）。
    #     b) 装饰可见度（FAIL）：.deco .grid/.scan 线色 color-mix 百分比 × opacity 对 --bg 的
    #        有效对比度 <1.1:1 = 隐身（dim 档 grid 深底 1.03:1 实测 bug 即此抓法——调浓不删）。
    #     c) 装饰件数（FAIL）：.deco 容器直接子元素 >2 = 违「一页装饰 ≤2 件」。
    #     d) 焦点让位（提示）：.stamp-num 与 .cover-title 同在封面且 CSS 字号比 <1.3 = 让位不足。
    #     e) 口径注（提示）：检出 .stamp-num 但无 .stamp-pre/.stamp-axis/.cm-l 伴随。
    cover_event = None
    if pages:
        _cov_attrs, _cov_inner = pages[0]
        _cov_cls = set(re.findall(r'class\s*=\s*["\']([^"\']+)', _cov_attrs))
        _cov_cls |= set(c for _t, a in tags(_cov_inner) for c in (a.get("class") or "").split())
        _has_stamp = bool(_cov_cls & {"stamp-num", "cm-v"})
        _has_metrics = "has-metrics" in _cov_cls and "cover-metrics" in _cov_cls
        _has_dv = any(c.startswith("dv-") for c in _cov_cls) or any("data-device" in a for _t, a in tags(_cov_inner))
        cover_event = {"stamp": _has_stamp, "metrics": _has_metrics, "dv": _has_dv}
        result["cover_visual_event"] = cover_event
        if not (_has_stamp or _has_metrics or _has_dv):
            fails.append("平庸封面：视觉事件证据全缺（无 stamp 级数字 / 无 .has-metrics+.cover-metrics / "
                         "无 .dv- 装置标记）→ 按 decoration-vocab §五：排版装置（stamp 巨数/编辑语法）"
                         "为默认经营项，纯大标题不算视觉事件")
        if _has_stamp and "cover-title" in _cov_cls:
            def _rule_fs(cls):
                for sel, bd, _s, _e in brace_blocks(css_nc):
                    if re.search(r'\.%s\b' % cls, sel):
                        m = re.search(r'font-size\s*:\s*([\d.]+)px', bd)
                        if m:
                            return float(m.group(1))
                return None
            _fs_stamp, _fs_title = _rule_fs("stamp-num"), _rule_fs("cover-title")
            if _fs_stamp and _fs_title and _fs_stamp / max(_fs_title, 1) < 1.3:
                hints.append("封面焦点让位疑似不足：stamp %gpx vs 标题 %gpx（<1.3 倍）——"
                             "stamp 当主角时标题应退档（AI投毒标本 228→104）" % (_fs_stamp, _fs_title))
        if "stamp-num" in _cov_cls and not (_cov_cls & {"stamp-pre", "stamp-axis", "cm-l"}):
            hints.append("封面巨型数字缺口径注（.stamp-pre/.stamp-axis/.cm-l 皆无）→ "
                         "钩子四约束第 2 条：数字必带口径（「2分钟」必带「从发布到被采纳」）")
    # b) 装饰可见度：deck 实际使用的 .deco 词条对底色算有效对比度（复用 11a 的 _ratio/_tok/bgc）
    #    使用前提（2026-10-24 复查补）：body 没挂 .deco / 没用对应词条时不判——CSS 里留着旧参数
    #    词条规则 ≠ 页面用了它，不设前提会把「不用装饰的合法 deck」与存量旧稿永久判红。
    #    dim 档按连乘取保守值：有效 opacity = 基础规则 op × dim 规则 op（新 CSS 基础规则
    #    无 opacity=1，连乘与覆盖两读法数值等价；旧稿两级都有 opacity 时连乘更低、防高估可见度）。
    deco_invis = []
    _body_cls = set()
    for _cm in re.finditer(r'class\s*=\s*["\']([^"\']+)["\']', body):
        _body_cls |= set(_cm.group(1).split())
    _deco_dim_used = any(
        "deco" in _cs and "dim" in _cs
        for _cs in (m.group(1).split() for m in re.finditer(r'class\s*=\s*["\']([^"\']+)["\']', body)))
    if bgc and "deco" in _body_cls:
        _ink3 = _tok('--ink')
        _base_op, _dim_op, _pcts = {}, {}, {}
        for sel, bd, _s, _e in brace_blocks(css_nc):
            _w = re.search(r'\.deco(\.dim)?\s+\.(grid|scan)\b', sel)
            if not _w:
                continue
            _m = re.search(r'opacity\s*:\s*([\d.]+)', bd)
            _op = float(_m.group(1)) if _m else 1.0
            if _w.group(1):                    # .deco.dim 词条规则：只带 opacity 折扣
                _dim_op[_w.group(2)] = _op
            else:                              # 基础规则：opacity + color-mix 浓度
                _base_op[_w.group(2)] = _op
                _pcts[_w.group(2)] = [float(_p) for _p in re.findall(r'color-mix\([^{};]*?([\d.]+)\s*%', bd)]
        for _kind in ("grid", "scan"):
            if _kind not in _body_cls or _kind not in _base_op:
                continue                       # 页面没用该词条 / CSS 未定义：不判
            for _p in _pcts[_kind]:
                if not _ink3:
                    break
                for _sfx, _op in (("", _base_op[_kind]),
                                  ("（dim）", _base_op[_kind] * _dim_op.get(_kind, 1.0))):
                    if _sfx and not _deco_dim_used:
                        continue
                    _alpha = (_p / 100.0) * _op
                    _cr = round(_ratio((*_ink3[:3], _alpha), bgc), 2)
                    if _cr < 1.1:
                        deco_invis.append("%s%s 有效覆盖 %.1f%%（对比度 %.2f:1 <1.1 隐身）"
                                          % (_kind, _sfx, _alpha * 100, _cr))
    deco_invis = list(dict.fromkeys(deco_invis))   # 同词条同数值只报一次（双渐变线不双报）
    result["deco_invisible"] = deco_invis
    for s in deco_invis[:3]:
        fails.append("装饰隐身：%s → 调浓词条参数（mix 百分比或 opacity），不是删装饰——"
                     "「设计上算数」的前提是看得见" % s)
    # c) 装饰件数：.deco 容器直接子元素 ≤2
    #    2026-10-24 复查修：class 精确分词（防 deco-wrap/deco-stage 误计）+ 统计任意标签（不只 div）
    deco_over = []
    for m in re.finditer(r'<(\w+)[^>]*class\s*=\s*["\']([^"\']+)["\'][^>]*>', body):
        if "deco" not in m.group(2).split():
            continue
        _tag = m.group(1)
        _seg = body[m.end():]
        _depth, _pos = 1, 0
        for _t in re.finditer(r'<%s\b|</%s>' % (_tag, _tag), _seg):
            _depth += 1 if _t.group(0).startswith('<' + _tag) else -1
            if _depth == 0:
                _pos = _t.start()
                break
        _inner = _seg[:_pos]
        # void 元素（img/br/hr 等无闭合标签）计件但不增深度——深度只增不减会把
        # 后续真子元素全部漏计（2026-10-24 审核实测：.deco 内 <img>+2×<div> 真 3 件报 0 件）
        _VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                 "link", "meta", "param", "source", "track", "wbr"}
        _cnt, _d = 0, 0
        for _t in re.finditer(r'<(\w+)[^>]*>|</(\w+)>', _inner):
            if _t.group(1):
                if _d == 0:
                    _cnt += 1
                if _t.group(1).lower() not in _VOID:
                    _d += 1
            else:
                _d -= 1
        if _cnt > 2:
            deco_over.append(_cnt)
    result["deco_child_over"] = deco_over
    if deco_over:
        fails.append("装饰件数超限：.deco 容器直接子元素 %s（>2）→ 违「一页装饰 ≤2 件」"
                     % "、".join(map(str, deco_over[:3])))

    result["fails"] = fails
    result["hints"] = hints
    result["warns"] = hints          # 兼容旧键名：语义已改为「提示」，不参与判定
    result["verdict"] = "FAIL" if fails else "PASS"

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0 if not fails else 1

    print("=" * 78)
    print("静态一致性探针 —", os.path.basename(path))
    print("=" * 78)
    print("扫描基数  section %d / class 属性 %d / 内联 style %d / svg %d / css 规则 %d"
          % (scan["section"], scan["class_attr"], scan["inline_style"], scan["svg"], scan["css_rule"]))
    print("强调容器频次：", result["containers"])
    print("强调形态数：%d 种" % result["emphasis_containers"])
    print("缺 hl 卡片：%d 个" % result["cards_missing_hl"])
    print("内联字号：%d 处｜<11.5px（统一口径）%d 处｜低于技能双轨地板 %d 处"
          % (result["inline_fontsize"], result["inline_fontsize_below_floor_uniform"],
             result["inline_fontsize_below_floor_skill"]))
    print("内联硬编码颜色：%d 处" % result["inline_hex_colors"])
    print("页间竖间距：%s" % (result["gap_values"] or "统一"))
    print("光晕 border-important 规则：%d 条" % len(result["glow_border_important"]))
    print("单列纵排逃逸：%s" % ([(e["page"], e["items"]) for e in result.get("single_column_escape", [])] or "无"))
    print("孤儿 class：%d 个%s｜悬空 CSS 变量：%s"
          % (len(result["orphan_classes"]),
             ("（致命: %s）" % ", ".join("." + c for c in result["orphan_classes_critical"]))
             if result["orphan_classes_critical"] else "",
             ", ".join(result["dangling_vars"]) or "无"))
    print("骨架完整性（#12）：%d/%d 组通过%s"
          % (result["skeleton_checks_total"] - len(result["skeleton_checks_hit"]),
             result["skeleton_checks_total"],
             ("｜命中: %s" % ", ".join(result["skeleton_checks_hit"])) if result["skeleton_checks_hit"] else ""))
    print("可视化规范（#13）：%d/6 组通过%s"
          % (6 - len(result["vis_checks_hit"]),
             ("｜命中: %s" % ", ".join(result["vis_checks_hit"])) if result["vis_checks_hit"] else ""))
    print("口径自洽（#14）：组 %d / FAIL 面 %d / 判据 %d｜文档宣称 %d 处｜差异 %d 处"
          % (result["src_groups"], result["src_fails"], result["src_criteria"],
             result["decl_count"], len(result["consistency_drifts"])))
    if not result["decl_count"]:
        print("口径自洽：文档未出现数字宣称，跳过比对")
    _ce = result.get("cover_visual_event")
    print("封面断言（#15）：视觉事件 %s｜装饰隐身 %d 处｜装饰件数超限 %d 处"
          % (("stamp√ " if _ce["stamp"] else "") + ("metrics√ " if _ce["metrics"] else "")
             + ("dv√" if _ce["dv"] else "") if _ce and (_ce["stamp"] or _ce["metrics"] or _ce["dv"])
             else ("全缺（平庸封面）" if _ce else "未检出封面页"),
             len(result.get("deco_invisible", [])),
             len(result.get("deco_child_over", []))))
    for s in result["glow_border_important"][:3]:
        print("   ·", s)
    print()
    for f in fails:
        print("  [严重]", f)
    for h in hints:
        print("  [提示]", h)
    print("\n结论:", ("干净（0 项待处理）" if result["verdict"] == "PASS"
                    else "待处理 %d 项（严重 %d / 提示 %d）——逐项处理或说明理由后交付"
                    % (len(fails) + len(hints), len(fails), len(hints))))

    if "--json-out" in sys.argv:
        out = sys.argv[sys.argv.index("--json-out") + 1]
        json.dump(result, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("明细:", out)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
