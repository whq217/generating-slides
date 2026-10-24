# Chart Recipes — 六类数据图表可复制模板

> **用途**：查"我要表达什么关系" → 拿到 SVG 骨架（v2 主路径，照抄即得生长动画）或 ECharts option（例外路径）→ 改数据。
> **前置规则（2026-10-22 v2 化）**：① 容器一律 `.chart`（手写 SVG；底盘已接 `.bar/.line/.dot` 生长动画，零 JS）；② **任何情况下禁止 CDN/外链**——ECharts 仅在用户明确要求"可交互图表"时启用，且必须把 `echarts.min.js` 内联进产物，违者等于毁掉"双击即放映"；③ SVG / option 内禁止写死 hex，一律取 v2 token：`--ink`（主文字）/`--ink-dim`（次级）/`--accent`（强调）/`--line-struct`（网格轴线等结构线，≥3:1 投影可见；`--hairline` 只做装饰分隔禁用于结构，0-23 切换）/`--font-serif`（数字衬线）/`--font-sans`（正文字体栈）。**SVG fill 优先级铁律（0-24 svgprobe 实测）：呈现属性最低——元素挂的类里若有 fill 规则（.cy/.cv 等），`fill="…"` 属性（var 或 hex）一律被静默覆盖；要元素级覆写只能写 `style="fill:…"`（内联声明赢）。类没有 fill 规则时（.bar），`fill="var(--accent)"` 合法生效。机检口径：有 fill 属性 + 挂了定义 fill 的类 + style 无 fill → 报。**

## 两档配色（先选档，再查表）

| 档 | 判定 | 参数倾向 | 主推预设 |
|---|---|---|---|
| **商务档（默认）** | 受众是评审/领导/甲方 | 单色系（accent 主 + 明度阶梯），不用五色 | Business Blue / Swiss Modern / Stripe Professional |
| 技术档 | 受众是开发者/技术发布会 | 五色可用，辉光可开 | Terminal Green / Linear Dark / MongoDB / 8-Bit Orbit |

---

## §1 选型表（数据关系 → 图表）

| 数据关系 | 首选 | 备用（相邻页换图用这档，不为多样性牺牲选型） | 触发场景 |
|---|---|---|---|
| **体量比较** | 柱状图（Y 轴必须从 0 起） | 条形图（类目名长时） | 各区产值对比、厂商份额 |
| **时间趋势** | 折线图 | 柱线组合（量+率双轴）、面积图 | 月度走势、季度同比 |
| **占比构成** | 环形图（中心放总值） | 堆叠条形（组件多时） | 预算构成、收入结构 |
| **偏差（对参照±）** | 发散条形图 | 子弹图（对目标值） | 顺差逆差、达标/未达标 |
| **排序变化** | 有序条形图 | 斜率图（两期排名变化） | 榜单、竞品位次变动 |
| **相关/流动** | 散点图 | 气泡图、瀑布图（增减分解） | 投入产出、成本拆解 |

**砍掉的类别及理由（防误选）**：地图系（choropleth 等）——PPT 低频且需地理数据，确需时走 ECharts map 特例；弦图/桑基/网络图——投影距离下可读性差，资金流向用瀑布图替代；小提琴/蜂群/并行坐标——数据新闻专用，用箱线图或直方图兜底。

## §2 SVG 骨架通用段（v2 主路径，六类模板共用）

手写 SVG 是默认路径（99% 场景）：容器挂 `.chart`，底盘已接生长动画（`effects.css`），**照抄类名即得动画，零 JS**：

```html
<svg class="chart" viewBox="0 0 1200 380" style="width:100%;height:auto">
  <!-- 网格/轴线：不加类名（自动静止，防误伤）；stroke 走 var(--line-struct)（结构线 ≥3:1，hairline 投影会隐） -->
  <line x1="80" y1="330" x2="1160" y2="330" stroke="var(--line-struct)"/>
  <!-- 柱：<rect class="bar">（竖向生长；--i:1,2,3 逐根错开；横向条形用 class="bar-h"） -->
  <rect class="bar" style="--i:0" x="120"  y="150" width="72" height="180" fill="var(--accent)"/>
  <rect class="bar" style="--i:1" x="300"  y="200" width="72" height="130" fill="var(--accent)"/>
  <!-- 折线：<path class="line">（描线动画；必须 fill="none"）；数据点：<circle class="dot"> -->
  <path class="line" d="M120 200 L360 170 L600 210" fill="none" stroke="var(--accent)" stroke-width="3"/>
  <!-- 文字档（底盘 core.css 已定义，直接挂类）：.cl 26 类目 / .cv 32 数值 / .cy 21 图例 /
       .cs 19 小注 / .axis-lbl 22 轴标 / .bar-val 30 柱顶数值——fill 已走 token，禁写死 hex -->
  <text class="axis-lbl" x="156" y="360" text-anchor="middle">华东</text>
  <text class="cv" x="156" y="130" text-anchor="middle">312</text>
</svg>
<!-- 脚注：来源锚（红线①）；类名是 .footmark（v2 无 .source） -->
<div class="footmark">来源：公司年报，2025</div>
```

