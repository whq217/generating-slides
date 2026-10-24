# Generating Slides v2 — 投影级网页演示文稿生成技能

**简体中文** ｜ [English](README_en.md)

> 给 Claude Code 用的技能包：按「版面率 → 字号 → 秩序」三层底层约束 + 焦点判断层，生成 1920×1080 单文件 HTML 演示稿（内置交互三件套 + 动画库 + PDF 双出口），产出前过机验。
>
> **执行规则以 [SKILL.md](SKILL.md) 为准，本文件仅为安装与概览说明**（2026-10-21 立：防两文件漂移）。
>
> **来源声明**：本技能基于 Zara Zhang 的开源项目 [Frontend Slides](https://github.com/zarazhangrui/frontend-slides)（MIT License）二次开发，非原创首发；排版底盘与流程为本包自有。整体依 MIT 分发，上游版权声明见 [SKILL.md](SKILL.md) 文末《来源与许可》。

## 这个技能做什么

用户说一句「帮我做个关于 XXX 的 PPT」，技能按**七阶段**走：阶段 0 读项目 CLAUDE.md（没有则跳过）→ 配置 → 内容准备 → 内容优化（静默）→ 大纲 → 风格选择 → 生成（含 6.5 机验）→ 交付。**每个阶段的用户确认点都是硬停点**，等答复不算停顿。

产出是一个 HTML 文件，CSS/JS 全内联，无 CDN、无构建工具，双击即放映（1920×1080 等比缩放，任何屏幕不变形）。

## 核心约定（v2 范式）

| 层 | 管什么 | 红线 |
|---|---|---|
| 底盘·版面率 | 有没有站住版面 | 密排 ≥60% 面积且宽 ≥80% / 双栏 ≥45% / 单焦点主角块 ≥60% 版心 |
| 阅读·字号 | 站住了看不看得见 | 正文地板 22px（1/50 屏高）/ 标题主张型锁 84px / 仪式位 110-140px |
| 秩序·分组对齐间距 | 看见了乱不乱 | 间距三档跟层级树 / 容器阶梯卡>线>留白 / 一页一左轴 |
| 焦点·强调判断 | 强调谁、怎么强调、强调到几分 | 焦点服从论述意图 / 视觉重量守恒（hero 禁垫色块）/ 颜色稀缺配额 / 卡片同构化优先 |

- **底盘唯一·装配式**：`assets/chassis-v2.html` 是唯一底盘（装配产物，**禁手改**）；源码在 `assets/chassis/`（冻结）+ `assets/modules/`（功能件），改完跑 `node scripts/build-chassis.mjs` 重建
- **密度前置分档**：低 ≤40 / 中 40-120 / 高 120-200 / 超 >200 砍字砍页（cut never compress）
- **槽位判定树**：内容逻辑决定槽位，禁临时发明
- **动画自动路由**：内容侧重 × 氛围 → 套餐，默认克制档，不逐个问客户

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

## 目录结构

```
generating-slides/
├── SKILL.md                    # 主文件：范式总纲 + 七阶段流程 + 槽位判定树 + 包内文件地图
├── README.md                   # 安装与概览（中文）
├── README_en.md                # 安装与概览（English）
├── references/                 # 17 份方法文件，按阶段/页型触发读取；无触发不加载
│   ├── layout-rules-v2.md      # 三层规则全文（阶段 6 前必读）
│   ├── focus-judgment.md       # 焦点与强调判断层（阶段 3 定档后 + 阶段 6）
│   ├── presets-index.md       # 22 套预设索引+2×2 四池路由（阶段 5 先读，物理分离地图层）
│   ├── style-presets.md        # 22 套预设规格正文（Grep 直达小节）
│   ├── decoration-vocab.md     # 装饰层词汇库：两铁律（颜色一锅汤/装饰一套词）+ 词条 + 数据型封面三段式 + 踩坑（阶段 5.3/6）
│   ├── content-preparation.md  # 素材提取：docx/pptx 命令、Windows 编码坑、图片筛选
│   ├── content-optimization.md # 内容优化原则（§3.1-3.8），含焦点判定
│   ├── title-copy-types.md    # 标题文案分型：体裁三档配比/位置轴/钩子四约束/字号身份裁决
│   ├── number-typography.md    # 数字排版 R1-R6 + 断言 349 清单
│   ├── chart-recipes.md        # 六类图表：手写 SVG 主路径 + ECharts 例外（须内联）+ 动画时机
│   ├── diagram-patterns.md     # 九配方结构图示（G-01~G-09）
│   ├── animation-routing.md    # 类型×氛围 → 动画套餐自动路由 + 三层收敛
│   ├── anim-recipes.md         # 代码动画三问闸门/配额/五配方（按需件）
│   ├── image-handling.md       # 图片唯一出口是封面
│   ├── speaker-mode.md         # 讲者窗口行为说明（底盘已内置 S 键）
│   ├── iterative-edit.md       # 迭代改稿：备份 → 手术式改 → 回归
│   └── offline-export.md       # PDF / 离线
├── assets/
│   ├── chassis-v2.html         # 底盘唯一来源（build 产物，禁手改）
│   ├── chassis/                # 冻结源码：core.css / core.js / template.html
│   ├── modules/                # 功能件：interactions / print / effects / anim-runtime
│   └── diagram-gallery.html    # 九配方可运行参考（本地打开即看，非交付模板）
├── scripts/
│   ├── build-chassis.mjs       # 改底盘源码/模块后必跑：重建 chassis-v2.html（--no-effects 出精简版）
│   ├── measure-layout.js       # 版率+欠填机验（浏览器注入型探针，本机 Chrome headless，零 npm 依赖；兼容 .reveal 系入场类）
│   ├── crowd-probe.py          # 拥挤探针：间距贴死/重叠/行高异常（需 playwright；缺则 SKIP）
│   ├── check-deck.py           # 产物级断言四类：hero-num 单位灰 / SVG 着色 / 文本 y 越界 / 字号档位
│   ├── verify-consistency.py   # 静态一致性检查（纯 Python）
│   ├── verify-all.py           # 机验门禁总入口：build 一致 / 正负样本闸 / 旧术语零命中
│   └── extract-pptx.py         # .pptx 提取（需 python-pptx）
├── samples/
│   ├── good/chassis.html       # 正样本（官方底盘，双脚本必须全绿）+ 负样本的补丁基座
│   ├── patches.json            # 25 份负样本的行级补丁（含各自 sha256），不随包分发全文
│   ├── build_samples.py        # 现场生成负样本到临时目录（逐份 sha256 自证，不写包目录）
│   ├── gen_patches.py          # 改基座 / 改样本后重算 patches.json
│   ├── _base/                  # 无法由基座派生的独立稿（截断版 bad-scan-base-empty）
│   └── expected.json           # 每份负样本的期望（退出码 + 输出须含关键词），verify-all 逐条比对
├── LICENSE                     # MIT 正本 + 上游与第三方署名
└── .gitignore
```

## 机验

生成完不是交付完，跑完脚本才算。不达标只走白名单手段（换纵向布局 / 升字号 / 换轻容器 / 砍页并页），**永不加填充物凑版率**。

| 脚本 | 能查什么 | 依赖 |
|---|---|---|
| `measure-layout.js` | 版率口径 + 欠填带（vacMax / vacBottom，探针强制可见防动画骗检、剔除边注四件套） | 本机 Chrome |
| `verify-consistency.py` | 静态一致性（**单一报告制**，2026-10-23 立）：**[严重]**（exit 1 = 打回信号，逐项处理或说明理由后交付）= 骨架完整性 / 孤儿组件类（类名基准=底盘 CSS 注册表自动提取） / 强调容器形态数>6 / 缺 hl 卡>5 / 内联字号<11.5px 超 10 处 / 页间 gap>2 种（生成端写了内联 gap 才生效，否则显示「统一」）/ 光晕配色 bug / 字号变量悬空 / 封面字号覆盖 / 图表与图示规范 / 口径自洽 / 解析层基数自证（2026-10-23 M9：单双引号通吃 + 基数为 0 报解析异常，绿报告必须能证明「看见了没事」）；**[提示]** = 硬编码色 / 辅助色 tone / 单列纵排 / 图示节点上限（不影响退出码，处理决定权在使用方） | 纯 Python |
| `crowd-probe.py` | 拥挤探针：组内间距贴死 / 文字重叠 / 行高异常 | playwright（缺则 SKIP） |
| `check-deck.py` | 产物断言四类：hero-num 单位灰 / SVG 着色 / 文本 y 越界 / 字号档位（**区间+地板两级**，2026-10-23 区间化：越界 [8.4, 176]px 即严重；区间内非底盘/规则档位只提示不拦截——创意值放行、越界才红） | 纯 Python |
| `verify-all.py` | 门禁总入口（2026-10-23 立）：build 重建逐字节一致 + 正样本全绿 + 负样本按 `samples/expected.json` 逐条比对（负样本由 `patches.json` 现场生成、25 份 sha256 自证，含单引号双写法）+ 旧术语零命中；改解析器/检查器后必跑 | 纯 Python（build 步需 node，无则 SKIP） |

**关于 playwright（可选依赖，2026-10-24 补）**：本包生成和交付 PPT 不依赖它——没装只是「拥挤探针」这一项可选检查自动跳过（显示 [SKIP]，不是报错，可忽略）。想启用这项检查的，可在自己的 Python 环境执行 `pip install playwright`；不装，一切照常。

## 真源地图（出错查这里，2026-10-23 立）

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

## 与 v1 的关系

v1（Reveal.js 1200×700 + 19 主题 + 30 布局）已于 2026-10-20 移出本包，不随包分发、不删除。

> **GitHub 存档**：v1 的完整源码保存在本仓库标签 [v1.0-revealjs](https://github.com/whq217/generating-slides/tree/v1.0-revealjs)。
> 需要旧版可执行 `git checkout v1.0-revealjs` 取回；`master` 分支只承载 v2（chassis-v2 内核）。
> 两版不兼容：v1 依赖 Reveal.js、6 阶段流程、`name: slides`；v2 零外部依赖、7 阶段、`name: generating-slides`。

## 更新记录

- **2026-10-24（四）** — ①**去维护史化**：SKILL.md 正文 17 处内联批注（"某日立 / 某日拍板 / 某日移除"类版本账）剥离，只留行为理由，日期账迁到本节末尾清单——这些是给人看的维护记录，不该占 agent 运行时上下文。②**补回署名**：1.0.0 有、1.1.0 漏掉的「女娲·Skill造人术」MIT 出处声明（SKILL.md《来源与许可》+ 上方致谢）已恢复，按本包自家署名纪律不得倒退。③**samples 补丁化**：25 份负样本原为 1089 行底盘全文副本、仅注入一处缺陷，改由基座 + `patches.json` 现场生成（逐份 sha256 自证），目录从 2.6 MB 降到 784 KB，打包后减约七成。验证：verify-all 54/54 PASS（负样本经现场生成后逐条比对，与原文逐字节一致）。

- **2026-10-24（三）** — 移除 N 键提词面板：主窗口是投屏，提词面板观众可见（0-23 已废"开 S 自动跟开"，本次删 N 手动功能本体，交互四件套变三件套 E/D/S）。提词职责全归 S 演讲者窗口备注卡（NOTES 数据源不变）。同步改 core.js/template/interactions.css/interactions.js + SKILL.md/speaker-mode.md/README 口径 + 产物页脚 hint 文案。验证：N 键无反应、翻页正常、S 演讲者窗口正常弹出；build + verify-all 54/54 PASS。
- **2026-10-24（二）** — 修复 BroadcastChannel 回声回环：同一 deck 开多个标签页/窗口时，任一侧翻页 → 广播 → 对侧跟翻后再广播 → 双方无限互踢（实测一次翻页 3 秒内页面重演上万次：数字滚动反复重启即"一直闪"、页码乱跳、主体空白；重开浏览器单实例即自愈，故呈偶发）。修法：core.js 拆 go/__goto（同页短路 + 收广播只跳页不回播），interactions.js 两处收消息点改走 __goto。验证：双标签页复测回环归零、跟翻同步保留；build 重建 + verify-all 54/54 PASS。
- **2026-10-24** — crowd-probe 容错：缺 playwright 时打印 [SKIP] + exit 0，不再 traceback 崩溃；SKILL.md（compatibility / 阶段 6.5 / 文件表）、README.md（目录树 / 机验表）同步写明"缺则 SKIP、不判红、禁临时安装、跑不了须在交付说明注明未验"。验收：verify-all 54/54 PASS；旧版 vs 新版（有 playwright）输出 SHA256 逐字节一致；无 playwright 时 exit 0 单行 [SKIP]；仓库 chassis-v2.html 与 build 产物哈希一致。

#### SKILL.md 内联批注迁出清单（2026-10-24 迁至此处，原文已从 SKILL.md 剥离）

| 日期 | 事项 |
|---|---|
| 2026-10-20 | 流程外壳恢复 v1 七阶段（此前曾切 v2 八阶段） |
| 2026-10-21 | 底盘改装配式架构：源码在 `assets/chassis/` + `assets/modules/`，`chassis-v2.html` 为装配产物、禁手改，改完跑 `build-chassis.mjs` 重建 |
| 2026-10-21 | 阶段 1 接入体裁档位推断（A 纯书面 / B 汇报+现场讲 / C 纯演讲），不新增提问轮次 |
| 2026-10-21 | 拥挤探针 `crowd-probe.py` 上线：组内间距贴死 / 文字重叠 / 正文级行高 <1.25 专项机验 |
| 2026-10-21 | PDF 双出口：交付时问"要不要 PDF 版" + 页面内 P 键随时打印 |
| 2026-10-21 | README 同步闸：涉 SKILL.md 结构性变更的轮次，收尾必查 README（根因：README 曾停旧版 47 轮无人触发更新） |
| 2026-10-22 | 风格四池改 2×2 结构：暗系按能量切（冲击 / 沉静）、亮系按底色质感切（纸感编辑 / 清爽现代） |
| 2026-10-22 | 预览=迷你成品定案（A 案）：预览卡内嵌真 chassis 舞台，同 token 档位、同槽位判定树，再等比 `scale` 缩小 |
| 2026-10-22 | 卡片默认无盒判定链：出卡须自证属四场景之一（身份独立并列 / 引用切出 / 选择性突出 / 异构视觉单元并列），说不出即撤盒 |
| 2026-10-22 | Chrome 路径解析补充：Windows 常不在 PATH，需按 `%LOCALAPPDATA%` / `%ProgramFiles%` 逐级探测 |
| 2026-10-22 | headless 导出必须加独立 `--user-data-dir`，否则占用默认实例、交付时 `start` 不弹窗（实测坑） |
| 2026-10-22 | 同类错误全扫制：用户指出一处 → 修该处 → 立即全 deck / 全包扫同类，可断言的进机验 |
| 2026-10-23 | 5.3 即兴派生通道试点：四池与点名都不匹配时按主题派生，须写配色理由，交付时问是否入册 |
| 2026-10-23 | 装饰配方映射接入阶段 5：预设/即兴配方 → 装饰词汇库选主签名（≤2 种全片贯穿） |
| 2026-10-23 | `measure-layout.js` 装饰层 `.deco` 双口径排除：装饰参与构图但版率不算数 |
| 2026-10-23 | `verify-consistency.py` 改单一报告制：只出问题清单、不做交付裁决 |
| 2026-10-24 | 移除 N 键提词面板（主窗口是投屏、观众可见），交互四件套 → 三件套 E/D/S，提词职责归 S 演讲者窗口备注卡 |

## 致谢

基于 @zarazhangrui 的 [Frontend Slides](https://github.com/zarazhangrui/frontend-slides)（MIT）构建，v2 范式由 Hongqing W 重构。阶段 3「内容优化」参考 [女娲·Skill造人术](https://github.com/alchaincyf/nuwa-skill) 的 Steve Jobs 视角 Skill（MIT）。

## 许可证

MIT License。法律正本见 [LICENSE](LICENSE)（含上游 Frontend Slides 与女娲·Skill造人术的第三方声明）；正文口径见 [SKILL.md](SKILL.md) 文末《来源与许可》。

---

本技能由公众号「庆哥聊AI」整理发布，免费使用。
