/* ============================================================
   数字滚动（动画件，按需装配；2026-10-21 v2 原生）
   读数字元素终值自动滚，生成端零属性配合：
   命中 .hero-num / .metric .mv / .num / .roll
   千分位/小数位/正负号/单位（small）原样保留；
   data-final 缓存终值供重播；编辑态与 reduced-motion 跳过。
   驱动用 setTimeout(16ms)——headless/打印等无帧环境同样可跑。
   ============================================================ */
var REDUCE_MOTION = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function rollNums(slide) {
  if (!slide || REDUCE_MOTION || document.body.classList.contains('edit-mode')) return;
  slide.querySelectorAll('.hero-num, .metric .mv, .num, .roll').forEach(function (el) {
    if (el.querySelector('canvas,svg')) return;
    var tn = null;
    for (var i = 0; i < el.childNodes.length; i++) {
      if (el.childNodes[i].nodeType === 3 && el.childNodes[i].nodeValue.trim()) { tn = el.childNodes[i]; break; }
    }
    if (!tn) return;
    var finalText = el.getAttribute('data-final') || tn.nodeValue;
    el.setAttribute('data-final', finalText);
    var m = /([+-]?)([\d,]+(?:\.\d+)?)/.exec(finalText.trim());
    if (!m) return;
    var target = parseFloat(m[2].replace(/,/g, ''));
    if (!isFinite(target) || target === 0) return;
    var dec = m[2].indexOf('.') === -1 ? 0 : m[2].split('.')[1].length;
    var hasComma = m[2].indexOf(',') !== -1;
    var pre = finalText.trim().slice(0, m.index) + m[1];
    var suf = finalText.trim().slice(m.index + m[0].length);
    function fmt(v) {
      var s = v.toFixed(dec);
      if (hasComma) { var p = s.split('.'); p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ','); s = p.join('.'); }
      return pre + s + suf;
    }
    var t0 = performance.now(), DUR = 1100;
    (function tick() {
      var pr = Math.min((performance.now() - t0) / DUR, 1);
      var ease = 1 - Math.pow(1 - pr, 3);
      tn.nodeValue = fmt(target * ease);
      if (pr < 1) setTimeout(tick, 16); else tn.nodeValue = fmt(target);   // setTimeout 驱动：headless/打印等无帧环境同样可跑
    })();
  });
}

/* ============================================================
   step 叙事（逐步揭示，2026-10-21 v2 原生）
   元素挂 class="step"（焦点数字可挂 "step impact" 弹入）；
   点击/翻页键：先逐个亮出本页 step，全亮完才翻页；左向逆序收起。
   纪律（承 v1 初见密度教训）：同类正文组首条不挂 step，防「翻到即空页」。
   ============================================================ */
function __stepReset(slide) {
  if (!slide) return;
  slide.querySelectorAll('.step').forEach(function (el) { el.classList.remove('on'); });
  slide.__spotIdx = -1;
  __spotApply(slide);
}
function __stepConsume(dir) {
  var s = slides[cur];
  if (!s) return false;
  var steps = s.querySelectorAll('.step');
  if (steps.length) {
    var shown = s.querySelectorAll('.step.on');
    if (dir >= 0) {
      if (shown.length < steps.length) { steps[shown.length].classList.add('on'); return true; }
      return false;                                       // 全亮完 → 放行翻页
    } else {
      if (shown.length > 0) { shown[shown.length - 1].classList.remove('on'); return true; }
      return false;                                       // 全收完 → 放行回上一页
    }
  }
  return __spotConsume(s, dir);                           // 本页无 .step → 聚光式接管
}

/* ============================================================
   聚光式 step（2026-10-22 软拦截版）：并列板块"讲到谁亮谁"。
   组容器挂 class="spot-group"，子项按 DOM 序为聚光序列。
   节奏（维护者实测裁定）：初始全亮 → 点按逐项聚光 → 末项后即放行翻页
   （内容全可见=软拦截，动画服务讲述不绑架讲述，无"收束态"）。
   单点模式：容器加 data-spot="1"（只聚光第 1 项，点一下→再点翻页）；
   遍历模式默认全项。使用前提：客户明确要求的讲述编排才配（按需件，
   生成端推断不出讲述意图，禁自动添加）；组直接子项不挂 .rv。
   ============================================================ */
