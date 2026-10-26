---
name: generating-slides
slug: generating-slides
displayName: 网页幻灯片制作专家
display_name: 网页幻灯片制作专家
display_name_en: Web Slide Deck Expert
version: 1.6.5
author: 庆哥聊AI
copyright: Hongqing W
license: MIT
summary: "说一句话或丢一份材料，出可直接放映的网页幻灯片——单文件 HTML、七步引导、三层排版硬约束、交付前自动体检。"
description: "把一句话需求或现成材料做成可放映的网页幻灯片（单文件 HTML）。三种用法：从零生成（「做个 Q3 复盘 PPT，12 页，给管理层看」）/ 重排材料（「这份 docx 做成 10 页汇报稿」）/ 只改指定页（「第 3 页太挤，砍一半」）。内置 22 套风格预设、三层排版硬约束、交付前自动机验。**触发场景：** 用户说「帮我做PPT」「创建演示」「做个汇报」「制作slides」「生成幻灯片」「准备一份展示」「做个介绍」「make a presentation」「create slides」时使用；即使没明确说做 PPT，提到需要展示、汇报或介绍的内容（如「我要给领导做个汇报」「帮我准备下周分享的材料」「做个产品介绍」）也应使用此技能。"
description_zh: "把一句话需求做成可直接放映的网页幻灯片：单文件 HTML、1920×1080 投影级版面、七阶段引导式确认。内置 22 套风格预设与三层排版红线（版面率→字号→秩序），交付前用机验脚本自动检查；支持 P 键导出 PDF，附 E 编辑／D 画笔／S 演讲者窗口三重交互。"
description_en: "A single-file HTML deck generator for projection-grade presentations. Seven-stage guided workflow, 22 style presets, a three-layer layout system (fill ratio, type scale, visual order), and built-in checker scripts that verify each deck before delivery."
tags: [演示文稿, PPT, 幻灯片, 汇报, 网页幻灯片]
compatibility: "生成期零外部依赖（纯静态单文件）。机验：Chrome headless（measure-layout.js 版率）+ verify-consistency.py（纯 Python 零依赖）；crowd-probe.py 需 playwright（缺则打印 [SKIP] 跳过，不判红、禁临时安装）。可选：python-pptx/docx（素材提取）、Node.js（底盘构建）。"
---

<!--
  Slides Skill — 流程外壳 v1 七阶段 + 排版内核 v2（三层底层约束）
  MIT License — © 2025 Zara Zhang (original framework)
                © 2026 Hongqing W (v2 paradigm)
-->

# Generating Slides — 投影级网页演示生成器

**流程体验 = v1 七阶段（每阶段等用户确认）；排版内核 = v2 三层规则（版面率→字号→秩序）**

