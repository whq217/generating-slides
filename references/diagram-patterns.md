# Diagram Patterns — 九种结构图示配方（G 系列）

> **加图前必过的一问：删掉这个图，读者会丢文字补不回来的信息吗？——不会就不加图。**
> 定位：内容页图片已砍（唯一出口是封面），无数据页（观点/架构/方法论）的视觉主力。总路由：**有数据走 [chart-recipes.md](chart-recipes.md)，无数据走本库，过程走动画**（静态版即 G-01 管线）。

## 目录

§1 公共约定（§1.1 两档配色 → §1.2 变量补充段 → §1.3 class 契约）→ §2 九个配方（G-01 管线流 / G-02 分层栈 / G-03 2×2 矩阵 / G-04 时间线 / G-05 中心辐射 / G-06 对比表 / G-07 漏斗 / G-08 同心环 / G-09 韦恩）→ §3 触发矩阵 → §4 本地化约束 → §5 图标规范 → §6 验收指针

高频入口：无数据页选型 → §3 触发矩阵；配色两档 → 本文首节；断言 D-2/D-3 口径 → §4/§6。可运行参考：[../assets/diagram-gallery.html](../assets/diagram-gallery.html)。

## §1 公共约定

> 三个公共段（配色 / 变量 / class 契约）在动任何配方之前先读——它们决定图形能不能跟着主题翻面。

### §1.1 两档配色（先选档）

| 档 | 判定 | 参数 | 主推预设 |
|---|---|---|---|
| **商务档（默认）** | 受众是评审/领导/甲方 | `--g-glow:0`、`--g-bar:3px`、`--g-line:1.5px`、只用 accent 单色系 | Business Blue / Swiss Modern / Stripe Professional |
| 技术档 | 受众是开发者/技术发布会 | `--g-glow:12px`、`--g-bar:6px`、`--g-line:2px`、五色可用 | Terminal Green / Linear Dark / MongoDB / 8-Bit Orbit |

### §1.2 变量补充段（用时粘进产物 `:root`，chassis 不预置；**漏粘本节变量的产物，图示淡底会退化为透明**）

```css
:root {
  --g-glow: 0;         /* 技术档 12px；商务档 0（辉光在亮色/纸感主题上最违和） */
  --g-bar: 3px;        /* 分层栈左缘彩条；技术档 6px */
  --g-line: 1.5px;     /* 连线/描边；技术档 2px */
  --g-node-radius: 6px;
  --g-tone-1: var(--accent);                       /* 主强调 */
  --g-tone-2: var(--accent2, var(--accent));        /* 辅助色 */
  --g-tone-3: color-mix(in srgb, var(--accent) 70%, #fff);  /* 提亮档 */
  --g-tone-4: color-mix(in srgb, var(--accent) 55%, #000);  /* 压暗档，仅负向语义 */
  --g-tone-5: color-mix(in srgb, var(--accent) 40%, #fff);  /* 淡档 */
  --accent2: var(--accent);   /* v2 底盘无第二强调色：默认与 accent 同值；预设点名第二色时覆盖 */
  --accent-light: color-mix(in srgb, var(--accent) 8%, transparent);  /* 图示淡底（G-05/06/07 专用） */
}
```

### §1.3 class 契约（断言靠它落地，所有配方共用）

| 类名 | 含义 |
|---|---|
| `.g-canvas` + `.g--<mode>` | 图示外层容器（两类同元素，mode 见各配方） |
| `.g-node` | 单个节点/步骤/卡片（全模式统一） |

```css
/* === 图示公共段（用时粘进产物 <style>；v2 token 版 2026-10-22）=== */
.g-canvas { display: flex; align-items: stretch; gap: var(--s-in); }
.g-canvas .g-node {
  background: color-mix(in srgb, var(--ink) 4%, transparent);
  border: 1px solid var(--hairline);
  border-radius: var(--g-node-radius); padding: 18px 20px;
  box-shadow: 0 0 var(--g-glow) color-mix(in srgb, var(--accent) 35%, transparent);
}
.g-canvas .g-title { font-size: 24px; font-weight: 600; color: var(--ink); }
.g-canvas .g-desc  { font-size: 22px; color: var(--ink-dim); line-height: 1.5; }  /* 22px=字号地板档 */
/* SVG 图示公共类（fill 必须显式写：SVG 文本不吃 CSS 继承） */
.g-canvas svg .i-faint   { fill: currentColor; opacity: 0.08; }
.g-canvas svg .i-stroke  { fill: none; stroke: currentColor; stroke-width: var(--g-line); }
.g-canvas svg text       { font-family: var(--font-sans); fill: var(--ink); }
.g-canvas svg .i-label    { font-size: 24px; font-weight: 600; fill: var(--ink); }
.g-canvas svg .i-label-sm { font-size: 20px; fill: var(--ink-dim); }
```