function __spotApply(slide) {
  var items = slide.querySelectorAll('.spot-group > *');
  var idx = slide.__spotIdx;
  items.forEach(function (el, i) {
    el.classList.toggle('spot-dim', idx >= 0 && idx < items.length && i !== idx);
  });
}
function __spotConsume(s, dir) {
  var items = s.querySelectorAll('.spot-group > *');
  if (!items.length) return false;
  var group = s.querySelector('.spot-group');          // data-spot 挂组容器（一页一组纪律）
  var N = Math.min(parseInt(group.getAttribute('data-spot') || items.length, 10) || items.length, items.length);
  var idx = s.__spotIdx == null ? -1 : s.__spotIdx;      // -1 初始全亮 … 0..N-1 聚光
  if (dir >= 0) {
    if (idx < N - 1) { s.__spotIdx = idx + 1; __spotApply(s); return true; }
    return false;                                        // 末项聚光后 → 放行翻页
  } else {
    if (idx > -1) { s.__spotIdx = idx - 1; __spotApply(s); return true; }
    return false;                                        // 退回初始态 → 放行回上一页
  }
}

/* ============================================================
   折线精确描线：量每条 .line 真实长度写入 --len（dasharray 写死 2600 时
   线长 550 的折线前 20% 动画在空白期后突然出现——2026-10-21 维护者实测生硬）
   ============================================================ */
document.addEventListener('slide:enter', function (e) {
  var slide = e.target;
  if (!slide || !slide.querySelectorAll) return;
  slide.querySelectorAll('.chart .line').forEach(function (p) {
    if (p.dataset.lenDone) return;
    try { p.style.setProperty('--len', p.getTotalLength()); p.dataset.lenDone = '1'; } catch (err) {}
  });
});

/* ============================================================
   3D 悬停（品牌风卡片可选）：挂 .tilt-card 自动生效；reduced-motion 跳过
   ============================================================ */
(function () {
  if (REDUCE_MOTION) return;
  document.querySelectorAll('.tilt-card').forEach(function (card) {
    card.addEventListener('mousemove', function (e) {
      var r = card.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5;
      var y = (e.clientY - r.top) / r.height - 0.5;
      card.style.transform = 'rotateY(' + (x * 8) + 'deg) rotateX(' + (-y * 8) + 'deg)';
    });
    card.addEventListener('mouseleave', function () { card.style.transform = 'rotateY(0) rotateX(0)'; });
  });
})();

/* ============================================================
   粒子背景（科技氛围签名，Neon Cyber/Data Dark 类）：页面含 .particle-canvas 才初始化
   ============================================================ */
(function () {
  var canvas = document.querySelector('.particle-canvas');
  if (!canvas || REDUCE_MOTION) return;
  var ctx = canvas.getContext('2d');
  var accent = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#E8A33D';
  var particles = [], COUNT = 48, MAXD = 130;
  function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
  resize(); window.addEventListener('resize', resize);
  for (var i = 0; i < COUNT; i++) {
    particles.push({ x: Math.random() * canvas.width, y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.32, vy: (Math.random() - 0.5) * 0.32, r: Math.random() * 1.5 + 0.5 });
  }
  (function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fillStyle = accent; ctx.globalAlpha = 0.55; ctx.fill();
      for (var j = i + 1; j < particles.length; j++) {
        var q = particles[j], dx = p.x - q.x, dy = p.y - q.y, d = Math.sqrt(dx * dx + dy * dy);
        if (d < MAXD) {
          ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y);
          ctx.strokeStyle = accent; ctx.globalAlpha = 0.14 * (1 - d / MAXD); ctx.lineWidth = 0.5; ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  })();
})();

/* ============================================================
   打字机（点名单用）：挂 .typewriter，首次进场逐字显示
   ============================================================ */
var twDone = new Set();
document.addEventListener('slide:enter', function (e) {
  var slide = e.target;
  if (twDone.has(slide.id) || REDUCE_MOTION) return;
  var els = slide.querySelectorAll('.typewriter');
  if (!els.length) return;
  twDone.add(slide.id);
  els.forEach(function (el, k) {
    var text = el.textContent;
    el.textContent = '';
    el.classList.add('tw-on');
    var delay = 300 + k * 600;
    text.split('').forEach(function (ch, i) {
      setTimeout(function () {
        var sp = document.createElement('span');
        sp.className = 'tw-ch';
        sp.textContent = ch;
        el.appendChild(sp);
      }, delay + i * 70);
    });
  });
});
