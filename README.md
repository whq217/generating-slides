# Generating Slides v2 — 投影级网页演示文稿生成技能

**简体中文** ｜ [English](README_en.md)

> **A Claude Code skill that turns one sentence or a document into a projector-grade HTML slide deck.**
> Single self-contained file, zero dependencies, no CDN or build step — layered layout rules (coverage · type size · order · focus) enforced before output, with a built-in pre-delivery check.
> → Full English documentation: [README_en.md](README_en.md)

> 给 Claude Code 用的技能包：按「版面率 → 字号 → 秩序」三层底层约束 + 焦点判断层，生成 1920×1080 单文件 HTML 演示稿（内置交互三件套 + 动画库 + PDF 双出口），产出前过机验。
>
> **执行规则以 [SKILL.md](SKILL.md) 为准，本文件仅为安装与概览说明**（2026-10-21 立：防两文件漂移）。
>
> **来源声明**：本技能基于 Zara Zhang 的开源项目 [Frontend Slides](https://github.com/zarazhangrui/frontend-slides)（MIT License）二次开发，非原创首发；排版底盘与流程为本包自有。整体依 MIT 分发，上游版权声明见 [SKILL.md](SKILL.md) 文末《来源与许可》。

## 30 秒上手

> 装好后直接说话，不用记命令。

| 你说 | 会发生什么 |
|---|---|
| 「帮我做个关于 2026Q3 运营复盘的 PPT，12 页，给管理层看」 | 从零生成：配置 → 素材 → 大纲 → 风格预览 → 生成 → 机验 → 交付 |
| 「这份 docx 做成 10 页汇报稿」 | 重排现成材料，风格另起一轮选 |
| 「第 3 页太挤了，砍掉一半，别动版式」 | 改稿轮次：只动指定页，砍字不缩字号，改完复跑同页机验 |

生成完双击 HTML 即放映；放映时 → 翻页、**E** 编辑、**D** 画笔、**S** 演讲者窗口、**P** 出 PDF。

## 走一遍完整的（一句话 → 终稿）

> 以「做个 2026Q3 运营复盘，12 页，给管理层看」为例，全流程 7 个确认点。

| 阶段 | 它会做什么 | 你大概只回一句 |
|---|---|---|
| 1 配置 | 一次问完：页数规模、内容侧重、素材来源、视觉素材 | 「10 页 / 平衡型 / 只有主题 / 无图」 |
| 2 素材 | 搜真实行业数据，整理成一页摘要 | 「可以」 |
| 3 优化 | 静默执行（焦点定档、密度分档、文案分型），不打扰你 | —— |
| 4 大纲 | 给出逐页大纲，每页带「来源 / 焦点 / 槽位 / 密度 / 文案类型」 | 「第 5 页并到第 4 页」 |
| 5 风格 | 给 4 个氛围选项 → 出 1 张真实预览 | 「B2 清爽现代」 |
| 6 生成 | 按底盘装配，逐页落盘，封面先过目再放量 | 「继续」 |
| 6.5 机验 | 量版率、查字号/溢出/拥挤，不达标先修再交 | —— |
| 交付 | 打开 HTML，问要不要 PDF 版 | 「要 PDF」 |

**终稿长什么样**：单个 HTML 文件，1920×1080 舞台；封面有一个第一视觉事件（本例＝Q3 核心数字 + 口径注），趋势/构成/排行三张图各占一页，结束页收口。双击即放，按 E 可改、D 可画、S 讲者窗口、P 出 PDF。

## 这个技能做什么

> **读者声明（1026）**：本包全部规则面向 AI 执行者编写——用户无需阅读或理解任何规则概念，全程自然语言对话即可完成制作，不存在使用门槛。

用户说一句「帮我做个关于 XXX 的 PPT」，技能按**七阶段**走：阶段 0 读项目 CLAUDE.md（没有则跳过）→ 配置 → 内容准备 → 内容优化（静默）→ 大纲 → 风格选择 → 生成（含 6.5 机验）→ 交付。**每个阶段的用户确认点都是硬停点**，等答复不算停顿。风格选择阶段有**客户自带风格直通道**：给了实物（HTML/PPTX/截图/色值）或点名已存预设 → 跳过提问与预览直接提取风格配方采用；只给含糊词 → 出预览图指认；禁止拿库内预设顶替客户实物。

产出是一个 HTML 文件，CSS/JS 全内联，无 CDN、无构建工具，双击即放映（1920×1080 等比缩放，任何屏幕不变形）。

## 它不会做什么

- **不会替你默认选风格** —— 阶段 5 必问；只有你给了实物（HTML/PPTX/截图/色值）才走直通道提取
- **不会跳过确认点自己往下跑** —— 七阶段每步都是硬停点，等答复不算停顿
- **不会用缩小字号硬塞内容** —— 超密度（>200 字/页）砍字或砍页，cut never compress
- **内容页不配图** —— 图片唯一出口是封面
- **不达标不交付** —— 交付前必跑机验。其中 `crowd-probe` 依赖 playwright 属**可选**：没装就自动跳过（`[SKIP]`），不影响出稿
- **生成期零外部依赖** —— 无 CDN、无构建步骤、无 npm 安装，产物是单个自包含 HTML

## 常见问题

> 都是实际会被问的那几句。这里只回答「你该怎么办」，不讲原理。

**字太多放不下，会给我把字号缩小吗？**
不会。它宁可砍字、或者拆成两页，字号不缩。宁可少说，也不让你在投影上看不清。

**我自己有想要的风格，会被换成它内置的那套吗？**
不会。有成品（网页、PPT、截图）或色值就丢给它，它照你的提取；只给一个词（比如「科技风」），它会先出几套让你挑，不替你做决定。

**内容页能配图吗？**
生成时不会配。内容页一律无图，要表达就用图表或图示——这是排版选择，不是功能缺失。
它目前也**不会自己生成图片**：不搜图、不放占位图、也不会编一个图片地址出来。封面图只用你提供的；你没提供，就用纯 CSS 渐变做背景。
生成完之后你想自己在 HTML 里贴图，那是手工编辑，不在它的流程里。

**它能自己往下跑、不用我管吗？**
不能。每一步都会停下来等你点头，包括选风格、看大纲、封面过目。等你回复不算卡住。

**导出 PDF 要先装什么吗？**
不用。放映时按 **P** 就能打印成 PDF，用的是浏览器自带能力；离线批量导出的命令，只在批量场景才用得上。

**生成完还能改吗？**
能。放映时按 **E** 直接改，改完自动下载新的 HTML；只想动某一页就跟它说页号。

**我需要先准备什么材料？**
一句话或一份材料都行。有 Word / PDF / PPT 就丢给它；只有一个主题，它会自己去搜真实数据。
说得含糊也没关系——像「帮我准备份材料」「下周要分享点东西」，它会先问一句「要的是 PPT 吗」，再问几页、给谁看。它不会替你猜你要的是文档还是表格。

**装好之后第一句该怎么说？**
直接说需求：「做个 Q3 复盘 PPT，12 页，给管理层看」。上面「30 秒上手」还有两种说法。

## 安装

装到 Claude Code 的 skills 目录，**目录名必须是 `generating-slides`**（与 SKILL.md 的 `name` 一致）。

从本仓库直接克隆：

```bash
git clone https://github.com/whq217/generating-slides.git ~/.claude/skills/generating-slides
```

后续更新只需拉取：

```bash
git -C ~/.claude/skills/generating-slides pull
```

Windows PowerShell：

```powershell
git clone https://github.com/whq217/generating-slides.git "$env:USERPROFILE\.claude\skills\generating-slides"
```

也可以下载 ZIP 解压后整目录复制，确保解压出的文件夹改名为 `generating-slides`：

```bash
cp -r generating-slides ~/.claude/skills/generating-slides
```

## 放映时的键盘操作（底盘内置，2026-10-21 起）

| 键 | 功能 |
|---|---|
| → / ↓ / PageDown / 空格 / 点右半屏 | 下一页 |
| ← / ↑ / PageUp / 点左半屏 | 上一页 |
| **E** | 编辑模式（Done 退出并自动下载新 HTML，编辑结果即文件） |
| **D** | 画笔（右键清屏，翻页自动清） |
| **S** | 演讲者模式（独立窗口 + 双屏跟翻 + 备注卡提词） |
| **P** | 打印 / PDF（print CSS 锁 16:9 每页一张） |

PDF 交付出口：交付时问一句要不要 PDF 版；chrome `--headless --print-to-pdf` 零依赖秒出（见 SKILL.md 交付节）。

## 核心约定（v2 范式）

| 层 | 管什么 | 红线 |
|---|---|---|
| 底盘·版面率 | 有没有站住版面 | 密排 ≥60% 面积且宽 ≥80% / 双栏 ≥45% / 单焦点主角块 ≥60% 版心 |
| 阅读·字号 | 站住了看不看得见 | 正文地板 22px（1/50 屏高）/ 标题主张型锁 84px / 仪式位 110-140px |
| 秩序·分组对齐间距 | 看见了乱不乱 | 间距三档跟层级树 / 容器阶梯卡>线>留白 |
| 焦点·强调判断 | 强调谁、怎么强调、强调到几分 | 焦点服从论述意图 / 视觉重量守恒（hero 禁垫色块）/ 颜色稀缺配额 / 卡片同构化优先 |

- **底盘唯一·装配式**：`assets/chassis-v2.html` 是唯一底盘（装配产物，**禁手改**）；源码在 `assets/chassis/`（冻结）+ `assets/modules/`（功能件），改完跑 `node scripts/build-chassis.mjs` 重建
- **密度前置分档**：低 ≤40 / 中 40-120 / 高 120-200 / 超 >200 砍字砍页（cut never compress）
- **槽位判定树**：内容逻辑决定槽位，禁临时发明
- **动画自动路由**：内容侧重 × 氛围 → 套餐，默认克制档，不逐个问客户

## 与 v1 的关系

v1（Reveal.js 1200×700 + 19 主题 + 30 布局）已于 2026-10-20 移出本包，不随包分发、不删除。

> **GitHub 存档**：v1 的完整源码保存在本仓库标签 [v1.0-revealjs](https://github.com/whq217/generating-slides/tree/v1.0-revealjs)。
> 需要旧版可执行 `git checkout v1.0-revealjs` 取回；`master` 分支只承载 v2（chassis-v2 内核）。
> 两版不兼容：v1 依赖 Reveal.js、6 阶段流程、`name: slides`；v2 零外部依赖、7 阶段、`name: generating-slides`。

---

## 维护者与二次开发

> 以下三节面向**改这个包的人**，不是使用者。用完就走的话，上面已经够了。

### 包内结构（GitHub 访客 / 二次开发）

```
generating-slides/
├── SKILL.md                    # 主文件：范式总纲 + 七阶段流程 + 槽位判定树 + 包内文件地图（references 逐条说明见此处）
├── README.md                   # 安装与概览（中文）
├── README_en.md                # 安装与概览（English）
├── CHANGELOG.md                # 版本变更记录（1.0.0 → 当前，整链）
├── references/                 # 17 份方法文件，按阶段/页型触发读取；无触发不加载
├── assets/                     # chassis-v2.html（底盘产物，禁手改）+ chassis/（冻结源码）+ modules/（功能件）+ diagram-gallery.html
├── scripts/                    # build-chassis.mjs / measure-layout.js / crowd-probe.py / check-deck.py / verify-consistency.py / verify-all.py / extract-pptx.py
├── samples/                    # 机验回归集：good/ 正样本 + _base/ 独立稿 + patches.json + expected.json + 两个生成脚本
├── LICENSE                     # MIT 正本
├── NOTICE                      # 署名与第三方声明
├── .gitattributes              # 换行锁 LF——机验依赖逐字节 sha256
└── .gitignore
```

`tools/`（`check-version.py` 发版前版本一致性检查、`build_platform_pkg.py` 平台包派生）属仓库基建，不进平台分发包；各文件职责明细见 `SKILL.md` 的「包内文件地图」。

### 机验

生成完不是交付完，跑完脚本才算。不达标只走白名单手段（换纵向布局 / 升字号 / 换轻容器 / 砍页并页），**永不加填充物凑版率**。

| 脚本 | 能查什么 | 依赖 |
|---|---|---|
| `measure-layout.js` | 版率口径 + 欠填带（vacMax / vacBottom，探针强制可见防动画骗检、剔除边注四件套） | 本机 Chrome |
| `verify-consistency.py` | 静态一致性（**单一报告制**，2026-10-23 立）：**[严重]**（exit 1 = 打回信号，逐项处理或说明理由后交付）= 骨架完整性 / 孤儿组件类（类名基准=底盘 CSS 注册表自动提取） / 强调容器形态数>6 / 缺 hl 卡>5 / 内联字号<11.5px 超 10 处 / 页间 gap>2 种（生成端写了内联 gap 才生效，否则显示「统一」）/ 光晕配色 bug / 字号变量悬空 / 封面字号覆盖 / 封面断言（视觉事件三选一全缺 = 平庸封面 / 装饰可见度 <1.1:1 隐身——仅 deck 实际用了 `.deco` 词条才判 / `.deco` 直接子元素 >2） / 图表与图示规范 / 口径自洽 / 解析层基数自证（2026-10-23 M9：单双引号通吃 + 基数为 0 报解析异常，绿报告必须能证明「看见了没事」）；**[提示]** = 硬编码色 / 辅助色 tone / 单列纵排 / 图示节点上限 / 封面焦点让位梯度 / 巨数口径注缺失（不影响退出码，处理决定权在使用方） | 纯 Python |
| `crowd-probe.py` | 拥挤探针：组内间距贴死 / 文字重叠 / 行高异常 | playwright（缺则 SKIP） |
| `check-deck.py` | 产物断言四类：hero-num 单位灰 / SVG 着色 / 文本 y 越界 / 字号档位（**区间+地板两级**，2026-10-23 区间化：越界 [8.4, 176]px 即严重；区间内非底盘/规则档位只提示不拦截——创意值放行、越界才红） | 纯 Python |
| `verify-all.py` | 门禁总入口（六步）：build 重建逐字节一致 + 正样本全绿（含 `.deco` 装饰层正样本 `deco-cover.html`）+ 负样本按 `samples/expected.json` 逐条比对（负样本由 `patches.json` 现场生成、26 份 sha256 自证，含单引号双写法）+ 旧术语零命中 + 样本内嵌 deco 参数 == `effects.css` + 行为级探针（Chrome→measure-layout / playwright→crowd-probe，缺环境 SKIP）；改解析器/检查器/`effects.css` 后必跑 | 纯 Python（build 步需 node，无则 SKIP） |

**关于 playwright（可选依赖，2026-10-24 补）**：本包生成和交付 PPT 不依赖它——没装只是「拥挤探针」这一项可选检查自动跳过（显示 [SKIP]，不是报错，可忽略）。想启用这项检查的，可在自己的 Python 环境执行 `pip install playwright`；不装，一切照常。

### 真源地图（出错查这里）

每类事实只有一个权威文件——其他地方只放指针、不放值；两处打架时，下表说了算。

| 事实 | 唯一真源 | 备注 |
|---|---|---|
| 字号档位（合法值） | `assets/chassis/core.css` 实有档位 + `check-deck.py` 的区间红线 | 判据两级（2026-10-23 区间化）：越界（<8.4 / >176px）即严重；底盘实有档位启动时自动提取（改底盘自动跟）；规则批准档位内联 `RULE_PX` 出处标死；区间内档位外值只提示放行 |
| 版面/排版规则 | `references/layout-rules-v2.md` | 三层约束、密度分档、槽位判定树 |
| 页面骨架类名/组件 | `assets/chassis/core.css` + `assets/modules/*.css` 的注册表标记（`@critical`/`@hook`/`@svg-text`，2026-10-23 M1 立） | 孤儿类断言与 SVG 白名单的基准，检查器运行时自动提取——**加组件类在定义块体首打标记即跟，禁手抄进脚本**；无定义的纯 JS 钩子登记在 core.css 顶部 `@hook-declared` 声明行；v1 类名残留由 S8 指纹处理 |
| 底盘 | `assets/chassis/`（源码，冻结）+ `assets/modules/`（功能件） | `chassis-v2.html` 是 build 产物**禁手改**：改完跑 `node scripts/build-chassis.mjs` 重建 |
| 风格预设（色板/字体） | `references/style-presets.md` | `presets-index.md` 只是索引（指针），正文约 1700 行禁全量读 |
| 图示配方/变量 | `references/diagram-patterns.md` §1.2 | 变量补充段必须粘进产物 `:root`，漏粘图示淡底退化为透明 |
| 数字排版（含封面数字判角色三分） | `references/number-typography.md` | 判据已内联 R2 判定树下方（原包外《封面字体规范》§2.1a，不再作依赖） |
| 机检口径 | 各脚本 docstring | 文档宣称数字与脚本实数不一致时，verify-consistency #14 报口径漂移 |

## 更新记录

> 版本号跟内容走，不跟发布次数走：`1.0.0` 是对外首版，`1.1.0`～`1.1.2` 为**内部打样、从未对外**，`1.2.0` 起本仓库为唯一真源（`1.2.0` 即当前线上版本）。逐版明细见 `git log`。

| 版本 | 日期 | 要点 |
|---|---|---|
| **1.6.2** | 2026-10-26 | 提可查性与可修复性（不改功能行为）：「包内文件」表重排为「我要干什么→读哪个文件」定位表、新增「依赖与失败场景」节（Node/Chrome/playwright + 模糊指令引导）、依赖缺失的终端提示改为白话（说清不影响出稿、给出安装指引）、待校准阈值统一标为「观察值·不作断言」；新增 `CHANGELOG.md` 与完整场景示例；README 新增「常见问题」8 条（大白话、面向用户） |
| **1.6.1** | 2026-10-26 | 外部评审三项必修：备份目录迁出包外、`verify-all` 两处 subprocess 补 UTF-8、门禁增第 6 步行为探针；另修裸代号释义、七阶段计数说明、frontmatter 死键。补 `display_name` / `display_name_en`——开放平台按下划线字段解析，此前只有驼峰 `displayName`（SkillHub 通道用），上传即报缺展示名 |
| **1.6.0** | 2026-10-26 | 三刀瘦身：`description` 600→230 字（常驻 token）、主干减负（机验跑法与 PDF 路径下沉 references）、新增 NEVER 速查表 |
| **1.5.0** | 2026-10-25 | 第二批松绑：图示九配方降为基线参考、卡片配额改场合判断、封面确认点、装饰签名默认 ≤2 |
| **1.4.0** | 2026-10-25 | 客户自带风格升级为**配方级**提取（渐变/封面装置/标题用色节奏/容器浓度），禁库内预设顶替实物 |
| **1.3.0** | 2026-10-25 | 阶段 5 新增客户自带风格直通道（实物直通提取 / 含糊词出图指认） |
| **1.2.0** | 2026-10-25 | 封面构图总纲：义务制取代封闭菜单，封面须有「第一视觉事件」，机验新增 #15 封面断言 |
| 1.1.x | 2026-10-24 | 内部打样：去维护史化、samples 补丁化、N 键提词面板移除、BroadcastChannel 回环修复 |
| 1.0.0 | 2026-10-22 | 对外首版 |

## 致谢

基于 @zarazhangrui 的 [Frontend Slides](https://github.com/zarazhangrui/frontend-slides)（MIT）构建，v2 范式由 Hongqing W 重构。阶段 3「内容优化」参考 [女娲·Skill造人术](https://github.com/alchaincyf/nuwa-skill) 的 Steve Jobs 视角 Skill（MIT）。

## 许可证

MIT License。法律正本见 [LICENSE](LICENSE)；署名范围与第三方声明见 [NOTICE](NOTICE)（上游 Frontend Slides 取自哪些部分、本包原创清单、nuwa-skill 引用范围、v1 的 Reveal.js 声明）；正文口径见 [SKILL.md](SKILL.md) 文末《来源与许可》。

---

本技能由公众号「庆哥聊AI」整理发布，免费使用。