## §2 九个配方

> 九个配方的可运行参考实现见包内 [assets/diagram-gallery.html](../assets/diagram-gallery.html)（本地打开即看，改 `:root` 变量可预览换色/两档切换；非交付模板）。

### G-01 管线流 `g--pipeline`（配方变体）

**触发**：顺序过程、数据处理链、审批流。**反触发**：阶段并行或无序（那是 G-05）；要"动"转动画 Stepper。**上限**：≤5 节点。

```html
<div class="g-canvas g--pipeline">
  <div class="g-node" style="flex:1;border-top:3px solid var(--g-tone-1)">
    <div class="g-title">① 采集</div><div class="g-desc">多源数据接入</div></div>
  <div class="g-arrow" aria-hidden="true">→</div>
  <div class="g-node" style="flex:1;border-top:3px solid var(--g-tone-2)">
    <div class="g-title">② 清洗</div><div class="g-desc">去重补缺归一</div></div>
  <div class="g-arrow" aria-hidden="true">→</div>
  <div class="g-node" style="flex:1;border-top:3px solid var(--g-tone-3)">
    <div class="g-title">③ 建模</div><div class="g-desc">特征与训练</div></div>
  <div class="g-arrow" aria-hidden="true">→</div>
  <div class="g-node" style="flex:1;border-top:3px solid var(--g-tone-1)">
    <div class="g-title">④ 交付</div><div class="g-desc">接口输出</div></div>
</div>
```
```css
.g--pipeline { flex-direction: row; }
.g--pipeline .g-arrow { align-self: center; color: var(--g-tone-1);
  font-size: 22px; font-weight: 700; padding: 0 2px; }
```
色彩递进=方向感，读者不读字也能看出流向。

### G-02 分层栈 `g--stack`（新布局入口）

**触发**：依赖层级（UI→API→数据→设施）、抽象层级。**反触发**：横向沟通的关系（图不是栈）。**上限**：≤4 层。

```html
<div class="g-canvas g--stack" style="flex-direction:column;gap:8px;width:100%">
  <div class="g-node g-layer" style="--layer:var(--g-tone-1)">
    <div class="g-title">L4 · 应用层</div><div class="g-desc">门户与移动端</div></div>
  <div class="g-node g-layer" style="--layer:var(--g-tone-2)">
    <div class="g-title">L3 · 服务层</div><div class="g-desc">微服务与网关</div></div>
  <div class="g-node g-layer" style="--layer:var(--g-tone-3)">
    <div class="g-title">L2 · 数据层</div><div class="g-desc">库仓与消息队列</div></div>
  <div class="g-node g-layer" style="--layer:var(--g-tone-5)">
    <div class="g-title">L1 · 设施层</div><div class="g-desc">算力网络与安全</div></div>
</div>
```
```css
.g--stack .g-layer { border-left: var(--g-bar) solid var(--layer, var(--g-tone-1));
  border-top: none; }
```
左缘彩条是承重视觉——不用箭头也能读出层级。**禁止内联写死彩条颜色**（D-2 会打回），一律走 `--layer` 变量。

### G-03 2×2 矩阵 `g--matrix`（补象限画法）

**触发**：两个正交维度的分类决策（风险×影响、价值×成本）。**反触发**：只有一个变量（写列表）；2 东西 2 维度（写散文）。**上限**：2×2 封顶。

```html
<div class="g-canvas g--matrix" style="display:grid;
     grid-template-columns:auto 1fr 1fr;grid-template-rows:1fr 1fr auto;gap:10px">
  <div class="g-axis" style="writing-mode:vertical-rl;transform:rotate(180deg)">影响度 →</div>
  <div class="g-node" style="border-top:3px solid var(--g-tone-3)"><div class="g-title">观察</div><div class="g-desc">低影响低成本</div></div>
  <div class="g-node" style="border-top:3px solid var(--g-tone-1)"><div class="g-title">重点投入</div><div class="g-desc">高影响低成本</div></div>
  <div></div>
  <div class="g-node" style="border-top:3px solid var(--g-tone-5)"><div class="g-title">放弃</div><div class="g-desc">低影响高成本</div></div>
  <div class="g-node" style="border-top:3px solid var(--g-tone-2)"><div class="g-title">排期</div><div class="g-desc">高影响高成本</div></div>
  <div></div>
  <div class="g-axis" style="grid-column:2/4;text-align:center">投入成本 →</div>
</div>
```
```css
.g--matrix .g-axis { font-size: 20px; color: var(--ink-dim);
  letter-spacing: 0.1em; align-self: center; text-align: center; }
```
象限命名用含义不用坐标——"重点投入"胜过"高影响低成本"。

