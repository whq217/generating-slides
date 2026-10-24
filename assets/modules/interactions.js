/* ============================================================
   交互四件套（基本件，2026-10-21 v2 原生重写）：
   E 编辑 / D 画笔 / S 演讲者 / preview 模式（N 提词面板已移除 2026-10-24，职责归 S 演讲者窗口备注卡）
   守卫纪律：编辑态/预览态不翻页；画笔右键清屏；
   E/D/S 在 contenteditable 聚焦时不触发；禁自动恢复 localStorage
   依赖 core.js 的 slides/cur/NOTES/paint/go（顶层共享变量）
   ============================================================ */

// ========== Preview-only 模式（演讲者 iframe 预览：?preview=N 只渲染第 N 页，隐藏 chrome） ==========
(function () {
  var m = /[?&]preview=(\d+)/.exec(location.search || '');
  if (!m) return;
  var targetIdx = parseInt(m[1], 10) - 1;
  window.__previewOnly = true;
  window.__previewIdx = targetIdx;
  var style = document.createElement('style');
  style.textContent = '.pen-toggle,.pen-canvas,.spk-toggle,.edit-hotzone,.edit-toggle{display:none!important}'
    // CSS 层直接显示目标页（零时序依赖兜底；nth 特异度压过 .slide.active 源码默认）
    + ' .slide{display:none!important}'
    + ' .slide:nth-of-type(' + (Math.max(1, targetIdx + 1)) + '){display:flex!important;flex-direction:column!important}';
  document.head.appendChild(style);
  // JS 层补切 active 类（与 CSS 双保险；file+query 文档脚本时序不可靠，2026-10-21 headless 实测）
  var jump = function () {
    var ss = document.querySelectorAll('.slide');
    if (!ss.length) { if (jump.n++ < 50) setTimeout(jump, 100); return; }
    var t = Math.max(0, Math.min(ss.length - 1, targetIdx));
    ss.forEach(function (s, i) { s.classList.toggle('active', i === t); });
  };
  jump.n = 0;
  if (document.readyState === 'complete') jump();
  else window.addEventListener('DOMContentLoaded', jump);
})();

// ========== 画笔（D 键 / 右下角按钮；红色 3px 圆头，右键清屏，翻页自动清） ==========
var penCanvas = document.getElementById('penCanvas'), penCtx = penCanvas.getContext('2d'), penToggle = document.getElementById('penToggle'), isPen = false, isDraw = false;
function resizePen() { penCanvas.width = window.innerWidth; penCanvas.height = window.innerHeight; }
resizePen(); window.addEventListener('resize', resizePen);
function clearPen() { penCtx.clearRect(0, 0, penCanvas.width, penCanvas.height); }
function togglePen() { isPen = !isPen; penCanvas.classList.toggle('active', isPen); penToggle.classList.toggle('active', isPen); }
penToggle.addEventListener('click', togglePen);
penCanvas.addEventListener('mousedown', function (e) {
  if (e.button === 2) return;
  isDraw = true;
  penCtx.lineWidth = 3; penCtx.lineCap = 'round'; penCtx.lineJoin = 'round'; penCtx.strokeStyle = 'rgba(255,50,50,0.9)';
  penCtx.beginPath(); penCtx.moveTo(e.clientX, e.clientY);
});
penCanvas.addEventListener('mousemove', function (e) { if (!isDraw) return; penCtx.lineTo(e.clientX, e.clientY); penCtx.stroke(); });
penCanvas.addEventListener('mouseup', function () { isDraw = false; });
penCanvas.addEventListener('mouseleave', function () { isDraw = false; });
penCanvas.addEventListener('contextmenu', function (e) { e.preventDefault(); clearPen(); });

