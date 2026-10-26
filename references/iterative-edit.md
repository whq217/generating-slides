# 迭代更新方法（防止回归）

**触发场景**：用户对已生成的PPT提出修改需求（加功能、改页面、调风格）时。

**核心规则**：每次修改前先备份，改后用 Grep 验证核心功能未被误删，绝不整段重写 `<style>` 或 `<script>` 块。

## 改稿四型（先判型，再动手）

走进来的是「修改需求」时，**第一件事是判型**——四型动作完全不同，判错会白做一整轮。本节的入口来自 `SKILL.md` 流程节的「改稿轮次」定义（已有产物的局部修改不进七阶段）。

| 型 | 用户怎么说 | 动作 | 禁止 |
|---|---|---|---|
| ① 指令型 | 「第 3 页砍一半」「这句改短」 | 按下方原则 1-3 做外科手术：备份 → 行级 Edit → 跑回归清单 + 同页机验 | 禁顺手改别的页 |
| ② 否决型（方案不行） | 「封面不行」「这页没感觉」 | **不出文字解释**：先自查该页主角/槽位/版率哪条没立住 → 出 2-3 个重设计方案（每案一句话说清差异）→ 用户选 → 重做该页 → 复跑机验 | 禁直接动手改一版就交 |
| ③ 换皮型 | 「太暗了」「换个配色」「换个风格」 | 只动四样：五件套 token（`--bg/--ink/--ink-dim/--accent/--hairline`）→ 字体栈 → `.deco` 配方浓淡 → `.rv` 延迟编排；**页结构/槽位/文案/NOTES 一律不动**；改完复跑 measure-layout + verify-consistency | 禁重排版面、禁重写页面内容 |
| ④ 全局否决型 | 「整体风格不对」且 ③ 解决不了 | 回 `SKILL.md` 阶段 5 重选，按 5.0 → 5.1 走；回流程前先跟用户确认「是换皮还是重做」 | 禁未试 ③ 就直接回流程 |

**判型口诀：能改字就不改版，能换皮就不重做，能重做一页就不回流程。**

换皮的取值出处：五件套映射见 [style-presets.md](style-presets.md) 顶部《v2 五件套映射表》；装饰浓淡与配方见 [decoration-vocab.md](decoration-vocab.md) §三/§四。

---

## 原则1：先备份再改动

每次修改前，先创建备份目录并存入备份（**默认 = 产物文件同目录下的 `.backups/`**，跟随文件不散落；可用环境变量 `BACKUP_DIR` 指定其他位置）：
```bash
# bash（Git Bash / WSL）
BACKUP_DIR="${BACKUP_DIR:-$(dirname "文件.html")/.backups}"
mkdir -p "$BACKUP_DIR"
cp "文件.html" "$BACKUP_DIR/文件_$(date +%Y%m%d_%H%M%S).html"
```
```powershell
# PowerShell（无 bash 环境时）
$backupDir = if ($env:BACKUP_DIR) { $env:BACKUP_DIR } else { Join-Path (Split-Path "文件.html" -Parent) '.backups' }
New-Item -ItemType Directory -Force $backupDir | Out-Null
Copy-Item "文件.html" (Join-Path $backupDir ("文件_{0}.html" -f (Get-Date -Format "yyyyMMdd_HHmmss")))
```

**备份后必须告诉用户：**
> 备份已保存到 `<产物目录>/.backups/文件_20260405_143022.html`（或 `$BACKUP_DIR` 指定目录），改坏了可随时恢复。

**恢复方式：**
```bash
cp "${BACKUP_DIR:-$(dirname "原文件.html")/.backups}/备份文件名.html" "原文件.html"
```

**多步编辑中间备份：** 每完成2-3个Edit，更新一次备份点（执行同样的cp命令）。这样后续Edit出错时恢复到最近的 checkpoint，而不是最初的备份，避免丢失已完成的改动。

---

## 原则2：外科手术式 Edit — 三级升级路径

**禁区：** 整段重写整个 `<style>` 或 `<script>` 块（极易误删已有功能）

### L1 行级 Edit（默认）
直接 Edit，old_string 在文件中唯一。
- CSS 新增：在 `<style>` 块末尾（`</style>` 前）插入新规则，不修改已有规则
- JS 新增：在对应功能模块注释后插入，不修改已有代码
- HTML 修改：精确匹配目标页面 `<section class="slide" id="pN">` 的首行+内容特征，只替换该页
- 讲稿修改：精确匹配 `NOTES` 对象内对应页键值替换

