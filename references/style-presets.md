# 风格预设库 — 22 套（2×2 四池：暗系两类 / 亮系两类）

> 配色/组件/装饰规格真源（2026-10-23 重建：每套收录完整卡——原值色板、字体配对、签名元素、组件样式、设计规则、装饰配方）。索引与四池路由见 [presets-index.md](presets-index.md)；底盘结构永远走 chassis-v2——预设给色板原值与字体建议，产物按下方《v2 五件套映射表》折算，缺项走派生公式。

## v2 五件套映射表（产物只认这几个变量，2026-10-22 立）

> 阶段 6 结构永远走 chassis-v2，预设只供颜色与字体。**下表之外的变量名一律不许写进产物**：预设正文里的 `--bg-primary / --text-primary / --card-bg` 等历史名只作原值出处。

| v2 token | 管什么 | 取值优先级（在本节 `:root` 里找） | 缺项派生公式 |
|---|---|---|---|
| `--bg` | 页面底 | `--bg` > `--bg-primary` > `--slide-bg`/`--stage-bg` > `--bg-page`/`--bg-void`/`--cream`/`--parchment` | 无（每套必须给底色） |
| `--ink` | 主文字 | `--ink` > `--text-primary` > `--text-heading` > `--near-black`/`--ink-black`/`--clay-black` | 无（必须给） |
| `--ink-dim` | 次级文字（正文灰） | `--text-secondary` > `--text-muted` > `--dim`/`--mid`/`--text-grey`/`--text-body`/`--olive-gray` | `color-mix(in srgb, var(--ink) 58%, var(--bg))` |
| `--accent` | 唯一强调色 | `--accent` > `--accent-*` > `--fire-orange`/`--cinnabar`/`--terracotta`/`--mongo-green`/`--cy`/`--liu-gold` | 无（必须给） |
| `--hairline` | 发丝线 / 分隔 / 网格 | `--line` > `--border*` > `--hairline` | `color-mix(in srgb, var(--ink) 16%, transparent)`（暗底可 20%） |
| `--warn` | 语义辅助色（警示/风险/对比数字） | 预设卡映射块的 warn 行 | 缺省 = `var(--accent)`（= 无第二色）；只落内容禁进装饰 |

**两条纪律**：
1. **组件降级**：本节里的按钮 / 徽章 / 阴影 / 装饰线是**气质参考**；v2 底盘没有 button、卡片阴影、通用 badge（唯一 badge 是封面 `.cover-badge`）。落地产物只取颜色与字体栈，**禁止为还原按钮而新造组件类**（会触发孤儿类断言 FAIL）。
2. **缺项一律按公式派生**，禁现场臆造色值——这是同一套预设跨 deck 不跑偏的唯一保障。

## 字体落地表（跨平台栈规则，2026-10-22 立）

> **技能包不随带任何字体文件。** 字体属于使用者的运行环境：他装了某字体，CSS 里写了原名就自动命中；没装就自动回落。包内只规定"栈怎么写"。
> **唯一写法（顺序固定）**：`预设原名` → `平台替代（Windows / macOS 各写一个）` → `通用族兜底（sans-serif / serif / monospace，必须有）`。
> **三条硬规则**：① 每栈必须含通用族收尾，**禁把单一平台专有字体当唯一项**（否则 Mac/Linux 会跳到很远的 fallback，观感打架）；② 禁 CDN / 外部 webfont / 字体 base64 内联（产物零外链、包内零字体）；③ 中文一律靠系统字体（微软雅黑 / 苹方 / Noto Sans SC / 思源宋体 / 宋体 / 楷体），**不追求跨平台字形一致**——中文外观随使用者机器，这是唯一现实且零成本的选择（中文字体单文件 12-20MB，塞不进产物）。

| 预设字体（原） | 跨平台栈写法 |
|---|---|
| Archivo Black / Archivo | `"Archivo Black", "Arial Black", "Helvetica Neue", Arial, sans-serif` |
| Tektur | `"Tektur", "站酷酷黑", "Impact", "Arial Black", sans-serif` |
| Bebas Neue 感（压缩 display） | `"Bebas Neue", "Bebas", "Impact", "Arial Black", sans-serif`（⚠️ 这三族**无中文字形**：中文标题必落 sans 兜底——中文压缩感靠 `'Noto Sans SC'/思源黑体` 900 + `letter-spacing` 收紧 + `transform:scaleX(.9)` 现造，勿以为挂了栈就有中文压缩体） |
| Inter / Work Sans / DM Sans / Outfit / Nunito / Space Grotesk / Chakra Petch / IBM Plex Sans / Anthropic Sans | `"<原名>", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif` |
| JetBrains Mono / Space Mono | `"<原名>", "Consolas", "SF Mono", Menlo, monospace` |
| Cormorant / Cormorant Garamond / Source Serif 4 / Anthropic Serif | `"<原名>", "Source Han Serif SC", "Songti SC", "SimSun", serif` |
| Noto Serif SC | `"Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif` |
| Bodoni Moda | `"Bodoni Moda", "Bodoni MT", "Source Han Serif SC", serif` |
| Helvetica Neue | `"Helvetica Neue", Arial, "Segoe UI", "PingFang SC", sans-serif` |
| 楷体 KaiTi / STKaiti | `"KaiTi", "Kaiti SC", "STKaiti", "SimSun", serif` |
| Noto Sans SC / 微软雅黑 / 宋体（中文兜底） | `"Noto Sans SC", "PingFang SC", "Microsoft YaHei", "SimHei", sans-serif` |

**中文兜底三平台**：Windows `"Microsoft YaHei"` / macOS `"PingFang SC"` / 通用 `"Noto Sans SC"`；衬线中文用 `"Source Han Serif SC"`（Win/mac 通用；Linux 上同名族是 Noto Serif CJK SC，落到 `serif` 也能看）。

**给使用者的说明**：想还原某套预设的原版字形，自己在系统里装对应字体即可——Archivo Black / Tektur / Bebas Neue / Inter / Cormorant / Bodoni Moda 等均为 SIL OFL 1.1，免费商用、可自由安装；**装完本机自动命中，技能包不用改、产物不用改**。

**字号复核**：换字体后字宽会变。84px 锁档标题若已接近行宽上限，先降字或改行，别硬塞（Arial Black / Impact 的同磅宽窄与 Archivo 系列不同）。

## 装饰配方（每套一行，词条真源 [decoration-vocab.md](decoration-vocab.md)）

每套卡的**装饰配方**行给两件事：主签名词条选配（atmos 明暗渐变 / grid 技术网格 / scan 扫描线，封面浓 `.deco` / 内容页淡 `.deco.dim`）。预设只是框架起点——主题需要时基础词条覆盖不了的形态（含立式装置）可按 decoration-vocab.md「主题装置」开窗即兴发明，版面三约束与机验零松动。两铁律（**颜色一锅汤 / 装饰一套词**）、浓淡挂法、token 开口子（`--deco-tint/x/y/size/cell/line`、`--radius-card`、`--shadow-card`）全部见 decoration-vocab.md，此处不重复。结构线纪律：图表网格/轴线/层级连线等投影上必须可见的线用 `--line-struct`（≥3:1），`--hairline`（≈1.3:1）只做装饰分隔、投影会隐——生成端自绘结构图（金字塔/天平/时间轴连线）一律吃 `--line-struct`。装饰颜色只吃 `var()` 链，母色 = 本套 accent（`--deco-tint` 默认即 accent）。

---

## A1 冲击暗色

### 1. Bold Signal（醒目信号）

**气质：** 自信、大胆、高冲击力
**适用场景：** 产品发布、融资路演、重大宣布

**字体：**
- 标题：`Archivo Black` (900)（落地："Archivo Black", "Arial Black", "Helvetica Neue", Arial, sans-serif）
- 正文：`Space Grotesk` (400/500)（落地："Space Grotesk", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --bg-primary: #1a1a1a;
    --bg-gradient: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
    --card-bg: #FF5722;
    --text-primary: #ffffff;
    --text-on-card: #1a1a1a;
    --accent: #FF5722;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #1a1a1a;
    --ink: #ffffff;
    --ink-dim: color-mix(in srgb, var(--ink) 58%, var(--bg));
    --accent: #FF5722;
    --hairline: color-mix(in srgb, var(--ink) 16%, transparent);
}
```

**装饰配方：** 主签名 atmos（暖橙微光，封面浓 / 内容页 dim）——海报大色块已是主角，装饰只垫底不抢戏

**签名元素：**
- 大胆的彩色卡片作为焦点（橙/珊瑚色调）
- 大号章节编号（01, 02...）
- 导航面包屑带活跃/非活跃透明度

**组件样式：**

*按钮：*
- 主按钮：bg `#FF5722`，白字（`#ffffff`），圆角 8px，`font-weight: 700`（Archivo Black），hover 时 `filter: brightness(1.15)` + `transform: translateY(-2px)`
- 次按钮：bg transparent，`#FF5722` 文字，`2px solid #FF5722`，圆角 8px，hover 时填充 `bg rgba(255,87,34,0.1)`
- 强调按钮：bg `#1a1a1a`，`#FF5722` 文字，`1px solid #FF5722`，圆角 8px，hover 时 `border-color: #ffffff`

*卡片：*
- 普通卡片：bg `#2d2d2d`，圆角 8px，`border: none`，`box-shadow: 0 8px 32px rgba(0,0,0,0.4)`
- 高亮/焦点卡片：bg `#FF5722`（橙/珊瑚色块），文字 `#1a1a1a`，圆角 8px，`box-shadow: 0 12px 40px rgba(255,87,34,0.3)`，标题用 Archivo Black
- 数据卡片：bg `#1a1a1a`，`2px solid #FF5722` 顶部边框，圆角 8px，数据数字用 `#FF5722` + `font-size: 3rem` + Archivo Black

*标签/徽章：*
- 方角（`border-radius: 0` 或 2px），bg `#FF5722`，白字，`font-weight: 700`（Space Grotesk 500），`text-transform: uppercase`
- 章节编号标签：超小字号，`#FF5722` 文字，`letter-spacing: 2px`，如 "01 / 05"
- 暗色标签：bg `#2d2d2d`，`#FF5722` 文字，`1px solid #FF5722`

*阴影层级：*
- L1 卡片：`0 4px 16px rgba(0,0,0,0.3)` — 深色基底上的微妙浮起
- L2 重阴影：`0 8px 32px rgba(0,0,0,0.5)` — 普通卡片和交互元素
- L3 强调阴影：`0 12px 48px rgba(255,87,34,0.25), 0 4px 16px rgba(0,0,0,0.4)` — 橙色色块焦点卡片，带暖色光晕