`prefers-reduced-motion` 下底盘自动降级静态，生成端无需处理。

## §2b ECharts 通用设置（例外路径，用户明说要交互才用）

```js
// 色板从 CSS 变量读（换主题自动跟着变，禁止写死 hex）
const cs = getComputedStyle(document.documentElement);
const C = {
  accent: cs.getPropertyValue('--accent').trim(),
  accent2: cs.getPropertyValue('--accent').trim(),  // v2 无 --accent2，辅色一律从 accent 派生
  text: cs.getPropertyValue('--ink-dim').trim(),
  heading: cs.getPropertyValue('--ink').trim(),
  border: cs.getPropertyValue('--line-struct').trim()  /* 网格/轴线结构线（0-23 切：hairline 投影会隐） */
};
const BASE = {
  textStyle: { fontFamily: cs.getPropertyValue('--font-sans').trim(), fontSize: 20, color: C.text },
  grid: { left: 8, right: 8, top: 12, bottom: 8, containLabel: true },
  animationDuration: 600, animationEasing: 'cubicOut'
  // 不设 title：结论写在页标题（.head h2，一图一结论，避免双层标题）
  // 不设 legend：系列 ≤2 时用直接标注；≥3 系列才开，且 fontSize ≥20
};
// 明度阶梯：正 ratio 提亮、负值压暗（图内禁止写死 hex，全部从 accent 派生）
const lift = (r) => echarts.color.lift(C.accent, r);
```

## §3 六类模板

### 3.1 体量比较 · 柱状图【完整可跑示例 ①】

适用信号：各区/各厂商/各品类数值对比。约束：类目 ≤6；类目名长改横向条形图。

```js
chart1: {
  ...BASE,
  xAxis: { type: 'category', data: ['华东', '华南', '华北', '西南', '东北'],
    axisLabel: { fontSize: 20, color: C.text },
    axisLine: { lineStyle: { color: C.border } }, axisTick: { show: false } },
  yAxis: { type: 'value', min: 0,            // 柱状图 Y 轴必须从 0 起
    axisLabel: { fontSize: 20, color: C.text },
    splitLine: { lineStyle: { color: C.border, type: 'dashed' } } },
  series: [{ type: 'bar', data: [312, 268, 195, 121, 86],
    barWidth: '46%',
    itemStyle: { color: C.accent, borderRadius: [4, 4, 0, 0] },
    label: { show: true, position: 'top', fontSize: 20, color: C.heading, formatter: '{c}' } }]
}
```

页内配套（SVG 主路径）：`<svg class="chart" viewBox="0 0 1200 380">…（照 §2 骨架，柱挂 class="bar"、线挂 class="line"、点挂 class="dot"）…</svg>` + 脚注 `<div class="footmark">来源：公司年报，2025</div>`（图表数字绕不过红线①，必须锚出处）。
例外路径（用户明说要交互时才用）：`<div class="chart" id="chart1" style="height:380px"></div>` + 内联 echarts.min.js。

### 3.2 占比构成 · 环形图【完整可跑示例 ②】

适用信号：预算/收入/人口构成。约束：**组件 ≤5**，超出改堆叠条形；中心放总值。

```js
chart2: {
  ...BASE,
  series: [{ type: 'pie', radius: ['52%', '78%'], center: ['50%', '50%'],
    data: [
      { value: 42, name: '产品收入' }, { value: 27, name: '服务收入' },
      { value: 18, name: '授权收入' }, { value: 13, name: '其他' } ],
    label: { fontSize: 20, color: C.text, formatter: '{b} {d}%' },
    itemStyle: { borderColor: 'transparent', borderWidth: 2 },
    color: [C.accent, C.accent2, lift(0.45), lift(0.25)] }],
  graphic: [{ type: 'text', left: 'center', top: 'middle',
    style: { text: '1.2亿', fontSize: 22, fontWeight: 700, fill: C.heading } }]
}
```

### 3.3 时间趋势 · 折线图【骨架 + 关键行】

适用信号：月度/季度走势。约束：数据点 ≤12，超过先抽稀到双周/月度。

