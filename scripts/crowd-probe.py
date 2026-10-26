# -*- coding: utf-8 -*-
"""拥挤探针：查文字挤压（组内间距贴死 / 文字重叠 / 行高异常）
用法：python crowd-probe.py <deck.html 绝对路径>
依赖：playwright + 系统 Chrome（channel="chrome"，无需下载 chromium）
缺依赖：打印 [SKIP] 并以 exit 0 退出（缺环境不算产物问题，不判红、禁临时安装）
来源：2026-10-21 实测沉淀（组内间距漏改事故催生）
输出：逐页打印问题清单（贴太近 / 重叠 / 行高密）。大字 display 级 0.9x 行高是设计参数不算问题，
      本探针只报 <1.25 行高且字号 ≥20px 的"正文级"元素、间距 <14px 的贴边、任何 bounding box 相交。
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from playwright.sync_api import sync_playwright
    _HAS_PLAYWRIGHT = True
except ImportError:
    sync_playwright = None
    _HAS_PLAYWRIGHT = False

JS = """() => {
  const slides = document.querySelectorAll('.slide, section.slide');
  const out = [];
  slides.forEach((s, i) => {
    s.style.cssText += ';display:block !important;visibility:visible !important;opacity:1 !important;position:absolute !important;top:0 !important;left:0 !important;';
    const texts = [];
    s.querySelectorAll('*').forEach(el => {
      if (!el.textContent || !el.textContent.trim() || el.children.length) return;
      const st = getComputedStyle(el);
      if (st.display === 'none' || st.visibility === 'hidden' || parseFloat(st.opacity) === 0) return;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      const fs = parseFloat(st.fontSize), lh = parseFloat(st.lineHeight) || fs * 1.4;
      const isDisplay = !!el.closest('[class*="dv-"], .hero-num, .ritual');
      texts.push({ t: el.textContent.trim().slice(0, 16), x: r.x, y: r.y, w: r.width, h: r.height, fs, ratio: lh / fs, el, isDisplay });
    });
    const probs = [];
    for (let a = 0; a < texts.length; a++) {
      const A = texts[a];
      if (A.ratio < 1.25 && A.fs >= 20 && !A.isDisplay) probs.push('行高密[' + A.t + '] ratio=' + A.ratio.toFixed(2));
      for (let b2 = a + 1; b2 < texts.length; b2++) {
        const B = texts[b2];
        if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
        const ox = Math.min(A.x + A.w, B.x + B.w) - Math.max(A.x, B.x);
        const oy = Math.min(A.y + A.h, B.y + B.h) - Math.max(A.y, B.y);
        if (ox > 4 && oy > 4) probs.push('重叠[' + A.t + '×' + B.t + '] ' + Math.round(ox) + 'x' + Math.round(oy));
        else if (ox > 40) {
          const gap = B.y >= A.y ? B.y - (A.y + A.h) : A.y - (B.y + B.h);
          if (gap > 0 && gap < 14) probs.push('贴太近[gap=' + Math.round(gap) + '] ' + A.t + ' → ' + B.t);
        }
      }
    }
    out.push({ page: i + 1, problems: probs.slice(0, 8), n: texts.length });
  });
  return out;
}"""

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    if not _HAS_PLAYWRIGHT:
        print("[SKIP] 本机解释器 %s 未安装 playwright，拥挤探针跳过。"
              "（缺环境不算产物问题；要跑请换装了 playwright 的解释器，"
              "禁临时安装）" % sys.executable)
        sys.exit(0)
    path = os.path.abspath(sys.argv[1]).replace('\\', '/')
    if not path.startswith('file:'):
        path = 'file:///' + path.lstrip('/')
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto(path)
        pg.wait_for_timeout(2200)
        results = pg.evaluate(JS)
        b.close()
    bad = 0
    for r in results:
        tag = "OK" if not r["problems"] else "问题"
        print(f"P{r['page']} [{tag}] 文本块{r['n']}")
        for q in r["problems"]:
            print("   -", q)
            bad += 1
    print(f"\n汇总：{len(results)} 页，{bad} 处问题" + ("（全净）" if bad == 0 else ""))

if __name__ == "__main__":
    main()
