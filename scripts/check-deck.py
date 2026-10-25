# -*- coding: utf-8 -*-
"""产物同类错误检查（2026-10-22 立；2026-10-23 B 方案重构字号档位；2026-10-23 P0：解析硬化+区间化+基数自证；2026-10-23 M1：白名单换注册表自动提取）
用法: python scripts/check-deck.py <deck.html 路径>
检查四类: ① hero-num 染 accent 时单位 .u 必须显式 ink-dim
        ② SVG text 必有着色（fill 或白名单类，防深底黑字；白名单从底盘 CSS 注册表
          自动提取 @svg-text 标记——加图表文字类打标即跟，禁手抄）
        ③ text 标签不出画布（y 边界）
        ④ 字号档位（区间+地板两级，2026-10-23 区间化）：合法 = var(--fs-*) token ∪ em 系列
          ∪ [8.4, 176] px 区间（rem 按 16 换算）。越界 → [严重] exit 1（地板 8.4=layout-rules §2.2
          署名豁免值；上限 176=number-typography R4 焦点数字上限）；区间内但非底盘/规则档位 →
          [提示] 留痕不拦截（创意值放行）。替代原「枚举白名单外即报」形态——曾把规则批准的
          13/15px 误杀（F2），白名单式判据也反创作自由。底盘实有档位仍自动提取，改底盘自动跟。
 基数自证（M9）：body 切分过短 / 未找到 <body> / 产物 CSS 无 font-size / SVG 白名单 <5 类 →
          「解析异常/基准为空」不得 PASS——「没解析到」≠「看见了没事」，单引号整稿曾让检查全绿。"""
import re, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = sys.argv[1] if len(sys.argv) > 1 else None
if not DECK:
    print('用法: python check-deck.py <deck.html 路径>'); sys.exit(1)
s = open(DECK, encoding='utf-8').read()

# —— body 切分：锚 </head>（core.css:56 注释里有字面量 <body>，按首次出现切会切进样式表，2026-10-23 修）
_m = re.search(r'</head>\s*<body[^>]*>', s, re.S)
body = (s[_m.end():] if _m else s.split('<body', 1)[1] if '<body' in s else '').split('<script', 1)[0]
# —— 属性规范化视图（2026-10-23 M8）：单引号属性值统一双引号、属性名转小写。
#    只对切掉 <script> 的 body 做；单引号 HTML 是合法产物写法，解析层不得对它失明。
body = re.sub(r"([A-Za-z-]+)\s*=\s*'([^'\n]*)'",
              lambda m: m.group(1).lower() + '="' + m.group(2) + '"', body)

def content_css(html):
    """全部 <style> 内容，剔除工具件模块段——interactions(按钮/提词面板 12/14/17px) 与
    print(打印导出 10/11/12/14/16/42px) 的字号是工具档，不属投影版面档位，不参与基准也不受检。
    每个 style 段独立切块剔除：drop 状态不跨段（末段以 print 结尾时不能把生成端新增段连带丢弃）"""
    keep = []
    for seg in re.findall(r'<style[^>]*>(.*?)</style>', html, re.S):
        parts = re.split(r'(/\* ===== modules/[^*]+ ===== \*/)', seg)
        out, drop = [], False
        for p in parts:
            if p.startswith('/* ===== modules/'):
                drop = ('interactions' in p) or ('print' in p)
            elif not drop:
                out.append(p)
        keep.append('\n'.join(out))
    return '\n'.join(keep)

issues = []   # 严重：exit 1
hints = []    # 提示：留痕不拦截

# —— 基数自证（M9）：检查器对这份文件失明时不得 PASS
if not _m and '<body' not in s:
    issues.append('解析异常：未找到 <body> → 检查器对这份文件失明，勿当通过')
if len(body) < 200:
    issues.append('解析异常：body 切分仅 %d 字符 → 先查文件结构与 <body> 锚点，勿当通过' % len(body))

for m in re.finditer(r'<div class="(hero-num[^"]*)"([^>]*)>([^<]*)<span class="u"([^>]*)>', body):
    cls, attrs, num, u = m.groups()
    if 'accent' in attrs and 'ink-dim' not in u:
        issues.append('单位未灰: ' + num.strip())

# —— 标题句末句号率（0-23 立，title-copy-types 标点纪律）：标题不用句末句号；问/叹按语气保留；
#    引文照抄；>1/3 出提示不拦截（3 页起启用，避免小样本失真）
_h2s = [re.sub(r'<[^>]+>', '', t).strip() for t in re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S)]
if len(_h2s) >= 3:
    _ended = sum(1 for t in _h2s if t.endswith('。') or t.endswith('.'))
    if _ended * 3 > len(_h2s):
        hints.append('标题句号率 %d/%d（>1/3）：页面标题不用句末句号，问/叹按语气保留，引文照抄' % (_ended, len(_h2s)))