// ========== 编辑模式（E 键 / 左上角热区；叶子文本元素开 contenteditable，Done 退出并自动下载新 HTML） ==========
var editToggle = document.getElementById('editToggle'), hotzone = document.querySelector('.edit-hotzone'), isEdit = false, hideT;
function toggleEdit() {
  isEdit = !isEdit;
  document.body.classList.toggle('edit-mode', isEdit);
  editToggle.classList.toggle('active', isEdit);
  document.querySelectorAll('.slide').forEach(function (s) {
    s.querySelectorAll('div,p,span,li,h1,h2,h3,h4,strong,em,a').forEach(function (el) {
      if (!el.querySelector('div,section,nav')) el.contentEditable = isEdit ? 'true' : 'false';
    });
  });
  if (isEdit) { editToggle.textContent = 'Done'; editToggle.title = '退出编辑并导出 HTML (E)'; }
  else {
    editToggle.textContent = 'Edit'; editToggle.title = '编辑模式 (E)';
    // 0-23 修复：Save 名不副实（localStorage 只写不读是死写入）→ 改为导出新 HTML 文件，编辑结果真正可留
    try {
      var blob = new Blob(['<!DOCTYPE html>\n' + document.documentElement.outerHTML], { type: 'text/html' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = (document.title || 'deck').replace(/[\\/:*?"<>|]/g, '').slice(0, 40) + '-edited-' + new Date().toISOString().slice(0, 19).replace(/[T:]/g, '') + '.html';
      a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
    } catch (e) { /* 导出失败不阻断退出编辑 */ }
    document.querySelectorAll('[data-final]').forEach(function (el) { el.removeAttribute('data-final'); });  // 编辑后清缓存，重滚读新值
  }
}
editToggle.addEventListener('click', toggleEdit);
hotzone.addEventListener('mouseenter', function () { clearTimeout(hideT); editToggle.classList.add('show'); });
hotzone.addEventListener('mouseleave', function () { hideT = setTimeout(function () { if (!isEdit) editToggle.classList.remove('show'); }, 400); });
editToggle.addEventListener('mouseenter', function () { clearTimeout(hideT); });
editToggle.addEventListener('mouseleave', function () { hideT = setTimeout(function () { if (!isEdit) editToggle.classList.remove('show'); }, 400); });
hotzone.addEventListener('click', toggleEdit);

// ========== 演讲者模式（S 键：独立窗口 + iframe 像素级预览 + BroadcastChannel 双向同步） ==========
var spkToggle = document.getElementById('spkToggle');
var presenterWin = null;
var spkChannelName = 'slides-presenter-' + location.pathname;
var spkBc = null;
try { spkBc = new BroadcastChannel(spkChannelName); } catch (e) {}

function getSlideMeta() {
  var meta = [];
  slides.forEach(function (s, i) {
    var titleEl = s.querySelector('h2, h1');
    meta.push({
      title: titleEl ? titleEl.textContent.trim() : ('第 ' + (i + 1) + ' 页'),
      notes: (NOTES[s.id] || []).map(function (t) { return '<div>' + t + '</div>'; }).join('')
    });
  });
  return meta;
}

function toggleSpeaker() {
  if (presenterWin && !presenterWin.closed) { presenterWin.focus(); return; }
  var deckUrl = location.protocol + '//' + location.host + location.pathname;
  var slideMeta = getSlideMeta();
  var total = slides.length;
  var startIdx = cur;
  var storageKey = 'slides-presenter-layout:' + location.pathname;
  presenterWin = window.open('', 'slides-presenter', 'width=1280,height=820,menubar=no,toolbar=no');
  if (!presenterWin) { alert('请允许弹出窗口以使用演讲者视图'); return; }
  presenterWin.document.open();
  presenterWin.document.write(buildPresenterWindow(deckUrl, slideMeta, total, startIdx, storageKey));
  presenterWin.document.close();
  spkToggle.classList.add('active');
  // 0-23 三修：S 不再连锁主窗口提词面板——主窗口是投屏，面板会盖压轴句且观众可见；
  // 演讲者窗口自带 pcard-notes 备注卡，提词职责归它（原 10-21"主窗口跟开"需求就此废止）
  paint();
  paint();
  var checkClosed = setInterval(function () {
    if (presenterWin && presenterWin.closed) {
      clearInterval(checkClosed);
      presenterWin = null;
      spkToggle.classList.remove('active');
    }
  }, 500);
}

function buildPresenterWindow(deckUrl, slideMeta, total, startIdx, storageKey) {
  return '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><title>演讲者视图</title>'
  + '<style>'
  + '*{margin:0;padding:0;box-sizing:border-box}'
  + 'html,body{width:100%;height:100%;overflow:hidden;background:#1a1d24;color:#e6edf3;font-family:-apple-system,BlinkMacSystemFont,"Noto Sans SC",sans-serif}'
  + '#stage{position:absolute;inset:0;overflow:hidden}'
  + '.pcard{position:absolute;background:#0d1117;border:1px solid rgba(255,255,255,.1);border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,.45);display:flex;flex-direction:column;overflow:hidden;min-width:180px;min-height:100px;transition:box-shadow .2s,border-color .2s}'
  + '.pcard:hover{border-color:rgba(88,166,255,.3)}'
  + '.pcard-head{display:flex;align-items:center;gap:10px;padding:8px 12px;background:rgba(255,255,255,.04);border-bottom:1px solid rgba(255,255,255,.06);cursor:move;user-select:none;flex-shrink:0}'
  + '.pcard-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}'
  + '.pcard-title{font-size:11px;letter-spacing:.15em;text-transform:uppercase;font-weight:700;color:#8b949e;flex:1}'
  + '.pcard-meta{font-size:11px;color:#6e7681}'
  + '.pcard-body{flex:1;position:relative;overflow:hidden;min-height:0}'
  + '.pcard-preview .pcard-body{background:#000}'
  + '.pcard-preview iframe{position:absolute;top:0;left:0;width:1920px;height:1080px;border:none;transform-origin:top left;pointer-events:none;background:transparent}'
  + '.preview-end{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#484f58;font-size:14px;letter-spacing:.12em}'
  + '.pcard-notes .pcard-body{padding:14px 18px;overflow-y:auto;font-size:16px;line-height:1.75;color:#d0d7de;font-family:"Noto Sans SC",-apple-system,sans-serif}'
  + '.pcard-notes .pcard-body:empty::before{content:"（这一页还没有备注）";color:#484f58;font-style:italic}'
  + '.pcard-notes .pcard-body:focus{outline:none;background:rgba(255,255,255,.03);border-radius:4px}'
  + '.pcard-notes .pcard-body div{margin-bottom:6px}'
  + '.pcard-timer .pcard-body{display:flex;flex-direction:column;gap:14px;padding:18px 20px;justify-content:center}'
  + '.timer-display{font-family:"SF Mono","JetBrains Mono",monospace;font-size:42px;font-weight:700;color:#3fb950;letter-spacing:.04em;line-height:1}'
  + '.timer-row{display:flex;align-items:center;gap:12px;font-size:14px;color:#8b949e}'
  + '.timer-row .label{font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#6e7681}'
  + '.timer-row .val{color:#e6edf3;font-weight:600;font-family:"SF Mono",monospace}'
  + '.timer-controls{display:flex;gap:8px;flex-wrap:wrap}'
  + '.timer-btn{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);color:#e6edf3;padding:6px 12px;border-radius:6px;font-size:12px;cursor:pointer;font-family:inherit}'
  + '.timer-btn:hover{background:rgba(88,166,255,.15);border-color:#58a6ff}'
  + '.pcard-resize{position:absolute;right:0;bottom:0;width:18px;height:18px;cursor:nwse-resize;z-index:5;background:linear-gradient(135deg,transparent 50%,rgba(255,255,255,.25) 50%,rgba(255,255,255,.25) 60%,transparent 60%,transparent 70%,rgba(255,255,255,.25) 70%,rgba(255,255,255,.25) 80%,transparent 80%)}'
  + '.pcard-resize:hover{background:linear-gradient(135deg,transparent 50%,#58a6ff 50%,#58a6ff 60%,transparent 60%,transparent 70%,#58a6ff 70%,#58a6ff 80%,transparent 80%)}'
  + '.hint-bar{position:fixed;bottom:0;left:0;right:0;background:rgba(0,0,0,.6);backdrop-filter:blur(10px);border-top:1px solid rgba(255,255,255,.08);padding:6px 16px;font-size:11px;color:#8b949e;display:flex;gap:18px;align-items:center;z-index:1000}'
  + '.hint-bar kbd{background:rgba(255,255,255,.08);padding:1px 6px;border-radius:3px;font-family:"SF Mono",monospace;font-size:10px;border:1px solid rgba(255,255,255,.1);color:#e6edf3}'
  + '.reset-layout{margin-left:auto;background:transparent;border:1px solid rgba(255,255,255,.15);color:#8b949e;padding:3px 10px;border-radius:4px;font-size:11px;cursor:pointer;font-family:inherit}'
  + '.reset-layout:hover{background:rgba(248,81,73,.15);border-color:#f85149;color:#f85149}'
  + 'body.is-dragging *{user-select:none!important}'
  + 'body.is-dragging iframe{pointer-events:none!important}'
  + '</style></head><body>'
  + '<div id="stage">'
  + '<div class="pcard pcard-preview" id="card-cur"><div class="pcard-head" data-drag><span class="pcard-dot" style="background:#58a6ff"></span><span class="pcard-title">当前页</span><span class="pcard-meta" id="cur-meta">-</span></div><div class="pcard-body"><iframe id="iframe-cur"></iframe></div><div class="pcard-resize" data-resize></div></div>'
  + '<div class="pcard pcard-preview" id="card-nxt"><div class="pcard-head" data-drag><span class="pcard-dot" style="background:#bc8cff"></span><span class="pcard-title">下一页</span><span class="pcard-meta" id="nxt-meta">-</span></div><div class="pcard-body"><iframe id="iframe-nxt"></iframe></div><div class="pcard-resize" data-resize></div></div>'
  + '<div class="pcard pcard-notes" id="card-notes"><div class="pcard-head" data-drag><span class="pcard-dot" style="background:#f0883e"></span><span class="pcard-title">备注（可编辑）</span></div><div class="pcard-body" id="notes-body" contenteditable="true"></div><div class="pcard-resize" data-resize></div></div>'
  + '<div class="pcard pcard-timer" id="card-timer"><div class="pcard-head" data-drag><span class="pcard-dot" style="background:#3fb950"></span><span class="pcard-title">计时器</span></div><div class="pcard-body"><div class="timer-display" id="timer-display">00:00</div><div class="timer-row"><span class="label">页码</span><span class="val" id="timer-count">1 / ' + total + '</span></div><div class="timer-controls"><button class="timer-btn" id="btn-prev">&larr; 上一页</button><button class="timer-btn" id="btn-next">下一页 &rarr;</button><button class="timer-btn" id="btn-reset">&#9201; 重置</button></div></div><div class="pcard-resize" data-resize></div></div>'
  + '</div>'
  + '<div class="hint-bar"><span><kbd>&larr; &rarr;</kbd> 翻页</span><span><kbd>R</kbd> 重置计时</span><span><kbd>Esc</kbd> 关闭</span><span style="color:#6e7681">拖动卡片头部移动 &middot; 拖动右下角调整大小 &middot; 备注可直接编辑</span><button class="reset-layout" id="reset-layout">重置布局</button></div>'
  + '<scr' + 'ipt>'
  + '(function(){'
  + 'var slideMeta=' + JSON.stringify(slideMeta) + ';'
  + 'var total=' + total + ';'
  + 'var idx=' + startIdx + ';'
  + 'var deckUrl=' + JSON.stringify(deckUrl) + ';'
  + 'var STORAGE_KEY=' + JSON.stringify(storageKey) + ';'
  + 'var bc;try{bc=new BroadcastChannel("slides-presenter-' + location.pathname + '");}catch(e){}'
  + 'var iframeCur=document.getElementById("iframe-cur"),iframeNxt=document.getElementById("iframe-nxt");'
  + 'var notesBody=document.getElementById("notes-body"),curMeta=document.getElementById("cur-meta"),nxtMeta=document.getElementById("nxt-meta");'
  + 'var timerDisplay=document.getElementById("timer-display"),timerCount=document.getElementById("timer-count");'
  + 'function defaultLayout(){var w=window.innerWidth,h=window.innerHeight-36;return{"card-cur":{x:16,y:16,w:Math.round(w*.55)-24,h:Math.round(h*.62)-16},"card-nxt":{x:Math.round(w*.55)+8,y:16,w:w-Math.round(w*.55)-24,h:Math.round(h*.42)-16},"card-notes":{x:Math.round(w*.55)+8,y:Math.round(h*.42)+8,w:w-Math.round(w*.55)-24,h:h-Math.round(h*.42)-16},"card-timer":{x:16,y:Math.round(h*.62)+8,w:Math.round(w*.55)-24,h:h-Math.round(h*.62)-16}};}'
  + 'function applyLayout(l){Object.keys(l).forEach(function(id){var el=document.getElementById(id);if(el&&l[id]){el.style.left=l[id].x+"px";el.style.top=l[id].y+"px";el.style.width=l[id].w+"px";el.style.height=l[id].h+"px";}});rescaleAll();}'
  + 'function readLayout(){try{var s=localStorage.getItem(STORAGE_KEY);if(s)return JSON.parse(s);}catch(e){}return defaultLayout();}'
  + 'function saveLayout(){var l={};["card-cur","card-nxt","card-notes","card-timer"].forEach(function(id){var el=document.getElementById(id);if(el)l[id]={x:parseInt(el.style.left,10)||0,y:parseInt(el.style.top,10)||0,w:parseInt(el.style.width,10)||300,h:parseInt(el.style.height,10)||200};});try{localStorage.setItem(STORAGE_KEY,JSON.stringify(l));}catch(e){}}'
  + 'function rescaleIframe(iframe){if(!iframe||iframe.style.display==="none")return;var body=iframe.parentElement,cw=body.clientWidth,ch=body.clientHeight;if(!cw||!ch)return;var s=Math.min(cw/1920,ch/1080);iframe.style.transform="scale("+s+")";var sw=1920*s,sh=1080*s;iframe.style.left=Math.max(0,(cw-sw)/2)+"px";iframe.style.top=Math.max(0,(ch-sh)/2)+"px";}'
  + 'function rescaleAll(){rescaleIframe(iframeCur);rescaleIframe(iframeNxt);}'
  + 'window.addEventListener("resize",rescaleAll);'
  + 'document.querySelectorAll("[data-drag]").forEach(function(handle){handle.addEventListener("mousedown",function(e){if(e.button!==0)return;var card=handle.closest(".pcard");if(!card)return;e.preventDefault();document.body.classList.add("is-dragging");var sx=e.clientX,sy=e.clientY,sl=parseInt(card.style.left,10)||0,st=parseInt(card.style.top,10)||0;function onM(ev){card.style.left=Math.max(0,Math.min(window.innerWidth-100,sl+ev.clientX-sx))+"px";card.style.top=Math.max(0,Math.min(window.innerHeight-50,st+ev.clientY-sy))+"px";}function onU(){document.body.classList.remove("is-dragging");document.removeEventListener("mousemove",onM);document.removeEventListener("mouseup",onU);saveLayout();}document.addEventListener("mousemove",onM);document.addEventListener("mouseup",onU);});});'
  + 'document.querySelectorAll("[data-resize]").forEach(function(handle){handle.addEventListener("mousedown",function(e){if(e.button!==0)return;var card=handle.closest(".pcard");if(!card)return;e.preventDefault();e.stopPropagation();document.body.classList.add("is-dragging");var sx=e.clientX,sy=e.clientY,sw=parseInt(card.style.width,10)||card.offsetWidth,sh=parseInt(card.style.height,10)||card.offsetHeight;function onM(ev){card.style.width=Math.max(180,sw+ev.clientX-sx)+"px";card.style.height=Math.max(100,sh+ev.clientY-sy)+"px";if(card.querySelector("iframe"))rescaleIframe(card.querySelector("iframe"));}function onU(){document.body.classList.remove("is-dragging");document.removeEventListener("mousemove",onM);document.removeEventListener("mouseup",onU);rescaleAll();saveLayout();}document.addEventListener("mousemove",onM);document.addEventListener("mouseup",onU);});});'
  + 'var iframeReady={cur:false,nxt:false};'
  + 'window.addEventListener("message",function(e){if(!e.data||e.data.type!=="preview-ready")return;'
  + 'if(e.source===iframeCur.contentWindow){iframeReady.cur=true;postGoto(iframeCur,idx);}'
  + 'if(e.source===iframeNxt.contentWindow){iframeReady.nxt=true;postGoto(iframeNxt,idx+1<total?idx+1:idx);}'
  + 'rescaleAll();});'
  + 'function postGoto(iframe,n){try{iframe.contentWindow.postMessage({type:"presenter-goto",idx:n},"*");}catch(e){}}'
  + 'function update(n){n=Math.max(0,Math.min(total-1,n));idx=n;'
  + 'if(iframeReady.cur)postGoto(iframeCur,n);curMeta.textContent=(n+1)+"/"+total;'
  + 'if(n+1<total){iframeNxt.style.display="";var endEl=document.querySelector("#card-nxt .preview-end");if(endEl)endEl.remove();if(iframeReady.nxt)postGoto(iframeNxt,n+1);nxtMeta.textContent=(n+2)+"/"+total;}'
  + 'else{iframeNxt.style.display="none";var body=document.querySelector("#card-nxt .pcard-body");if(body&&!body.querySelector(".preview-end")){var end=document.createElement("div");end.className="preview-end";end.textContent="— 已是最后一页 —";body.appendChild(end);}nxtMeta.textContent="END";}'
  + 'notesBody.innerHTML=slideMeta[n].notes||"";'
  + 'timerCount.textContent=(n+1)+" / "+total;'
  + 'saveNotesBack();}'
  + 'var tStart=Date.now();'
  + 'var timerIv=setInterval(function(){var s=Math.floor((Date.now()-tStart)/1000),mm=String(Math.floor(s/60)).padStart(2,"0"),ss=String(s%60).padStart(2,"0");timerDisplay.textContent=mm+":"+ss;},1000);'
  + 'function resetTimer(){tStart=Date.now();timerDisplay.textContent="00:00";}'
  + 'function saveNotesBack(){try{var bc2=new BroadcastChannel("slides-presenter-' + location.pathname + '");bc2.postMessage({type:"notes-update",idx:idx,notes:notesBody.innerHTML});setTimeout(function(){bc2.close();},100);}catch(e){}}'
  + 'notesBody.addEventListener("blur",saveNotesBack);'
  + 'if(bc){bc.onmessage=function(e){if(!e.data)return;if(e.data.type==="go")update(e.data.idx);else if(e.data.type==="notes-update"){slideMeta[e.data.idx]=slideMeta[e.data.idx]||{};slideMeta[e.data.idx].notes=e.data.notes;}};}'
  + 'function go(n){update(n);if(bc)bc.postMessage({type:"go",idx:idx});}'
  + 'document.getElementById("btn-prev").addEventListener("click",function(){go(idx-1);});'
  + 'document.getElementById("btn-next").addEventListener("click",function(){go(idx+1);});'
  + 'document.getElementById("btn-reset").addEventListener("click",resetTimer);'
  + 'document.getElementById("reset-layout").addEventListener("click",function(){if(confirm("恢复默认卡片布局？")){try{localStorage.removeItem(STORAGE_KEY);}catch(e){}applyLayout(defaultLayout());}});'
  + 'document.addEventListener("keydown",function(e){if(e.metaKey||e.ctrlKey||e.altKey)return;switch(e.key){case"ArrowRight":case" ":case"PageDown":go(idx+1);e.preventDefault();break;case"ArrowLeft":case"PageUp":go(idx-1);e.preventDefault();break;case"Home":go(0);break;case"End":go(total-1);break;case"r":case"R":resetTimer();break;case"Escape":window.close();break;}});'
  + 'iframeCur.addEventListener("load",function(){rescaleIframe(iframeCur);});'
  + 'iframeNxt.addEventListener("load",function(){rescaleIframe(iframeNxt);});'
  + 'applyLayout(readLayout());'
  + 'iframeCur.src=deckUrl+"?preview="+(idx+1);'
  + 'if(idx+1<total)iframeNxt.src=deckUrl+"?preview="+(idx+2);'
  + 'notesBody.innerHTML=slideMeta[idx].notes||"";'
  + 'curMeta.textContent=(idx+1)+"/"+total;'
  + 'nxtMeta.textContent=(idx+2<total?(idx+2)+"/"+total:"END");'
  + 'timerCount.textContent=(idx+1)+" / "+total;'
  + '})();'
  + '</scr' + 'ipt></body></html>';
}

// 主窗口：接收演讲者窗口消息——go 跟翻（双屏同步）、备注编辑回写 NOTES
if (spkBc) {
  spkBc.onmessage = function (e) {
    if (!e.data) return;
    if (e.data.type === 'go' && typeof e.data.idx === 'number') __goto(e.data.idx);   // 收广播只跳页不回播（防多实例回声回环，2026-10-24）
    else if (e.data.type === 'notes-update' && typeof e.data.idx === 'number') {
      var s = slides[e.data.idx];
      if (!s) return;
      var tmp = document.createElement('div');
      tmp.innerHTML = e.data.notes || '';
      var arr = [];
      tmp.querySelectorAll('div,li,p').forEach(function (el) { var t = el.textContent.trim(); if (t) arr.push(t); });
      if (!arr.length && tmp.textContent.trim()) arr.push(tmp.textContent.trim());
      NOTES[s.id] = arr;
      paint();
    }
  };
}
spkToggle.addEventListener('click', toggleSpeaker);

// ========== Preview-only：只听翻页指令（跳页已在前置检测块完成；iframe 内不广播，防 nxt 预览污染主窗口） ==========
if (window.__previewOnly) {
  window.addEventListener('message', function (e) {
    if (!e.data) return;
    if (e.data.type === 'presenter-goto') __goto(parseInt(e.data.idx, 10));   // 同页短路防重播（2026-10-24）
  });
  try { window.parent && window.parent.postMessage({ type: 'preview-ready' }, '*'); } catch (ex) {}
}