*装饰线：*
- 分割线：`2px solid #FF5722`（粗线，自信），长度不超过容器 40%，左对齐
- 面包屑分隔：`color: rgba(255,255,255,0.3)`，活跃项 `color: #FF5722`

**设计规则：**

*推荐：*
- 橙色(#FF5722)大色块作为焦点，每页最多2处橙色高亮
- 使用超大章节编号(01, 02...)建立页面间节奏感
- 阴影带橙色光晕时才使用L3级别，日常停留在L1-L2

*避免：*
- 不要将 #FF5722 同时用于标题、背景和装饰
- 不要使用细线或轻量圆角 — border-radius 不超过 8px
- 不要添加渐变背景 — 纯色深灰才是正确基调

---

### 2. 8-Bit Orbit（像素街机）

**气质：** 复古未来、16-bit 街机、CRT 怀旧
**适用场景：** 游戏行业、增长战报、年轻化发布

**字体：**
- 标题：`Tektur`（像素网格几何 display）（落地："Tektur", "站酷酷黑", "Impact", "Arial Black", sans-serif）
- 正文：`Chakra Petch` (400/500)（落地："Chakra Petch", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 代码/数据：`Space Mono`（落地："Space Mono", "Consolas", "SF Mono", Menlo, monospace）
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --bg-void: #0A0E27;
    --bg-navy: #0F1B3D;
    --neon-cyan: #5EDCF4;
    --neon-pink: #F0A6CA;
    --neon-yellow: #F4D03F;
    --soft-lavender: #E2D5F2;
    --text-primary: #FFFFFF;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #0A0E27;
    --ink: #FFFFFF;
    --ink-dim: color-mix(in srgb, var(--ink) 58%, var(--bg));
    --accent: #5EDCF4;
    --hairline: color-mix(in srgb, var(--ink) 16%, transparent);
}
```

**装饰配方：** 主签名 scan+atmos（CRT 扫描线 + 暗角星场，封面浓 / 内容页 dim）——浓度只走 .deco 词条两档（scan 基础 10%、dim ×.55），禁另写 opacity（旧超低透明度写法 2026-10-24 废止：叠上新基数≈0.5% 有效覆盖，深底隐身）

**签名元素：**
- 4px 像素单位（一切尺寸对齐 4 的倍数）
- CRT 扫描线覆盖 + 轻暗角 + 星场点缀
- 硬偏移阴影（4px 递增堆叠，禁软阴影/禁 glow）
- 像素点阵装饰条

**组件样式：**

*按钮：*
- 主按钮：bg `#5EDCF4`，文字 `#0A0E27`，圆角 0，`box-shadow: 4px 4px 0 #0F1B3D`，hover 位移 `-2px,-2px` + 阴影 `6px 6px 0`
- 强调按钮：bg `#F4D03F`，文字 `#0A0E27`，同硬阴影规格

*卡片：*
- 普通卡片：bg `#0F1B3D`，圆角 0，`border: 1px solid rgba(94,220,244,.3)`，硬偏移阴影 `4px 4px 0 rgba(94,220,244,.15)`
- 数据卡片：像素边框（`outline: 1px dashed` + 实线双层），数字用 Space Mono 700 + neon-cyan

*标签/徽章：*
- 方角，bg `rgba(94,220,244,.12)`，文字 `#5EDCF4`，`letter-spacing: 2px`
- 分数/进度条：8 段像素块（实心/空心交替）

**设计规则：**

*推荐：*
- 三霓虹分工：青=信息/数据、粉=提示/叙事、黄=得分/强调
- 扫描线浓度只走 .deco 两档（scan 10% / dim ×.55），暗角随 atmos 词条不吃额外 opacity（氛围不抢戏）

*避免：*
- 不要用软阴影、发光、渐变——本预设的"亮"靠色相不靠光效
- 不要打破 4px 网格（半像素感即穿帮）

---

### 3. Broadside（墨底大报）

**气质：** 报纸头版、火橙引题、编辑权威
**适用场景：** 行业洞察、年度复盘、深度报道式演讲

**字体：**
- 标题：压缩 display（Bebas Neue 感，中文用 `'Noto Sans SC'` 900 + 压缩字距）（落地："Bebas Neue", "Bebas", "Impact", "Arial Black", sans-serif）
- 正文：`'Noto Serif SC', 'Source Han Serif SC', serif`（报纸衬线）（落地："Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif）
- 中文回退：`'Noto Serif SC', 'Source Han Serif SC', serif`

**配色：**
```css
:root {
    --bg-ink: #111111;
    --bg-ink-alt: #1A1A18;
    --fire-orange: #E85D26;
    --text-primary: #F0ECE5;
    --text-secondary: #888880;
    --text-hint: #505048;
    --border-dark: #282826;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #111111;
    --ink: #F0ECE5;
    --ink-dim: #888880;
    --accent: #E85D26;
    --hairline: #282826;
}
```

**装饰配方：** 主签名 grid（hairline 报格网，封面浓 / 内容页 dim）——网格密度对齐报纸格律，母色走墨系不走橙

**签名元素：**
- 火橙引题（kicker/引语专用，非装饰）
- 报纸双栏衬线正文
- 细墨分隔线（hairline 报格）
- 头版式层级：引题 → 大标题 → 副题 → 双栏

**组件样式：**

*按钮：*
- 主按钮：bg `#E85D26`，文字 `#111111`，圆角 0，`font-weight: 900`
- 次按钮：transparent，`1px solid #F0ECE5`，白字，圆角 0

*卡片：*
- 引语卡：bg `#1A1A18`，`border-left: 3px solid #E85D26`，衬线斜体
- 数据卡：墨底 + 火橙大数字（衬线 oldstyle 数字）

*标签/徽章：*
- 版面标签：`#888880` 小字大写 + 字距 3px（报眉感）
- 火橙标签：文字 `#E85D26`，无底（专色墨逻辑）

**设计规则：**

*推荐：*
- 火橙只给引题与关键数据（专色墨，一页 ≤2 处）
- 分隔线用 `#282826`，密度对齐报纸格律

*避免：*
- 不要圆角、不要阴影——铅字盘没有这些
- 不要让橙做大面积底（那是 Bold Signal 的活法，本报只做专色）

---

### 4. Sentry（深紫工程）

**气质：** 深紫画布、青柠撞色、可观测工程
**适用场景：** 技术复盘、监控报告、SaaS 产品

**字体：**
- 标题：`Inter` (600)（落地："Inter", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 正文：`Inter` (400)（落地同上）
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --bg-primary: #1f1633;
    --bg-deep: #150f23;
    --border-purple: #362d59;
    --accent-purple: #6a5fc1;
    --violet-deep: #422082;
    --lime: #c2ef4e;
    --coral: #ffb287;
    --pink: #fa7faa;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #1f1633;
    --ink: #ffffff;
    --ink-dim: color-mix(in srgb, var(--ink) 58%, var(--bg));
    --accent: #c2ef4e;
    --hairline: #362d59;
    --warn: #ffb287;   /* 珊瑚=警告状态点，只落内容 */
}
```

**装饰配方：** 主签名 atmos+grid（深空渐变 + 测距网，封面浓 / 内容页 dim）——可观测工程的"仪器感"由网格承担

**签名元素：**
- 三层紫阶梯底（#1f1633 / #150f23 / #422082）
- 青柠 accent（撞色点睛，不铺量）
- 珊瑚/粉仅状态点缀
- 半透明紫边框卡

**组件样式：**

*按钮：*
- 主按钮：bg `#c2ef4e`，文字 `#1f1633`，圆角 6px，`font-weight: 600`
- 次按钮：bg `#6a5fc1`，白字，圆角 6px

*卡片：*
- 普通卡片：bg `#150f23`，圆角 8px，`border: 1px solid #362d59`
- 高亮卡片：bg `#422082`，`border: 1px solid rgba(106,95,193,.5)`，数据数字青柠

*标签/徽章：*
- 圆角 999px，bg `rgba(194,239,78,.12)`，文字 `#c2ef4e`
- 状态点：珊瑚 #ffb287（警告）/ 粉 #fa7faa（装饰）

**设计规则：**

*推荐：*
- 青柠=行动/正向，紫系=结构与层级——撞色只在青柠上
- 底层三紫用透明度或明度区分，不引入新色相

*避免：*
- 不要让青柠和珊瑚粉同页等量（青柠主导）
- 不要纯黑底——紫才有"深空感"

---

### 5. Kraken（近黑紫）

**气质：** 加密交易、专业深沉、紫即交互
**适用场景：** 金融科技、量化报告、交易平台

**字体：**
- 标题：`Inter` (600/700)（落地："Inter", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 正文：`Inter` (400)（落地同上）
- 数字：tabular-nums
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --bg-primary: #101114;
    --kraken-purple: #7132f5;
    --purple-dark: #5741d8;
    --purple-deep: #5b1ecf;
    --text-secondary: #686b82;
    --text-primary: #ffffff;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #101114;
    --ink: #ffffff;
    --ink-dim: #686b82;
    --accent: #7132f5;
    --hairline: color-mix(in srgb, var(--ink) 16%, transparent);
}
```

**装饰配方：** 主签名 atmos（紫调微光，封面浓 / 内容页 dim）

**签名元素：**
- 近黑底 + 克紫单 accent
- 紫渐变（仅 CTA 与焦点卡：#5741d8→#5b1ecf）
- 数字金融感：tabular-nums + 等宽排版

**组件样式：**

*按钮：*
- 主按钮：bg `#7132f5`，白字，圆角 8px，hover `#5741d8`
- 渐变按钮：`linear-gradient(135deg, #5741d8, #5b1ecf)`，白字，圆角 8px

*卡片：*
- 普通卡片：bg `#16171c`，圆角 10px，`border: 1px solid #26272e`
- 高亮卡片：`border: 1px solid rgba(113,50,245,.4)` + 紫光晕 `0 0 24px rgba(113,50,245,.15)`

*标签/徽章：*
- 圆角 6px，bg `rgba(113,50,245,.14)`，文字 `#9d7dfa`

**设计规则：**

*推荐：*
- 紫=交互/行动语义，白=数据，灰蓝=说明
- 涨跌语义色可引入（绿/红），但不与紫竞争面积

