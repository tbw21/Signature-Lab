/* Sole historical session journal. Existing unique-transaction counts are a read-only
 * projection of these immutable public entries, never a second writable ledger.
 * Current result evidence remains owned by the existing immutable result snapshot. */
class TbwSessionJournal {
    #entries = []; #plan = null; #cursor = 0; #phase = 'manual'; #reason = '';
    #approved = new WeakSet(); #checks = Object.freeze([]);
    get canRecord() { return this.#entries.length < 2000; }
    get locked() { return !!this.#plan && this.#phase !== 'ended'; }
    get hasPlan() { return !!this.#plan; }
    get canAdvance() { return this.#phase === 'ready'; }
    get canReceive() { return !this.locked || this.#phase === 'receiving'; }
    checks(extra) {
        return extra?.completed ? tbwFreeze($p(this.#checks, this.#checkSummary(extra))) : this.#checks;
    }
    #checkSummary(report) {
        return {transactionId:report.evidence.transactionId, test:report.test, result:report.result,
            scenario:report.scenario, completedAt:report.createdAt};
    }
    #append(entry) {
        if (!this.canRecord) throw new Error('Session history limit reached. Save the reports and start a fresh disposable wallet.');
        this.#entries.push(tbwFreeze({...entry, index:this.#entries.length+1,
            sessionId:this.locked ? this.#plan.id : null,
            caseNumber:this.locked ? this.#cursor+1 : null}));
    }
    inspect() {
        const entries = this.#plan ? this.#entries.filter(e=>e.sessionId===this.#plan.id) : [];
        const checks = entries.filter(e=>e.type==='check' && e.completed);
        return tbwFreeze({phase:this.#phase,active:this.locked,hasPlan:this.hasPlan,
            planId:this.#plan?.id ?? null,planSha256:this.#plan?.sha256 ?? null,
            current:this.#plan ? this.#cursor+1 : null,requested:this.#plan?.requested ?? 0,
            completed:checks.length,matched:checks.filter(e=>e.result==='match').length,
            differed:checks.filter(e=>e.result==='mismatch').length,
            metadataWarnings:checks.filter(e=>e.metadataStatus==='unexpected').length,
            incomplete:entries.filter(e=>e.type==='check'&&!e.completed).length,
            captureFailures:entries.filter(e=>e.type==='capture-error').length,
            notCompleted:(this.#plan?.requested ?? 0)-checks.length,
            reason:this.#reason,canAdvance:this.canAdvance,canReceive:this.canReceive,
            evidenceScope:'Imported responses; physical signer origin is not attested.'});
    }
    status() { return this.inspect(); }
    plan(count, context, generate) {
        if (this.#plan || this.#entries.length) throw new Error('Start a fresh disposable wallet before planning another session.');
        if (typeof tbwMakeGuidedPlan !== 'function') throw new Error('Guided planning is unavailable. Individual checks are still available.');
        const plan = tbwMakeGuidedPlan(count, context, generate);
        this.#approved.add(plan); return plan;
    }
    apply(plan) {
        if (this.#plan || this.#entries.length || !this.#approved.has(plan)) throw new Error('Only a fresh locally prepared plan can be started.');
        this.#approved.delete(plan);this.#plan=plan;this.#cursor=0;this.#phase='receiving';this.#reason='';
        return this.currentCase();
    }
    currentCase() { return this.#plan?.cases[this.#cursor] ?? null; }
    verify(binding) {
        if (!this.locked) return true;
        if (binding.walletSession !== this.#plan.walletSession || binding.rootPublicKey !== this.#plan.rootPublicKey ||
            binding.policy !== this.#plan.policy || binding.psbtVersion !== this.#plan.psbtVersion ||
            binding.caseIdentity !== this.currentCase().identity || binding.caseNumber !== this.#cursor+1)
            throw new Error('The wallet, transaction or policy differs from the frozen session plan. End this session before changing it.');
        return true;
    }
    record(report) {
        if (!this.canReceive) throw new Error('The guided session is not accepting another response.');
        const entry={type:'check',createdAt:report.createdAt,test:report.test,scenario:report.scenario,
            completed:report.completed,result:report.result,
            transactionId:report.evidence?.transactionId ?? null,
            artifactSha256:report.evidence?.artifactSha256 ?? null,
            signaturesVerified:report.evidence?.signaturesVerified ?? 0,
            metadataStatus:report.metadata?.status ?? null,
            matchedAlgorithms:[...(report.matchedAlgorithms ?? [])],
            policy:report.signingPolicy.id,error:report.error ? String(report.error).slice(0,1000) : null};
        this.#append(entry);
        if (report.completed) this.#checks=tbwFreeze($p(this.#checks,this.#checkSummary(report)));
        if (this.locked) {
            if (!report.completed || report.result !== 'match' || report.metadata?.status === 'unexpected') {
                this.#phase='halted';this.#reason=!report.completed ? 'The response could not be checked.' :
                    report.result !== 'match' ? 'The signatures differ from the required reference.' : 'The returned file contains unexpected metadata.';
            } else this.#phase=this.#cursor+1===this.#plan.requested ? 'complete' : 'ready';
        }
    }
    halt(message, type='control-error', code=null) {
        if (!this.locked || this.#phase==='halted') return false;
        this.#reason=String(message).slice(0,1000);
        this.#append({type,createdAt:new Date().toISOString(),message:this.#reason,code});
        this.#phase='halted';return true;
    }
    advance() {
        if (!this.canAdvance) throw new Error('Check the current transaction before advancing. Halted sessions must be ended explicitly.');
        this.#cursor++;this.#phase='receiving';return this.currentCase();
    }
    rollback(reason='Ended by the operator.') {
        if (!this.locked) return this.inspect();
        this.#append({type:'end',createdAt:new Date().toISOString(),previousPhase:this.#phase,
            reason:String(reason).slice(0,240)});
        if (!this.#reason) this.#reason=String(reason).slice(0,240);
        this.#phase='ended';return this.inspect();
    }
    report() {
        if (!this.#plan) throw new Error('No guided session has been planned.');
        return tbwFreeze({schema:'tbw-physical-session-summary-v1',tool:'The Bitcoin Way Signature Lab',build:TBW_BUILD,
            plan:this.#plan,status:this.inspect(),events:this.#entries.filter(e=>e.sessionId===this.#plan.id),
            evidenceScope:'This is a public plan and summary, not a full replay bundle. Save each current result separately with Save evidence before advancing when original responses are needed.',
            deviceOrigin:'not-attested',firmwareInspected:false,
            limitation:'Physical signing and approval are required but are not attested by the browser. Matching responses are not a firmware safety certificate. Counts measure imported checks, not proven hardware executions. No locally held seed or private key is exported.'});
    }
}
