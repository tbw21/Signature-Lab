#!/usr/bin/env python3
"""Run applicable frozen-candidate software stages; never patch or retry the candidate.
Requires preinstalled test tools listed in README. A failure stops the selected stage.
Individual stages may share an output directory, but existing result files are refused.
"""
from pathlib import Path
import argparse,subprocess,sys,os,hashlib,json
ROOT=Path(__file__).resolve().parent
STAGES=['environment','readability','evidence-upgrade','source-audit','static','core','browser','sessions','ux','remediation','calm','independent','tools','package','origins','alignment','onboarding','copy','reference','clarity','wallet-card','polish','delivery','feedback','harness']
class EnvironmentUnavailable(Exception): pass
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('html',type=Path);p.add_argument('archive',type=Path);p.add_argument('results',type=Path);p.add_argument('--stage',choices=['all',*STAGES],default='all');p.add_argument('--job',help='Run one exact named job for bounded execution; dependencies must already exist');p.add_argument('--list-jobs',action='store_true',help='Print the canonical job plan without executing tests');a=p.parse_args()
    html=a.html.resolve();archive=a.archive.resolve();out=a.results.resolve()
    if out.is_relative_to(ROOT):raise ValueError('Results must be outside the frozen source tree')
    identities={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [html,archive]};out.mkdir(parents=True,exist_ok=True)
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'};executed=[]
    def call(name,args,extra=None):
        if a.job and a.job!=name:return None
        executed.append(name)
        if a.list_jobs:return None
        result=out/(name+'.json');log=out/(name+'.log')
        if result.exists() or log.exists():raise FileExistsError('Refusing to replace previous evidence: '+name)
        if name != 'environment':
            prerequisite=out/'environment.json'
            if not prerequisite.is_file() or json.loads(prerequisite.read_text()).get('status')!='ready':
                raise EnvironmentUnavailable('Run --stage environment first; prerequisites have not been established.')
        print('RUN '+name,flush=True)
        with log.open('x') as stream:
            r=subprocess.run(list(map(str,args)),cwd=ROOT,env={**env,**(extra or {})},stdout=stream,stderr=subprocess.STDOUT,timeout=180)
        if name == 'environment' and r.returncode == 3:raise EnvironmentUnavailable('Missing or mismatched prerequisites; inspect '+str(result)+'. No candidate test was run.')
        if r.returncode:raise RuntimeError(name+' failed; inspect '+str(log)+'. Do not patch frozen bytes.')
        return result
    for stage in STAGES if a.stage=='all' else [a.stage]:
        before=len(executed)
        if stage=='environment':call('environment',[sys.executable,'tools/qualification_environment.py',out/'environment.json'])
        if stage=='readability':
            call('readability-static',[sys.executable,'tests/readability-static.py',html,out/'readability-static.json'])
            for first,last in [(1,8),(9,16),(17,24),(25,32),(33,40)]:
                name=f'readability-browser-{first}-{last}';call(name,[sys.executable,'tests/readability-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='evidence-upgrade':
            call('evidence-static',[sys.executable,'tests/evidence-static.py',html,out/'evidence-static.json'])
            for first,last in [(1,6),(7,10),(11,15),(16,20),(21,24)]:
                name=f'retention-{first}-{last}';call(name,['node','tests/evidence-retention.cjs',html,out/(name+'.json')],{'TEST_RANGE':f'{first}:{last}'})
            for first,last in [(1,8),(9,16),(17,24),(25,32)]:
                name=f'metadata-fixtures-{first}-{last}';call(name,['node','tests/metadata-fixtures.cjs',html,out/(name+'.json')],{'TEST_RANGE':f'{first}:{last}'})
            call('metadata-replay',[sys.executable,'tests/metadata-replay.py',html,out,out/'metadata-replay.json'])
            for first,last in [(1,2),(3,4),(5,6),(7,8)]:
                name=f'defects-{first}-{last}';call(name,['node','tests/deliberate-defects.cjs',html,out/(name+'.json')],{'TEST_RANGE':f'{first}:{last}'})
            for first,last in [(1,5),(6,10),(11,18)]:
                name=f'evidence-browser-{first}-{last}';call(name,[sys.executable,'tests/evidence-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='source-audit':
            call('audit-static',[sys.executable,'tests/audit-static.py',html,out/'audit-static.json'])
            call('audit-delivery',[sys.executable,'tests/audit-delivery.py',html,out/'audit-delivery.json'])
            for first,last in [(1,22),(23,40),(41,49)]:
                name=f'audit-contract-{first}-{last}';call(name,['node','tests/audit.cjs',html,out/(name+'.json')],{'TEST_RANGE':f'{first}:{last}'})
            for first,last in [(1,7),(8,14),(15,21)]:
                name=f'audit-browser-{first}-{last}';call(name,[sys.executable,'tests/audit-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='static':call('static',['node','tests/static.cjs',html,out/'static.json'])
        if stage=='core':
            for prefix,script,ranges in [('bbqr','unit.cjs',[(1,15),(16,40),(41,62)]),('regression','reliability.cjs',[(1,20),(21,40),(41,54)])]:
                for first,last in ranges:
                    name=f'{prefix}-{first}-{last}';call(name,['node','tests/'+script,html,out/(name+'.json')],{'TEST_RANGE':f'{first}:{last}'})
            call('camera',['node','tests/camera.cjs',html,out/'camera.json'])
        if stage=='browser':
            for first,last in [(1,20),(21,40),(41,48),(49,62)]:
                name=f'browser-{first}-{last}';call(name,[sys.executable,'tests/browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
            for first,last in [(1,15),(16,23)]:
                name=f'reliability-browser-{first}-{last}';call(name,[sys.executable,'tests/reliability-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='sessions':
            for first,last in [(1,29),(30,33),(34,38)]:
                name=f'sessions-{first}-{last}';call(name,['node','tests/sessions.cjs',html,out/(name+'.json')],{'TEST_RANGE':f'{first}:{last}'})
            for first,last in [(1,7),(8,14),(15,21),(22,28)]:
                name=f'sessions-browser-{first}-{last}';call(name,[sys.executable,'tests/sessions-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='ux':
            for first,last in [(1,12),(13,24),(25,36),(37,48)]:
                name=f'ux-{first}-{last}';call(name,[sys.executable,'tests/ux-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='remediation':
            for first,last in [(1,30),(31,50),(51,55)]:
                name=f'remediation-{first}-{last}';call(name,['node','tests/remediation.cjs',html,out/(name+'.json')],{'TEST_RANGE':f'{first}:{last}'})
            for first,last in [(1,9),(10,17),(18,28)]:
                name=f'remediation-browser-{first}-{last}';call(name,[sys.executable,'tests/remediation-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='calm':
            for first,last in [(1,10),(11,20),(21,30),(31,40)]:
                name=f'calm-{first}-{last}';call(name,['node','tests/calm.cjs',html,out/(name+'.json')],{'TEST_RANGE':f'{first}:{last}'})
            for first,last in [(1,8),(9,16),(17,24),(25,32)]:
                name=f'calm-browser-{first}-{last}';call(name,[sys.executable,'tests/calm-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
            call('output-oracle',[sys.executable,'tests/output-oracle.py',out/'calm-31-40-outputs.json',out/'output-oracle.json'])
        if stage=='alignment':
            for first,last in [(1,7),(8,15),(16,22)]:
                name=f'alignment-browser-{first}-{last}';call(name,[sys.executable,'tests/alignment-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='onboarding':
            call('onboarding-build',[sys.executable,'tests/onboarding-build.py',html,out/'onboarding-build.json'])
            call('onboarding-demo',['node','tests/onboarding.cjs',html,out/'onboarding-demo.json'])
            for first,last in [(1,5),(6,9),(10,14),(15,18)]:
                name=f'onboarding-browser-{first}-{last}';call(name,[sys.executable,'tests/onboarding-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='copy':
            call('copy-static',[sys.executable,'tests/copy-static.py',html,out/'copy-static.json'])
            for first,last in [(1,7),(8,11),(12,18)]:
                name=f'copy-browser-{first}-{last}';call(name,[sys.executable,'tests/copy-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='reference':
            call('reference-static',[sys.executable,'tests/reference-static.py',html,out/'reference-static.json'])
            for first,last in [(1,12),(13,24)]:
                name=f'reference-contract-{first}-{last}';call(name,['node','tests/reference.cjs',html,out/(name+'.json')],{'TEST_RANGE':f'{first}:{last}'})
            for first,last in [(1,7),(8,14)]:
                name=f'reference-browser-{first}-{last}';call(name,[sys.executable,'tests/reference-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
            call('reference-vectors',['node','tests/reference-vectors.cjs',html,out/'reference-vectors.json'])
            call('reference-independent',[sys.executable,'tests/reference-independent.py',out/'reference-vectors.json',out/'reference-independent.json'])
        if stage=='clarity':
            call('clarity-static',[sys.executable,'tests/clarity-static.py',html,out/'clarity-static.json'])
            for first,last in [(1,10),(11,20)]:
                name=f'clarity-contract-{first}-{last}';call(name,['node','tests/clarity.cjs',html,out/(name+'.json')],{'TEST_RANGE':f'{first}:{last}'})
            for first,last in [(1,10),(11,20),(21,30)]:
                name=f'clarity-browser-{first}-{last}';call(name,[sys.executable,'tests/clarity-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='wallet-card':
            call('wallet-card-static',[sys.executable,'tests/wallet-card-static.py',html,out/'wallet-card-static.json'])
            for first,last in [(1,7),(8,15),(16,26)]:
                name=f'wallet-card-browser-{first}-{last}';call(name,[sys.executable,'tests/wallet-card-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='polish':
            call('polish-static',[sys.executable,'tests/polish-static.py',html,out/'polish-static.json'])
            for first,last in [(1,7),(8,15),(16,25),(26,33)]:
                name=f'polish-browser-{first}-{last}';call(name,[sys.executable,'tests/polish-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='delivery':
            call('delivery-static',[sys.executable,'tests/delivery-static.py',html,out/'delivery-static.json'])
            for first,last in [(1,12),(13,24)]:
                name=f'delivery-contract-{first}-{last}';call(name,['node','tests/delivery.cjs',html,out/(name+'.json')],{'TEST_RANGE':f'{first}:{last}'})
            for first,last in [(1,7),(8,15),(16,22),(23,29)]:
                name=f'delivery-browser-{first}-{last}';call(name,[sys.executable,'tests/delivery-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='feedback':
            call('feedback-static',[sys.executable,'tests/feedback-static.py',html,out/'feedback-static.json'])
            for first,last in [(1,12),(13,24),(25,37)]:
                name=f'feedback-contract-{first}-{last}';call(name,['node','tests/feedback.cjs',html,out/(name+'.json')],{'TEST_RANGE':f'{first}:{last}'})
            for first,last in [(1,7),(8,16),(17,23),(24,29)]:
                name=f'feedback-browser-{first}-{last}';call(name,[sys.executable,'tests/feedback-browser.py',html,out/(name+'.json'),out/'screenshots'],{'TEST_RANGE':f'{first}:{last}'})
        if stage=='harness':
            call('harness-browser-1-3',[sys.executable,'tests/startup-harness.py',html,out/'harness-browser-1-3.json',out/'screenshots'])
        if stage=='independent':
            call('crypto-vectors',['node','tests/generate-vectors.cjs',html,out/'crypto-vectors.json'])
            for name,script in [('independent-crypto','independent-crypto.py'),('independent-structure','independent-structure.py')]:call(name,[sys.executable,'tests/'+script,out/'crypto-vectors.json',out/(name+'.json')])
            call('evidence-vectors',['node','tests/evidence-fixtures.cjs',html,out/'evidence-vectors.json'])
            call('evidence-replay',[sys.executable,'tests/evidence.py',out/'evidence-vectors.json',out/'evidence-replay.json'])
        if stage=='tools':call('release-tools',[sys.executable,'tests/release-tools.py',out/'release-tools.json'])
        if stage=='package':call('package',[sys.executable,'tests/package.py',html,archive,out/'package.json'])
        if stage=='origins':call('origins',[sys.executable,'tests/origins.py',html,out/'origins.json'])
        if a.list_jobs:continue
        if any(hashlib.sha256(Path(name).read_bytes()).hexdigest()!=value for name,value in identities.items()):raise RuntimeError('Frozen candidate identity changed; qualification rejected')
        if len(executed)==before:continue
        receipt=out/((('job-'+a.job) if a.job else stage)+'-identity.json')
        with receipt.open('x') as f:json.dump({'stage':stage,'jobs':executed[before:],'completeStage':not bool(a.job),'candidateIdentities':identities,'unchangedAfterStage':True},f,indent=2)
    if a.list_jobs:print(json.dumps(executed));return
    if not executed:raise ValueError('No matching qualification job selected')
    print('Selected software jobs completed. Review unavailable/external gates separately; no hardware or publisher acceptance implied.')
if __name__=='__main__':
    try:main()
    except EnvironmentUnavailable as exc:print('QUALIFICATION UNAVAILABLE-ENVIRONMENT: '+str(exc),file=sys.stderr);sys.exit(3)
    except Exception as exc:print('QUALIFICATION STOPPED: '+str(exc),file=sys.stderr);sys.exit(1)