### G-04 时间线 `g--timeline`（配方变体）

**触发**：有时序的事件（事故、路线图、版本史）。**反触发**：顺序无关（列表即可）。**上限**：≤5 钉。

```html
<div class="g-canvas g--timeline" style="flex-direction:column;padding:8px 0 0">
  <div class="g-axisline" aria-hidden="true"></div>
  <div style="display:flex;gap:12px">
    <div style="flex:1;text-align:center">
      <div class="g-when">2024 Q1</div><div class="g-pin" style="background:var(--g-tone-1)"></div>
      <div class="g-node"><div class="g-title">立项</div><div class="g-desc">需求冻结</div></div></div>
    <div style="flex:1;text-align:center">
      <div class="g-when">2024 Q3</div><div class="g-pin" style="background:var(--g-tone-4)"></div>
      <div class="g-node"><div class="g-title">预警</div><div class="g-desc">延期两周</div></div></div>
    <div style="flex:1;text-align:center">
      <div class="g-when">2025 Q1</div><div class="g-pin" style="background:var(--g-tone-2)"></div>
      <div class="g-node"><div class="g-title">上线</div><div class="g-desc">全量发布</div></div></div>
  </div>
</div>
```
```css
.g--timeline { position: relative; }
.g--timeline .g-axisline { position: absolute; top: 40px; left: 4%; right: 4%; height: var(--g-line);
  background: linear-gradient(90deg, var(--hairline), var(--g-tone-1), var(--hairline)); }
.g--timeline .g-when { font-size: 20px; color: var(--ink-dim); margin-bottom: 6px; }
.g--timeline .g-pin { width: 12px; height: 12px; border-radius: 50%;
  border: 2px solid var(--bg); margin: 0 auto 10px; }
```
钉色语义：accent=常规、压暗档=异常/预警、辅色=里程碑。

### G-05 中心辐射 `g--radial`（同构删条目）

**触发**：一核心连 N 并行物（平台+能力、taxonomy）。**反触发**：关系是顺序的（G-01）；spokes >4 改表格。**上限**：≤4 spokes。

```html
<div class="g-canvas g--radial" style="display:grid;
     grid-template-columns:1fr 1.3fr 1fr;grid-template-rows:1fr 1fr;gap:12px;align-items:center">
  <div class="g-node"><div class="g-title">获客</div><div class="g-desc">渠道与线索</div></div>
  <div class="g-node g-hub"><div class="g-title">数据中台</div><div class="g-desc">统一资产与服务</div></div>
  <div class="g-node"><div class="g-title">风控</div><div class="g-desc">授信与反欺诈</div></div>
  <div class="g-node"><div class="g-title">运营</div><div class="g-desc">活动与留存</div></div>
  <div></div>
</div>
```
```css
.g--radial .g-hub { border: var(--g-line) solid var(--g-tone-1);
  background: var(--accent-light, color-mix(in srgb, var(--accent) 8%, transparent)); text-align: center; padding: 20px 16px; }
```
hub 占中心格本身就读出辐射关系，不需要连线；≥5 spokes 说明结构不适合辐射，改对比表。

### G-06 对比表 `g--compare`（配方变体）

**触发**：N 选项 × M 标准的评估选型。**反触发**：2 选项 2 标准（散文/并列卡）。**上限**：行 ≤4 × 列 ≤5。

