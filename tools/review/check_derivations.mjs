import {spawn} from 'node:child_process';
import {readFile, writeFile, mkdtemp, mkdir} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve, dirname} from 'node:path';
import {pathToFileURL, fileURLToPath} from 'node:url';

const root = resolve(import.meta.dirname, '../..');
const out = resolve(root, 'tmp/derivations-qa');
await mkdir(out, {recursive: true});
const topics = JSON.parse(await readFile(`${root}/content/derivations.json`, 'utf8'));
const checks = [];
const check = (value, message) => { if (!value) throw Error(message); checks.push(message); };
const cache = new Map();
async function source(path) {
  if (!cache.has(path)) cache.set(path, await readFile(path, 'utf8'));
  return cache.get(path);
}
// Verify the whole graph, including cross-page fragment targets and assets.
let checkedLinks = 0;
for (const path of [resolve(root, 'derivations/index.html'), ...topics.map(t => resolve(root, t.file))]) {
  const html = await source(path);
  for (const match of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    const url = new URL(match[1].replaceAll('&amp;', '&'), pathToFileURL(path));
    check(url.protocol === 'file:', `Offline link: ${match[1]}`);
    const target = fileURLToPath(url);
    const targetSource = await source(target);
    if (url.hash) check(targetSource.includes(`id="${url.hash.slice(1)}"`), `Fragment exists: ${match[1]}`);
    checkedLinks++;
  }
}
check(topics.length >= 91 && new Set(topics.map(t => t.chapter)).size === 44, 'Explanations cover all 44 chapters');
const summary = await source(resolve(root, 'Physics_Review_and_Summary_Tutorial.html'));
check((summary.match(/class="derivation-resources"/g) || []).length === 44, 'Every summary has a formula panel');
for (const t of topics) check(summary.includes(`href="${t.file}"`), `Summary links to ${t.slug}`);
const provenance = JSON.parse(await readFile(`${root}/content/equation-provenance.json`,'utf8'));
for (const item of [...provenance.notes,...provenance.source]) {
  const target = new URL(item.href,pathToFileURL(`${root}/`));
  const html = await source(fileURLToPath(target));
  check(html.includes(`id="${target.hash.slice(1)}"`),`Equation proof exists: ${item.href}`);
}
for (const row of provenance.source) check(summary.includes(`id="${row.id}"`),`Source equation return exists: ${row.id}`);
await writeFile(`${out}/static-checks.json`,JSON.stringify({passed:checks.length,checkedLinks,topics:topics.length,chapters:44},null,2));
if (process.argv.includes('--static-only')) {
  console.log(JSON.stringify({passed:checks.length,checkedLinks,topics:topics.length,chapters:44,browser:'not requested'},null,2));
  process.exit(0);
}
const profile = await mkdtemp(`${tmpdir()}/physics-inquiry-qa-`);
const chrome = spawn(process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  '--headless=new', '--disable-gpu', '--disable-background-networking', '--disable-default-apps',
  '--no-first-run', '--no-default-browser-check', `--user-data-dir=${profile}`, '--remote-debugging-port=0', 'about:blank'
], {stdio: 'ignore'});
let socket;
const delay = ms => new Promise(r => setTimeout(r, ms));
const errors = [];
try {
  let port;
  for (let i=0; i<200; i++) {
    if (chrome.exitCode !== null || chrome.signalCode !== null) throw Error('Chrome exited before starting. Use --static-only for file/link verification in restricted environments.');
    try { port = (await readFile(`${profile}/DevToolsActivePort`, 'utf8')).split('\n')[0]; break; } catch {}
    await delay(100);
  }
  if (!port) throw Error('Chrome test endpoint unavailable. Use --static-only for file/link verification.');
  const targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  socket = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl);
  await new Promise((r,j) => {socket.addEventListener('open',r,{once:true});socket.addEventListener('error',j,{once:true});});
  let sequence = 0;
  const pending = new Map();
  socket.addEventListener('message', event => {
    const data = JSON.parse(event.data);
    if (data.method === 'Runtime.exceptionThrown') errors.push(data.params.exceptionDetails.text);
    if (data.id) {
      const call = pending.get(data.id); pending.delete(data.id);
      if (data.error) call.reject(Error(data.error.message)); else call.resolve(data.result);
    }
  });
  const cdp = (method, params={}) => new Promise((resolve,reject) => {
    const id = ++sequence; pending.set(id,{resolve,reject}); socket.send(JSON.stringify({id,method,params}));
  });
  const evaluate = async expression => {
    const result = await cdp('Runtime.evaluate', {expression,returnByValue:true,awaitPromise:true});
    if (result.exceptionDetails) throw Error(JSON.stringify(result.exceptionDetails));
    return result.result.value;
  };
  async function waitFor(expression) {
    for (let i=0;i<200;i++) {if (await evaluate(expression)) return; await delay(100);}
    throw Error(`Timed out: ${expression}`);
  }
  const navigate = async path => {
    await cdp('Page.navigate', {url: new URL(path, pathToFileURL(`${root}/`)).href});
    await waitFor('document.readyState === "complete"');
  };
  const screenshot = async name => {
    const result = await cdp('Page.captureScreenshot',{format:'png'});
    await writeFile(`${out}/${name}.png`,Buffer.from(result.data,'base64'));
  };
  await cdp('Page.enable'); await cdp('Runtime.enable');
  await cdp('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});
  await navigate('Physics_Review_and_Summary_Tutorial.html#chapter-19');
  await waitFor('document.querySelector("#chapter-19 .source-image").complete');
  check(await evaluate('!document.querySelector("#chapter-19").hidden && document.querySelectorAll("#chapter-19 .formula-link").length>=3'), 'Summary displays the matching formula choices');
  check(await evaluate('document.querySelectorAll(".source-topic-link").length>30'), 'Original-image headings have clickable explanation overlays');
  await screenshot('summary-desktop');
  const entry = topics.find(t => t.slug === 'ideal-gas');
  await evaluate('document.querySelector("#chapter-19--ideal-gas a").click()');
  await waitFor('location.pathname.endsWith("/derivations/ideal-gas.html") && document.readyState==="complete"');
  check(await evaluate('document.querySelectorAll(".step").length===5'), 'Summary link opens the full ideal-gas explanation');
  await screenshot('ideal-gas-desktop');
  await evaluate('document.querySelector("#step-4 .branch").click()');
  await waitFor('location.pathname.endsWith("/equipartition.html") && document.readyState==="complete"');
  check(await evaluate('document.querySelector("[data-context-return]").getAttribute("href")==="ideal-gas.html#step-4"'), 'Deeper branch returns to the exact parent step');
  await evaluate('document.querySelector("[data-context-return]").click()');
  await waitFor('location.hash==="#step-4" && document.readyState==="complete"');
  check(await evaluate('document.querySelector(":target").id==="step-4"'), 'Return link restores the parent derivation location');
  await evaluate('document.querySelector(".summary-return a").click()');
  await waitFor(`location.hash === '#${entry.summaryAnchor}' && document.readyState === 'complete'`);
  check(await evaluate('!document.querySelector("#chapter-19").hidden && document.querySelector(":target").id==="chapter-19--ideal-gas"'), 'Summary return opens the right chapter and preserves its exact formula anchor');
  await delay(200);
  check(await evaluate('(()=>{const r=document.querySelector(":target").getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight})()'), 'Returned formula is visible in the viewport');
  await evaluate('document.querySelector("#selectable-toggle").checked=true;document.querySelector("#selectable-toggle").dispatchEvent(new Event("change"))');
  check(await evaluate('document.querySelectorAll("#chapter-19 .regenerated-page a[data-derivation-link]").length>0'), 'Selectable textbook headings link directly to explanations');
  await evaluate('document.querySelector("#chapter-19 .regenerated-page a[data-derivation-link]").dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true}))');
  await waitFor('location.pathname.includes("/derivations/") && document.readyState==="complete"');
  check(await evaluate('!!document.querySelector(".step")'), 'A selectable source heading opens a derivation');
  // Every explanation must render, including its local styles, on desktop and phone.
  for (const t of topics) {
    await navigate(t.file);
    check(await evaluate('document.querySelector("h1") && document.querySelectorAll(".step").length>=4 && getComputedStyle(document.querySelector(".step")).borderTopStyle==="solid"'), `Explanation renders: ${t.slug}`);
    check(await evaluate('document.documentElement.scrollWidth<=innerWidth'), `Desktop fits: ${t.slug}`);
  }
  await cdp('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
  for (const t of topics) {
    await navigate(t.file);
    check(await evaluate('document.documentElement.scrollWidth<=innerWidth'), `Phone fits: ${t.slug}`);
  }
  await navigate('derivations/carnot.html'); await screenshot('carnot-mobile');
  await navigate('derivations/index.html');
  await evaluate('document.querySelector("#topic-search").value="entropy";document.querySelector("#topic-search").dispatchEvent(new Event("input"))');
  check(await evaluate('document.querySelectorAll(".directory-chapter:not([hidden]) li:not([hidden])").length>0 && [...document.querySelectorAll(".directory-chapter:not([hidden]) li:not([hidden])")].some(li=>li.textContent.includes("entropy"))'), 'Index search finds relevant explanations');
  await evaluate('document.querySelector("#topic-search").value="zzzz-no-topic";document.querySelector("#topic-search").dispatchEvent(new Event("input"))');
  check(await evaluate('!document.querySelector("#no-results").hidden && document.querySelectorAll(".directory-chapter:not([hidden])").length===0'), 'Index search handles no matches');
  await navigate('derivations/entropy.html?from=javascript:alert(1)&step=step-1');
  check(await evaluate('document.querySelector("[data-context-return]").getAttribute("href").startsWith("../Physics_")'), 'Invalid return contexts retain the safe summary fallback');
  await screenshot('entropy-mobile');
  check(errors.length===0, 'No browser JavaScript exceptions');
  await writeFile(`${out}/checks.json`,JSON.stringify({passed:checks.length,checkedLinks,errors,checks},null,2));
  console.log(JSON.stringify({passed:checks.length,checkedLinks,topics:topics.length,chapters:44,errors},null,2));
  await cdp('Browser.close').catch(()=>{});
} finally {socket?.close();chrome.kill('SIGTERM');}