# SVG 文字白名单：底盘 CSS 注册表自动提取（M1，2026-10-23，原手抄 7 类已删——
# 行内标记 @svg-text 打在 .chart 文字类定义块，加新图表文字类打标即自动跟）
def _blocks(css):
    out, i, n, cur = [], 0, len(css), 0
    while i < n:
        if css[i] == '{':
            d, j = 1, i + 1
            while j < n and d:
                d += (css[j] == '{') - (css[j] == '}')
                j += 1
            out.append((css[cur:i].strip(), css[i+1:j-1]))
            cur = j
            i = j
            continue
        i += 1
    return out

WL = set()
try:
    _src = open(os.path.join(PKG, 'assets', 'chassis-v2.html'), encoding='utf-8').read()
    _css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', _src, re.S))
    _dm = re.search(r'@svg-text-declared\s*:\s*([^*]+)', _css)
    if _dm:
        WL.update(_dm.group(1).strip().split())
    for _sel, _bd in _blocks(_css):
        _m = re.match(r'\s*/\*\s*@svg-text\s*\*/', _bd)
        if not _m:
            continue
        for _part in _sel.split(','):
            _part = re.sub(r'::?[a-zA-Z-]+(\([^)]*\))?', '', _part.strip())
            _segs = _part.split()
            if _segs:
                WL.update(re.findall(r'\.(-?[_a-zA-Z][\w-]*)', _segs[-1]))
except OSError:
    pass
if len(WL) < 5:
    issues.append('SVG 白名单提取异常：%d 类（阈值 5）→ 底盘标记或 chassis-v2.html 损坏，勿当通过' % len(WL))

for m in re.finditer(r'<text ([^>]*)>', body):
    a = m.group(1)
    fv = re.search(r'fill="([^"]*)"', a)
    sv = re.search(r'style="([^"]*)"', a)
    c = re.search(r'class="([a-z-]+)"', a)
    in_wl = bool(c and c.group(1) in WL)
    if not fv:
        if not (in_wl or (sv and re.search(r'fill\s*:', sv.group(1)))):
            issues.append('SVG 黑字风险: ' + a[:60])

for vw, vh, inner in re.findall(r'<svg[^>]*viewbox="0 0 (\d+) (\d+)"[^>]*>(.*?)</svg>', body, re.S | re.I):
    h = int(vh)
    for y in re.findall(r'<text[^>]* y="(-?\d+)"', inner):
        y = int(y)
        if y < 20 or y > h - 6:
            issues.append('标签出画布 y=%d h=%d' % (y, h))

# —— ④ 字号档位（区间+地板两级；基准自动提取 + 规则批准档位小集合）——
deck_css = content_css(s)
if not re.search(r'font-size', deck_css, re.I):
    issues.append('档位基准为空：产物 CSS 无任何 font-size 规则 → 检查无效，勿当通过')

# 基准一（自动）：底盘内容层实有 px 档位——改底盘加档位即自动合法，无需动本文件
CHASSIS = os.path.join(PKG, 'assets', 'chassis-v2.html')
AUTO_PX = {v.lower() for v in re.findall(
    r'font-size:\s*([0-9.]+px)', content_css(open(CHASSIS, encoding='utf-8').read()), re.I)}
# 基准二（手工，稳定小集合）：规则文档批准、底盘未内置的生成期档位——改规则先改这里，出处标死
RULE_PX = {
    '28px',                                     # layout-rules §2.2 高密度行组小标题
    '72px', '76px', '88px', '96px',             # layout-rules §2.3 话题型标题密度带
    '84px',                                     # layout-rules §2.3 主张型锁死（底盘走 token，直写字面量亦合法）
    '92px',                                     # number-typography C1 metric 固定写法
    '110px', '120px', '126px', '132px',         # layout-rules §2.4 仪式位闭环 110-140（112/140 底盘已有）
    '176px',                                    # number-typography R4 焦点数字上限
    '13px', '15px',                             # layout-rules §2.2 meta 档 14-16px / 边注装饰 12-13px 豁免带内值（F2 修）
}
EM = {'0.28em', '0.36em', '0.4em', '0.42em', '0.5em', '0.6em', '0.8em', '1em'}  # em 派生（随父级档位走）
KNOWN_PX = AUTO_PX | RULE_PX
FLOOR_PX, CAP_PX = 8.4, 176.0   # 地板=layout-rules §2.2 署名豁免值；上限=number-typography R4

