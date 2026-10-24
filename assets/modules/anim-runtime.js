/* ============================================================
   代码动画运行时（2026-10-21 · v6 规格平移 v2 底盘）
   只管生命周期，不懂绘制：生成端逐页写绘制逻辑（anim-recipes 五配方），
   注册进来即获得——首次进场起播 / 翻回自动重播 / 切页即停 /
   reduced 直接终态 / 打印前终态 / 点击容器重播 / 时长硬顶 4s。
   ============================================================ */
var __anims = {};
function __anim(pageId, drawFn, opts) {
  __anims[pageId] = { fn: drawFn, opts: opts || {}, raf: null, timer: null };
}
function __animFinal(a) {
  if (a.raf) clearTimeout(a.raf);
  if (a.timer) clearTimeout(a.timer);
  a.raf = null; a.timer = null;
  try { a.h && a.h.final(); } catch (e) {}
}
function __animPlay(pageId) {
  var a = __anims[pageId];
  if (!a || !a.fn) return;
  __animFinal(a);                                   // 先归终态再重播（清上一轮）
  var dur = Math.min(4000, Math.max(600, a.opts.dur || 2000));   // v6 硬顶 4s
  var delay = Math.min(800, Math.max(0, a.opts.delay != null ? a.opts.delay : 300));
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  try { a.h = a.fn(); } catch (e) { return; }        // 绘制控制器实例化：{step(t), final()}
  if (!a.h || typeof a.h.final !== 'function') return;
  if (reduced) { a.h.final(); return; }              // reduced：直接终态，不跑
  a.timer = setTimeout(function () {
    var t0 = performance.now();
    (function tick() {
      var t = Math.min((performance.now() - t0) / dur, 1);
      try { a.h.step(t); } catch (e) { return; }
      if (t < 1) a.raf = setTimeout(tick, 16);       // setTimeout 驱动：headless/打印等无帧环境同样可跑（rollNums 同款教训）
      else { a.raf = null; a.h.final(); }            // 播完停终态，不循环
    })();
  }, delay);
}
document.addEventListener('slide:enter', function (e) {
  var id = e.target && e.target.id;
  if (id && __anims[id]) __animPlay(id);             // 首次/翻回都重播
});
window.addEventListener('beforeprint', function () { // 打印/PDF 前全部定格终态（未播过的先实例化再定格，防空白页）
  Object.keys(__anims).forEach(function (k) {
    var a = __anims[k];
    if (!a.h && a.fn) { try { a.h = a.fn(); } catch (e) { return; } }
    __animFinal(a);
  });
});
window.__anim = __anim;   // 生成端接口（底盘 JS 在 IIFE 内，不导出则页面脚本调不到）