```js
/* xAxis: { type:'category', data:[...月份] } */
/* yAxis: { type:'value', axisLabel:{fontSize:20} } */
series: [{ type: 'line', smooth: false, symbol: 'circle', symbolSize: 6,
  lineStyle: { color: C.accent, width: 2.5 },
  itemStyle: { color: C.accent },
  /* 面积变体：areaStyle 用 color-mix(in srgb, C.accent 12%, transparent) 拼半透明主色（v2 无 --accent-rgb） */
  label: { show: true, fontSize: 20 } }]
```

两期对比用双线（accent + accent2，直接标注线名，不开 legend）。

### 3.4 偏差 · 发散条形图【骨架 + 关键行】

适用信号：对参照的正负偏差。约束：正负两侧同色系左右分色。

```js
/* yAxis: { type:'category', data:[...条目] }（横向条形，条目名可长） */
series: [{ type: 'bar',
  data: [{value: 18, itemStyle:{color: lift(0)}},
         {value:-7, itemStyle:{color: lift(-0.45)}} /* 正=accent 负=压暗档 */],
  label: { show:true, position:'right', fontSize: 20 } }]
/* 配 xAxis.value 轴 + 一条 0 值 markLine（参照线，lineStyle color:C.border） */
```

### 3.5 排序变化 · 有序条形 / 斜率图【骨架 + 关键行】

适用信号：榜单、位次变动。约束：条目 ≤6。两期排名变化优先斜率图：`series.type:'line'`，每条目一 series（首末两点），`xAxis.data:['2024','2025']`，位次反转 `yAxis.inverse: true`，label 显示名次。

### 3.6 相关/流动 · 散点 / 瀑布图【骨架 + 关键行】

适用信号：两变量关系 / 增减分解。约束：散点 ≤30 点；瀑布 ≤6 级（用堆叠柱实现：透明垫底柱 + 增减着色柱，正值 accent、负值 accent 暗档）。**散点图必须提醒读者"相关≠因果"**（NOTES 讲稿或图旁一行）。

## §4 可读性红线（SVG viewBox 380 高 / ECharts 容器同高）

1. 图内文字地板：**19px**（沿用底盘 `.cs` 档；轴标签 `.axis-lbl` 22px、图例 `.cy` 21px、数值 `.cv` 32px、类目 `.cl` 26px）。12px 是 v1 印刷尺寸，投影下不可读——出现即返工
2. 一图一结论：图表标题写结论（"Q3 留存超计划 18%"），不写"Q3 数据"——结论落在**页标题**（`.head h2`，见 core.css），option 不设 title
3. 柱/条 Y 轴从 0 起（`min: 0` 或不写；显式写非 0 min 会被断言打 WARN）
4. 环形组件 ≤5；饼与环形全 deck 二选一统一
5. SVG 用 §2 骨架的紧凑值，380 高度下留足轴标签空间，不挤图例

## §5 验收指针

图表断言：C-1 图内字号地板（SVG 手写图按渲染后字号、ECharts 例外按 option 字号）/ C-2 缺来源脚（`.footmark`）/ C-3 Y 轴非 0 / C-4 环形超 5——由 `scripts/verify-consistency.py` 图表节承担（**严重级**：命中即 exit 1 打回），命中给位置+修复指引。图表页占位率单独走 35% 分支（380 容器结构性达不到 60%；量测走 measure-layout 版率口径）。
## §6 动画规范（2026-10-21 立：生长时机统一翻到页）

**主路径（手写 SVG）：零 JS**——类名与骨架见 §2（柱 `bar` / 横条 `bar-h` / 线 `line` / 点 `dot`），底盘在页激活（`.active`）时自动触发生长动画：翻到页才动、离页自动重置、`--i` 逐根错开、`--d` 起步延迟可选。`prefers-reduced-motion` 自动降级静态。

**例外路径（ECharts，用户明说要交互才用）两条铁律**：
1. **init 时机 = 该页首次进场**——监听底盘 `slide:enter` 事件（底盘 `go()` 每次进页都会派发，detail.index 为页序号），首次命中才 `echarts.init` + `setOption`。动画自然从翻到页开始，而不是全 deck 加载时一次跑完。
2. **动画参数**：BASE 之上补逐项错开——`animationDelay: (idx) => idx * 120`（柱/条逐根生长）；折线 `animationDuration: 1100`。

```js
// ECharts 页监听模板（放在 chartConfigs 定义之后）
var p5inited = false;
document.getElementById('p5').addEventListener('slide:enter', function () {
  if (p5inited) return; p5inited = true;
  echarts.init(document.querySelector('#p5 .chart')).setOption(chartConfigs.chart1);
});
```

**数字滚动**：`.hero-num` / `.metric .mv` / `.num` / `.roll` 命中自动滚（1.1s easeOutCubic，千分位/小数/正负号/单位原样保留），生成端无需任何属性。
