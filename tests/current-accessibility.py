#!/usr/bin/env python3
"""Current-version browser accessibility and geometry acceptance; no historical projections.
Controlled offline Chromium only. The tests do not claim native OS/browser or WCAG certification.
"""
from pathlib import Path
import json,sys,traceback
from playwright.sync_api import sync_playwright
INPUT=Path(sys.argv[1]);OUT=Path(sys.argv[2]);OUT.parent.mkdir(parents=True,exist_ok=True)
html=INPUT.read_text();rows=[]
def check(n,fun):
 try:fun();rows.append({'name':n,'status':'passed'});print('PASSED',n,flush=True)
 except Exception:rows.append({'name':n,'status':'failed','reason':traceback.format_exc()});print('FAILED',n,traceback.format_exc().splitlines()[-1],flush=True)
def expect(b,msg):
 if not b: raise AssertionError(msg)
def navigate(page, tab):
 """Use currently visible navigation, not retired hidden workspace buttons.

 No application state mutation from test JS: users can reach these views
 through the Settings drawer or the visible Back to test button.
 """
 if tab == 'test':
  landing=page.locator('#start-safe-test')
  if landing.is_visible():
   landing.click(timeout=10000)
   return
  if page.locator('#wallet-safety').is_visible(): return
  back = page.locator('#advanced-view button:visible, #session-view button:visible').filter(has_text='Back to test').first
  if back.count() and back.is_visible():
   back.click(timeout=10000)
  else:
   page.locator('a.brand').click(timeout=10000)
   if landing.is_visible(): landing.click(timeout=10000)
  return
 drawer=page.locator('#tbw-settings > summary')
 drawer.click(timeout=10000)
 label = 'Advanced testing' if tab == 'advanced' else 'Session history'
 page.locator('.tbw-drawer-workspace button').filter(has_text=label).click(timeout=10000)

def layout(page):
 return page.evaluate('''() => {
 const width=document.documentElement.clientWidth;
 const scroll=document.documentElement.scrollWidth;
 const controls=[...document.querySelectorAll('button,a,input,select,textarea,summary')].filter(e=>e.checkVisibility({checkVisibilityCSS:true,checkOpacity:true}) && !e.closest('.sr-only'));
 const bad=controls.map(e=>{const r=e.getBoundingClientRect();return {id:e.id,tag:e.tagName,w:r.width,l:r.left,r:r.right,sw:e.scrollWidth,cw:e.clientWidth}}).filter(x=>x.w>0 && (x.l<-3 || x.r>width+3));
 return {width,scroll,bad};
 }''')
with sync_playwright() as playwright:
 browser=playwright.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width in [320,390,768,1440]:
  ctx=browser.new_context(viewport={'width':width,'height':960},offline=True)
  page=ctx.new_page();requests=[];errors=[]
  page.on('request',lambda r:requests.append(r.url));page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='load',timeout=30000);page.locator('html[data-app-ready="true"]').wait_for(timeout=20000)
  def visible(sel):
   page.locator(sel).first.wait_for(state='visible',timeout=10000)
  for tab,selector in [('test','#wallet-safety'),('advanced','#advanced-title'),('session','#session-title')]:
   navigate(page,tab)
   def f(tab=tab,selector=selector):
    visible(selector);x=layout(page);expect(all(h>=44 for h in page.locator('.header-actions > .help-control, .header-actions > .tbw-header-theme, #tbw-settings > summary').evaluate_all('(es)=>es.filter(e=>e.getClientRects().length).map(e=>e.getBoundingClientRect().height)')),f'{tab} visible header navigation target under 44px');expect(x['scroll']<=width+2,f'{tab} scroll overflow {x}');expect(not x['bad'],f'{tab} control overflow {x}')
   check(f'{width}px {tab} default reflow',f)
  def doubled():
   navigate(page,'test');visible('#wallet-safety')
   page.evaluate("""() => {const es=[...document.querySelectorAll('body *')].filter(e=>!['SCRIPT','STYLE','TEMPLATE'].includes(e.tagName));const sizes=es.map(e=>getComputedStyle(e).fontSize);es.forEach((e,i)=>e.style.fontSize=(parseFloat(sizes[i])*2)+'px')}""")
   for tab,sel in [('test','#wallet-safety'),('advanced','#advanced-title'),('session','#session-title')]:
    navigate(page,tab);visible(sel)
    x=layout(page);expect(x['scroll']<=width+2,f'200% font overflow {tab}: {x}');expect(not x['bad'],f'200% controls overflow {tab}: {x}')
  if width in (320,390):check(f'{width}px 200% all-text size across Test Advanced Session',doubled)
  def spacing():
   page.evaluate("""() => {document.documentElement.style.fontSize='100%';for(const e of document.querySelectorAll('body *'))e.style.fontSize=''}""")
   page.add_style_tag(content='''*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}''')
   for tab,sel in [('advanced','#advanced-title'),('session','#session-title')]:
    navigate(page,tab);visible(sel)
    x=layout(page);expect(x['scroll']<=width+2,f'{tab} text spacing overflow {x}')
   # preserve controls, no horizontal crop of main navigation at normal 100% text size
  if width in (320,390):check(f'{width}px increased text spacing across Advanced and Session',spacing)
  def forced():
   page.emulate_media(forced_colors='active');expect(page.evaluate("matchMedia('(forced-colors: active)').matches"),'forced colors not active');navigate(page,'test');visible('#wallet-safety');expect(page.locator('#tbw-settings > summary').evaluate('(e)=>parseFloat(getComputedStyle(e).borderTopWidth)')>=1,'visible Settings control missing forced-color border')
   x=layout(page);expect(x['scroll']<=width+2,f'forced-colors overflow {x}');page.emulate_media(forced_colors='none')
  check(f'{width}px forced colors visibility/reflow',forced)
  def keyboard():
   page.evaluate("""() => {document.documentElement.style.fontSize='100%';for(const e of document.querySelectorAll('body *'))e.style.fontSize=''}""")
   page.locator('.help-control').focus();page.keyboard.press('Enter');visible('#help-title')
   first=page.locator('.help-topic>summary').first;first.focus();page.keyboard.press('Enter');expect(first.evaluate('(e)=>e.parentElement.open'),'Help summary not expanded')
   link=first.locator('xpath=following-sibling::ul/li/a').first;link.focus();page.keyboard.press('Enter')
   href=link.get_attribute('href');target=page.locator(href)
   target.wait_for(state='visible',timeout=10000)
   expect(target.evaluate('(e)=>e.open'),'Help target not open');
   target.locator('> .help-answer-nav a').first.click()
   expect(page.evaluate('document.activeElement.id')=='help-title','Help return did not focus Help heading')
   page.get_by_role('link',name='Back to test',exact=True).first.click();visible('#wallet-safety')
  if width in (390,1440):check(f'{width}px keyboard Help disclosure and focus return',keyboard)
  check(f'{width}px no script errors or network requests',lambda:expect(not errors and not requests,f'errors={errors}, requests={requests}'))
  ctx.close()
 browser.close()
result={'schema':'tbw-current-accessibility-v1','artifactSha256':__import__('hashlib').sha256(INPUT.read_bytes()).hexdigest(),'environment':'offline Chromium setContent; no real hardware/optics/native origin','passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows}
OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'failed':result['failed']}));sys.exit(bool(result['failed']))
