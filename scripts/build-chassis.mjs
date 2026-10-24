#!/usr/bin/env node
// build-chassis.mjs — 底盘装配脚本（确定性装配，AI 禁手拼禁手改产物）
//
// 用法：
//   node scripts/build-chassis.mjs                 全量装配（默认：core + 基本件 + 动画件）
//   node scripts/build-chassis.mjs --no-effects    精简装配（用户明说"不要动画"时才用）
//
// 装配表（顺序即依赖顺序：core 先载，模块函数靠 typeof 守卫，缺失=功能静默禁用）
// 改完 chassis/ 或 modules/ 后必须重跑本脚本，chassis-v2.html 是产物禁手改。

import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const read = (f) => readFileSync(join(root, 'assets', f), 'utf8');
const noEffects = process.argv.includes('--no-effects');

const CSS_MODULES = [
  'chassis/core.css',
  ...(noEffects ? [] : ['modules/effects.css']),
  'modules/interactions.css',
  'modules/print.css',
];
const JS_MODULES = [
  'chassis/core.js',
  'modules/interactions.js',
  ...(noEffects ? [] : ['modules/effects.js', 'modules/anim-runtime.js']),
];

const banner = `<!-- ⚠️ 本文件由 scripts/build-chassis.mjs 装配生成（${noEffects ? '精简装配 --no-effects' : '全量装配'}）——禁手改；改 assets/chassis/ 或 assets/modules/ 后重跑 build -->
`;

const css = CSS_MODULES.map((f) => `/* ===== ${f} ===== */\n` + read(f)).join('\n\n');
const js = JS_MODULES.map((f) => `// ===== ${f} =====\n` + read(f)).join('\n\n');
const tpl = read('chassis/template.html');

const out = tpl
  .replace('/*__CHASSIS_CSS__*/', () => css)
  .replace('/*__CHASSIS_JS__*/', () => js)
  .replace('<!DOCTYPE html>', '<!DOCTYPE html>\n' + banner);

// 装配校验：关键标记必须齐全，缺一个就失败退出
const mustHave = ['var slides', 'function go(', '__chassisInit', 'penCanvas', 'toggleSpeaker',
  '@page', 'notes-panel', 'slide:enter',
  ...(noEffects ? [] : ['rollNums', 'chart-grow', '__stepConsume', 'zoomPop', 'animScaleIn', 'typewriter', '__anim'])];
const missing = mustHave.filter((k) => !out.includes(k));
if (missing.length) {
  console.error('BUILD FAIL - 缺失标记:', missing.join(', '));
  process.exit(1);
}
if (noEffects && (out.includes('function rollNums') || out.includes('@keyframes chart-grow'))) {
  console.error('BUILD FAIL - --no-effects 产物不应含动画件定义');
  process.exit(1);
}

writeFileSync(join(root, 'assets', 'chassis-v2.html'), out);
console.log(`BUILD OK → assets/chassis-v2.html（${CSS_MODULES.length} css + ${JS_MODULES.length} js 模块${noEffects ? '，精简装配' : '，全量装配'}，${Buffer.byteLength(out, 'utf8')} 字节 / ${out.length} 字符）`);