for v in (x.strip() for x in re.findall(r'font-size:\s*([^;}]+)', deck_css, re.I)):
    lv = v.lower()
    if lv.startswith('var(--fs-') or lv.endswith('em'):
        continue
    m = re.match(r'([0-9.]+)(px|rem)$', lv)
    if not m:
        continue  # calc()/clamp() 等表达式静态探针不判，越界数值才拦
    px = float(m.group(1)) * (16 if m.group(2) == 'rem' else 1)
    if px < FLOOR_PX or px > CAP_PX:
        issues.append('字号越界 %.1fpx（地板 8.4 / 上限 176）: ' % px + v)
    elif lv not in KNOWN_PX:
        hints.append('非底盘/规则档位（区间内放行，创意值留痕）: ' + v)

# —— ④b token 值区间（2026-10-24 对齐补）：--fs-* 的定义值同样受 8.4–176 约束 ——
#     只查 font-size 字面量会漏掉「改 token 升字号」这条主路径（实测 --fs-num-hero: 228px 仍 PASS），
#     与 SKILL 阶段 6.5「档位外的字号一律报」不符。token 名合法 ≠ 值合法，两件事分开判。
for _m in re.finditer(r'--fs-[a-z0-9-]+\s*:\s*([0-9.]+)px', deck_css, re.I):
    _px = float(_m.group(1))
    if _px < FLOOR_PX or _px > CAP_PX:
        issues.append('token 字号越界 %.1fpx（地板 8.4 / 上限 176）: %s' % (_px, _m.group(0)))

# —— 行内 font-size（0-23 补）：style="...font-size:XXpx..." 与 <style> 段同口径（区间拦截/档位提示）
for v in (x.strip() for x in re.findall(r'style="[^"]*font-size:\s*([^;"]+)', body, re.I)):
    lv = v.lower()
    if lv.startswith('var(--fs-') or lv.endswith('em'):
        continue
    m = re.match(r'([0-9.]+)(px|rem)$', lv)
    if not m:
        continue
    px = float(m.group(1)) * (16 if m.group(2) == 'rem' else 1)
    if px < FLOOR_PX or px > CAP_PX:
        issues.append('行内字号越界 %.1fpx（地板 8.4 / 上限 176）: ' % px + v)

# —— fill 属性被类规则覆盖（0-24 二修，svgprobe 实测定向；须在 deck_css 定义后）：
#    真实机理 = 呈现属性优先级最低：元素挂的类里若有 fill: 规则（.cy/.cv 等），fill 属性（var() 或 hex）
#    一律静默失效，与值无关；类无 fill 规则时 fill="var(…)" 合法生效（.bar 实测橙）。
#    判据 = 同一元素既有 fill 属性、又挂定义了 fill 的类，且 style 无 fill → 报；
#    style 含 fill: 者豁免（内联声明赢，最终色正确）。
FILL_CLS = set()
for _css_src in (deck_css, content_css(open(CHASSIS, encoding='utf-8').read())):
    for _sel, _bd in _blocks(_css_src):
        if re.search(r'fill\s*:', _bd):
            for _part in _sel.split(','):
                _part = re.sub(r'::?[a-zA-Z-]+(\([^)]*\))?', '', _part.strip())
                _segs = _part.split()
                if _segs:
                    FILL_CLS.update(re.findall(r'\.(-?[_a-zA-Z][\w-]*)', _segs[-1]))
for m in re.finditer(r'<(text|rect|circle|path|line|polygon|tspan)\s([^>]*)>', body):
    tag, a = m.groups()
    if 'fill="' not in a:
        continue
    sv = re.search(r'style="([^"]*)"', a)
    if sv and re.search(r'fill\s*:', sv.group(1)):
        continue
    c = re.search(r'class="([^"]+)"', a)
    if c and any(x in FILL_CLS for x in re.split(r'\s+', c.group(1).strip())):
        issues.append('fill 属性被类规则覆盖，实际不生效；要么删掉属性靠类着色，要么把颜色写进 style=: <%s %s>' % (tag, a[:60]))
    elif lv not in KNOWN_PX:
        hints.append('行内非底盘/规则档位（区间内放行）: ' + v)

for h in hints:
    print('  [提示]', h)
if issues:
    print('\n'.join('[严重] ' + i for i in issues))
    print('check-deck: %d 项严重（单位/SVG着色/标签画布/字号档位）' % len(issues))
else:
    print('check-deck: 检查全 PASS（单位/SVG着色/标签画布/字号档位）'
          + ('｜%d 条提示' % len(hints) if hints else ''))
sys.exit(1 if issues else 0)
