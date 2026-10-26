# 离线与 PDF 导出（v2）

**触发场景**：用户提到无网络环境 / 内网 / 备用文件，或要 PDF 版。

---

## 离线：无需任何流程

v2 产物本身是**零外链单文件**——CSS/JS 全内联、系统字体栈（无 webfont、无 Font Awesome、无 CDN），双击即放映。**离线环境天然可用，不需要"离线打包"**（v1 时代的下载 CDN 资源内联流程已随 v1 退役，无对象）。

唯一体积来源是封面 base64 图（规范 ≤500KB，见 image-handling）；交付时如用户嫌大，提示压缩封面图后重新内联。

## PDF：唯一出口 = chrome headless 一条命令（2026-10-26 起真源在本文件）

```
chrome --headless=new --user-data-dir="%TEMP%\chrome-pdf-profile" --no-pdf-header-footer --virtual-time-budget=6000 --print-to-pdf="输出.pdf" "file:///绝对路径.html"
```

- **headless 一律加独立 `--user-data-dir`**——否则占用默认实例，交付时 `start` 打不开页面
- virtual-time 预算让数字滚动跑完再落纸；print CSS 已锁每页 16:9 零边距、chrome 全退出、动画定格终值——底盘自带，无需额外处理
- 页面内 **P 键**打印同源（print.css 同一份）
- ~~export-pdf.sh 装机路线~~已退役（2026-10-22，与"零外部依赖"原则及 chrome 双轨冲突）

### Chrome 路径解析（Windows 常不在 PATH）

先试 `chrome`；失败依次试 `%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe`、`%ProgramFiles%\Google\Chrome\Application\chrome.exe`、`%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe`（本机实测 Chrome 在 `%LOCALAPPDATA%`）。

## 体积提示

- HTML/PDF 超预期（>10MB）→ 先查封面图是否超 500KB 规范，压图重嵌
- PDF 文本矢量为主，正常几十页体积远小于 HTML
