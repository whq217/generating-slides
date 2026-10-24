/* 用法（2026-10-22 补，直跑 node 会报 window 未定义——本脚本是浏览器注入型）：
   1. 把本脚本文本注入产物【最后一个】</body> 前——禁用 replace 首匹配：装配 JS 的演讲者窗口模板里
      含字符串字面量 '</body>'（先于真闭合标签出现），首匹配会把脚本注进 JS 字符串导致 NO REPORT（2026-10-21 实测坑）。
      写法：i = deck.lastIndexOf('<\/body>'); deck.slice(0,i) + '<script>' + 本文件 + '<\/script>' + deck.slice(i)
      （注释里的闭合 script 标签必须带反斜杠转义，否则 HTML 解析器会提前截断注入脚本）
   2. chrome --headless=new --disable-gpu --allow-file-access-from-files --virtual-time-budget=20000 --dump-dom "file:///产物.html"
   3. 从 dump 里 grep 'REPORT::' 取版率行（titleBox / contentBox 面积占比，剔除边注四件套）
      + 欠填行 vacMax（最大连续空带）/ vacBottom（底部连续空带），判定口径 → layout-rules §1.2b
   2026-10-21 兼容补：入场类复位扩展到 .reveal 系（测外部产物用；本包 .rv 不受影响）
   2026-10-22 欠填补：vacuum 带（治"overflow 只测溢出不测欠填"——下半大空而探针全过的实测病） */
(function () {
  function leafHasText(el) {
    if (!el.textContent || !el.textContent.trim()) return false;
    for (var i = 0; i < el.children.length; i++) {
      if (el.children[i].textContent && el.children[i].textContent.trim()) return false;
    }
    return true;
  }
  function boxOf(list) {
    var x1 = 1e9, y1 = 1e9, x2 = -1e9, y2 = -1e9;
    list.forEach(function (r) {
      x1 = Math.min(x1, r.left); y1 = Math.min(y1, r.top);
      x2 = Math.max(x2, r.right); y2 = Math.max(y2, r.bottom);
    });
    return { x: x1, y: y1, w: x2 - x1, h: y2 - y1 };
  }
  window.addEventListener('load', function () {
    setTimeout(function () {
      var out = [];
      var slides = document.querySelectorAll('section.slide');
      var savedStyles = [];
      slides.forEach(function (s) {
        savedStyles.push([s, s.getAttribute('style') || '']);
        s.style.cssText += ';display:block !important;visibility:visible !important;opacity:1 !important;position:absolute !important;top:0 !important;left:0 !important;transform:none !important;';
        s.querySelectorAll('.rv, .reveal, .reveal-scale, .reveal-left, .reveal-blur').forEach(function (el) {
          el.style.opacity = '1'; el.style.transform = 'none';
        });
      });
      try {
        slides.forEach(function (s, i) {
          var pr = s.getBoundingClientRect();
          if (pr.width < 10) return;
          var titles = [];
          s.querySelectorAll('h1,h2').forEach(function (t) {
            var r = t.getBoundingClientRect();
            if (r.width > 10 && t.textContent.trim()) titles.push(t);
          });
          var titleRects = titles.map(function (t) { return t.getBoundingClientRect(); });
          var titleSet = new Set(titles);
          var contentRects = [];
          s.querySelectorAll('*').forEach(function (el) {
            if (titleSet.has(el)) return;
            if (el.closest('.folio, .footmark, .corner-note, .hint')) return;
          if (el.closest('.deco')) return;  // 装饰层不计版率（2026-10-23 立：装饰参与构图但探针不算数；CSS-only 装饰天然不计，此行兜底装饰带文字的场景）
            var st = getComputedStyle(el);
            if (st.display === 'none' || st.visibility === 'hidden' || parseFloat(st.opacity) === 0) return;
            if (!leafHasText(el)) return;
            var r = el.getBoundingClientRect();
            if (r.width < 2 || r.height < 2) return;
            contentRects.push(r);
          });
          var id = s.id || s.getAttribute('data-slide-id') || (s.getAttribute('data-title') || '') || ('idx' + i);
          var line = '#' + i + ' ' + id + ' page=' + Math.round(pr.width) + 'x' + Math.round(pr.height);
          if (titleRects.length) {
            var tb = boxOf(titleRects);
            line += ' | titleBox w=' + Math.round(tb.w / pr.width * 100) + '% h=' + Math.round(tb.h / pr.height * 100) + '%';
          } else { line += ' | titleBox none'; }
          if (contentRects.length) {
            var cb = boxOf(contentRects);
            line += ' | contentBox(除标题) w=' + Math.round(cb.w / pr.width * 100) + '% h=' + Math.round(cb.h / pr.height * 100) + '% area=' + Math.round(cb.w * cb.h / (pr.width * pr.height) * 100) + '%';
          } else { line += ' | contentBox none'; }
          // 欠填探针（2026-10-22 立）：页高垂直切 10 带占空，报底部连续空带 + 最大连续空带。
          // 占带集合 = 文本叶子（同 contentBox 口径，剔边注四件套）+ img/canvas/svg
          // （ECharts 渲 canvas 无 DOM 文本，不纳入则图表页必误报）
          var occ = [];
          for (var k = 0; k < 10; k++) occ.push(false);
          function occupy(r) {
            var a = Math.max(0, Math.floor((r.top - pr.top) / pr.height * 10));
            var b = Math.min(10, Math.ceil((r.bottom - pr.top) / pr.height * 10));
            for (var k = a; k < b; k++) occ[k] = true;
          }
          contentRects.forEach(occupy);
          s.querySelectorAll('img,canvas,svg').forEach(function (el) {
            if (el.closest('.deco')) return;  // 装饰装置（svg 画的柱阵/图形等）不计占位——与文本口径同排除
            var st2 = getComputedStyle(el);
            if (st2.display === 'none' || st2.visibility === 'hidden' || parseFloat(st2.opacity) === 0) return;
            var r = el.getBoundingClientRect();
            if (r.width < 2 || r.height < 2) return;
            occupy(r);
          });
          var vacMax = 0, run = 0, vacBottom = 0;
          for (var k = 0; k < 10; k++) { run = occ[k] ? 0 : run + 1; if (run > vacMax) vacMax = run; }
          for (var k = 9; k >= 0 && !occ[k]; k--) vacBottom++;
          line += ' | vacMax=' + vacMax + ' vacBottom=' + vacBottom + '/10';
          out.push(line);
        });
      } finally {
        savedStyles.forEach(function (p) {
          if (p[1]) p[0].setAttribute('style', p[1]); else p[0].removeAttribute('style');
        });
      }
      var d = document.createElement('div');
      d.id = 'layout-report';
      d.textContent = 'REPORT::' + out.join(' ;; ');
      document.body.appendChild(d);
    }, 800);
  });
})();