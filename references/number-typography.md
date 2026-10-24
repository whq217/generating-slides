# 数字排版规则 — 数字与文本的对齐纪律

> 版本：2026-10-20 v4（v3 及以前已随 v1 存档废弃。v4 依《排版规则总集》三层体系重校：①字号绝对值全部换 1920×1080 舞台新量级（比例纪律不变）；②双档间距同步三档制；③B 式挂配重比检验；④槽位引用改 chassis-v2 判定树；⑤C1 卡盒降发丝线；⑥R1.5 口径收窄（349 断言同步）；⑦动画入 frame pre-printed 纪律）
> **画布前提：1920×1080 底盘**（chassis-v2）。所有字号绝对值按 1080 屏高制，换算旧 700 画布 ×0.65。
> 病根：数字包进色块（chip/方块）再与文本排在一起——色块按盒边界对齐、文本按基线对齐，**两套对齐系统打架**，永远对不齐；且默认比例数字"1"窄"8"宽，多列数字纵向参差。另一高频翻车：数字条与不相干容器强行同幅。
> 外部依据：Material Design 3（tabular numbers 用于数据扫读对齐）；KPI 卡业界共识（Ant Statistic / Harvard Stats Cards / Zebra BI：数字=视觉 hero、最大+semibold，标签约 1/3~1/2 字号）。
> 主题中立：颜色/字号走主题变量，规则只管结构与对齐。
> 机验：断言 349（数字上色块 / 缺 tabular-nums / 无内容支撑强行同幅）属**严重级**（命中即 exit 1 打回），另走 measure-layout 版率口径。

---

# 第一部分：规则

## R1 数字本身的纪律（四条铁律 + 宽度纪律）

1. **数字禁上色块**——数字不包 chip/方块/彩色底。强调手段三选一（每处只用一种）：角条（4×32px 色条）/ 细下划线（2px，宽 ≤ 数字宽）/ 整卡淡染（≤10% 透明度 tint）
2. **多数字并列必须等宽**——`font-variant-numeric: tabular-nums`（或 mono 字体）。表格列、指标卡组、排行列表一律生效；单个孤立数字可豁免
3. **数字左对齐为默认**——卡片内/列表内/表格内一律左对齐；**居中仅限一种情况**：单个数字独占页面焦点位（如 D-1 焦点数字、`.step.impact` 弹入的大数字）
4. **层级 ≥3:1，单位缩小挂尾**——数字 : 标签字号比 ≥3:1（新量级参考 92px : 16px——标签走 meta 档，**禁再出现 11.5px 级耳语标签**，1/61 屏高病的历史教训）；单位写法 `92<small style="font-size:0.4em">%</small>`，不与数字同大
5. **数字条宽度纪律（v4 口径收窄）**——禁的是**无内容支撑的强行同幅**：与下方容器同现且数量不匹配（如 2 数字 vs 3 卡）时禁拉成同幅；**等宽 metric 栏每栏有实内容（数字+标签）合法**（chassis-v2 `.metric{flex:1}` 即此形态）。断言 349a 口径同步收窄

## R2 数字与正文的组合：先判位，再选模式

**判定树：**

```
这个数字是……
├─ 数据（量值/比例/结果）→ 模式 A 或 B —— 数字当主角，大而重
├─ 序号（第几条/第几章）  → 模式 C —— 数字当装饰，轻而淡
├─ 标题句内的数字（"十年 60 秒：持志如心痛"）
│                         → 随标题样式，不套三模式（标题已是最高层级，
│                           多位数字开 tabular-nums 保宽即可）
└─ 封面标题位的数字 → 判角色三分（卖点/佐证/氛围）→ 主角式/高亮式/背景式
                          （见本节下方摘要：
                            卖点须过转述测试——听众会后转述会念出它吗；
                            高亮仅限标题句 ≤2 处；氛围数字垫底不进文本流）
```

**封面标题位数字·判角色三分（原《封面字体规范》§2.1a，2026-10-23 内联入包，包外原文不再作为依赖）**

| 角色 | 判据 | 排法 |
|---|---|---|
| 卖点 | 过**转述测试**：听众会后会主动念出它吗 | 主角式：与标题同轴、数字独立成行 |
| 佐证 | 支撑标题里的结论，不抢主位 | 高亮式：句内上色，**全篇 ≤2 处** |
| 氛围 | 只是背景纹理 | 背景式：垫底、低透明度，**不进文本流** |

排别扭的病例，八成是判位判反了：把序号排成主角（01 抢了标题的戏），或把数据排成装饰（71.7% 缩成小角标）。

**三模式：**

| 模式 | 结构 | 适用 |
|---|---|---|
| **A 上下式**（stat headline） | 大数字在上，正文紧贴在下 | 单个关键数据需要展开解释——报告正文页、论证页 |
| **B 左右式**（数字锚点） | 数字占左窄栏 25~30%，正文占右 70% | 数字短（≤4 字符）+ 正文长；多组并列时（重复成阵列） |
| **C 编号章节式**（editorial numbering） | 序号淡排在标题上方/左侧，真标题+正文在下 | 并列章节、方法论列表 |

