"""Scoped real-application SeedQR enlargement regression. No wallet secrets are printed."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
assert len(sys.argv)==2
HTML=Path(sys.argv[1]).read_text()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
 for width,height,theme in [(320,640,'dark'),(320,640,'light'),(390,844,'dark'),(390,844,'light'),(768,900,'dark'),(768,900,'light'),(1440,900,'dark'),(1440,900,'light')]:
  page=browser.new_page(viewport={'width':width,'height':height})
  errors=[];requests=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('request',lambda request:requests.append(request.url))
  page.set_default_timeout(10000)
  page.set_content(HTML,wait_until='domcontentloaded',timeout=20000)
  page.evaluate('t=>document.querySelector(".shell")._x_dataStack[0].setThemePreference(t)',theme)
  page.locator('#start-safe-test').click()
  page.locator('.seed-qr canvas').wait_for(state='visible',timeout=18000)
  def metrics():return page.evaluate('''()=>{
    const c=document.querySelector('.seed-scan.premium-qr-card'),q=c.querySelector('.seed-qr'),a=c.querySelector('.seed-qr-actions'),b=a.querySelector('button'),z=document.querySelector('.shell')._x_dataStack[0];
    const box=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,right:r.right,bottom:r.bottom}};
    return {expanded:z.seedQrExpanded,cls:c.classList.contains('seed-expanded'),position:getComputedStyle(c).position,mode:document.documentElement.dataset.theme,
      qr:box(q),canvas:box(q.querySelector('canvas')),card:box(c),actions:box(a),button:box(b),label:b.textContent.trim(),aria:b.getAttribute('aria-expanded'),
      checksum: q.querySelector('canvas').toDataURL().slice(-120),window:{w:innerWidth,clientW:document.documentElement.clientWidth,h:innerHeight}}; }''')
  base=metrics()
  assert base['label']=='Enlarge QR' and base['aria']=='false' and not base['expanded']
  page.get_by_role('button',name='Enlarge QR').click()
  page.wait_for_timeout(70)
  enlarged=metrics()
  assert enlarged['cls'] and enlarged['expanded'] and enlarged['aria']=='true' and enlarged['label']=='Reduce QR'
  assert enlarged['position']=='fixed',enlarged
  assert base['checksum']==enlarged['checksum'], 'QR canvas changed when enlarging'
  assert enlarged['qr']['w'] > base['qr']['w']+18,(base,enlarged)
  assert abs(enlarged['qr']['w']-enlarged['button']['w']) < 2,enlarged
  assert abs((enlarged['card']['x']+enlarged['card']['w']/2)-enlarged['window']['clientW']/2)<=9,enlarged
  assert abs((enlarged['card']['y']+enlarged['card']['h']/2)-height/2)<=9,enlarged
  assert enlarged['card']['x']>=0 and enlarged['card']['right']<=enlarged['window']['clientW']+1 and enlarged['card']['y']>=0 and enlarged['card']['bottom']<=height+1,enlarged
  assert len(errors)==0 and len(requests)==0,(errors,requests)
  if width==390 and theme=='dark':page.screenshot(path='/mnt/data/rc25-work/rc25-expanded-dark-390.png',timeout=18000)
  if width==1440 and theme=='light':page.screenshot(path='/mnt/data/rc25-work/rc25-expanded-light-1440.png',timeout=18000)
  page.keyboard.press('Escape')
  page.wait_for_timeout(30)
  esc=metrics(); assert not esc['expanded'] and esc['label']=='Enlarge QR' and esc['position']!='fixed',esc
  page.get_by_role('button',name='Enlarge QR').click()
  page.get_by_role('button',name='Reduce QR').click()
  reduce=metrics();assert not reduce['expanded'] and reduce['label']=='Enlarge QR',reduce
  page.get_by_role('button',name='Enlarge QR').click()
  page.locator('.premium-words-card h3').click()
  outside=metrics();assert not outside['expanded'],outside
  assert not errors and not requests,(errors,requests)
  results.append({'width':width,'height':height,'theme':theme,'base_qr_width':round(base['qr']['w']),'expanded_qr_width':round(enlarged['qr']['w']),'button_width':round(enlarged['button']['w']),'expanded_position':enlarged['position'],'escape':True,'reduce':True,'outside':True,'js_errors':len(errors),'network':len(requests)})
  print('PASS',width,theme,round(base['qr']['w']),'->',round(enlarged['qr']['w']),flush=True)
  page.close()
 browser.close()
Path('/mnt/data/rc25-work/RC25-SEEDQR-BROWSER-RECEIPT.json').write_text(json.dumps({'cases':results,'passed':len(results),'failed':0},indent=2))
assert len(results)==8
