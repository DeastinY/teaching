import { chromium } from 'playwright-chromium';
const b = await chromium.launch({ executablePath:'/usr/lib/chromium/chromium', args:['--no-sandbox','--disable-dev-shm-usage'] });
const ctx=await b.newContext({viewport:{width:1600,height:1000},deviceScaleFactor:0.72}); const p=await ctx.newPage();
const errs=[]; p.on('pageerror',e=>errs.push(e.message.split('\n')[0]));
await p.goto('http://localhost:4177/',{waitUntil:'networkidle'}); await p.waitForTimeout(2500);
const r=await p.evaluate(()=>{
  function lum(c){const[r,g,b]=c.match(/\d+\.?\d*/g).slice(0,3).map(Number).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b;}
  function ratio(a,bg){const L1=lum(a),L2=lum(bg),[hi,lo]=L1>L2?[L1,L2]:[L2,L1];return (hi+.05)/(lo+.05);}
  const fails=[];
  document.querySelectorAll('p,h1,h2,h3,dd,dt,li,strong,span,a').forEach(el=>{
    if(!el.textContent.trim()||el.closest('.skip'))return;
    const cs=getComputedStyle(el); const px=parseFloat(cs.fontSize);
    let bg='rgb(250,248,245)',n=el;
    while(n&&n!==document.body){const c=getComputedStyle(n).backgroundColor;
      if(c&&c!=='rgba(0, 0, 0, 0)'){bg=c;break;} n=n.parentElement;}
    const c=ratio(cs.color,bg); const need=(px>=24||(px>=18.66&&+cs.fontWeight>=700))?3:4.5;
    if(c<need) fails.push({t:el.textContent.trim().slice(0,22),c:+c.toFixed(2)});
  });
  return {fails:fails.length, sample:fails.slice(0,3),
    papers:[...document.querySelectorAll('.paper')].map(a=>({
      yr:a.querySelector('.when').textContent.trim().replace(/\s+/g,' '),
      venue:a.querySelector('.venue').textContent})),
    count:document.querySelector('.count').textContent,
    hScroll:document.documentElement.scrollWidth>innerWidth,
    screens:+(document.documentElement.scrollHeight/innerHeight).toFixed(1)};});
console.log('contrast failures:', r.fails, r.sample.length?JSON.stringify(r.sample):'');
console.log('papers header says:', r.count);
r.papers.forEach(x=>console.log('  ', x.yr.padEnd(22), x.venue));
console.log('hScroll:', r.hScroll, '| screens:', r.screens, '| JS errors:', errs.length||'none');
await p.evaluate(()=>document.querySelectorAll('section')[3].scrollIntoView());
await p.waitForTimeout(1500);
await p.screenshot({path:'/tmp/claude-1000/-home-richard-projects-teaching/e8798320-63ad-4b31-8362-de5732f60dca/scratchpad/papers4.png'});
await b.close();