*避免：*
- 不要紫大面积铺底（紫是交互色不是装饰色）
- 不要超过一个渐变元素/页

---

## A2 沉静暗色

### 6. Dark Botanical（暗夜植物）

**气质：** 优雅、精致、高级感
**适用场景：** 奢侈品、文化艺术、高端品牌

**字体：**
- 标题：`Cormorant` (400/600) — 优雅衬线（落地："Cormorant", "Source Han Serif SC", "Songti SC", "SimSun", serif）
- 正文：`IBM Plex Sans` (300/400)（落地："IBM Plex Sans", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 中文回退：`'Noto Serif SC', 'Source Han Serif SC', serif`

**配色：**
```css
:root {
    --bg-primary: #0f0f0f;
    --text-primary: #e8e4df;
    --text-secondary: #9a9590;
    --accent-warm: #d4a574;
    --accent-pink: #e8b4b8;
    --accent-gold: #c9b896;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #0f0f0f;
    --ink: #e8e4df;
    --ink-dim: #9a9590;
    --accent: #d4a574;
    --hairline: color-mix(in srgb, var(--ink) 16%, transparent);
}
```

**装饰配方：** 主签名 atmos（金粉光斑团，封面浓 / 内容页 dim）——原版"模糊重叠渐变圆"即 atmos 原型；金色主导粉色点缀，光斑只垫底

**签名元素：**
- 抽象柔和渐变圆（模糊、重叠）
- 暖色调点缀（粉、金、赭）
- 细竖线装饰
- 斜体签名排版

**组件样式：**

*按钮：*
- 主按钮：bg `rgba(212,165,116,0.12)`，文字 `#d4a574`，圆角 16px，`1px solid rgba(212,165,116,0.25)`，hover 时 `box-shadow: 0 0 20px rgba(212,165,116,0.15)`
- 强调按钮：bg `#d4a574`，文字 `#0f0f0f`，圆角 16px，hover 时 `filter: brightness(1.1)`
- 幽灵按钮：bg transparent，文字 `#e8b4b8`，`1px solid rgba(232,180,184,0.2)`，圆角 16px

*卡片：*
- 普通卡片：bg `rgba(255,255,255,0.03)`，圆角 12px，`border: 1px solid rgba(212,165,116,0.08)`，`box-shadow: 0 8px 32px rgba(212,165,116,0.06)`
- 高亮卡片：bg `rgba(212,165,116,0.06)`，`border: 1px solid rgba(212,165,116,0.2)`，`box-shadow: 0 0 24px rgba(212,165,116,0.1)` 暖金辉光
- 数据卡片：bg `rgba(232,180,184,0.05)`，`border: 1px solid rgba(232,180,184,0.15)`，数据数字用 `#d4a574` 大字号

*标签/徽章：*
- 圆角 12px（柔和），bg `rgba(212,165,116,0.1)`，文字 `#d4a574`，字体 IBM Plex Sans 500
- 粉色标签：bg `rgba(232,180,184,0.1)`，文字 `#e8b4b8`
- 章节标签：左侧 `border-left: 2px solid #c9b896` 细竖线装饰，文字用斜体

*阴影层级：*
- L1 卡片：`0 6px 24px rgba(0,0,0,0.3)` — 暗底上的柔和浮起
- L2 暖辉光：`0 0 20px rgba(212,165,116,0.1)` — 暖金光晕，hover 元素
- L3 双暖辉光：`0 0 30px rgba(212,165,116,0.15), 0 0 60px rgba(232,180,184,0.08)` — 金粉双色辉光，封面焦点

*装饰线：*
- 分割线：`1px solid rgba(212,165,116,0.12)`，两端渐隐
- 竖线装饰：`width: 1px; background: linear-gradient(180deg, #d4a574, transparent)` 用于章节分隔

**设计规则：**