```html
<div class="g-canvas g--compare" style="display:block;width:100%">
  <table class="g-table">
    <thead><tr><th>方案</th><th>初始成本</th><th>年运维</th><th>风险</th><th>结论</th></tr></thead>
    <tbody>
      <tr class="g-hi"><td><strong>自建</strong></td><td>340 万</td><td>180 万</td><td>团队缺口</td>
        <td><span class="g-badge g-yes">采纳</span></td></tr>
      <tr><td>采购 SaaS</td><td>120 万</td><td>260 万</td><td>数据出境</td>
        <td><span class="g-badge g-hold">备选</span></td></tr>
      <tr><td>混合</td><td>210 万</td><td>200 万</td><td>双头管理</td>
        <td><span class="g-badge g-no">排除</span></td></tr>
    </tbody>
  </table>
</div>
```
```css
.g--compare .g-table { width: 100%; border-collapse: collapse; font-size: 22px; }  /* 正文地板档；380 高放不下就删列拆页，不缩字号 */
.g--compare th { font-size: 22px; color: var(--ink-dim); font-weight: 600;
  text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--hairline); }
.g--compare td { padding: 8px 10px; border-bottom: 1px solid var(--hairline); }
.g--compare .g-hi { background: var(--accent-light, color-mix(in srgb, var(--accent) 8%, transparent)); }
.g--compare .g-badge { font-size: 20px; padding: 2px 10px; border-radius: 999px; }
.g--compare .g-yes { background: var(--g-tone-1); color: var(--bg); }
.g--compare .g-hold { border: var(--g-line) solid var(--g-tone-2); color: var(--g-tone-2); }
.g--compare .g-no  { border: var(--g-line) solid var(--hairline); color: var(--ink-dim); }
```
推荐行用底色+徽章，不只打星号。数字带论据（"340 万"胜过"成本中等"），遵守内容红线①。

### G-07 漏斗 `g--funnel`（新布局入口）

**触发**：逐级收敛（销售管线、筛选漏斗）。**反触发**：阶段不收敛（那是 G-01）。**上限**：≤4 级。

```html
<div class="g-canvas g--funnel" style="flex-direction:column;align-items:center;gap:8px;width:100%">
  <div class="g-node" style="width:100%;text-align:center">
    <div class="g-title">线索 · 12,400</div><div class="g-desc">全量 100%</div></div>
  <div class="g-node" style="width:78%;text-align:center">
    <div class="g-title">商机 · 3,100</div><div class="g-desc">转化 25%</div></div>
  <div class="g-node" style="width:56%;text-align:center">
    <div class="g-title">报价 · 930</div><div class="g-desc">转化 30%</div></div>
  <div class="g-node g-final" style="width:36%;text-align:center">
    <div class="g-title">成交 · 341</div><div class="g-desc">整体 2.8%</div></div>
</div>
```
```css
.g--funnel .g-final { border: var(--g-line) solid var(--g-tone-1);
  background: var(--accent-light, color-mix(in srgb, var(--accent) 8%, transparent)); }
```
**每级必标转化率**，故事在比例里不在绝对数里。

### G-08 同心环 `g--rings`（同构删条目）

**触发**：分层防御、信任层级、渐进深度——"外护内"语义。**反触发**：无该语义（改 G-05 或表格）。**上限**：≤4 环。

```html
<div class="g-canvas g--rings" style="justify-content:center">
  <svg viewBox="0 0 400 200" style="color:var(--g-tone-1);max-width:520px" role="img" aria-label="四层同心环">
    <circle class="i-faint" cx="200" cy="100" r="90"/>
    <circle class="i-faint" cx="200" cy="100" r="65"/>
    <circle class="i-faint" cx="200" cy="100" r="40"/>
    <circle cx="200" cy="100" r="18" fill="currentColor" opacity="0.25"/>
    <circle class="i-stroke" cx="200" cy="100" r="18" stroke-width="2"/>
    <text class="i-label-sm" x="296" y="104">边界防护</text>
    <text class="i-label-sm" x="271" y="104">检测响应</text>
    <text class="i-label-sm" x="246" y="104">身份权限</text>
    <text class="i-label" x="200" y="105" text-anchor="middle">核心数据</text>
  </svg>
</div>
```
由外向内=防护递进；标签放环右侧逐层内收，与半径对齐。

### G-09 韦恩 `g--venn`（新布局入口）

**触发**：集合交叠是论点本身（能力交叉区、复合定位）。**反触发**：交集无意义（改 G-03 矩阵）。**上限**：两集合（三集及以上投影不可读）。