**B 式阵列与排行条形的边界**：需要排序比较（条形长度=值）→ 横向条形图表（chart-recipes 排行配方）；并列陈述不排序 → B 式阵列。

## R3 组合模式四细则（A/B/C 都必须过）

1. **亲密性是命门（三档制语言）**：数字和它的正文/标签是一个组——**组内（数字↔标签/正文）14-18px，数字块与数字块之间（板块间）64-72px**；多层结构按"档位跟层级树走"（layout-rules-v2 §3.3），禁等距
2. **对齐挂锚**：A 式数字左缘=正文左缘；B 式两栏各挂网格线且 `align-items: baseline`（正文首行与数字基线对齐——治"两套对齐系统打架"的关键一行）；C 式序号可与标题同轴或悬挂
3. **比例悬殊**：数据数字 : 正文 = 4:1~5:1（新量级：88~120px 配 22~24px 正文）；C 式序号可大但视觉重量轻（细字重 200 + 透明度 0.2~0.4——"大而轻"与 A 式"大而重"是字重轴两极）
4. **说明标签不插队**：eyebrow 标签放数字**上方**或右侧，绝不插在数字和正文中间；eyebrow ≤8 字、正文块 ≤2 句

与 R1.4 的关系（不冲突）：3:1 管"数字:耳语标签"（指标位），4:1~5:1 管"数字:正文"（标题块）——正文大于标签，比例自然更大。

## R4 场景矩阵（数字位全景）

| 场景 | 排法 | 对齐 |
|---|---|---|
| 焦点大数字（一页一个） | **140~176px**（低密度页主角，字号补偿撑版面），可居中 | 居中允许（唯一豁免） |
| 指标组（metric 行） | 发丝线式 metric（→ C1，chassis-v2 `.metric`），数字左对齐+等宽+`flex:1` 等宽栏 | 左 |
| 表格数字列 | `tabular-nums` + 右对齐或小数点对齐（整数列右对齐，带单位列左对齐） | 按列统一 |
| 排行列表 | 等宽数字，数字列纵向右对齐，条形长度=值 | 数字右、标签左 |
| 行内数字（正文句中） | 不加粗不放大不染色（加粗是标题句特权；染色是链接的惯例含义——NN/g 链接可视化规范。标题句内数字可高亮 → R2 判定树下方摘要·高亮式），与正文同号 | 随文本 |
| 数字+单位 | 单位缩小挂尾（0.4em），不空格分写 | — |
| 数字做标题 | 判位三分 → R2 三模式 | → R3 |
| 封面标题位数字 | 判角色：卖点（转述测试）/ 佐证（高亮 ≤2）/ 氛围（垫底）→ R2 判定树下方摘要·三模式 | → R2 |

**B 式补充判定（v4）**：模式 B 左右式属"横排论证结构"（数字锚+正文展开），不是主从——须过两翼配重比检验（高度比 0.5-1，layout-rules-v2 §1.5）：新量级下（88-120px 数字配 2-3 行 22-24px 正文）天然达标；正文仅单行时改 A 式纵排。

## R5 验收清单

- 全 deck 无"数字在色块上"（机验 349c）
- 表格数字列/指标组 `tabular-nums`（机验 349b）
- 数字条无"无内容支撑强行同幅"（机验 349a，v4 收窄口径）
- 数字 : 标签字号比 ≥3:1 且标签 ≥16px meta 档（抽 3 处量）
- 居中数字仅出现在焦点位（一页 ≤1 个）
- 单位全部缩小挂尾
- 组合模式四问：组内间距明显小于块间距（14-18 vs 64-72）？数据数字 ≥4 倍正文？序号够轻？eyebrow 没插队？

## R6 与既有体系的关系（指针网 v4）

- 排版总纲：**[layout-rules-v2.md](layout-rules-v2.md)**（三层结构）——本文是"数字位"在第二/三层下的细则
- 底盘与槽位：[assets/chassis-v2.html](../assets/chassis-v2.html)（`.metric`/`.hero-num`/`.row .no` 已按本规则预置）
- 焦点判型：SKILL.md 核心原则（数字是焦点 → 焦点数字槽位；标题与主角互斥）
- 动画：frame pre-printed 纪律（chassis-v2 `.rv` + `--d` 延迟入场），数字弹入统一克制 fade-up，禁 zoom-pop 式夸张弹跳
- 字数联动：标签 ≤6 字、eyebrow ≤8 字（content-optimization 3.2）
- 图表联动：ECharts 数值轴"从 0 起 + 等宽"（chart-recipes §4）
- 封面数字位：标题分型三模式（主角式/高亮式/背景式）+ 转述测试 → R2 判定树下方摘要（原《封面字体规范》§2.1a，已内联入包）
- 机验：scripts/measure-layout.js（版率口径）

---

# 第二部分：案例（挂在规则下，可直接贴）

## C1 metric 发丝线配方（v4：卡盒降发丝线，hairlines over boxes）→ 支撑 R1.2/3/4、R4 指标组

