#!/usr/bin/env python3
"""Scoped native disclosure/CTA presentation tests; not end-to-end application acceptance."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT = Path(__file__).resolve().parents[1]
css = (ROOT/'src/style.css').read_text()
assert '/* RC19 - unified disclosure affordances' in css
# Only the final scoped component rules are rendered. Browser policy forbids real-origin navigation.
component = '/* RC19 - unified disclosure affordances' + css.split('/* RC19 - unified disclosure affordances',1)[1]
base=':root{--premium-ink:#ecf2f8;--premium-surface:#0f2333;--premium-tint:#132c3d;--premium-edge:#305065;--orange:#f39405;--premium-soft:#b8c7d3}.button{cursor:pointer}.details>summary{display:flex}'
fixture='''<div class="shell"><div id="test-view"><details class="details output-review" id="output-review"><summary><span>Review 2 outputs</span></summary><p>Details</p></details><details class="details transaction-meta secondary-review" id="transaction-details"><summary>Transaction details</summary><p>Details</p></details></div><div id="session-view" class="premium-session-view"><div class="session-content-grid"><div class="session-resources"><details class="session-interpretation" id="session-interpretation"><summary>How to read this record</summary><p>Explanation</p></details><details class="details" id="session-evidence-tools"><summary>Session evidence &amp; diagnostics</summary><div>Evidence</div></details></div><div class="session-history-pane"><h3>Test history</h3><div class="session-empty"><h3>No checks completed yet</h3><p>Run a test to start collecting results.</p><button class="button primary">Go to test →</button></div></div></div></div></div>'''
html='<!doctype html><html data-theme="dark"><head><meta charset="utf-8"><style>'+base+component+'</style></head><body>'+fixture+'</body></html>'
selectors=['#output-review','#transaction-details','#session-interpretation','#session-evidence-tools']
results=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    for width in (1440,):
        page=browser.new_page(viewport={'width':width,'height':900})
        page.set_content(html,wait_until='domcontentloaded',timeout=10000)
        for theme in ('dark','light'):
            page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
            for selector in selectors:
                row=page.locator(selector)
                row.evaluate('e=>e.removeAttribute("open")')
                summary=row.locator(':scope > summary')
                b=summary.evaluate('e=>({display:getComputedStyle(e).display,cursor:getComputedStyle(e).cursor,label:getComputedStyle(e,"::after").content})')
                summary.click(timeout=2500)
                a=summary.evaluate('e=>({open:e.parentElement.open,label:getComputedStyle(e,"::after").content})')
                assert b['display']=='flex' and b['cursor']=='pointer' and 'Show' in b['label'] and a['open'] and 'Hide' in a['label'],(width,theme,selector,b,a)
                # Keyboard Space closes native details: retains real browser semantics.
                summary.focus();summary.press('Space',timeout=2500)
                assert not row.evaluate('e=>e.open'),(width,theme,selector,'Space did not close')
                results.append(f'{width}-{theme}-{selector}')
            c=page.locator('.session-empty .button.primary').evaluate('e=>({color:getComputedStyle(e).color,cursor:getComputedStyle(e).cursor})')
            assert c['color']=='rgb(7, 24, 32)' and c['cursor']=='pointer',(width,theme,c)
            results.append(f'{width}-{theme}-CTA')
        page.close()
    browser.close()
print(json.dumps({'scope':'isolated CSS/native detail semantics; full app navigation excluded','passed':len(results),'failed':0,'cases':results}))