*推荐：*
- 暖金(#d4a574)是视觉锚点，用于标题、数据和关键交互元素
- 装饰线使用渐隐效果(两端渐隐)，营造优雅感
- 圆角保持 12-16px 的柔和范围，与衬线字体气质一致

*避免：*
- 不要使用纯白(#ffffff)文字 — 使用 #e8e4df 暖白
- 不要让粉色和金色同等权重 — 金色主导，粉色点缀
- 不要使用粗线或直角 — 本主题追求柔软精致

---

### 7. Terminal Green（终端绿）

**气质：** 极客、黑客美学、开发者专属
**适用场景：** 技术分享、开发者大会、代码演示

**字体：**
- 全局：`JetBrains Mono` (400/700) — 纯等宽（落地："JetBrains Mono", "Consolas", "SF Mono", Menlo, monospace）
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --bg-primary: #0d1117;
    --accent-green: #39d353;
    --text-primary: #c9d1d9;
    --text-secondary: #8b949e;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #0d1117;
    --ink: #c9d1d9;
    --ink-dim: #8b949e;
    --accent: #39d353;
    --hairline: color-mix(in srgb, var(--ink) 16%, transparent);
}
```

**装饰配方：** 主签名 scan（CRT 全屏扫描纹，封面浓 / 内容页 dim）——扫描线是终端的灵魂签名，浓度只走 .deco 词条两档（scan 基础 10%、dim ×.55），禁另写 opacity（旧超低透明度写法 2026-10-24 废止：叠上新基数≈0.3% 有效覆盖，深底隐身）

**签名元素：**
- 扫描线效果
- 闪烁光标
- 代码语法高亮风格
- 命令行提示符装饰

**组件样式：**

*按钮：*
- 主按钮：bg `rgba(57,211,83,0.12)`，文字 `#39d353`，圆角 2px（直角终端感），`border: 1px solid rgba(57,211,83,0.3)`，前缀 `▶` 装饰，hover 时 `box-shadow: 0 0 12px rgba(57,211,83,0.3)`
- 执行按钮：bg `#39d353`，文字 `#0d1117`，圆角 2px，`font-family: JetBrains Mono`，hover 时 `filter: brightness(1.1)` + 绿色发光
- 幽灵按钮：bg transparent，文字 `#8b949e`，`1px solid #30363d`，圆角 2px，hover 时文字变 `#39d353`

*卡片：*
- 普通卡片：bg `#161b22`，圆角 4px，`border: 1px solid #30363d`，顶栏 `padding: 8px 12px; border-bottom: 1px solid #30363d; background: #0d1117`（终端窗口头，可放3个圆点 `● ● ●`）
- 高亮卡片：bg `#161b22`，`border: 1px solid rgba(57,211,83,0.3)`，`box-shadow: 0 0 16px rgba(57,211,83,0.08)` 绿色微辉光，行号 `border-right: 1px solid #30363d; padding-right: 12px; color: #484f58`
- 数据卡片：bg `#0d1117`，`border: 1px solid #30363d`，数据数字用 `#39d353` + JetBrains Mono 700，前缀 `$` 命令行提示符

*标签/徽章：*
- 直角（border-radius: 0 或 2px），bg `rgba(57,211,83,0.12)`，文字 `#39d353`，`font-family: JetBrains Mono`
- 注释标签：文字 `#8b949e`，前缀 `// `（注释风格）
- 语法标签：模拟语法高亮 — 关键字 `#ff7b72`（红），字符串 `#a5d6ff`（蓝），数字 `#79c0ff`
- commit 标签：bg `rgba(57,211,83,0.15)`，文字 `#39d353`，前缀 `●`（类似 git status）

*阴影层级：*
- L1 终端：`0 2px 8px rgba(0,0,0,0.5)` — 深色内凹感
- L2 绿辉：`0 0 16px rgba(57,211,83,0.1)` — 绿色微光
- L3 扫描辉光：`0 0 24px rgba(57,211,83,0.15), 0 0 48px rgba(57,211,83,0.05)` — CRT 显示器辉光效果

*装饰线：*
- 分割线：`1px solid #30363d`，可加注释 `// ────────────`
- 扫描线：`background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px)` 覆盖全屏
- 光标：`border-right: 2px solid #39d353; animation: blink 1s step-end infinite` 闪烁光标效果

**设计规则：**

*推荐：*
- 绿色(#39d353)用于成功/执行/核心数据，灰色(#8b949e)用于辅助信息
- 终端窗口头(三圆点+暗栏)是每张卡片的标配
- 命令行提示符($)和注释前缀(//)是签名装饰元素

*避免：*
- 不要引入彩色高亮 — 本主题严格限制在绿/灰/暗色范围（语法高亮三色仅限代码块内）
- 不要使用 sans-serif 或 serif 字体 — 必须等宽
- 不要让背景亮于 #161b22 — 深色是终端的基础

---

### 8. Linear Dark（Linear 深色）

**气质：** 暗色优先、精密工程、开发者工具美学
**适用场景：** 开发者工具、技术产品、项目管理

**字体：**
- 标题：`Inter` (510 — 介于常规和中等之间) — `font-variation-settings: "wght" 510`（落地："Inter", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 正文：`Inter` (400)（落地同上）
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --bg-marketing: #08090a;
    --bg-panel: #0f1011;
    --bg-surface: #191a1b;
    --text-primary: #f7f8f8;
    --text-secondary: #d0d6e0;
    --text-muted: #8a8f98;
    --accent-indigo: #5e6ad2;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #08090a;
    --ink: #f7f8f8;
    --ink-dim: #8a8f98;
    --accent: #5e6ad2;
    --hairline: color-mix(in srgb, var(--ink) 16%, transparent);
}
```

**装饰配方：** 主签名 atmos（亮度阶梯微光，**全片 dim、封面略浓**）——Linear 的克制是身份，装饰浓度全库最低档

**签名元素：**
- 暗色原生画布 — 从 #08090a 到 #191a1b 的亮度阶梯
- weight 510 — "介于常规和中等之间"的独有字重
- 半透明白色边框 rgba(255,255,255,0.05-0.08)
- Indigo(#5e6ad2)是唯一的彩色

**组件样式：**

*按钮：*
- 主按钮：bg `#5e6ad2`，白字，圆角 6px，hover 时 bg `#828fff`
- 幽灵按钮：bg `rgba(255,255,255,0.02)`，文字 `#e2e4e7`，`1px solid rgb(36,40,44)`，圆角 6px
- 药丸按钮：bg transparent，文字 `#d0d6e0`，圆角 9999px，`1px solid rgb(35,37,42)`

*卡片：*
- 普通卡片：bg `rgba(255,255,255,0.02)`，圆角 8px，`border: 1px solid rgba(255,255,255,0.08)`
- 高亮卡片：bg `rgba(255,255,255,0.05)`，`border: 1px solid rgba(255,255,255,0.08)`，圆角 12px
- 数据卡片：bg `#191a1b`，数据数字用 `#f7f8f8` + Inter 510 + `font-size: 3rem`

*标签/徽章：*
- 药丸标签：bg transparent，文字 `#d0d6e0`，圆角 9999px，`1px solid rgb(35,37,42)`，Inter 510
- 成功标签：bg `#10b981`，文字 `#f7f8f8`，圆角 50%
- 微标签：bg `rgba(255,255,255,0.05)`，文字 `#f7f8f8`，圆角 2px，`border: 1px solid rgba(255,255,255,0.05)`

*阴影层级：*
- L1 微浮：`rgba(0,0,0,0.03) 0px 1.2px 0px`
- L2 表面：bg 透明度递增(0.02→0.04→0.05) + 半透明边框
- L3 悬浮：`rgba(0,0,0,0.4) 0px 2px 4px`

*装饰线：*
- 分割线：`1px solid rgba(255,255,255,0.05)` — 呢喃级分割
- 边框：`1px solid rgba(255,255,255,0.08)` — 标准级

**设计规则：**

*推荐：*
- weight 510 是核心辨识度 — 它创造了"轻微强调但不喊叫"的独特感觉
- 暗色表面通过 rgba(255,255,255, 0.02→0.04→0.05) 递增来表示层级
- 主文字使用 #f7f8f8 而非纯白 #ffffff — 防止暗底上的视觉刺眼

*避免：*
- 不要使用纯白(#ffffff)作为主文字色 — #f7f8f8 更舒适
- 不要使用不透明背景色做按钮 — 透明度系统是核心
- 不要使用超过 590 的字重 — Linear 的极限是 590

---

### 9. MongoDB（森林黑电绿）

**气质：** 数据森林、蓝黑底电绿、工程生命感
**适用场景：** 数据库/基础设施、数据年报、技术白皮书

**字体：**
- 标题：`Inter` / `Work Sans` (600/700)（落地："Work Sans", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 正文：`Inter` (400)（落地："Inter", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 代码：`JetBrains Mono`（落地："JetBrains Mono", "Consolas", "SF Mono", Menlo, monospace）
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --forest-black: #001e2b;
    --mongo-green: #00ed64;
    --green-deep: #00684a;
    --action-blue: #006cfa;
    --blue-hover: #3860be;
    --text-primary: #ffffff;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #001e2b;
    --ink: #ffffff;
    --ink-dim: color-mix(in srgb, var(--ink) 58%, var(--bg));
    --accent: #00ed64;
    --hairline: color-mix(in srgb, var(--ink) 16%, transparent);
}
```

**装饰配方：** 主签名 atmos+grid（顶部青渐变 + 设施网，封面浓 / 内容页 dim）

**签名元素：**
- 森林黑蓝底（非纯黑，带青调深度）
- 电绿=数据生命力（CTA/关键数）
- 行动蓝=链接/次交互
- 顶部深青渐变（#002838→#001e2b）

**组件样式：**

*按钮：*
- 主按钮：bg `#00ed64`，文字 `#001e2b`，圆角 4px，`font-weight: 700`
- 次按钮：transparent，`1px solid rgba(0,237,100,.4)`，文字 `#00ed64`

*卡片：*
- 普通卡片：bg `#00293a`，圆角 6px，`border: 1px solid rgba(0,237,100,.12)`
- 数据卡片：数字电绿 + JetBrains Mono，标签白

*标签/徽章：*
- 方角，bg `rgba(0,237,100,.1)`，文字 `#00ed64`
- 命令行提示：`$` 前缀 + 等宽绿字

**设计规则：**

*推荐：*
- 绿=正向/数据、蓝=行动——双色分工严格
- 大数字用绿 + mono，中文说明用白

*避免：*
- 不要绿蓝同元素混用
- 不要让底亮于 #00394a（深是森林的基础）

---

### 10. Deep Teal Review（冰青复盘）

**气质：** 冰青数据、蓝黑沉静、复盘叙事
**适用场景：** 年度复盘、市场分析、经营报告（自家新能源 deck 实证色系）

**字体：**
- 数字：`Archivo`, `'Helvetica Neue'`, sans-serif（落地："Archivo", "Arial Black", "Helvetica Neue", Arial, sans-serif）
- 中文：`'Noto Sans SC', sans-serif`（落地："Noto Sans SC", "PingFang SC", "Microsoft YaHei", "SimHei", sans-serif）

**配色：**
```css
:root {
    --stage-bg: #05080B;
    --slide-bg: #0B0F14;
    --ink: #E8F1F5;
    --mid: #93A4B0;
    --dim: #5C6B78;
    --cy: #2BE0C8;   /* 青绿=数据/正向 */
    --am: #FFB020;   /* 琥珀=强调/中间档 */
    --co: #FF5A5F;   /* 珊瑚=负向/警示 */
    --line: #232F3A;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #0B0F14;
    --ink-dim: #93A4B0;
    --accent: #2BE0C8;
    --hairline: #232F3A;
    --warn: #FF5A5F;   /* 珊瑚=负向警示；琥珀 #FFB020=强调档，两者都只落数字/文字不进装饰 */
}
```

**装饰配方：** 主签名 atmos+grid（冰青仪表光 + 精密网格，封面浓 / 内容页 dim）——NEV 青族复盘即从本套派生（见 .claude-design/custom-presets.md）

**签名元素：**
- 全站一个色温：底/字/线全蓝灰族，零跳色温
- 三功能色纪律：青绿=数据正向、琥珀=强调、珊瑚=负向
- 双层底（stage #05080B 托 slide #0B0F14）
- 文字三级冰白阶梯（#E8F1F5/#93A4B0/#5C6B78）

**组件样式：**

*按钮：*
- 主按钮：bg `#2BE0C8`，文字 `#0B0F14`，圆角 6px
- 线框按钮：`1px solid #232F3A`，文字 `#93A4B0`

*卡片：*
- 普通卡片：bg `#0E141B`，圆角 8px，`border: 1px solid #232F3A`
- 数据卡片：大数字青绿 + Archivo，增幅琥珀、降幅珊瑚

*标签/徽章：*
- bg `rgba(43,224,200,.1)`，文字 `#2BE0C8`，圆角 4px
- 负向标签：bg `rgba(255,90,95,.1)`，文字 `#FF5A5F`

**设计规则：**

*推荐：*
- 分隔线永远 #232F3A（同色温纪律的守门员）
- 三功能色不得互换语义（珊瑚不做强调、琥珀不做负向）

*避免：*
- 不要引入第四功能色
- 不要纯黑或纯白（破坏冰蓝灰色温）

---

## B1 纸感编辑

### 11. Paper & Ink（纸与墨）

**气质：** 编辑风格、文学感、深思熟虑
**适用场景：** 年度总结、深度报告、品牌故事

**字体：**
- 标题：`Cormorant Garamond` + `Source Serif 4`（落地："Cormorant Garamond", "Source Han Serif SC", "Songti SC", "SimSun", serif）
- 正文：`Source Serif 4` (400)（落地："Source Serif 4", "Source Han Serif SC", "Songti SC", "SimSun", serif）
- 中文回退：`'Noto Serif SC', 'Source Han Serif SC', serif`

**配色：**
```css
:root {
    --bg-cream: #faf9f7;
    --text-primary: #1a1a1a;
    --text-secondary: #555555;
    --accent-crimson: #c41e3a;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #faf9f7;
    --ink: #1a1a1a;
    --ink-dim: #555555;
    --accent: #c41e3a;
    --hairline: color-mix(in srgb, var(--ink) 16%, transparent);
}
```

**装饰配方：** 主签名 atmos（纸面明暗，**全片 dim**）——纸感以留白为主，装饰是"纸在灯下"的极淡明暗，不是图形

**签名元素：**
- 首字下沉（Drop Caps）
- 引用块（Pull Quotes）
- 优雅水平分割线
- 深红强调色

**组件样式：**

*按钮：*
- 主按钮：bg `#1a1a1a`（墨色），文字 `#faf9f7`（纸色），圆角 4px，hover 时 `border-bottom: 2px solid #c41e3a`（深红下划线，像笔划标注）
- 强调按钮：bg `#c41e3a`（深红），文字 `#faf9f7`，圆角 4px，hover 时 `filter: brightness(1.1)`
- 幽灵按钮：bg transparent，文字 `#1a1a1a`，`1px solid #555555`，圆角 4px，hover 时文字变 `#c41e3a`

*卡片：*
- 普通卡片：bg `#faf9f7`，圆角 0，`box-shadow: inset 0 0 0 1px #ddd`（内凹阴影，像纸张压痕），`border: none`
- 引用卡片：bg `#faf9f7`，左侧 `border-left: 3px solid #c41e3a`，首字母 `float: left; font-size: 3em; line-height: 0.8; color: #c41e3a`（首字下沉效果）
- 数据卡片：bg `#ffffff`，`border: 1px solid #e8e6dc`，数据数字用 Cormorant Garamond 600 + `#c41e3a`

*标签/徽章：*
- 圆角 0（方正，文学感），bg `rgba(196,30,58,0.08)`，文字 `#c41e3a`，字体 Source Serif 4 italic
- 注释标签：bg `#f0eee6`（旧纸色），文字 `#555555`，左侧有 `em-dash` 装饰 `—`
- 章节标记：纯文字 `font-variant: small-caps`，`letter-spacing: 2px`，`color: #c41e3a`

*阴影层级：*
- L1 纸压：`inset 0 0 0 1px #ddd` — 内凹，像纸上的压痕
- L2 页浮：`0 2px 12px rgba(0,0,0,0.06)` — 轻微浮起
- L3 深红投影：`0 4px 16px rgba(196,30,58,0.08)` — 淡红色调阴影

*装饰线：*
- 分割线：`1px solid #c41e3a`，宽度 40px（短而精），居中，两端可加小菱形装饰 `◆`
- 引用分割：`3px solid #c41e3a`，左侧定位

**设计规则：**

*推荐：*
- 深红(#c41e3a)是唯一的视觉焦点，用于首字下沉和关键标注
- 内凹阴影(inset shadow)模拟纸张压痕，是本主题独有的深度语言
- 分割线短而精(40px)，居中，可加菱形装饰

*避免：*
- 不要使用 sans-serif 字体 — 必须保持衬线字体的文学气质
- 不要使用圆角 — 纸与墨是方正的，border-radius: 0
- 不要让深红大面积出现 — 它是笔划标注，不是背景色

---

### 12. Notebook Tabs（笔记本标签）

**气质：** 编辑风格、有条理、优雅触感
**适用场景：** 教学课件、研究报告、知识分享

**字体：**
- 标题：`Bodoni Moda` (400/700) — 经典编辑（落地："Bodoni Moda", "Bodoni MT", "Source Han Serif SC", serif）
- 正文：`DM Sans` (400/500)（落地："DM Sans", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 中文回退：`'Noto Serif SC', 'Source Han Serif SC', serif`

**配色：**
```css
:root {
    --bg-outer: #2d2d2d;
    --bg-page: #f8f6f1;
    --text-primary: #1a1a1a;
    --tab-1: #98d4bb;
    --tab-2: #c7b8ea;
    --tab-3: #f4b8c5;
    --tab-4: #a8d8ea;
    --tab-5: #ffe6a7;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #f8f6f1;
    --ink: #1a1a1a;
    --ink-dim: color-mix(in srgb, var(--ink) 58%, var(--bg));
    --accent: #98d4bb;
    --hairline: color-mix(in srgb, var(--ink) 16%, transparent);
}
```

**装饰配方：** 主签名 atmos（纸面微光，**全片 dim**）——五色标签是内容层导航（每章一色固定），不算装饰层；装饰只做纸感底光

**签名元素：**
- 纸张容器 + 柔和阴影
- 右侧彩色章节标签（竖排文字）
- 左侧装订孔装饰
- 标签字号随视口缩放

**组件样式：**

*按钮：*
- 主按钮：bg `#f8f6f1`（纸张色），文字 `#1a1a1a`，圆角 0，`1px solid #d4d0c8`，`box-shadow: 2px 2px 0 #d4d0c8`（纸张层叠感），hover 时阴影位移 `4px 4px`
- 彩色按钮：bg `#98d4bb`（标签色），文字 `#1a1a1a`，圆角 0，hover 时切换为 `#c7b8ea`
- 线框按钮：bg transparent，文字 `#1a1a1a`，`1px dashed #9a9590`（虚线，像手写笔记边框）

*卡片：*
- 普通卡片：bg `#f8f6f1`，圆角 0，`box-shadow: 3px 3px 0 #d4d0c8`（纸张叠放效果），`border-left: 3px double #9a9590`（双线装饰像笔记本边距）
- 高亮卡片：bg `#98d4bb`（薄荷标签色），文字 `#1a1a1a`，圆角 0，`box-shadow: 4px 4px 0 rgba(0,0,0,0.1)`
- 数据卡片：bg `#f8f6f1`，右上角折角效果 `box-shadow`，数据数字用 Bodoni Moda 700

*标签/徽章：*
- 竖排标签：宽 24px，bg `#98d4bb` / `#c7b8ea` / `#f4b8c5` / `#a8d8ea` / `#ffe6a7`（5色轮替），竖排文字 `writing-mode: vertical-rl`，圆角 0
- 行内标签：bg `#ffe6a7`（便签黄），文字 `#1a1a1a`，圆角 0，`font-style: italic`
- 装订孔：`width: 8px; height: 8px; border-radius: 50%; border: 1px solid #9a9590` 等距排列在左侧

*阴影层级：*
- L1 纸张：`2px 2px 0 #d4d0c8` — 纸张叠加，硬边
- L2 折页：`4px 4px 0 #d4d0c8` — 更厚的层叠
- L3 浮页：`6px 6px 12px rgba(0,0,0,0.08)` — 多页堆叠的自然阴影

*装饰线：*
- 分割线：`1px solid #d4d0c8`，左侧带装订孔对齐标记
- 页面边缘：`border-right: 1px dashed #d4d0c8`（模拟笔记本右边距线）

**设计规则：**

*推荐：*
- 纸张色(#f8f6f1)作为内容底色，深灰(#2d2d2d)作为外围
- 彩色标签(5色轮替)与章节一一对应，建立视觉导航
- 装订孔和虚线是"手写笔记"感觉的关键，不可省略

*避免：*
- 不要使用渐变或发光 — 本主题追求纸张质感
- 不要让标签颜色混用 — 每个章节固定一种颜色
- 不要使用 sans-serif 圆角按钮 — 保持编辑/文学气质

---

### 13. Ink Garden（水墨雅集）

**气质：** 古典雅致、温润书卷、诗意留白
**适用场景：** 文化报告、政府汇报、教育演讲、传统产业展示、茶道/书法/国画主题

**字体：**
- 标题：`Noto Serif SC` (600/700) — 宋体衬线，古典庄重（落地："Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif）
- 正文：`Noto Sans SC` (400/500) — 清晰无衬线，阅读舒适（落地："Noto Sans SC", "PingFang SC", "Microsoft YaHei", "SimHei", sans-serif）
- 英文回退：`'Cormorant Garamond', serif`（落地："Cormorant Garamond", "Source Han Serif SC", "Songti SC", "SimSun", serif）

**配色：**
```css
:root {
    --bg-primary: #f5f0e8;            /* 宣纸米白 */
    --bg-gradient: linear-gradient(135deg, #f5f0e8 0%, #ede7d9 50%, #f0eadb 100%);
    --bg-dark: #2c2420;               /* 深褐墨色（深色页） */
    --bg-card: #faf7f2;               /* 浅宣纸（卡片底） */
    --text-heading: #2a1f18;          /* 浓墨标题 */
    --text-body: #5c4d3c;             /* 淡墨正文 */
    --accent: #c8963e;                /* 赤金（主强调） */
    --accent-light: rgba(200,150,62,0.10);
    --accent-secondary: #a06426;      /* 古铜（辅强调） */
    --border: #d8cdb8;                /* 宣纸灰边 */
    --ink-wash: rgba(42,31,24,0.06);  /* 水墨晕染色 */
    --seal-red: #c23a2b;              /* 印章朱砂红 */

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #f5f0e8;
    --ink: #2a1f18;
    --ink-dim: #5c4d3c;
    --accent: #c8963e;
    --hairline: #d8cdb8;
}
```

**装饰配方：** 主签名 atmos（**墨晕扩散**，封面浓 / 内容页 dim）——原版"radial-gradient 模拟墨迹扩散"即 atmos 的墨晕变体，角落低不透明度晕染；朱砂仅印章不算装饰

**签名元素：**
- 水墨晕染背景纹理（CSS radial-gradient 模拟墨迹扩散）
- 银杏叶 SVG 装饰（金色描边，`opacity: 0.15`）
- 印章风格圆形编号（朱砂红圆 + 白色篆字壹贰叁）
- 竖排标题变体（`writing-mode: vertical-rl`，仅封面可选）
- 古典花边框（双线 border + 角花纹 SVG）

**组件样式：**

*按钮：*
- 主按钮：bg `#c8963e`，白字 `#ffffff`，圆角 4px，`font-weight: 600`（Noto Serif SC），hover 时 `filter: brightness(1.1)` + `transform: translateY(-2px)`
- 次按钮：bg `transparent`，`#c8963e` 文字，`1px solid #c8963e`，圆角 4px，hover 时 `bg rgba(200,150,62,0.08)`
- 印章按钮：bg `#c23a2b`（朱砂红），白字，圆角 50%（圆形），`min-width: 44px`，`min-height: 44px`，`font-family: serif`，hover 时 `box-shadow: 0 0 12px rgba(194,58,43,0.4)`

*卡片：*
- 普通卡片：bg `#faf7f2`，圆角 4px，`border: 1px solid #d8cdb8`，`box-shadow: 0 2px 8px rgba(42,31,24,0.06)`
- 高亮/焦点卡片：bg `linear-gradient(135deg, rgba(200,150,62,0.08), rgba(200,150,62,0.03))`，`border: 1px solid rgba(200,150,62,0.25)`，左侧 `3px solid #c8963e`，标题用 Noto Serif SC 700
- 数据卡片：bg `#faf7f2`，`border-top: 2px solid #c8963e`，数据数字用 `#2a1f18` + `font-size: 2.5rem` + Noto Serif SC 600 + `letter-spacing: -0.5px`

*标签/徽章：*
- 方角标签（`border-radius: 2px`），bg `rgba(200,150,62,0.10)`，`#a06426` 文字，`font-weight: 500`（Noto Sans SC），`letter-spacing: 1px`
- 印章编号标签：bg `#c23a2b` 圆形（32px），白字篆体，`font-family: serif`，对应壹/贰/叁/肆/伍
- 暗色标签：bg `rgba(42,31,24,0.06)`，`#5c4d3c` 文字，`border: 1px solid #d8cdb8`

*阴影层级：*
- L1 浮墨：`0 2px 8px rgba(42,31,24,0.06)` — 宣纸上的微妙浮起
- L2 重墨：`0 4px 20px rgba(42,31,24,0.10)` — 普通卡片和交互元素
- L3 金晕：`0 8px 32px rgba(200,150,62,0.15), 0 2px 8px rgba(42,31,24,0.08)` — 赤金焦点卡片，带暖色光晕

*装饰线：*
- 分割线：`2px solid #c8963e`（赤金线），长度不超过容器 30%，左对齐
- 双线边框：外层 `1px solid #d8cdb8` + 内层 `1px solid #d8cdb8`（间距 4px），用于内容框
- 水墨晕染：`radial-gradient(ellipse at 80% 20%, rgba(42,31,24,0.04), transparent 60%)` — 角落装饰

**设计规则：**

*推荐：*
- 赤金(#c8963e)作为唯一强调色，每页最多2处金色高亮
- 大面积留白 — "计白当黑"，内容区不超过页面60%
- 使用水墨晕染效果（低不透明度 radial-gradient）营造纸面质感
- 封面可用竖排标题（`writing-mode: vertical-rl`）增加古典仪式感
- 数据页用印章编号替代阿拉伯数字，增强风格一致性

*避免：*
- 不要使用饱和度高的颜色 — 所有颜色必须带暖灰/棕底
- 不要使用纯白(#fff)背景 — 用宣纸米白(#f5f0e8)代替
- 不要使用现代几何装饰（圆点、三角、渐变色块）— 只用水墨、银杏、印章等传统元素
- 不要使用圆角超过 8px — 古典风格偏向方正（4px 为主）
- 不要同时使用赤金和朱砂红作为强调 — 两者互斥，赤金为主、朱砂仅限印章

---

### 14. Claude（暖纸沙龙）

**气质：** 文学沙龙、温暖智识、纸感科技
**适用场景：** 知识分享、AI/工具产品、深度方法论

**字体：**
- 标题：`Anthropic Serif`（落地："Anthropic Serif", "Source Han Serif SC", "Songti SC", "SimSun", serif；中文回退 Noto Serif SC）
- 正文：`Anthropic Sans`（落地："Anthropic Sans", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif；中文回退 Noto Sans SC）

**配色：**
```css
:root {
    --parchment: #f5f4ed;
    --ivory: #faf9f5;
    --warm-sand: #e8e6dc;
    --near-black: #141413;
    --olive-gray: #5e5d59;
    --terracotta: #c96442;
    --coral: #d97757;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #f5f4ed;
    --ink: #141413;
    --ink-dim: #5e5d59;
    --accent: #c96442;
    --hairline: #d1cfc5;
}
```

**装饰配方：** 主签名 atmos（羊皮纸暖光，封面浓 / 内容页 dim）——全暖是身份，光的色温也必须暖

**签名元素：**
- 羊皮纸底（非白非灰，暖奶油调）
- 赤陶 accent（土系橙，deliberately un-tech）
- 全暖调灰阶（每个灰都带黄棕底色，禁冷灰）
- ring 阴影（`0 0 0 1px #d1cfc5`）替代边框

**组件样式：**

*按钮：*
- 主按钮：bg `#c96442`，文字 `#faf9f5`，圆角 8px，ring 阴影 `0 0 0 1px #d1cfc5`
- 次按钮：bg `#e8e6dc`，文字 `#4d4c48`，圆角 8px

*卡片：*
- 普通卡片：bg `#faf9f5`，圆角 12px，无边框，ring 阴影
- 高亮卡片：bg `#e8e6dc` + 赤陶左边线 3px

*标签/徽章：*
- bg `rgba(201,100,66,.1)`，文字 `#c96442`，圆角 6px
- 珊瑚链接 `#d97757` 带下划线

**设计规则：**

*推荐：*
- 杂志式留白节拍，衬线标题主导层级
- 深段（#141413 底 + 暖白字）做章节切换

*避免：*
- 不要冷灰、不要蓝紫（全暖是身份）
- 不要高饱和强调（赤陶的克制是质感来源）

---

### 15. Florasis 花西子（黛蓝鎏金）

**气质：** 东方仪式、雕花刻本、黛蓝鎏金
**适用场景：** 国货品牌、文化产品、东方美学发布

**字体：**
- 标题：`'Noto Serif SC', 'Source Han Serif SC', serif`（宋体刻本感）（落地："Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif）
- 正文：`'Noto Sans SC', sans-serif`（落地："Noto Sans SC", "PingFang SC", "Microsoft YaHei", "SimHei", sans-serif）

**配色：**
```css
:root {
    --bg-page: #FFFFFF;
    --bg-soft: #FAFAFA;
    --dai-blue: #003B4A;      /* 黛蓝：古时画眉螺子黛 */
    --liu-gold: #F4D19E;      /* 鎏金：雕花口红纹样 */
    --ink-black: #141414;
    --text-grey: #5C5F62;
    --border-grey: #BABFC3;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #FFFFFF;
    --ink: #003B4A;      /* 黛蓝承担几乎所有文字（以妆载道纪律） */
    --ink-dim: #5C5F62;
    --accent: #F4D19E;   /* 鎏金只作点睛（强调条/纹样/分割） */
    --hairline: #BABFC3;
}
```

**装饰配方：** 主签名 atmos（暖金微光，**全片 dim**）——留白为主、金线克制；鎏金面积 <10% 是纪律红线，装饰浓度跟着压

**签名元素：**
- 黛蓝承担几乎所有文字与结构色
- 鎏金只作点睛（强调条/纹样/分割装饰，面积 <10%）
- 白底 + 黛蓝字的"以妆载道"纪律
- 雕花/回纹类装饰仅金线勾勒

**组件样式：**

*按钮：*
- 主按钮：bg `#003B4A`，文字 `#F4D19E`，圆角 4px（近方，仪式感）
- 次按钮：transparent，`1px solid #003B4A`，黛蓝字

*卡片：*
- 普通卡片：bg `#FAFAFA`，圆角 4px，`border: 1px solid #BABFC3`
- 仪式卡：bg `#003B4A`，鎏金字与纹样边框

*标签/徽章：*
- 鎏金描边标签：`1px solid #F4D19E`，黛蓝字
- 印章式方形标：黛蓝底鎏金字

**设计规则：**

*推荐：*
- 金永远稀疏（<10% 面积是纪律红线）
- 大标题用宋体 + 宽字距（刻本排印）

*避免：*
- 不要金大面积铺底（金是纹样不是色块）
- 不要高饱和现代色（破坏东方静气）

---

### 16. Palace Museum 故宫文创（宫墙红金）

**气质：** 宫墙红、琉璃金、隆重有分寸
**适用场景：** 文化 IP、国潮发布、节庆主题

**字体：**
- 标题：楷体题字（`KaiTi, 'STKaiti', serif`）（落地："KaiTi", "Kaiti SC", "STKaiti", "SimSun", serif）
- 正文：`'Noto Serif SC', serif`（落地："Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif）

**配色：**
```css
:root {
    --palace-red: #A90C0C;    /* 宫墙红：身份 */
    --cinnabar: #DC3900;      /* 朱砂：点睛/CTA */
    --satin-gold: #E4D9B9;    /* 绸金：气质 */
    --apricot: #FFF4DA;       /* 杏黄：浅色面 */
    --ink: #333333;
    --bg-page: #FFFFFF;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #FFFFFF;
    --ink: #333333;
    --ink-dim: color-mix(in srgb, var(--ink) 58%, var(--bg));
    --accent: #A90C0C;
    --hairline: #E4D9B9;
}
```

**装饰配方：** 主签名 atmos（暖金底纹光，封面浓 / 内容页 dim）；需要收边仪式感时按「主题装置」开窗即兴给

**签名元素：**
- 宫墙红做身份色（标题/关键块）
- **金色大面积做底纹而非块面**（祥云/海水江崖纹样，透明度低垫底）
- 朱砂点睛（CTA/hover）
- 楷体题字 + 红章

**组件样式：**

*按钮：*
- 主按钮：bg `#A90C0C`，绸金文字 `#FFF4DA`，圆角 2px
- 朱砂按钮：bg `#DC3900`，白字（行动专用）

*卡片：*
- 普通卡片：白底，`border: 2px solid #E4D9B9`
- 底纹卡：杏黄底 `#FFF4DA` + 金纹样垫底 + 墨字

*标签/徽章：*
- 红章：宫墙红描边方框 + 楷体字（藏/印/展）
- 绸金分隔线：`1px solid #E4D9B9`

**设计规则：**

*推荐：*
- 红金分工：红=身份与标题、金=底纹与装饰、朱砂=行动
- 纹样做背景透明度 ≤10%（隆重不闹）

*避免：*
- 不要红金同时大块面（隆重感来自分寸）
- 不要现代无衬线做标题（楷体是题字传统）

---

## B2 清爽现代

### 17. Swiss Modern（瑞士现代）

**气质：** 干净、精准、包豪斯风格
**适用场景：** 设计展示、数据报告、极简风格

**字体：**
- 标题：`Archivo` (800)（落地："Archivo Black", "Arial Black", "Helvetica Neue", Arial, sans-serif）
- 正文：`Nunito` (400)（落地："Nunito", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --bg-primary: #ffffff;
    --text-primary: #000000;
    --accent: #ff3300;
    --text-secondary: #666666;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #ffffff;
    --ink: #000000;
    --ink-dim: #666666;
    --accent: #ff3300;
    --hairline: #f0f0f0;
}
```

**装饰配方：** 主签名 grid（**可见瑞士网格**，封面浓 / 内容页 dim）——网格是包豪斯签名本身，白底上用 hairline 同族极淡线贯穿（color-mix 派生，禁写死 hex）；不用 atmos（无明暗，纯平）

**签名元素：**
- 可见网格线
- 不对称布局
- 几何形状装饰
- 红色单一强调色

**组件样式：**

*按钮：*
- 主按钮：bg `#ff3300`，文字 `#ffffff`，圆角 2px（近乎直角，包豪斯），`font-weight: 800`（Archivo），hover 时 `transform: translateX(4px)` 几何位移
- 次按钮：bg transparent，文字 `#000000`，`2px solid #000000`，圆角 0，hover 时 bg `#000` + 文字变白
- 线框按钮：bg transparent，文字 `#ff3300`，`1px solid #ff3300`，圆角 0，hover 时填充红色

*卡片：*
- 普通卡片：bg `#ffffff`，圆角 0，`border: 1px solid #e0e0e0`，无阴影，严格网格对齐
- 高亮卡片：bg `#ffffff`，`border-left: 4px solid #ff3300`（红色左边线强调），其余三边 `1px solid #e0e0e0`
- 数据卡片：bg `#ffffff`，`border: 1px solid #000000`，数据数字用 `#ff3300` + `font-size: 2.5rem` + Archivo 800

*标签/徽章：*
- 直角（border-radius: 0），bg `#ff3300`，白字，`font-weight: 800`，`text-transform: uppercase`，`letter-spacing: 1px`
- 中性标签：bg `#f0f0f0`，文字 `#666666`，直角
- 网格标签：背景带网格线纹理 `background-image: linear-gradient(#e0e0e0 1px, transparent 1px)`

*阴影层级：*
- L1 卡片：无阴影 — 纯边框，包豪斯不依赖阴影
- L2 微浮：`0 2px 8px rgba(0,0,0,0.06)` — 仅用于弹出层/模态
- L3 结构层：`0 4px 16px rgba(0,0,0,0.08)` — 仅用于叠放的纸张效果

*装饰线：*
- 分割线：`1px solid #000000`（纯黑，精确），或 `1px solid #ff3300`（红色强调）
- 网格线：`1px solid #f0f0f0` 贯穿页面，形成可见的网格结构

**设计规则：**

*推荐：*
- 红色(#ff3300)作为唯一强调色，用于关键标注和行动元素
- 网格线是签名元素，使用极淡的 #f0f0f0 贯穿页面
- 不对称布局是核心 — 避免居中对称

*避免：*
- 不要使用阴影 — 包豪斯不依赖阴影，纯边框分层
- 不要使用圆角 — border-radius 保持 0-2px
- 不要添加装饰图形 — 只用网格和色块

---

### 18. Business Blue（商务蓝）

**气质：** 专业、可信赖、稳重
**适用场景：** 商务汇报、企业介绍、政府报告

**字体：**
- 标题：`Outfit` (700/800)（落地："Outfit", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 正文：`Outfit` (400/500)（落地同上）
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --primary: #1E3A8A;
    --secondary: #3B82F6;
    --accent: #F59E0B;
    --bg: #F8FAFC;
    --text: #1E293B;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #F8FAFC;
    --ink: #1E293B;
    --ink-dim: color-mix(in srgb, var(--ink) 58%, var(--bg));
    --accent: #F59E0B;   /* 琥珀金=强调/行动；深蓝是结构色不是 accent */
    --hairline: #e2e8f0;
}
```

**装饰配方：** 主签名 atmos（蓝调微光，**全片 dim**）——商务的干净靠留白，装饰只做极淡的冷光层次

**签名元素：**
- 深蓝主色 + 琥珀金强调
- 固定顶部导航栏
- 卡片式数据展示
- 数据放大显示

**组件样式：**

*按钮：*
- 主按钮：bg `#1E3A8A`（深蓝），文字 `#ffffff`，圆角 6px，hover 时 bg `#3B82F6`（亮蓝），`box-shadow: 0 4px 12px rgba(30,58,138,0.3)`
- 强调按钮：bg `#F59E0B`（琥珀金），文字 `#1E293B`，圆角 6px，hover 时 `filter: brightness(1.1)` + `box-shadow: 0 4px 12px rgba(245,158,11,0.3)`
- 幽灵按钮：bg transparent，文字 `#1E3A8A`，`1px solid #1E3A8A`，圆角 6px，hover 时 bg `rgba(30,58,138,0.05)`

*卡片：*
- 普通卡片：bg `#ffffff`，圆角 8px，`border: 1px solid #e2e8f0`，`box-shadow: 0 2px 8px rgba(30,58,138,0.06)`
- 高亮卡片：bg `#ffffff`，`border-left: 4px solid #1E3A8A`，圆角 8px，`box-shadow: 0 4px 16px rgba(30,58,138,0.1)`
- 数据卡片：bg `#ffffff`，`border-top: 3px solid #3B82F6`，数据数字用 `#1E3A8A` + Outfit 800，底部金色下划线装饰

*标签/徽章：*
- 圆角 4px（稳重方正），bg `rgba(30,58,138,0.08)`，文字 `#1E3A8A`，字体 Outfit 500
- 金色标签：bg `rgba(245,158,11,0.1)`，文字 `#F59E0B`，圆角 4px
- 状态标签：小圆点 + 文字，`::before { content: ''; width:6px; height:6px; border-radius:50%; background:#10B981 }`

*阴影层级：*
- L1 卡片：`0 2px 8px rgba(30,58,138,0.06)` — 浅蓝阴影
- L2 悬停：`0 4px 16px rgba(30,58,138,0.1)` — 蓝色调浮起
- L3 金色焦点：`0 8px 24px rgba(245,158,11,0.12)` — 琥珀金辉光，用于CTA

*装饰线：*
- 分割线：`1px solid #e2e8f0`，可左侧加蓝色圆点标记
- 导航下划线：`2px solid #3B82F6`，用于活跃导航项

**设计规则：**

*推荐：*
- 深蓝(#1E3A8A)与琥珀金(#F59E0B)严格分工：蓝=结构/信任，金=行动/强调
- 数据卡片使用 Outfit 800 放大数字，搭配金色下划线装饰
- 状态标签用小圆点+文字组合，传达专业感

*避免：*
- 不要使用渐变 — 商务蓝追求稳重，不是花哨
- 不要让琥珀金和深蓝出现在同一按钮上
- 不要使用过大的圆角 — 保持 4-8px 的稳重方正感

---

### 19. Stripe Professional（Stripe 专业）

**气质：** 精密、自信、轻量级权威
**适用场景：** 金融科技、B2B 产品、SaaS 汇报

**字体：**
- 标题：`Work Sans` (300) — 轻量标题是 Stripe 的灵魂（落地："Work Sans", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 正文：`Work Sans` (400)（落地同上）
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --bg-primary: #ffffff;
    --bg-dark: #1c1e54;
    --text-heading: #061b31;
    --text-body: #64748d;
    --accent-purple: #533afd;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #ffffff;
    --ink: #061b31;
    --ink-dim: #64748d;
    --accent: #533afd;
    --hairline: #e5edf5;
}
```

**装饰配方：** 主签名 atmos（极淡，**全片 dim**）——留白即权威，装饰浓度全库最低档之一

**签名元素：**
- weight 300 轻量级标题 — "不靠粗体发声"
- 蓝色调多层阴影 rgba(50,50,93,0.25)
- 深靛蓝(#1c1e54)暗色区块
- 4-8px 保守圆角

**组件样式：**

*按钮：*
- 主按钮：bg `#533afd`，白字，圆角 4px，hover 时 bg `#4434d4`
- 幽灵按钮：bg transparent，文字 `#533afd`，`1px solid #b9b9f9`，圆角 4px，hover 时 bg `rgba(83,58,253,0.05)`
- 信息按钮：bg transparent，文字 `#061b31`，`1px solid #e5edf5`，圆角 4px

*卡片：*
- 普通卡片：bg `#ffffff`，圆角 6px，`border: 1px solid #e5edf5`，`box-shadow: rgba(50,50,93,0.25) 0px 30px 45px -30px, rgba(0,0,0,0.1) 0px 18px 36px -18px`
- 暗色卡片：bg `#1c1e54`，文字 `#ffffff`，圆角 6px，`border: 1px solid rgba(255,255,255,0.1)`
- 数据卡片：bg `#ffffff`，数据数字用 `#061b31` + Work Sans 300 + `font-size: 3rem`

*标签/徽章：*
- 圆角 4px，bg `rgba(83,58,253,0.08)`，文字 `#533afd`，Work Sans 400
- 成功标签：bg `rgba(21,190,83,0.2)`，文字 `#108c3d`，圆角 4px，`1px solid rgba(21,190,83,0.4)`
- 中性标签：bg `#ffffff`，文字 `#64748d`，圆角 4px，`border: 1px solid #e5edf5`

*阴影层级：*
- L1 氛围：`rgba(23,23,23,0.06) 0px 3px 6px` — 微弱浮起
- L2 标准：`rgba(23,23,23,0.08) 0px 15px 35px` — 标准卡片
- L3 蓝调：`rgba(50,50,93,0.25) 0px 30px 45px -30px, rgba(0,0,0,0.1) 0px 18px 36px -18px` — 蓝色调深度

*装饰线：*
- 分割线：`1px solid #e5edf5`
- 虚线装饰：`1px dashed #362baa` 用于占位区域
- 暗色区块边框：`1px solid rgba(255,255,255,0.1)`

**设计规则：**

*推荐：*
- 标题使用 weight 300 — 轻量级是 Stripe 的核心辨识度
- 所有阴影带蓝色调 rgba(50,50,93,0.25) — 阴影也是品牌的一部分
- 标题颜色使用 #061b31(深靛蓝)而非纯黑 — 这点微妙但重要

*避免：*
- 不要使用 weight 600-700 的粗体标题 — 300 是品牌声音
- 不要使用大于 8px 的圆角 — Stripe 追求保守精准
- 不要让品红/宝石红出现在按钮上 — 它们只用于装饰渐变

---

### 20. Notion Warm（Notion 温暖）

**气质：** 温暖极简、纸质感、工具即画布
**适用场景：** 知识管理、协作工具、SaaS 展示

**字体：**
- 标题：`Inter` (700) — `font-feature-settings: "lnum"`（落地："Inter", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 正文：`Inter` (400)（落地同上）
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --bg-primary: #ffffff;
    --bg-warm: #f6f5f4;
    --text-primary: rgba(0,0,0,0.95);
    --text-secondary: #615d59;
    --text-muted: #a39e98;
    --accent-blue: #0075de;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #ffffff;
    --ink: rgba(0,0,0,0.95);
    --ink-dim: #615d59;
    --accent: #0075de;
    --hairline: rgba(0,0,0,0.1);
}
```

**装饰配方：** 主签名 atmos（呢喃级，**全片 dim**）——白/暖白区域交替已是节奏，装饰只在暖白区给一点温度

**签名元素：**
- 温暖中性色 — 所有灰色带黄棕底色
- 呢喃边框：`1px solid rgba(0,0,0,0.1)` — 几乎看不见
- 白/暖白(#f6f5f4)交替区域
- 4-5 层阴影叠加，单层不透明度不超过 0.05

**组件样式：**

*按钮：*
- 主按钮：bg `#0075de`，白字，圆角 4px，hover 时 bg `#005bab`，active 时 `scale(0.9)`
- 次按钮：bg `rgba(0,0,0,0.05)`，文字 `rgba(0,0,0,0.95)`，圆角 4px，hover 时 `scale(1.05)`
- 药丸标签：bg `#f2f9ff`，文字 `#097fe8`，圆角 9999px，Inter 600 12px

*卡片：*
- 普通卡片：bg `#ffffff`，圆角 12px，`border: 1px solid rgba(0,0,0,0.1)`，4 层阴影(最大不透明度 0.04)
- 暖色卡片：bg `#f6f5f4`，圆角 12px，`border: 1px solid rgba(0,0,0,0.1)`
- 数据卡片：bg `#ffffff`，数据数字用 `rgba(0,0,0,0.95)` + Inter 700 + `font-size: 3rem`

*标签/徽章：*
- 药丸标签：bg `#f2f9ff`，文字 `#097fe8`，圆角 9999px，`letter-spacing: 0.125px`
- 暖灰标签：bg `rgba(0,0,0,0.05)`，文字 `#615d59`，圆角 4px
- 语义标签：绿色(#1aae39)/橙色(#dd5b00)/粉色(#ff64c8) 用于状态

*阴影层级：*
- L1 呢喃：`1px solid rgba(0,0,0,0.1)` — 边框级
- L2 柔和：4 层阴影(最大不透明度 0.04) — 内容卡片
- L3 深度：5 层阴影(最大不透明度 0.05, 52px blur) — 模态/焦点

*装饰线：*
- 分割线：`1px solid rgba(0,0,0,0.1)` — 呢喃级
- 区域分隔：通过白/暖白(#f6f5f4)背景切换实现
- 无硬线分隔 — 一切靠微妙对比

**设计规则：**

*推荐：*
- 使用温暖中性色 — #f6f5f4(暖白)、#615d59(暖灰)、#a39e98(暖浅灰)是 Notion 的灵魂
- 边框永远是呢喃级 1px solid rgba(0,0,0,0.1) — 存在但不打扰
- 白/暖白区域交替创造柔和节奏

*避免：*
- 不要使用冷灰色 — Notion 的灰色都带黄棕底色
- 不要使用超过 0.05 不透明度的单层阴影 — 阴影是"感觉"而非"看到"
- 不要使用纯黑(#000)文字 — 使用 rgba(0,0,0,0.95) 创造微妙温暖

---

### 21. Clay（奶油抹茶）

**气质：** 暖奶油、清新关系、轻盈现代
**适用场景：** CRM/关系管理、团队汇报、轻松商务

**字体：**
- 标题：`Inter` (600/700)（落地："Inter", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 正文：`Inter` (400)（落地同上）
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --cream: #faf9f7;
    --pure-white: #ffffff;
    --clay-black: #000000;
    --matcha-light: #84e7a5;
    --matcha-mid: #078a52;
    --matcha-deep: #02492a;
    --slushie: #3bd3fd;
    --lemon: #f8cc65;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #faf9f7;
    --ink: #000000;
    --ink-dim: color-mix(in srgb, var(--ink) 58%, var(--bg));
    --accent: #078a52;
    --hairline: #c9c6bd;
}
```

**装饰配方：** 主签名 atmos（奶油暖光，封面浓 / 内容页 dim）——抹茶三阶绿里 atmos 母色走 matcha-mid；圆角气质可开 --radius-card（12px，卡场景）

**签名元素：**
- 暖奶油纸底
- 抹茶三阶绿（浅点缀/中主色/深段底）
- 冰青/柠檬做数据点缀（清新不吵）
- 虚线边框纹理

**组件样式：**

*按钮：*
- 主按钮：bg `#078a52`，白字，圆角 999px
- 次按钮：白底，`1px dashed #c9c6bd`，墨字，圆角 999px

*卡片：*
- 普通卡片：bg `#ffffff`，圆角 16px，`box-shadow: 0 2px 12px rgba(0,0,0,.05)`
- 深段卡片：bg `#02492a`，暖白字（章节切换用）

*标签/徽章：*
- 圆形点：#84e7a5（正向）/ #3bd3fd（信息）/ #f8cc65（星标）

**设计规则：**

*推荐：*
- 抹茶绿主导，冰青/柠檬各 ≤1 处/页
- 全页圆角 ≥12px（轻盈气质）

*避免：*
- 不要锐利直角（Clay 无直角）
- 不要三色点缀同页等量（绿永远主导）

---

### 22. Capsule（奶油胶囊）

**气质：** 奶油画布、四彩胶囊、氛围光斑
**适用场景：** 产品发布、生活方式、轻快叙事

**字体：**
- 标题：`Inter` (700/800)（落地："Inter", "Segoe UI", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif）
- 正文：`Inter` (400/500)（落地同上）
- 中文回退：`'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif`

**配色：**
```css
:root {
    --cream: #F5F5F0;
    --ink: #1A1A1A;
    --coral: #E85D4E;
    --lime: #C4D94E;
    --lavender: #C5B5E0;
    --sky: #8BB4F7;

    /* v2 五件套映射（产物用这几个变量，缺项按映射表公式派生） */
    --bg: #F5F5F0;
    --ink-dim: color-mix(in srgb, var(--ink) 58%, var(--bg));
    --accent: #E85D4E;
    --hairline: color-mix(in srgb, var(--ink) 16%, transparent);
}
```

**装饰配方：** 主签名 atmos（**糖果色光斑 2-3 团**，封面浓 / 内容页 dim，全库唯一光晕预设）——光斑透明度 6-15%，角落锚定；圆角气质可开 --radius-card（16px）

**签名元素：**
- 奶油画布 + 糖果四色胶囊标签（coral/lime/lavender/sky）
- **radial-glow 氛围光斑**（糖果色 6-15% 透明度，角落锚定，全库唯一光晕预设）
- 胶囊形（999px）贯穿按钮与标签

**组件样式：**

*按钮：*
- 主按钮：bg `#E85D4E`，白字，圆角 999px
- 次按钮：白底，`1px solid #1A1A1A`，墨字，圆角 999px

*卡片：*
- 普通卡片：bg `#ffffff`，圆角 16px，柔影 `0 2px 12px rgba(0,0,0,.06)`
- 氛围背景：奶油底 + 2-3 团糖果 radial 光斑（`radial-gradient(ellipse ... rgba(232,93,78,.13), transparent 62%)` 式）

*标签/徽章：*
- 胶囊：四色轮替，白字或墨字，圆角 999px，`padding: 6px 16px`

**设计规则：**

*推荐：*
- 光斑 2-3 团/页，透明度 6-15%（氛围暖光不抢主体）
- 四彩有语义分工时优先 coral=行动，其余做分类标签

*避免：*
- 不要四色同页等量撒（选 1 主 + 其余点缀）
- 光斑透明度不要超 15%（变成色块即穿帮）

---

## 字体配对速查

| 预设 | Display 字体 | 正文字体 |
|------|--------------|----------|
| 1 Bold Signal | Archivo Black | Space Grotesk |
| 2 8-Bit Orbit | Tektur | Chakra Petch |
| 3 Broadside | 压缩 display（Bebas 感） | Noto Serif SC（落地 Source Han Serif SC） |
| 4 Sentry | Inter 600 | Inter |
| 5 Kraken | Inter 600/700 | Inter |
| 6 Dark Botanical | Cormorant | IBM Plex Sans |
| 7 Terminal Green | JetBrains Mono | JetBrains Mono |
| 8 Linear Dark | Inter 510 | Inter |
| 9 MongoDB | Inter/Work Sans | Inter |
| 10 Deep Teal Review | Archivo（数字） | Noto Sans SC |
| 11 Paper & Ink | Cormorant Garamond | Source Serif 4 |
| 12 Notebook Tabs | Bodoni Moda | DM Sans |
| 13 Ink Garden | Noto Serif SC | Noto Sans SC |
| 14 Claude | Anthropic Serif（中文 Noto Serif SC） | Anthropic Sans（中文 Noto Sans SC） |
| 15 Florasis 花西子 | Noto Serif SC | Noto Sans SC |
| 16 Palace Museum 故宫 | 楷体 KaiTi | Noto Serif SC |
| 17 Swiss Modern | Archivo 800 | Nunito |
| 18 Business Blue | Outfit | Outfit |
| 19 Stripe Professional | Work Sans 300 | Work Sans |
| 20 Notion Warm | Inter 700 | Inter |
| 21 Clay | Inter | Inter |
| 22 Capsule | Inter 700/800 | Inter |

## 装饰配方速查

| 预设 | 主签名词条 | 浓淡 | 主题装置 |
|------|-----------|------|------------|
| 1 Bold Signal | atmos（暖橙微光） | 封面浓/内容 dim | 数据封面可选 |
| 2 8-Bit Orbit | scan+atmos（CRT+暗角） | 封面浓/内容 dim | — |
| 3 Broadside | grid（报格网，墨系） | 封面浓/内容 dim | — |
| 4 Sentry | atmos+grid（深空+测距网） | 封面浓/内容 dim | — |
| 5 Kraken | atmos（紫调微光） | 封面浓/内容 dim | 数据封面可选 |
| 6 Dark Botanical | atmos（金粉光斑） | 封面浓/内容 dim | — |
| 7 Terminal Green | scan（CRT 全屏纹） | 封面浓/内容 dim | — |
| 8 Linear Dark | atmos（亮度阶梯微光） | 全片 dim | — |
| 9 MongoDB | atmos+grid（青渐变+设施网） | 封面浓/内容 dim | 数据封面可选 |
| 10 Deep Teal Review | atmos+grid（冰青仪表） | 封面浓/内容 dim | 数据封面推荐 |
| 11 Paper & Ink | atmos（纸面明暗） | 全片 dim | — |
| 12 Notebook Tabs | atmos（纸面微光） | 全片 dim | — |
| 13 Ink Garden | atmos（墨晕扩散） | 封面浓/内容 dim | — |
| 14 Claude | atmos（羊皮纸暖光） | 封面浓/内容 dim | — |
| 15 Florasis 花西子 | atmos（暖金微光） | 全片 dim | — |
| 16 Palace Museum | atmos（金纹光） | 封面浓/内容 dim | — |
| 17 Swiss Modern | grid（可见瑞士网格） | 封面浓/内容 dim | — |
| 18 Business Blue | atmos（蓝调微光） | 全片 dim | — |
| 19 Stripe | atmos（极淡） | 全片 dim | — |
| 20 Notion Warm | atmos（呢喃级） | 全片 dim | — |
| 21 Clay | atmos（奶油暖光） | 封面浓/内容 dim | — |
| 22 Capsule | atmos（糖果光斑，唯一光晕） | 封面浓/内容 dim | — |

## 避免使用的通用模式

**字体：** 避免把 Inter / Roboto / Arial / 系统 UI 字体当作**通用默认**（到处都用）。豁免：品牌复刻预设按品牌真实字体——Sentry / Kraken / Linear Dark / MongoDB / Notion Warm / Clay / Capsule 用 Inter，Stripe 用 Work Sans，属复刻事实不算踩线；但同一 deck 内不许再引入第二种 display。
**配色：** `#6366f1`（通用靛蓝），白色背景上的紫色渐变
**布局：** 全部居中，通用英雄区，千篇一律的卡片网格
**渐变与光晕：** 只用预设点名的（全库仅 Capsule 光斑、Kraken 紫渐变 CTA、Dark Botanical 金粉辉光有光效基因）；其余写纯色。

## CSS 注意事项

### 取反CSS函数

**错误 — 浏览器会静默忽略：**
```css
right: -clamp(28px, 3.5vw, 44px);   /* 浏览器忽略 */
```

**正确 — 用 calc() 包裹：**
```css
right: calc(-1 * clamp(28px, 3.5vw, 44px));  /* 生效 */
```

### 注释内禁写斜杠星号组合

CSS 注释里写 token 名时用顿号隔开（如"radius 与 shadow 两族 token"），**禁写 `--xxx-*/--yyy` 形式**——`*/` 会提前闭合注释，垃圾文本吞掉后续规则（实测坑：:root 整体失效、全片变量死）。