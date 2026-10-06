#!/usr/bin/env python3
"""Current-candidate readability/flow checks. No native fonts, hardware or optical claim."""
from pathlib import Path
exec((Path(__file__).parent/'ux-browser.py').read_text().split('\nwith sync_playwright() as pw:')[0],globals())
def settle(h):h.page.wait_for_timeout(100)
def box(h,s):
 h.page.locator(s).wait_for(state='visible');return h.page.locator(s).evaluate('(e)=>e.getBoundingClientRect().toJSON()')
def state(h):return h.call('return JSON.stringify([a.walletSession,a.stateSignature,a.psbtBase64,a.signingPolicy,a.sessionHistory,a.resultState,a.isTestComplete ? a.report() : null])')
def checks(h,minimum=14):
 assert h.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 bad=h.page.evaluate('''()=>[...document.querySelectorAll('button,summary,input,select,textarea')].filter(e=>e.checkVisibility()).filter(e=>{const r=e.getBoundingClientRect();return r.left< -1||r.right>innerWidth+1||((!['INPUT','TEXTAREA','SELECT'].includes(e.tagName))&&e.scrollWidth>e.clientWidth+2)}).map(e=>[e.id,e.textContent.slice(0,55),e.scrollWidth,e.clientWidth])''')
 assert not bad,bad
 fonts=h.page.evaluate('''()=>[...document.querySelectorAll('body *')].filter(e=>e.checkVisibility()&&!e.closest('.sr-only')&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).map(e=>({id:e.id,tag:e.tagName,cls:typeof e.className==='string'?e.className:'',t:e.textContent.slice(0,45),font:getComputedStyle(e).fontFamily,size:parseFloat(getComputedStyle(e).fontSize)})).filter(e=>e.tag!=='OPTION'&&e.tag!=='SCRIPT'&&e.tag!=='STYLE')''')
 assert all(x['font'].startswith('Helvetica') for x in fonts),fonts
 tiny=[x for x in fonts if x['size']<minimum];assert not tiny,tiny
 assert not h.errors,h.errors
 assert not h.requests,h.requests

def footer(h):
 m=h.page.evaluate('''()=>{const f=document.querySelector('footer'),r=f.getBoundingClientRect();const active=[...document.querySelectorAll('.panel,.aux-view,#help')].filter(e=>e.checkVisibility()).map(e=>e.getBoundingClientRect().bottom);return {gap:r.top-Math.max(...active),size:parseFloat(getComputedStyle(f).fontSize),pos:getComputedStyle(f).position,txt:f.textContent}}''')
 assert -1<=m['gap']<=65,m
 assert m['size']>=16 and m['pos']=='static',m
 assert 'oren-z0 / exfil-tester' in m['txt'] and 'MIT licence' in m['txt']

def accept(h,mode):
 d=h.config()
 if mode=='match':h.accept(d['tx'])
 elif mode=='review':
  raw=sign_psbt(d['psbt'],d['tx']);raw=raw[:5]+b'\x02\xfc\x41\x01\x42'+raw[5:];h.accept(raw.hex())
 else:h.call('a.goToStep(3);a.acceptArtifact("deadbeef")')
 settle(h)
 return d

