#!/usr/bin/env python3
"""Scoped browser regression: SOURCE CSS, representative markup, rendered contrast and containment."""
from pathlib import Path
import asyncio,json,sys
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
CSS=(ROOT/'src/style.css').read_text()
JS="""(el) => {
const s=getComputedStyle(el), b=el.getBoundingClientRect();
return {text:(el.textContent||'').trim(),fg:s.color,bg:s.backgroundColor,x:b.left,right:b.right,width:b.width,display:s.display}
}"""
MARKUP='''<!doctype html><html data-theme="{theme}"><head><meta charset="utf-8"><style>{css}</style></head><body style="margin:0">
<div id="tbw-landing" class="premium-landing" style="max-width:1000px;margin:auto"><div class="premium-journey"><article class="premium-journey-step"><div class="premium-journey-num">1</div><strong>Create test wallet</strong></article><article class="premium-journey-step"><div class="premium-journey-num">2</div><strong>Sign test transactions</strong></article><article class="premium-journey-step"><div class="premium-journey-num">3</div><strong>Verify results</strong></article></div></div>
<div class="page-container" style="max-width:1440px"><div class="session-tracker"><div class="tracker-identity"><span>Wallet TEST1234</span></div><button class="tracker-session tracker-status"><span>No checks yet</span><strong>1 checked</strong><span>0 differed</span></button></div>
<section id="test-view"><div class="result-limit"><span>It does not rule out malware. <a href="#limitations" data-faq-link>Understand the limits</a></span></div><details class="advanced-tools result-tools" open><summary>Evidence &amp; technical details</summary><div class="button-group"><button class="button secondary small">Save diagnostics</button></div><div class="advanced-body"><p>Evidence includes the returned data</p><a class="text-button" href="#evidence-help" data-faq-link>What the evidence can establish</a></div></details></section>
<section id="session-view"><div class="session-content-grid"><div class="session-resources"><details id="session-evidence-tools" class="details" open><summary>Session evidence &amp; diagnostics</summary><div class="details-body"><details class="details" open><summary>Diagnostic package</summary><div class="details-body"><div class="button-group"><button class="button secondary small">Save diagnostics</button></div></div></details></div></details></div></div></section>
</div></body></html>'''
def luminance(hex_color):
 c=hex_color.lstrip('#');r,g,b=[int(c[i:i+2],16)/255 for i in (0,2,4)];v=[(t/12.92 if t<=0.04045 else ((t+0.055)/1.055)**2.4) for t in [r,g,b]];return sum(a*b for a,b in zip(v,[.2126,.7152,.0722]))
def rgb_hex(s):
 parts=s.removeprefix('rgba(').removeprefix('rgb(').rstrip(')').split(',')
 return '#'+''.join(f'{int(round(float(x.strip()))):02x}' for x in parts[:3])
def contrast(a,b):
 a,b=sorted([luminance(rgb_hex(a)),luminance(rgb_hex(b))],reverse=True);return (a+.05)/(b+.05)
async def run():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'],timeout=15000)
  records=[]
  try:
   for width in (390,768,1440):
    for theme in ('light','dark'):
     page=await browser.new_page(viewport={'width':width,'height':900},color_scheme=theme)
     await page.set_content(MARKUP.format(theme=theme,css=CSS),wait_until='domcontentloaded',timeout=15000)
     sels={'limits':'#test-view .result-limit a[href="#limitations"]','evidence':'#test-view .result-tools a[href="#evidence-help"]','status':'.session-tracker .tracker-status span','count':'.session-tracker .tracker-status strong','journey':'.premium-journey-num'}
     color_results={}
     for name,sel in sels.items():
      el=page.locator(sel).first
      fg=await el.evaluate('(el)=>getComputedStyle(el).color')
      # get effective background from nearest non-transparent ancestor via computed colors
      bg=await el.evaluate('''el=>{let n=el;while(n){let c=getComputedStyle(n).backgroundColor;if(c && c!=='transparent' && c!=='rgba(0, 0, 0, 0)')return c;n=n.parentElement;}return getComputedStyle(document.documentElement).backgroundColor;}''')
      cr=contrast(fg,bg) if theme=='light' else None
      color_results[name]={'ratio':round(cr,2) if cr is not None else None,'fg':fg,'bg':bg}
      if theme=='light' and cr<4.5:raise AssertionError(f'contrast {name} {cr:.2f} theme={theme} width={width} {fg} on {bg}')
     overflow=[]
     for container,button in [('#test-view .result-tools','#test-view .result-tools > .button-group > .button'),('#session-view #session-evidence-tools','#session-view #session-evidence-tools .details-body .details-body .button')]:
      c=await page.locator(container).first.bounding_box();b=await page.locator(button).first.bounding_box()
      if not c or not b:raise AssertionError('Missing card or button')
      if b['x']+b['width']>c['x']+c['width']+0.5 or b['x']<c['x']-0.5:overflow.append({'container':container,'button':button,'cx':c['x'],'cw':c['width'],'bx':b['x'],'bw':b['width']})
     if overflow:raise AssertionError(f'overflow theme={theme} width={width} {overflow}')
     records.append({'viewport':width,'theme':theme,'contrast':color_results,'containment':'pass'})
     print(width,theme,'PASS',color_results if theme=='light' else 'contained',flush=True)
     await page.close()
  finally: await browser.close()
  out=Path.cwd()/'RC20-BROWSER-RECEIPT.json'
  out.write_text(json.dumps({'fixture':'source CSS and structural DOM fixture; not full app','cases':records,'passed':len(records),'failed':0},indent=2)+'\n')
  print('RESULT',out)
asyncio.run(run())
