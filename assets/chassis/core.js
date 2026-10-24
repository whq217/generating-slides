/* ============================================================
   底盘核心 JS：翻页 / 缩放 / 提词数据 / slide:enter 钩子 / 键盘分发
   模块接口（typeof 守卫调用，缺模块=功能静默禁用，永不报错）：
   · interactions.js → clearPen / toggleEdit / togglePen / toggleSpeaker / spkBc
   · effects.js      → rollNums
   ============================================================ */
var slides = document.querySelectorAll('.slide');
var cur = 0;

// 提词数据源（阶段 6 讲稿落点：每页 3-5 条要点；S 演讲者窗口备注卡读此数据源）
var NOTES = {
  p1: ["封面提词示例：一句话点破主题与场合。", "开场 30 秒说清「今天讲什么、为什么值得听」。"],
  p2: ["内容页提词示例：先抛主张，再走论据。", "关键数字停两拍，让听众看清量级。"]
};

function paint() {
  var ul = document.getElementById('notes-body');
  ul.innerHTML = '';
  (NOTES[slides[cur].id] || []).forEach(function (t) {
    var li = document.createElement('li');
    li.textContent = t;
    ul.appendChild(li);
  });
}

function __goto(n) {
  if (n < 0 || n >= slides.length || n === cur) return;   // 同页短路：同 channel 多实例广播回环时到此为止（2026-10-24 回环事故）
  slides[cur].classList.remove('active');
  cur = n;
  slides[cur].classList.add('active');
  if (typeof clearPen === 'function') clearPen();      // 翻页自动清笔迹
  if (typeof __stepReset === 'function') __stepReset(slides[cur]);   // step 叙事重置（离开再回来重播）
  paint();
  if (typeof rollNums === 'function') rollNums(slides[cur]);   // 数字滚动重播
  slides[cur].dispatchEvent(new CustomEvent('slide:enter', { detail: { index: cur }, bubbles: true }));  // ECharts/动画/typewriter 监听（bubbles 供 document 级监听收到）
}
function go(n) {
  __goto(n);
  if (typeof spkBc !== 'undefined' && spkBc && !window.__previewOnly) spkBc.postMessage({ type: 'go', idx: cur });  // 同步演讲者窗口；收消息方走 __goto 不回播，防 A↔B 回声死循环（2026-10-24）
}

// step 叙事消费（effects.js 提供；返回 true=本次交互被 step 吃掉不翻页）
function stepForward() { return typeof __stepConsume === 'function' && __stepConsume(1); }
function stepBack() { return typeof __stepConsume === 'function' && __stepConsume(-1); }

document.addEventListener('keydown', function (e) {
  if (window.__previewOnly) return;
  var inEd = !!(e.target && e.target.closest && e.target.closest('[contenteditable="true"],input,textarea'));
  if (e.key === 'e' || e.key === 'E') { if (!inEd && typeof toggleEdit === 'function') toggleEdit(); return; }
  if (e.key === 'd' || e.key === 'D') { if (!inEd && typeof togglePen === 'function') togglePen(); return; }
  if (e.key === 's' || e.key === 'S') { if (!inEd && typeof toggleSpeaker === 'function') toggleSpeaker(); return; }
  // N 提词面板已移除（2026-10-24）：主窗口是投屏观众可见，提词职责归 S 演讲者窗口备注卡
  if (e.key === 'p' || e.key === 'P') { if (!inEd && !document.body.classList.contains('edit-mode')) window.print(); return; }  // PDF 导出（print.css 已锁 16:9 分页）
  if (inEd) return;                                    // 输入态：翻页键还给文本操作
  if (document.body.classList.contains('edit-mode')) return;  // 编辑态：翻页键全禁（防打断编辑；退出用 E）
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') { e.preventDefault(); if (!stepForward()) go(cur + 1); }
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp' || e.key === 'PageUp') { e.preventDefault(); if (!stepBack()) go(cur - 1); }
});

// 点击/右键翻页守卫（判据=编辑态正在选字/点到交互控件才不翻；data-click-nav="off" 整页逃生）
// 0-24 修：选区判据限定编辑态——原版把放映态残留选区也当"正在选字"，点击翻页被静默拦死
// 只能刷新（WB v3 实测：P3 大数字被鼠标划过留下选区后，右半屏点击永久失效，键盘正常）。
function __flipBlocked(el) {
  if (document.body.classList.contains('edit-mode')
      && window.getSelection && String(window.getSelection()).trim()) return true;
  if (!el || !el.closest) return true;
  return !!el.closest('a,button,input,textarea,select,canvas,[contenteditable="true"]');
}
// 放映态 mousedown/touchstart 捕获阶段清残留选区（治"已经存在的选区"高亮残留；编辑态跳过）
['mousedown', 'touchstart'].forEach(function (ev) {
  document.addEventListener(ev, function () {
    if (document.body.classList.contains('edit-mode')) return;
    var sel = window.getSelection && window.getSelection();
    if (sel && String(sel).trim()) sel.removeAllRanges();
  }, true);
});
document.addEventListener('click', function (e) {
  if (window.__previewOnly) return;
  if (document.body.classList.contains('edit-mode')) return;
  if (document.documentElement.getAttribute('data-click-nav') === 'off') return;
  if (__flipBlocked(e.target)) return;
  if (e.clientX > window.innerWidth / 2) { if (!stepForward()) go(cur + 1); }
  else { if (!stepBack()) go(cur - 1); }
});
document.addEventListener('contextmenu', function (e) {
  if (typeof penCanvas === 'undefined' || !penCanvas || !penCanvas.classList.contains('active')) {
    // 画笔未激活时右键=上一页；激活时右键归画笔（清屏，见 interactions.js）
    if (window.__previewOnly) return;
    if (document.body.classList.contains('edit-mode')) return;
    if (document.documentElement.getAttribute('data-click-nav') === 'off') return;
    if (__flipBlocked(e.target)) return;
    e.preventDefault();
    go(cur - 1);
  }
});

function fit() {
  var s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
  document.getElementById('stage').style.transform = 'translate(-50%, -50%) scale(' + s + ')';
}
window.addEventListener('resize', fit);

function __chassisInit() {
  fit();
  paint();
  if (typeof rollNums === 'function') rollNums(slides[0]);
  if (slides[0]) slides[0].dispatchEvent(new CustomEvent('slide:enter', { detail: { index: 0 }, bubbles: true }));  // 首屏同样派发（typewriter 等监听）
}