> **来源声明**：本技能基于 Zara Zhang 的开源项目 [Frontend Slides](https://github.com/zarazhangrui/frontend-slides)（MIT License）二次开发，非原创首发；排版底盘、三层约束与机验流程为本包自有。整体依 MIT 分发，上游版权与许可声明见文末《来源与许可》。

## 排版内核总纲（阶段 6 生成的硬约束，生成前必读规则全文）

> **版面率管"有没有站住版面"，字号管"站住了看不看得见"，秩序管"看见了乱不乱"。下层不达标，上层免谈。**

```
第一层 底盘：版面率   → 密排 ≥60% 面积且宽 ≥80% / 双栏 ≥45% / 单焦点主角块 ≥60% 版心
第二层 阅读：字号     → 正文地板 22px（1/50 屏高）/ 标题 84px 锁档 / 仪式位 110-140px 闭环反推
第三层 秩序：分组对齐间距 → 间距三档跟层级树 / 容器阶梯卡>线>留白
```

**规则全文与机验口径 → [references/layout-rules-v2.md](references/layout-rules-v2.md)（阶段 6 前 MUST 整读全文：禁设行数范围、禁只读小节。阶段 6 除本文 + 槽位路由到的页型文件外，Do NOT 预加载其他 references）**

**焦点与强调判断（层级三问 / 手法八件套 / 视觉重量红线 / 颜色纪律 / 卡片分合）→ [references/focus-judgment.md](references/focus-judgment.md)（阶段 3 焦点定档后、阶段 6 排版时读）**

## 快速上手：两句典型指令

装好后直接说话，不需要记命令：

| 你说 | 会发生什么 |
|---|---|
| 「帮我做个关于 2026Q3 运营复盘的 PPT，12 页，给管理层看」 | 从零生成：配置 → 素材 → 大纲 → 风格预览 → 生成 → 机验 → 交付 |
| 「第 3 页太挤了，砍掉一半，别动版式」 | 改稿轮次：只动指定页，砍字不缩字号，改完复跑同页机验 |

**它不会做的事**：不会替你默认选风格，不会跳过确认点自己往下跑，不会用缩小字号的方式硬塞内容，也不会把内容页配图（图片唯一出口是封面）。

## 核心原则

1. **单文件输出** — 一个 HTML 含全部 CSS/JS，无外部依赖
2. **展示而非描述** — 生成视觉预览让用户"看"（真网页/预览文件），而不是用文字描述风格
3. **自动打开（一切生成物）** — HTML 文件（含风格预览、最终版）生成即 `cmd /c start "" "文件路径"` 打开（`start` 是 cmd 内建命令，必须经 `cmd /c` 转发；macOS/Linux 用 `open`/`xdg-open`）。**交付形态永远是 HTML 网页，禁以截图/图片替代**
4. **底盘唯一（阶段 6，装配式架构）** — 复制 [assets/chassis-v2.html](assets/chassis-v2.html) 为起点：1920×1080 舞台 + token + 页骨架 + 交互三件套（E 编辑 / D 画笔 / S 演讲者；提词职责归 S 演讲者窗口备注卡——主窗口是投屏观众可见）+ 动画库 + P 键 PDF 双出口。**chassis-v2.html 是装配产物禁手改**：源码在 `assets/chassis/`（核心：core.css/core.js/template.html，冻结）+ `assets/modules/`（功能件：interactions/print 基本件 + effects/anim-runtime 动画件），改完跑 `node scripts/build-chassis.mjs` 重建；新功能=新模块文件+装配表一行，**不再往底盘塞补丁**。用户明说"不要动画"→ `build-chassis.mjs --no-effects` 出精简底盘
5. **焦点唯一性前置判定** — 每页先答"这页强调什么"：标题当主角则升档、数字/金句当主角则标题退档，互斥，一页一个焦点
6. **标题三层身份** — 主张型（断言句）全片锁 84px ±0 / 话题型（描述句）密度带 72-96 / 仪式位另档；同密度档内 ±0
7. **cut never compress** — 超密度（>200 字/页）砍字或砍页，绝不缩字号硬塞
8. **机验闭环** — 生成后必跑 measure-layout.js 量版率；不达标回白名单手段调（换纵向/升字号/换轻容器/砍页），**永不加填充物**（60% 反噬史禁令）

## NEVER 速查（改稿轮次只读局部时必扫；散布各节的上下文版保留不动）

- 永不加填充物凑版面率 → 原则 8
- 超密度砍字砍页，绝不缩字号硬塞 → 原则 7
- 客户实物永远优先，禁拿库内预设顶替 → 阶段 5
- 色值只走五件套映射与派生公式，禁自造 → 阶段 6.2
- 封面装置按新主题推导，禁照搬参考物的主题装置 → 阶段 5
- 图片唯一出口是封面，内容页禁图 → 5.2
- 预览=迷你成品，禁手排示意 → 5.1
- 用装饰的页，内容必须包进 `.content`（漏包=装饰压字）→ 阶段 6.2
- 趋势/构成/排行数据必图表化，禁排纯数字组 → 阶段 6.6
- chassis-v2.html 是 build 产物禁手改，改源码必跑 build → 原则 4

---

## 工作流程

严格按照以下 **7 个阶段** 顺序执行，每个阶段等待用户确认后再进入下一阶段（阶段 0 为可选前置、6.5 为阶段 6 的机验子步；含交付共 8 个确认停点——「七阶段」是流程名号）。**已有产物的局部修改不进本流程**：改稿轮次＝只动指定页 / 只换配色，不重跑阶段 1-5，走 [references/iterative-edit.md](references/iterative-edit.md)（改完复跑同页 measure-layout 与 verify-consistency）。

### 阶段0：读取项目规则（可选，先于其他阶段）

**若项目根目录存在协作规则文件（如 `CLAUDE.md`、`AGENTS.md`），先读一遍，获取该项目的协作与输出约束，全程遵守。没有则直接进入阶段 1——禁止自行创建、禁止因此报错或卡住。若其中含风格偏好（或用户全局配置带偏好）：仅作为阶段 5 候选池的排序参考——不得跳过 5.0 氛围提问、不得替用户默认选定风格。**

> 本技能不依赖该文件即可完整运行；它的全部技术硬约束已内置于本文件与 `references/`。

### 阶段1：配置

**进门先确认产物（模糊说法才需要）**：用户说法里没有明确产物时——例如「帮我准备一份材料」「下周要分享点东西」——**先用一句话确认「要的是可放映的 PPT 吗」**，确认后再进四问。
**不要自行拆解用户意图**：别替他判断他要的是文档、表格还是 PPT，也别因为说法模糊就跳过四问直接开工；他不给方向，就给几个具体选项让他点。

使用宿主的**结构化提问**（如 AskUserQuestion）**一次性询问所有配置（合并为 1 次提问）**；宿主没有这类工具时，改用一条消息列编号选项，效果等价：

- **问题1 - 页数规模**：5页（快速）/ 10页（标准，推荐）/ 15页（详细）/ 20页（全面）/ 自定义（上限30页）
- **问题2 - 内容侧重**：数据驱动（多图表）/ 平衡型（推荐）/ 文字内容 / 演讲演示型（大字少文：标题=结论句、页面只留结论+关键数字，完整论述进 NOTES 讲稿）
- **问题3 - 内容素材**：有本地文件可提供（Word/PDF等） / 仅有主题，需要搜集资料 / 有PPT文件需要转换（.pptx）
- **问题4 - 视觉素材**：有本地图片可提供（**仅用于封面**） / 无图片，用CSS生成背景

同时收集主题/标题。用户已在消息中提供则直接使用。

**体裁档位推断（不新增提问轮次）**：阶段 1 顺带定标题体裁档（A 纯书面 / B 汇报+现场讲 / C 纯演讲，管标题句式配比）。用户话里已有线索的直接推断、不问："汇报/评审/内部会"→ B；"分享/发布/开场"→ C；"发出去看/邮件传阅"→ A。完全没提场合 → 仅在上述四问里加一项"这份材料会不会有人现场讲"。判据四问与三档配比 → [references/title-copy-types.md](references/title-copy-types.md) §2。注意与问题 2 的"演讲演示型"不同轴：那边管内容形态，这边管场合配比，互不代劳。

### 阶段2：内容准备

根据阶段1素材情况走三分支（**提取命令、编码 workaround、图片筛选细则 → [references/content-preparation.md](references/content-preparation.md)**）：

- **分支A 本地文件**：按文件类型提取（PDF/Markdown 直接 Read；docx 用 Python 提取，Windows 必须加 UTF-8 编码声明）→ 整理资料摘要 → 用户确认
- **分支B 仅主题**：WebSearch 搜真实资料（3-5 关键词覆盖行业数据/案例/趋势/权威观点，可并行）→ 资料摘要 → 用户确认
- **分支C .pptx**：`python scripts/extract-pptx.py <input.pptx> <output_dir>` → 展示提取结果 → 用户确认。图片只筛封面可用素材，其余丢弃

**素材体量控制（防爆上下文）**：<30KB 直接读；30-100KB 只读目录/标题结构+按需局部读；**>100KB 禁全量读**——先读标题结构，按大纲页面主题抽取相关段落（每页引用 ≤2KB 原文）。已有 outline/fields 类结构文件优先复用。

### 阶段3：内容优化（静默执行，不展示给用户）

系统自动执行优化原则（聚焦、三法则、焦点识别、层级分析、叙事节拍等）→ [references/content-optimization.md](references/content-optimization.md)。
焦点识别定档之后的强调判断（选什么手法、重量红线、用色纪律）→ [references/focus-judgment.md](references/focus-judgment.md)。
同时完成**密度分档预标注**：逐页按正文字数定档（低 ≤40 字 / 中 40-120 / 高 120-200 / 超 >200 砍字砍页），档位进阶段 4 大纲的密度列。
标题文案分型同步执行（§3.2 接线）：按阶段 1 体裁档位逐页标文案类型（结论/钩子/仪式）→ [references/title-copy-types.md](references/title-copy-types.md)。

### 阶段4：生成大纲

- 封面页第 1 页 + 结束页最后一页由大纲阶段自动追加，不计入用户指定页数。**封面 hook 管道**：封面 hook 候选取自本阶段大纲的焦点列与钩子页（用户未定标题时封面标题=全片第一个钩子句），禁生成封面时现场另挖——判定树与装置规则见 [references/decoration-vocab.md](references/decoration-vocab.md) §五封面构图总纲
- 数据驱动型标注图表页；按章节分组（每章 2-4 页）；总页数符合配置
- **大纲必须含内容映射**：每页带「来源 + 焦点 + 槽位 + 密度档 + 文案类型」列，如 `P5 国家政策 ← 来源：文档§3.1 焦点：数字 槽位：焦点数字 密度：低 类型：结论`。焦点四类（数字/结论/图表/清单），槽位按下方判定树映射；文案类型按 [title-copy-types.md](references/title-copy-types.md) 体裁档位配比标注（结论/钩子/仪式）；钩子页须同时在副行写出数据注，无数据注视为未完成。填不出 = 该页未完成，先提炼焦点或拆页并页
- **展示大纲，等待用户确认。**

### 阶段5：风格选择

**客户自带风格（2026-10-25 立，优先于下方标准流程）**

- 给了实物（成品 HTML / PPTX / 截图 / 色值）或点名已存自定义预设 → **跳过下方四池提问与风格预览**，直接提取实物**风格配方**采用——不只色板：渐变、封面装置的浓密度与态度、标题用色节奏（双色/字距）、容器浓度（玻璃卡/无盒）一并提取对齐；**装置的具体内容按新主题推导，禁照搬参考物的主题装置**（贴片/柱阵/圆环是上一个主题的隐喻物，跨主题照搬=套模板）。色板缺的角色才走派生公式；交付时亮一句所用配方供核对（1025 实测教训：只提色板=色对魂丢，参考物的丰富度全被底盘默认磨平）
- 只给了含糊词（如「科技风」）→ 不出文字追问，按词的气质挑 3 套出预览图让客户指认
- 客户实物永远优先，**禁止拿库内预设顶替**（1025 事故：用户自定义风格被旧入册青族顶替出稿）

无风格指定时，走以下标准流程。

**先读 [references/presets-index.md](references/presets-index.md)（22 套索引+四池路由），再按池/点名到 [references/style-presets.md](references/style-presets.md) Grep 预设名直达对应小节——勿全量读正文（约 1700 行）。** 核心理念：用户只答 1 个问题、看 1 个预览文件；封面布局根据内容自动决定。

#### 5.0 风格选择（1 次提问）

**用单选提问（4 选 1；宿主有结构化提问就用，否则用编号选项；2×2 结构——暗系按能量切、亮系按底色质感切）：** A1. 冲击暗色 / A2. 沉静暗色 / B1. 纸感编辑 / B2. 清爽现代

| 选项 | 预设池 | 氛围→入场节奏联动 |
|------|--------|---------------|
| A1. 冲击暗色 | Bold Signal, 8-Bit Orbit, Broadside, Sentry, Kraken | 震撼/自信 — 慢淡入+分层揭示 |
| A2. 沉静暗色 | Dark Botanical, Terminal Green, Linear Dark, MongoDB, Deep Teal Review | 冷静/精密 — 克制淡入 |
| B1. 纸感编辑 | Paper & Ink, Notebook Tabs, Ink Garden, Claude, 花西子, 故宫文创 | 温暖/感动 — 缓慢渐次揭示 |
| B2. 清爽现代 | Swiss Modern, Business Blue, Stripe, Notion, Clay, Capsule | 平静/专注 — 柔和淡入 |

**点名直达（白名单规则）：** 用户点名任意预设（如"用 Linear Dark"）→ 直接采用，跳过四池路由——**22 套全为白名单**。四池只管"用户没点名"的标准流程。

用户选择后，从对应池中选**最匹配主题的 3 套**生成预览。

#### 5.1 生成完整预览（1 个文件 · 迷你成品制）

3 个预设合并为**一个 HTML 文件**（CSS scroll-snap 全屏翻页），保存到 `.claude-design/slide-previews/preview-styles.html`，用 Write 一次写入。

**⚠️ 预览=迷你成品（皮肤+骨架同真）**：预览卡**必须内嵌真 chassis 舞台**——卡内页结构与成品同构（同一套 token 档位字号/间距、同一棵槽位判定树、边注四件套齐全），再 `transform: scale(卡宽/1920)` 等比缩小。等比缩放不改版面率/配重比，用户看到的就是成品版面的等比样。**禁手排示意**——只取预设色板组件、卡内版式不走 token 档位=只演示皮肤不演示骨架，属断层负样本。

卡对骨架（每套预设：封面卡+内容卡并排）：

```html
<div class="pv-card">                  <!-- aspect-ratio:16/9; width:46%; overflow:hidden -->
  <div class="pv-stage">               <!-- 1920×1080; transform-origin:top left; 色板+token 照搬 chassis -->
    <section class="slide">…</section> <!-- 过判定树选真槽位；字号/间距只取 token 档 -->
  </div>
</div>
<script>每卡按 卡宽/1920 设 scale（load+resize 双挂）</script>
```

- **卡片纪律**：封面卡与内容卡左右并排等大、垂直居中；禁 grid 等分拉伸填格、禁封面卡小于内容卡
- **内容页选样**：取大纲最典型一页（有论点有数据），预览阶段就执行版面约束（版率口径/22px 地板/槽位判定树同 layout-rules），不是事后声明
- **预览元信息在卡外**：风格名+气质标签放卡上方、"适合 | 签名 | 避免"放卡下方——不占卡内版面
- **机验边界**：预览不跑字号类探针（scale 后 getBoundingClientRect 为缩小值，绝对值口径必误报）；全量机验仍在阶段 6.5 对成品跑

浏览器打开预览 → 用户翻页对比 → 4 选 1 提问（三套风格 + D 混搭；宿主有结构化提问就用，否则编号选项）。混搭直接追问具体要求，不再生成预览。**封面确认点（2026-10-25 立）：首批生成（封面+前 2 页）后亮封面静帧过目——有异议先改封面再放量，无异议继续；不加新停顿，复用首批分批落盘节奏（1025 实测：封面是审美重灾区，用户对封面主张最强，事后返工成本最高）。**

#### 5.2 图片素材收集（可选 — 仅封面用图）

**图片唯一出口是封面**；内容页一律无图——数据可视化走图表（chart-recipes），机制走图示（diagram-patterns）。不主动搜图。嵌入规则 → [references/image-handling.md](references/image-handling.md)

#### 5.3 即兴派生通道（四池与点名都不匹配时）

**触发条件**：用户明否全部候选预览，或主题气质明确超出 22 套（如"新能源数据复盘"要冷青工业感、22 套无一命中）。触发后先声明走即兴，再动手。

**派生规则（自由但有自证）**：

1. **五件套 + --warn 从主题派生**：底/墨/灰/金/线 + 语义辅助色按对主题色的理解选定（青主调配琥珀黄这类冷暖对撞是合法产物，机械派生得不到），**必须写一句配色理由**（这套主题为什么配这组色），写不出 = 退回四池
2. **装饰配方走词汇库**：[references/decoration-vocab.md](references/decoration-vocab.md) 两铁律（颜色一锅汤/装饰一套词）+ 词条选配，主签名 ≤2 种全片贯穿
3. **四列迁移协议**：每个自创元素填「元素/容器/token 名/机验归属」，任一列填不出 = 不许上（不许临时发明类名——孤儿类断言照跑；自创元素若沉淀为底盘组件，在定义块体首打 `@critical`/`@hook`/`@svg-text` 注册标记，机检自动跟——见 core.css 注册表注释）
4. **试排对冲（成本≈0）**：全量生成前，先用用户真实的最难一页（表格/长标题/图示）试排确认成立，再放量
5. **入册问句**：交付时问一句"这套配色要不要存进你的自定义预设？"——**客户拍板，不自动入册**；点头则按 decoration-vocab §八格式追加到项目 `.claude-design/custom-presets.md`。**5.0 开场顺带检查该文件**：存在则并入候选池（与 22 套白名单同级，点名直达）

### 阶段6：生成演示文稿（v2 排版内核）

**选定风格 → 映射到 v2 底盘 → 按大纲逐页生成。**

1. **底盘**：复制 chassis-v2.html（1920×1080 舞台 + token + 页骨架 + 边注四件套 + 翻页 JS）
2. **风格映射**：所选预设的色板 → 按 [references/style-presets.md](references/style-presets.md) 顶部《v2 五件套映射表》折算到 chassis 的 `--bg/--ink/--ink-dim/--accent/--hairline`（缺项走派生公式，禁自造色值）；字体按同文件《字体落地表》取**跨平台栈**（顺序固定：预设原名 → 平台替代 Win/macOS 双写 → 通用族兜底；**包内不带任何字体文件，字形随使用者机器**，用户想还原原版就自己装 OFL 字体）（结构永远 v2，颜色跟预设走；入场节奏映射到 `.rv` 的 `--d` 延迟编排——氛围快慢由延迟疏密表达，禁夸张弹跳）
   **装饰配方映射**：预设/即兴配方 → [references/decoration-vocab.md](references/decoration-vocab.md) 选主签名（默认 ≤2 种；风格配方声明更多时按配方走——如魔鬼绿 4 件：渐变+装置+圆弧+光晕，2026-10-25 松绑；全片贯穿一致性不放松：封面浓 `.deco` / 内容页淡 `.deco.dim` / 装置仅首尾 `.deco.soft`）。用装饰的页：slide 首子元素挂 `.deco` 容器，**其余内容全部包进 `.content`**（漏包 = 装饰压字）；不用装饰的页结构照旧。`--warn` 由预设指定（写配色理由）或留空退回 accent；数据汇报型主题封面可启用数字条变体（slide 挂 `.has-metrics` + `.cover-metrics`，三段式铁律见词汇库 §5.3）；封面构图总纲（hook / 装置 / 数字条 / 四步流程）见词汇库 §五
3. **逐页生成**：按大纲从 P1 到 PN 顺序，逐页过判定树选槽位（见下）；字号/间距只取 token 档；密度按大纲档位执行（超密度已在大纲砍掉）；**动画按 [references/animation-routing.md](references/animation-routing.md) 自动路由**——按阶段 1 内容侧重 + 阶段 5 氛围查套餐，给元素挂类名即生效（`.rv` 分层入场为默认主力），**不逐个问客户**
4. **讲稿**：每页 3-5 条提词卡要点（不写逐字稿）写入产物 JS 的 `NOTES` 对象（键=页 id）——S 演讲者模式备注卡读此数据源
5. **长 deck 分批落盘**（3-4 页/批防爆上下文），静默执行不弹窗
6. **数据页铁律**：趋势/构成/排行数据必须图表化（ECharts 走 [chart-recipes](references/chart-recipes.md)，或 CSS 条形），排成纯数字组 = 违规返工

#### 槽位判定树（从同一 token 派生，禁临时发明）

```
这页内容的逻辑是……
├─ 围绕论点的论据        → 行组（编号或标记+小标题+正文，无盒）★主力——前缀二选一：序列关系（步骤/排名）→.no 编号，非序列→.sh-mark 标记，禁双前缀（layout-rules §3.2b）；**步骤序列升格判断（1025 庆哥立）：内容量多且层级分明＋组间信息量接近＋版率饱和不显空，三者同满足 → 升格步骤卡**——卡不卡看内容性质，不看组数配额
├─ 二维对比              → 双栏对比（中缝发丝线，非卡片）
├─ 单个关键数字          → 焦点数字（一页一个，主从纵排：数字上说明下贴身）
├─ 量值并列（2-4 指标）  → metric 发丝线组（等宽栏，每栏实内容）
├─ 趋势/时序数据         → 【图表】折线/柱状——禁排纯数字组
├─ 构成/占比数据         → 【图表】堆叠条/环状，或 CSS 占比条
├─ 排行对比              → 【图表】横向条形（长度=值，数字右对齐）
├─ 过程/机制/流向        → 三问闸门（[anim-recipes](references/anim-recipes.md)§一）：全过且配额内 → 代码动画；否则 → 图示（[diagram-patterns](references/diagram-patterns.md) 基线参考；介质开放：CSS 组合块优先，SVG 仅精确绘制）
└─ 表格数据              → 表格（数字列 tabular-nums）
```

- 卡片由场合判断（2026-10-25 松绑，原配额管制致版面单调）：命中四场景（身份独立并列块 / 引用切出 / 选择性突出 / 异构视觉单元并列 → focus-judgment §二「结构辅助·卡片四场景」）即出卡，数量跟内容组数走、不设硬上限；连续叙事、行组够用的场合不出卡。形态跟随风格配方（纸感→顶线卡 `card` 三段式、黑底科技→玻璃淡卡、品牌预设点名→盒装 `card-box`），多卡 `.card-row` 锁等宽等高，全片形态唯一
- 主从二式：从属轻（单行，高度比 <0.3）纵排贴身；从属重（3-4 行，0.5-1）横排两翼
- 压轴行两形态：金句级 32px/600/左轴；普通收束 16px 灰；内容定形态
- 可忽略信息（来源/备注/页码/落款）→ 角落位，退出内容轴
- 数字排版全规则 → [references/number-typography.md](references/number-typography.md)（判位三分/三模式/大而重大而轻）

#### 阶段 6.5：机验（必跑）

- `scripts/measure-layout.js` 版率口径（探针强制可见防动画骗检、剔除边注四件套；已兼容 `.reveal` 系入场类，测任意外部产物同样适用；**装饰层 `.deco` 双口径排除**——装饰参与构图但版率不算数）+ **欠填口径 vacMax/vacBottom**（页高 10 带垂直占空：文本叶子+img/canvas/svg；**vacBottom≥4（底 40% 空）→ 先查页型**——密排/双栏页=欠填回白名单手段调，单焦点页（金句/焦点数字/封面）豁免（§1.4 留白配主角）；只提示不 FAIL（阈值人判）→ layout-rules §1.2b）
- `python scripts/crowd-probe.py <产物.html 绝对路径>` 拥挤探针（相对路径会 ERR_FILE_NOT_FOUND）：组内间距 <14px 贴死 / 文字重叠 / 正文级行高 <1.25——"行组内标题贴正文"类事故的专项机验（需 playwright + 系统 Chrome；缺 playwright 时打印 `[SKIP]` 跳过，不算产物问题；禁临时安装；跑不了须在交付说明里注明"这一关未验"）

**measure-layout 跑法**（注入型，直跑 node 会 window 未定义）：三步 PowerShell（注入探针→headless 渲染→读 REPORT:: 行）→ 真源 [references/layout-rules-v2.md](references/layout-rules-v2.md)《附：measure-layout 跑法》；Chrome 路径解析 → [references/offline-export.md](references/offline-export.md)

- 数字排版验收清单（number-typography.md R5 的断言清单）
- `python scripts/verify-consistency.py <产物>` 静态一致性断言（纯 Python 零依赖）。**单一报告制**：脚本只出问题清单、不做交付裁决——[严重] = 骨架完整性（S1-S8=骨架八断言组、348/349=数字排版断言，编号定义见脚本内注释）/ 孤儿组件类 / 强调容器形态数（>6 种）/ 缺 hl 卡片（>5 个）/ 内联字号 <11.5px（>10 处）/ 页间竖间距（>2 种；仅当生成端写了内联 gap 时生效，否则显示「统一」）/ 光晕配色 bug / 字号类变量悬空 / 封面标题字号覆盖 / 封面断言（视觉事件三选一——stamp 级数字 / .has-metrics+.cover-metrics / `.dv-` 装置标记，全缺 = 平庸封面；装饰词条对底色有效对比度 <1.1:1 = 隐身，仅当 deck 实际用了 `.deco` 对应词条才判；`.deco` 直接子元素 >2 件）/ 图表与图示规范 / 口径自洽，命中即 exit 1（=打回信号，逐项处理或说明理由后交付）；[提示] = 内联硬编码色、辅助色 tone、单列纵排、图示节点上限（D-3）、封面焦点让位梯度 / 巨型数字口径注缺失，以及上述「越线项未越线时」的计数提醒。处理决定权在生成端与使用者（旧 FAIL/HINT 两级裁决已降为信息分级，不再写任何计数文件）
- `python scripts/check-deck.py <产物>` 同类错误全扫（四类：hero-num 单位灰 / SVG 着色 / 文本 y 越界 / **字号档位**——合法档位 = 底盘内容层实有档位**自动提取** ∪ `var(--fs-*)` token ∪ 规则批准档位，改底盘加档白名单自动跟，无手工同步）——改稿轮次与交付前各跑一次；档位外的字号一律报，先判断是底盘漏搬还是规则漏收，不要为了过检删规则（同类错误全扫制的机验落点）
- **两套字号地板并存，别混用**：`22px` 是**设计地板**（正文级实际字号，排版规则，见 layout-rules-v2 §2.1）；机验里的 `11.5px` 是**内联覆盖地板**（只查 `style` 内联 `font-size`，防规则段漏搬）。11.5–22px 之间属「机验不管、靠人眼与 §2.1 兜」的灰区，交付前需自行用 measure-layout 复核
- 不达标回白名单手段调（换纵向/升字号/换轻容器/砍页），永不加填充物

### 交付

完成后自动打开完整 HTML（一次），聊天内附首屏截图作补充预览。

**PDF 导出（双出口）**：交付时问用户"要不要 PDF 版"；用户页面内也可按 **P 键**随时打印。导出命令、Chrome 路径解析（Windows 常不在 PATH）、headless 注意事项（独立 `--user-data-dir`）→ 真源 [references/offline-export.md](references/offline-export.md)。

---

## 包内文件（按需取用，勿整包读）

技能包加载三层：本文件常驻 → `references/` 对应阶段才读 → `assets/` 复制即用、`scripts/` 直接跑。
**先按下表「我要干什么」定位，不要按文件名猜，更不要整包读。**

| 我要干什么 / 遇到什么 | 读这个 |
|---|---|
| 判断这页该强调谁、怎么强调 | `references/focus-judgment.md` |
| 选风格（22 套） | `references/presets-index.md`（只读索引；正文 `style-presets.md` Grep 预设名直达，约 1700 行勿全读） |
| 查某套风格的色板/字体规格 | `references/style-presets.md` |
| 决定封面怎么构图 | `references/decoration-vocab.md` §五 封面构图总纲 |
| 挑装饰手法、查装饰踩坑 | `references/decoration-vocab.md` 词条表 + 踩坑记录 |
| 把数据变成图 | `references/chart-recipes.md` |
| 用图示讲结构 | `references/diagram-patterns.md`（可运行参考 `assets/diagram-gallery.html`：改 `--accent` 一值九图全变色，非交付模板） |
| 数字怎么排 | `references/number-typography.md` |
| 定标题字号与句式 | `references/title-copy-types.md` + `references/layout-rules-v2.md` §2.3 |
| 版率不达标 / 页面欠填 | `references/layout-rules-v2.md` §1.2–1.3 + 反噬防火墙 |
| 定间距 / 对齐 / 容器 | `references/layout-rules-v2.md` §3 |
| 阶段 6 前读规则全文 | `references/layout-rules-v2.md`（此场景必须读全文） |
| 提取 docx/pptx/PDF 素材 | `references/content-preparation.md`；`.pptx` 用 `scripts/extract-pptx.py`（需 python-pptx） |
| 优化文案、砍字并页 | `references/content-optimization.md` |
| 用户给了图（唯一出口是封面） | `references/image-handling.md` |
| 只改指定页、别的不动 | `references/iterative-edit.md` |
| 导出 PDF / 离线交付 | `references/offline-export.md` |
| 讲者窗口 / 备注卡 | `references/speaker-mode.md`（底盘已内置 S 键） |
| 动画怎么选 | `references/animation-routing.md`；机制页另见 `references/anim-recipes.md` |
| **依赖报错（Node / Chrome / playwright）** | 下节《依赖与失败场景》 |
| 阶段 6 底盘 | `assets/chassis-v2.html`（build 产物禁手改；源码在 `assets/chassis/` + `assets/modules/`） |
| 改底盘后重建 | `scripts/build-chassis.mjs`（需 Node） |
| 量版率 + 欠填 | `scripts/measure-layout.js`（需 Chrome） |
| 查拥挤（间距贴死 / 重叠 / 行高） | `scripts/crowd-probe.py`（需 playwright，缺则 SKIP） |
| 查产物四类断言 | `scripts/check-deck.py`（hero-num 单位灰 / SVG 着色 / 文本 y 越界 / 字号档位区间 8.4–176px） |
| 静态一致性断言 | `scripts/verify-consistency.py`（纯 Python；孤儿类 / 字号地板 / 骨架完整性 / 扫描基数自证） |
| 改解析器或 `effects.css` 后验全部 | `scripts/verify-all.py`（build 一致 + 正负样本闸 + 旧术语零命中 + deco 参数对齐） |

## 依赖与失败场景（缺什么会怎样）

三条依赖**缺了都不阻断出稿**，但要按下表处理，别让用户以为技能坏了。

| 依赖 | 什么时候才需要 | 缺了会怎样 | 怎么补 / 怎么跟用户说 |
|---|---|---|---|
| **Node.js** | 只有改底盘源码或功能件后重建 `chassis-v2.html` 时才需要；**生成幻灯片完全不需要** | `build-chassis.mjs` 跑不了，现有 `chassis-v2.html` 照常可用 | 无需补，对用户不必提 |
| **Chrome** | ① `measure-layout.js` 量版率 ② 导出 PDF | 版率机验打印 `[SKIP]` 跳过；PDF 改用手动「打印 → 另存为 PDF」（P 键） | Windows 下 Chrome 常不在 PATH，探测与配置见 `references/offline-export.md`；交付时说明「版率未机验，已人工核对」 |
| **playwright** | 只有 `crowd-probe.py` 拥挤探针用 | 打印「可选检查未启用」并 exit 0，**不判红、不阻断交付** | 可选增强，不装也能正常出稿；要启用就装 playwright |

**用户说了模糊指令怎么办**：「随便做一下」「你看着办」「简单弄一个」——**不要猜，也不要替他默认风格**。按阶段 1 四问收敛；用户仍不给方向时，给 3 个具体选项让对方点（例：「10 页汇报型 / 5 页概要型 / 20 页详版，选哪个」）。

## 自信执行规则

1. chassis-v2 与 style-presets 各读一次即可复用；跨会话续做或目录被改过必须重读
2. 槽位选择最多推翻一次，第二次用默认（行组）
3. 阶段内快速推进不停顿——**但每个阶段的用户确认点是硬停点，等答复不算停顿**
4. **上下文纪律**：素材不全量读、references 按需读、长 deck 分批写盘

## 治理

- 结构约定：`references/`（读进上下文的知识）、`assets/`（复制进产物）、`scripts/`（直接执行）、`samples/`（机验门禁：`good/chassis.html` 正样本兼补丁基座 + `patches.json` 负样本行级补丁，`build_samples.py` 现场生成、`expected.json` 给期望；**负样本不随包分发全文**，加负样本时 patches.json 与 expected.json 必须同步）四分类
- **README 同步闸**：凡轮次涉及 SKILL.md 结构性变更（流程/交互/目录/文件清单），轮次收尾必查 README.md 是否需同步——与「改完必跑 build-chassis」同级肌肉记忆（根因：README 曾停旧版 47 轮无人触发更新）
- **同类错误全扫制**：用户指出一处错误 → 修该处 → **立即全 deck/全包扫同类**（`python scripts/check-deck.py <产物>` 跑单位/SVG着色/y 越界/字号档位四类）→ 可断言的进机验。**主动决策不等指**：错误修复的半径由 AI 判断执行，不是用户揪一耳改一处
- **常驻落点规则（2026-10-26 立）**：新规则只有两种合法写法——必须常驻的行为约束 → NEVER 速查加一行（本体一句＋指针），其余一律落 `references/` 并在对应阶段加触发指针；**阶段正文禁内联事故原文/理由/松绑史**（参照原则 8「60% 反噬史禁令」形态，正文只留边界短语）。已内联的存量不动，等真实误判再处理

## 来源与许可

**上游**：本包基于 [Frontend Slides](https://github.com/zarazhangrui/frontend-slides)（作者 @zarazhangrui，MIT License）二次开发——部分风格预设的色板与字体、`scripts/extract-pptx.py` 取自该库。底盘 chassis-v2（1920×1080 固定舞台）、三层版面约束、七阶段引导与机验闭环为本包自有。阶段 3「内容优化」另参考 [女娲·Skill造人术](https://github.com/alchaincyf/nuwa-skill) 的 Steve Jobs 视角（MIT License）。

**本包**：© 2026 Hongqing W — 对外署名「庆哥聊AI」，MIT License。

> **许可声明（MIT 要求的声明正本）**：上游版权声明与 MIT 许可声明须随本包及其副本一并分发。`LICENSE` 为法律正本；若分发渠道不接受 `LICENSE` 文件，**以本节承担该声明**，不视为放弃许可条件。
>
> Copyright (c) 2025 Zara Zhang (original framework) ｜ Copyright (c) 2026 Hongqing W (v2 paradigm)
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies, subject to the condition that the above copyright notice and this permission notice be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.