with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 env={'browser':browser.version,'origin':'controlled offline Chromium setContent','nativeHelvetica':False,'physicalSigner':False,'opticalScan':False}
 for w in [320,360,390,438,768,1024,1440]:
  def views(w=w):
   h=Harness(browser,width=w,height=1000);settle(h)
   assert h.page.locator('.brand-name').inner_text()=='Signature Lab'
   assert h.page.locator('body').evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')==18
   for v in ['test','advanced','session','test']:
    before=state(h);h.workspace(v);settle(h);checks(h);footer(h);assert state(h)==before
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'readability-wallet-{w}.png'),full_page=True)
   h.page.locator('#wallet-loaded').click();settle(h);checks(h);footer(h)
   label=h.page.locator('.scenario-line>span').first
   assert label.is_visible() and label.evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')>=14,'Scenario label hidden by zero-size style'
   h.page.locator('.stepper button').nth(2).click();settle(h);checks(h);footer(h)
   assert h.page.locator('.intake').is_visible();assert not h.call('return a.scan.active')
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'readability-intake-{w}.png'),full_page=True)
   close(h)
  test(f'Readability all workspaces and intake/footer at {w}px',views)
 for w in [390,1440]:
  for n in [12,24]:
   def qr(w=w,n=n):
    h=Harness(browser,width=w,height=1100);h.call('a.selectSeedLength(arg)',n);h.page.wait_for_function('('+APP+').seedQrVisible');settle(h)
    before=state(h);pixels=h.page.locator('[x-ref=seedQrCanvas]').evaluate('(e)=>e.toDataURL()')
    for action in ['Enlarge QR','Reduce QR']:
     h.page.get_by_role('button',name=action,exact=True).click();settle(h);checks(h);footer(h)
     assert state(h)==before and h.page.locator('[x-ref=seedQrCanvas]').evaluate('(e)=>e.toDataURL()')==pixels
     a=box(h,'#seed-qr-display');b=box(h,'#wallet-load-card');assert abs(a['left']-b['left'])<1 and abs(a['right']-b['right'])<1
    close(h)
   test(f'Readability QR alignment and pixel preservation {n} words {w}px',qr)
 for w in [320,390,768,1440]:
  def enlarged(w=w):
   h=Harness(browser,width=w,height=1100);h.page.evaluate(ENLARGE);settle(h)
   for v in ['test','advanced','session']:h.workspace(v);settle(h);checks(h);footer(h)
   close(h)
  test(f'Readability doubled text all workspaces {w}px',enlarged)
 for w in [320,1440]:
  def spacing(w=w):
   h=Harness(browser,width=w,height=1100);h.page.add_style_tag(content=TEXT_SPACE);settle(h)
   for v in ['test','advanced','session']:h.workspace(v);settle(h);checks(h);footer(h)
   close(h)
  test(f'Readability increased text spacing {w}px',spacing)
 for w in [390,1440]:
  for mode in ['match','review','incomplete']:
   def result(w=w,mode=mode):
    h=Harness(browser,width=w,height=1100);accept(h,mode);checks(h);footer(h)
    if mode=='review':assert h.call('return a.analysis.metadata.status')=='unexpected';assert h.page.locator('.file-review-action').is_visible()
    if mode=='match':assert h.call('return a.isTestComplete')
    actions=h.page.locator('.result-actions:visible .button')
    rects=[e.bounding_box() for e in actions.all()]
    for a,b in zip(rects,rects[1:]):
     if min(a['y']+a['height'],b['y']+b['height'])>max(a['y'],b['y'])+1:
      assert abs(a['y']-b['y'])<1 and abs(a['height']-b['height'])<1,(a,b)
    if mode=='review' and w==390:h.page.screenshot(path=str(SHOTS/'readability-review-390.png'),full_page=True)
    before=state(h);h.workspace('session');settle(h);h.workspace('test');settle(h);assert state(h)==before
    close(h)
   test(f'Readability {mode} result, warnings and equal action heights {w}px',result)
 for w in [390,1440]:
  for mode in ['example','replacement','help']:
   def dialog(w=w,mode=mode):
    h=Harness(browser,width=w,height=900);before=state(h)
    if mode=='example':h.page.locator('#try-example').click();settle(h);assert 'CHECK COMPLETE' in h.page.locator('#attack-example').inner_text()
    elif mode=='replacement':
     h.page.locator('#wallet-loaded').click();h.page.locator('.stepper button').first.click();settle(h);before=state(h);h.page.locator('#new-test-wallet').click();settle(h);assert h.page.locator('#wallet-replacement').is_visible()
    else:
     h.page.get_by_role('link',name='Help',exact=True).click();settle(h);footer(h)
     # Open the licence through its canonical existing link in the footer.
     h.page.locator('footer a[href="#license-help"]').click();settle(h);assert h.page.locator('.license-notice').is_visible()
    checks(h)
    if mode=='example' and w==390:h.page.screenshot(path=str(SHOTS/'readability-example-390.png'))
    if mode=='help':h.page.get_by_role('link',name='Back to test',exact=True).click()
    else:h.page.keyboard.press('Escape')
    settle(h);assert state(h)==before;close(h)
   test(f'Readability {mode} dialog/help and preserved state {w}px',dialog)
 for w in [320,390,1440]:
  def outputs(w=w):
   h=Harness(browser,width=w,height=1100);h.config();h.call("a.invalidate();a.outputs=Array.from({length:20},(_,i)=>({id:99000+i,amount:{value:'2000',error:null},dest:{value:'m/84h/0h/0h/0/'+i,error:null}}));a.recompute();a.goToStep(2)");settle(h)
   h.page.locator('.output-review>summary').click();settle(h);checks(h)
   m=h.page.evaluate('''()=>[...document.querySelectorAll('.review-outputs li')].map(e=>({text:e.textContent,rects:[...e.children].map(x=>({tag:x.tagName,cls:x.className,r:x.getBoundingClientRect().toJSON()}))}))''')
   assert len(m)==20,len(m)
   for item in m:
    for a,b in zip(item['rects'],item['rects'][1:]):
     a=a['r'];b=b['r'];assert min(a['right'],b['right'])-max(a['left'],b['left'])<=1 or min(a['bottom'],b['bottom'])-max(a['top'],b['top'])<=1,item
   h.open_settings();settle(h);checks(h)
   pairs=h.page.locator('.transaction-row>summary').evaluate_all("""es=>es.filter(e=>e.checkVisibility()).map(e=>{const label=e.querySelector('strong'),value=e.querySelector('.row-amount');let r=document.createRange();r.selectNodeContents(label);return {text:label.textContent,label:r.getBoundingClientRect().toJSON(),value:value.getBoundingClientRect().toJSON()}})""")
   assert len(pairs)>=20
   assert all(x['label']['right']<=x['value']['left']+1 or x['label']['bottom']<=x['value']['top']+1 for x in pairs),pairs
   close(h)
  test(f'Readability all 20 output labels and editor {w}px',outputs)
 def forced():
  h=Harness(browser,width=390);h.page.emulate_media(forced_colors='active',reduced_motion='reduce');settle(h);checks(h);footer(h);close(h)
 test('Readability forced colors and reduced motion',forced)
 def keyboard():
  h=Harness(browser,width=390);h.page.keyboard.press('Tab');h.page.get_by_role('link',name='Help',exact=True).focus();h.page.keyboard.press('Enter');settle(h)
  assert h.page.locator('#help').is_visible();h.page.get_by_role('link',name='Back to test',exact=True).focus();h.page.keyboard.press('Enter');settle(h);checks(h);close(h)
 test('Readability keyboard global Help and return route',keyboard)
 browser.close()
r={'suite':'Readability exact-candidate integration','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'environment':env,'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results}
OUT.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
