# 内容准备细则（阶段2）

> **定位（2026-10-20 重组）**：本文件从 SKILL.md 阶段2 下放而来——三种素材分支的提取命令、编码 workaround、图片筛选规则。阶段2 主流程（分支判断、确认节点）留在 SKILL.md。

---

## 分支A — 用户提供本地文件

| 文件类型 | 读取方式 |
|---|---|
| PDF | 直接 Read 工具（支持分页读取） |
| Word (.docx) | Python 提取（下方命令，需 `pip install python-docx`） |
| Markdown/纯文本 | 直接 Read 工具 |

**⚠️ Windows docx 提取必须加编码声明**，否则中文报 `UnicodeEncodeError: 'gbk'`：

```python
python -c "import sys; sys.stdout.reconfigure(encoding='utf-8'); from docx import Document; [print(p.text) for p in Document('文件路径').paragraphs if p.text.strip()]"
```

路径含中文导致 Bash 传参乱码时，改用 Python 内拼接路径：

```python
python -c "import sys,os; sys.stdout.reconfigure(encoding='utf-8'); from docx import Document; doc=Document(os.path.join(os.path.expanduser('~'),'Documents','中文文件名.docx')); [print(p.text) for p in doc.paragraphs if p.text.strip()]"
```

提取后整理为资料摘要，向用户展示并确认。

## 分支B — 仅提供主题，无原始文档

1. WebSearch 搜索真实资料，构思 3-5 个关键词，覆盖：行业数据、典型案例、趋势预测、权威观点
2. 可并行发起多个搜索
3. 汇总为资料摘要，向用户展示并确认

## 分支C — 用户提供 PPT 文件（.pptx）

提取脚本（需 `pip install python-pptx`）：

```bash
python scripts/extract-pptx.py <input.pptx> <output_dir>
```

- 脚本已内置 stdout UTF-8 重配置，Windows 直接运行即可——**不要**用 `python -c "reconfigure" && …` 双进程前缀（reconfigure 只作用于当前进程，对第二条命令无效）
- 输出：每页幻灯片的标题、文本内容、图片数量；图片保存在 `<output_dir>/assets/`
- **图片只筛封面可用素材**：横版做全出血背景 / 竖版做右图位，其余丢弃并告知；内容页无图位，不内联（图片唯一出口是封面，见 image-handling.md）
- 局限：PPT 中的动画、SmartArt、嵌入图表无法提取，纯文本和备注可保留