### L2 扩大上下文（L1失败时）
Edit 报 "old_string is not unique" → 先用 Grep 确认匹配数量，然后加前后行扩大 old_string 范围重试。仍然只改目标内容，只是匹配范围更大。

### L3 模块级替换（L2仍失败时）
用注释边界定位整个功能模块，替换该模块全部内容。模块边界示例：
- CSS: `/* === 画笔 === */` … `/* === 编辑 === */`
- JS: `// ========== 画笔 ==========` … `// ========== 编辑 ==========`
- HTML: `<!-- 📝 第3页：XXX -->` … `<!-- 📝 第4页：XXX -->`

L3 强制规则（必须全部执行）：
1. 替换前 Read 当前模块完整内容（不凭记忆写，从文件读取）
2. 替换后 Read 被替换区域，确认没丢规则
3. 跑原则3的 Grep 回归验证
4. 通知用户检查被替换模块的功能

**升级判断：** 能用 L1/L2 就不升到 L3。L3 是升级手段，不是首选。

---

## 原则3：改后回归验证清单

每次修改完成后，必须用 Grep 验证核心功能（不是手动检查，用工具确认）。关键项查核心代码片段，不只查名字：

```
回归验证项（每次修改后必检，指纹对齐 chassis-v2 底盘）：
□ 翻页核心           — grep "function go(n)" + grep "function paint()"（core.js 共享变量）
□ 键盘/点击翻页      — grep "addEventListener('keydown'" + grep "addEventListener('click'"（E/D/S/P 各键分发在位；底盘无滚轮通道，wheel 零命中属正常——2026-10-22 改后检实测）
□ 入场动画           — grep "\.rv" + grep "var(--d"（.rv 类 + 延迟编排两件都在）
□ 数字滚动           — grep "function rollNums"（翻页重播在 go 内：grep "rollNums(slides[cur])"）
□ 画笔工具           — grep "function togglePen" + grep "function clearPen" + grep "penCanvas.classList.toggle"（翻页自动清：go 内 clearPen 调用）
□ 编辑功能           — grep "function toggleEdit" + grep "contenteditable"
□ 演讲者模式         — grep "function toggleSpeaker" + grep "BroadcastChannel" + grep "buildPresenterWindow"
□ 备注卡             — grep "var NOTES"（演讲者窗口备注卡读 NOTES 对象，键=页 id）
□ Preview-only       — grep "?preview=N"（演讲者 iframe 预览只渲染单页）
□ 打印定格           — grep "\.rv { opacity: 1 !important"（print.css 强制定格终值防空白页）
```

如果验证失败，立即从备份恢复，然后重新做更小范围的修改。

---

## 原则4：功能模块边界清晰

产物是 chassis 装配出的单文件，CSS/JS 按模块注释分块，修改时以注释为边界：

```
<!-- CSS 四大装配块（build-chassis.mjs 按装配表拼入） -->
<style>
  /* ===== chassis/core.css ===== */      ← 舞台/token/页骨架/.rv（核心，禁散改）
  /* ===== modules/effects.css ===== */   ← 动画件（spot-group 等变体）
  /* ===== modules/interactions.css ===== */ ← 交互件（画笔/编辑/演讲者按钮）
  /* ===== modules/print.css ===== */     ← P 键打印/PDF 定格
</style>

<!-- JS 模块（注释块分隔） -->
<script>
  // ========== Preview-only 模式 ==========    (?preview=N 单页渲染)
  // ========== 画笔 ==========
  // ========== 编辑模式 ==========
  // ========== 演讲者模式 ==========
  // ========== Preview-only：只听翻页指令 ==========
  /* 生成端新增功能写在模块注释块之后、文件闭合前，不塞进底盘模块内部 */
</script>
```

**注意：改的是产物副本，不是 `assets/chassis-v2.html`**——底盘问题回技能包源码改+重建，产物只承载页面内容。

---

## 回滚策略

如果用户要求"去掉刚才加的功能"：
- 优先从备份恢复（最快、最安全）
- 如果没有备份，精确删除新增的代码块（依赖注释边界定位）
- **绝不通过重写整个文件来回滚**
