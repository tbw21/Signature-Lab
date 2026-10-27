from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
if len(sys.argv) < 2: raise SystemExit('Usage: python tests/rc24-layout-browser.py artifact.html [widths...]')
WIDTHS=[int(x) for x in sys.argv[2:]] or [320,390,768,1440]
HTML=Path(sys.argv[1]).read_text()
res=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
 for width in WIDTHS:
  for theme in ('light','dark'):
   page=b.new_page(viewport={'width':width,'height':940},device_scale_factor=1)
   errors=[];network=[]
   page.on('pageerror',lambda e: errors.append(str(e)))
   page.on('request',lambda r: network.append(r.url) if r.url.startswith('http') else None)
   try:
    page.set_content(HTML,wait_until='domcontentloaded',timeout=25000)
    page.evaluate("t=>document.querySelector('.shell')._x_dataStack[0].setThemePreference(t)",theme)
    page.locator('#start-safe-test').click(timeout=15000)
    ok=page.evaluate("async()=>await document.querySelector('.shell')._x_dataStack[0].openWorkspace('advanced')")
    assert ok, 'Advanced workspace navigation failed'
    page.evaluate("()=>{['guided-setup','transaction-editor','device-notes'].forEach(id=>document.getElementById(id).open=true)}")
    page.wait_for_timeout(100)
    adv=page.evaluate("""()=>{const ids=['guided-setup','transaction-editor','device-notes'];let rows=ids.map(id=>{const el=document.getElementById(id);const box=el.getBoundingClientRect();const t=el.querySelector(':scope > summary .section-copy').getBoundingClientRect();return {id,x:box.x,w:box.width,titleX:t.x,sw:el.scrollWidth,cw:el.clientWidth}});const bodies=['#guided-setup>.details-body>p','#device-notes>.details-body>p'];return {rows,bodyX:bodies.map(x=>document.querySelector(x)?.getBoundingClientRect().x),documentScroll:document.documentElement.scrollWidth,windowWidth:innerWidth}}""")
    rows=adv['rows'];assert max(row['x'] for row in rows)-min(row['x'] for row in rows)<=1,'Advanced card left edges differ'
    assert max(row['w'] for row in rows)-min(row['w'] for row in rows)<=1,'Advanced card widths differ'
    assert max(row['titleX'] for row in rows)-min(row['titleX'] for row in rows)<=1,'Advanced titles misaligned'
    assert all(abs(x-rows[0]['titleX'])<=1 for x in adv['bodyX']),'Advanced expanded text offset differs from titles'
    assert all(row['sw']<=row['cw']+2 for row in rows),'Advanced inner overflow'
    assert adv['documentScroll']<=adv['windowWidth']+2,'Document overflow in Advanced'
    page.evaluate("async()=>await document.querySelector('.shell')._x_dataStack[0].openWorkspace('test')")
    page.locator('#wallet-loaded').click(timeout=18000)
    page.wait_for_function("() => document.querySelector('.shell')._x_dataStack[0].transactionReady",timeout=25000)
    page.evaluate("()=>{['output-review','transaction-details'].forEach(id=>document.getElementById(id).open=true)}")
    page.wait_for_timeout(150)
    signed=page.evaluate("""()=>{const ids=['output-review','transaction-details'];let rows=ids.map(id=>{const e=document.getElementById(id),r=e.getBoundingClientRect(),summ=e.querySelector('summary').getBoundingClientRect();return {id,x:r.x,w:r.width,sw:e.scrollWidth,cw:e.clientWidth,summaryX:summ.x,summaryW:summ.width}});
    let selector=['#output-review>p','#output-review .review-outputs','#output-review .output-address','#transaction-details>dl','#transaction-details .transaction-id code'];let children=selector.map(sel=>{let e=document.querySelector(sel),r=e?.getBoundingClientRect(),p=e?.closest('#output-review,#transaction-details'),pr=p?.getBoundingClientRect();return{sel,x:r?.x,right:r?.right,parentX:pr?.x,parentRight:pr?.right,sw:e?.scrollWidth,cw:e?.clientWidth,text:e?.textContent?.trim().slice(0,25)}});return{rows,children,documentScroll:document.documentElement.scrollWidth,windowWidth:innerWidth}}""")
    assert signed['documentScroll']<=signed['windowWidth']+2,'Document overflow while reviewing signature'
    assert all(r['sw']<=r['cw']+2 for r in signed['rows']),'Expanded review hidden overflow'
    assert all((ch['x'] is None) or (ch['x']>=ch['parentX']-1 and ch['right']<=ch['parentRight']+1) for ch in signed['children']),'Expanded review content clipped outside its card'
    assert not errors and not network,'App errors/network requests'
    res.append({'width':width,'theme':theme,'pass':True,'advanced':adv,'review':signed,'errors':errors,'network':network})
    print('PASS',width,theme,'advanced 3/3 aligned; expanded outputs/txid contained; no document overflow',flush=True)
   except Exception as e:
    res.append({'width':width,'theme':theme,'pass':False,'error':str(e)})
    print('FAIL',width,theme,str(e)[:350],flush=True)
   finally:page.close()
 b.close()
p=Path.cwd() / ('RC24-LAYOUT-RECEIPT-'+str(WIDTHS[0])+'.json');p.write_text(json.dumps(res,indent=2))
assert all(item['pass'] for item in res),'Layout contract failed'