```
─────────────────────   ← border-top 发丝线（组间身份），非卡盒
92%                    ← 大数字：等宽、左对齐、600 字重
技能相关度 · 教培→心理咨询  ← 标签：16px meta 档，小 5 倍以上
```

```css
.metric { flex: 1; border-top: 1px solid var(--hairline); padding-top: 18px; }
.metric .mv {
    font-family: var(--font-serif);
    font-size: 92px;                /* 1080 舞台；主题可在 72~96px 内调 */
    font-weight: 600;
    font-variant-numeric: tabular-nums;
    line-height: 1;
    color: var(--ink);
    text-align: left;
}
.metric .mv small { font-size: 0.4em; font-weight: 400; opacity: 0.6; margin-left: 2px; }
.metric .md {
    font-size: 16px;                /* meta 档，禁回 11.5px */
    letter-spacing: 0.1em;
    color: var(--ink-dim);
    margin-top: 14px;
}
/* 强调三选一仍可用：角条/细下划线/整组淡染（禁色块包数字） */
```

## C2 模式 A 上下式 stat headline → 支撑 R2 模式 A

```html
<div class="num-block">
    <div class="num-eyebrow">峰值扩容费用</div>
    <div class="num-headline">3.7<small>倍</small></div>
    <p class="num-body">大促期间峰值扩容费用可达日常的 3.7 倍，缓存命中率仅 41%，低于行业基准 65%。</p>
</div>
```

```css
.num-block { max-width: 1100px; }             /* 正文限宽 ≈45 中文字 */
.num-eyebrow { font-size: 16px; letter-spacing: 0.14em; color: var(--ink-dim); margin-bottom: 10px; }
.num-headline {
    font-size: 96px; font-weight: 600; line-height: 1;
    font-variant-numeric: tabular-nums; color: var(--ink);
    margin-bottom: 14px;                      /* 组内紧（档3） */
}
.num-headline small { font-size: 0.4em; opacity: 0.6; margin-left: 2px; }
.num-body { font-size: 24px; line-height: 1.7; color: var(--ink-dim); }  /* 4:1 比例 */
.num-block + .num-block { margin-top: 64px; } /* 板块间（档1） */
```

## C3 模式 B 左右式数字锚点 → 支撑 R2 模式 B、R3.2 基线对齐

```html
<div class="num-anchor-row">
    <div class="num-anchor">280<small>万</small></div>
    <p class="num-anchor-body">每年多支出的扩容费用，相当于两条产线的年维护成本。</p>
</div>
```

```css
.num-anchor-row {
    display: grid;
    grid-template-columns: 30% 1fr;          /* 数字窄栏 */
    gap: 48px; align-items: baseline;        /* 基线对齐：治两套对齐打架 */
    padding: 22px 0;
}
.num-anchor-row + .num-anchor-row { border-top: 1px solid var(--hairline); }
.num-anchor {
    font-size: 88px; font-weight: 600; line-height: 1;
    font-variant-numeric: tabular-nums;
    color: var(--accent); text-align: left;
}
.num-anchor small { font-size: 0.4em; opacity: 0.6; }
.num-anchor-body { font-size: 24px; line-height: 1.6; color: var(--ink-dim); }
/* 配重检验：88px 数字配 2-3 行 24px 正文（高 115-154px）≈ 0.5-1 带内 ✓；正文仅单行时改 A 式纵排 */
```

## C4 模式 C 编号章节式 → 支撑 R2 模式 C、R3.3 序号轻处理

```html
<div class="chapter-item">
    <div class="chapter-num">01</div>
    <div>
        <h3 class="chapter-title">砍字不缩字</h3>
        <p class="chapter-body">页面装不下就砍内容或拆页，绝不缩小字号硬塞。</p>
    </div>
</div>
```

```css
.chapter-item {
    display: grid;
    grid-template-columns: 110px 1fr;
    gap: 32px; align-items: start;
}
.chapter-num {
    font-size: 72px; font-weight: 200;       /* 极细字重=轻（"大而轻"） */
    line-height: 1; color: var(--accent);
    opacity: 0.35;                            /* 透明度 0.2~0.4=装饰感 */
    font-variant-numeric: tabular-nums;
}
.chapter-title { font-size: 30px; font-weight: 600; color: var(--ink); margin-bottom: 8px; }
.chapter-body { font-size: 24px; line-height: 1.6; color: var(--ink-dim); }
.chapter-item + .chapter-item { margin-top: 64px; }
```

要点：序号"大而轻"（大字号+细字重+低透明度三件套）——和 A 式"大而重"（600 字重+主文字色）方向相反。

---

## 验收速查（30 秒版）

1. 扫每页：有没有数字被包在色块/方块里？→ 有即打回
2. 看表格/指标组：数字列纵向齐不齐？不齐=没开 tabular-nums
3. 看居中数字：是不是一页最多一个、且真在焦点位？
4. 看单位：%、万、亿 是不是比数字小一号挂着？
5. 看数字条：宽度是按内容收缩还是被拉满整行强行对齐卡片组？
6. 看数字标题块：块内间距明显小于块间距？数据 ≥4 倍正文？序号够轻？eyebrow 没插队？