```html
<div class="g-canvas g--venn" style="justify-content:center">
  <svg viewBox="0 0 400 200" style="color:var(--g-tone-2);max-width:520px" role="img" aria-label="两集合交集">
    <circle class="i-stroke" cx="150" cy="100" r="78" stroke-width="2" opacity="0.7"
      style="stroke:var(--g-tone-1)"/>
    <circle class="i-stroke" cx="250" cy="100" r="78" stroke-width="2" opacity="0.7"/>
    <path d="M 200,100 m -38,0 a 38,38 0 1,0 76,0 a 38,38 0 1,0 -76,0"
      fill="currentColor" opacity="0.2"/>
    <text class="i-label" x="105" y="105" text-anchor="middle">工程能力</text>
    <text class="i-label" x="295" y="105" text-anchor="middle">业务理解</text>
    <text class="i-label-sm" x="200" y="105" text-anchor="middle"
      style="fill:var(--ink);font-weight:700">解决方案力</text>
  </svg>
</div>
```
交集区是重点：唯一加填充的区域，语义命名（"解决方案力"）而非"A∩B"。

## §3 触发矩阵（内容信号 → 去处）

**直接落图示（3 个新入口，进阶段 6 槽位判定树的「图示」分支）：**

| 内容信号 | 路由 |
|---|---|
| 架构 / 技术栈 / 依赖层级 | **G-02**（`g--stack`） |
| 从 N 收敛到 / 转化率 / 漏斗 | **G-07**（`g--funnel`） |
| 交叉 / 交集 / 兼具 / 复合 | **G-09**（`g--venn`） |

**挂在内容槽位下画（6 个：先按判定树选槽位，再用本库配方画法）：**

| 内容信号 | v2 落点（槽位） | 配方 |
|---|---|---|
| 依次 / 步骤 / 阶段 / 流程 | 行组（`.row`）纵向序列 | G-01 |
| 时间点 / 里程碑 / 事件 / 演进 | 行组 或 图示占位 | G-04 |
| 以 X 为核心 / 围绕 / 支撑 N 大能力 | 行组 + 中心块 | G-05 |
| 对比 / 选型 / N 方案 × 量化标准 | 表格（数字列 tabular-nums） | G-06 |
| 两个维度 / 四象限 / 优先级矩阵 | 图示（独占内容区） | G-03 |
| 防线 / 层级保护 / 纵深 | 图示（独占内容区） | G-08 |

数字间关系（占比/趋势/对比/偏差/排序/相关）→ [chart-recipes.md](chart-recipes.md)。

## §4 本地化约束（全图通用）

1. **配色只走 token**：图形配色一律 `var(--g-tone-*)` / `var(--accent*)`，禁止图内写死色值——换主题图形不翻车；
2. **画布预算**：图示区高度 ≤380px（焦点槽标准）；宽度跟随布局分栏；
3. **节点上限**：管线/时间线 ≤5、辐射 ≤4、矩阵 2×2、漏斗 ≤4、对比表 ≤4×≤5——超限拆页或改表格（接密度预检）；
4. **中文标签**：节点标签 ≤8 字、图例/轴标 ≤6 字，超过先提炼（接文字提炼规则）；
5. **零外链**：图示一律纯 CSS/SVG 内联实现；ECharts 只在用户明确要求「可交互图表」时启用，且必须内联 `echarts.min.js`——任何 CDN 引用都等于交付失败；
6. **静态优先**：默认静态图（打印/PDF 友好），动画版仅核心论点页且占动画配额。

**反触发三条通用**：所在卡片已有 ≥100 字正文不加图；同页已有 2 个视觉组件不加第三个；纯数字论点用 stat 卡不用图。

## §5 图标规范

**本包零图标字体**（不引图标字体库、不引 CDN）。图标只用三种原生手段：① 底盘 `.sh-mark` 系列（实心竖块 / dash / 色点 / 空心框）；② SVG 内联 `path`（线性，`stroke` 走 `var(--ink-dim)`）；③ 纯色几何块 / 色点。全 deck 二选一不混用；同组图标视觉等重；色走主题变量；图标只作辅助语义（管线每阶段一个、辐射每个 spoke 一个），不替代文字标签。

## §6 验收指针

图示断言 D-2/D-3（`.g-*` 块内写死色值 / 节点上限）由 `scripts/verify-consistency.py` 承担：D-2 为硬打回项（命中即 exit 1），D-3 为提示（经验阈值，不拦交付）。**图示区高度 ≤380px（§4.2）与「加图四问」为人工纪律，静态正则拿不到渲染高度，不设机验**（如需机验，走 crowd-probe 的 playwright 通道另立 D-1，不在本轮范围）。加图四问自查（源 illustration-patterns 质量测试）：信息量（删图丢信息吗）/ 标签真实（无占位符）/ 克制（≤8 个标注元素、描边 1.5-2px）/ 不溢出（加图后过密度判据）。