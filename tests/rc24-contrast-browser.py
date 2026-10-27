from pathlib import Path
from playwright.sync_api import sync_playwright
import re,sys,json
if len(sys.argv)<2: raise SystemExit('Usage: python tests/rc24-contrast-browser.py artifact.html')
H=Path(sys.argv[1]).read_text()
def lum(c):
 nums=[float(x) for x in re.findall(r'[\d.]+',c)[:3]]
 if len(nums)!=3:return 0
 a=[]
 for x in nums:
  v=x/255;a.append(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4)
 return .2126*a[0]+.7152*a[1]+.0722*a[2]
def ratio(a,b):
 l1,l2=sorted((lum(a),lum(b)))
 return round((l2+.05)/(l1+.05),2)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
 for width,theme in [(390,'light'),(1440,'light'),(390,'dark'),(1440,'dark')]:
  page=b.new_page(viewport={'width':width,'height':900})
  page.set_content(H,wait_until='domcontentloaded')
  page.evaluate("t=>document.querySelector('.shell')._x_dataStack[0].setThemePreference(t)",theme)
  page.locator('#start-safe-test').click()
  page.evaluate("async()=>{let a=document.querySelector('.shell')._x_dataStack[0];await a.openWorkspace('advanced');a.settingsOpen=true;document.getElementById('transaction-editor').open=true;}")
  page.wait_for_timeout(100)
  cs=page.evaluate('''()=>{let s=['#advanced-view .transaction-row','#advanced-view .transaction-row>summary','#advanced-view .transaction-row>summary strong','#advanced-view .transaction-row .row-amount'];return s.map(x=>{const e=document.querySelector(x);const a=getComputedStyle(e);return{selector:x,foreground:a.color,background:a.backgroundColor,display:a.display}})}''')
  parentbg=next((x['background'] for x in cs if x['selector'].endswith('>summary')),None)
  score={x['selector']:ratio(x['foreground'],x['background'] if x['background']!='rgba(0, 0, 0, 0)' else parentbg) for x in cs if x['selector']!='#advanced-view .transaction-row'}
  print('CONTRAST',width,theme,score,flush=True)
  if theme=='light': assert all(x>=4.5 for x in score.values()),score
  if width==390 and theme=='light':page.screenshot(path=str(Path.cwd()/'rc24-editor-390-light-final.png'),full_page=True,timeout=15000)
  page.close()
 b.close()
