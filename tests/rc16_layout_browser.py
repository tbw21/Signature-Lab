#!/usr/bin/env python3
"""RC16 scoped layout regression; supplements rather than replaces canonical suite."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,os
html=Path(sys.argv[1]).read_text()
results=[]
shot_dir=Path(os.environ["RC16_SCREENSHOT_DIR"]) if os.environ.get("RC16_SCREENSHOT_DIR") else None
if shot_dir:shot_dir.mkdir(parents=True,exist_ok=True)
def ck(ok,msg):
 if not ok: raise AssertionError(msg)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for width in (390,768,1440):
  for theme in ('dark','light'):
   if len(sys.argv)>2 and str(width)!=sys.argv[2]:continue
   if len(sys.argv)>3 and theme!=sys.argv[3]:continue
   pg=browser.new_page(viewport={'width':width,'height':1000},accept_downloads=True)
   errors=[];network=[]
   pg.on('pageerror',lambda err:errors.append(str(err)))
   pg.on('request',lambda req:network.append(req.url) if req.url.startswith(('http://','https://')) else None)
   pg.set_content(html,wait_until='domcontentloaded')
   pg.wait_for_selector('html[data-app-ready="true"]',timeout=60000)
   pg.evaluate('(theme)=>document.querySelector(".shell")._x_dataStack[0].setThemePreference(theme)',theme)
   ck(pg.locator('#tbw-landing').is_visible(),'landing hidden')
   ck(pg.locator('.premium-journey-step img').count()==0,'products returned')
   pg.locator('#start-safe-test').click()
   ck(pg.locator('#wallet-fingerprint-value').is_visible(),'fingerprint removed')
   pg.wait_for_function('document.querySelector(".shell")._x_dataStack[0].transactionReady',timeout=14000)
   pg.locator('#wallet-loaded').click()
   pg.wait_for_selector('#sign-title:visible',timeout=8000)
   ck(pg.locator('#qr-format-label').inner_text()=='QR format','QR label changed')
   ck(pg.locator('#qr-format button').count()==2,'format functionality lost')
   ck(pg.locator('.psbt-actions button').count()==2,'PSBT actions lost')
   ck(pg.locator('#output-review').count()==1 and pg.locator('#transaction-details').count()==1,'disclosures lost')
   ck(pg.locator('.import-actions button').count()>=2,'return signing methods lost')
   pg.locator('[data-qr-mode="bbqr"]').click()
   ck(pg.locator('[data-qr-mode="bbqr"]').get_attribute('aria-pressed')=='true','BBQr unavailable')
   pg.locator('[data-qr-mode="ur"]').click()
   ck(pg.locator('[data-qr-mode="ur"]').get_attribute('aria-pressed')=='true','BC-UR unavailable')
   geom=pg.evaluate('''()=>{let a=s=>{let b=document.querySelector(s).getBoundingClientRect();return {x:b.x,y:b.y,width:b.width,height:b.height,bottom:b.bottom}};return {sign:a('.sign-layout'),summary:a('.sign-layout>.transaction-summary'),qr:a('.sign-layout>.qr-column'),selector:a('.qr-format-control'),actions:a('.psbt-actions'),heading:a('#sign-heading h2'),outer:document.body.scrollWidth}}''')
   ck(geom['outer']<=width+1,f'sign overflow {width} {geom["outer"]}')
   ck(abs(geom['qr']['height']-geom['summary']['height'])<2 if width>850 else True,f'uneven column height {geom}')
   ck(abs(geom['selector']['x']-geom['actions']['x'])<1.5 and abs(geom['selector']['width']-geom['actions']['width'])<1.5,f'QR selector/actions misaligned {geom}')
   if width==1440 and theme=='dark' and shot_dir:
    pg.screenshot(path=str(shot_dir/'rc16-signing-dark-1440.png'),full_page=False)
   pg.evaluate('document.querySelector(".shell")._x_dataStack[0].step=3')
   pg.locator('#result-pending').wait_for(state='visible',timeout=8000)
   ck(pg.locator('#verify-title').inner_text()=='Your result','results header incorrect')
   ck(pg.locator('#result-pending h3').inner_text()=='No results yet','empty state changed')
   ck(pg.locator('#result-pending button').count()==1,'return button absent')
   rg=pg.evaluate('''()=>{let a=s=>{let b=document.querySelector(s).getBoundingClientRect();return {x:b.x,y:b.y,width:b.width,height:b.height}};return {title:a('#verify-title'),empty:a('#result-pending'),body:document.body.scrollWidth}}''')
   ck(rg['title']['x']<width*.35,f'results heading right-aligned {rg}')
   ck(rg['empty']['width']<=820.5 and rg['body']<=width+1,f'result overflow or too-wide {rg}')
   if width==1440 and theme=='dark' and shot_dir:
    pg.screenshot(path=str(shot_dir/'rc16-empty-result-dark-1440.png'),full_page=False)
   pg.locator('#result-pending button').click()
   ck(pg.locator('#sign-title').is_visible(),'return button ineffective')
   ck(not errors,f'JS errors {errors}')
   ck(not network,f'network attempted {network}')
   results.append({'width':width,'theme':theme,'status':'passed','signGeometry':geom,'resultGeometry':rg,'pageErrors':0,'externalRequests':0})
   pg.close()
 browser.close()
print(json.dumps({'status':'passed','cases':len(results),'results':results},indent=2))
