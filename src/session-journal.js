/* Sole historical session journal. Existing unique-transaction counts are a read-only
 * projection of these immutable public entries, never a second writable ledger.
 * Current result evidence remains owned by the existing immutable result snapshot. */
// Optional evidence uses the existing public result export; never accept a private snapshot here.
const TBW_RETENTION_LIMITS = Object.freeze({bytes:16*1024*1024, payloads:256, captures:256});
function tbwDiagnosticCounts(value = {}) {
    const out = {};
    for (const key of ['frames','rejectedFrames','consecutiveRejected']) {
        const n = value?.[key]; if (Number.isSafeInteger(n) && n >= 0) out[key] = n;
    }
    if (['ur','bbqr','binary','specter'].includes(value?.family)) out.family = value.family;
    return out;
}
class TbwSessionJournal {
    #entries = []; #plan = null; #cursor = 0; #phase = 'manual'; #reason = '';
    #approved = new WeakSet(); #checks = Object.freeze([]);
    #retain = false; #retentionFault = null; #captureOmitted = 0;
    #summary(entry) { const {_attachment, _retention, ...summary} = entry; return tbwFreeze(summary); }
    get canRecord() { return this.#entries.filter(e=>e.type !== 'capture-attempt').length < 2000; }
    retentionPlan(enabled) {
        if (typeof enabled !== 'boolean') throw new TypeError('Retention must be explicitly enabled or disabled.');
        return Object.freeze({enabled, limits:TBW_RETENTION_LIMITS, allowed:!enabled || !this.#retentionFault});
    }
    retentionApply(enabled) {
        const plan=this.retentionPlan(enabled);
        if (!plan.allowed) throw new Error('Evidence retention stopped for this wallet. Save existing evidence; start a new test wallet to retain more.');
        this.#retain=enabled; return this.retentionStatus();
    }
    retentionRollback() { return this.retentionApply(false); } // Retained bytes are never deleted here.
    retentionVerify() {
        const status=this.retentionStatus();
        if (status.bytes>status.limits.bytes || status.retained>status.limits.payloads) throw new Error('Evidence retention invariant failed.');
        return status;
    }
    retentionStatus() {
        const checks=this.#entries.filter(e=>e.type==='check');
        const retained=checks.filter(e=>e._attachment);
        return tbwFreeze({enabled:this.#retain, fault:this.#retentionFault, checks:checks.length,
            retained:retained.length, missing:checks.length-retained.length,
            bytes:retained.reduce((n,e)=>n+e._attachment.bytes,0), limits:TBW_RETENTION_LIMITS,
            captures:this.#entries.filter(e=>e.type==='capture-attempt').length, omittedCaptures:this.#captureOmitted,
            allRecordedChecksRetained:checks.length>0 && checks.length===retained.length,
            scope:'Recorded checks only; not unrun planned cases, all optical observations or proof of device origin.'});
    }
    #attachment(report, evidence) {
        if (!this.#retain) return {_retention:'not-enabled'};
        if (this.#retentionFault) return {_retention:this.#retentionFault};
        if (!evidence) return {_retention:'no-complete-response-evidence'};
        try {
            if (evidence.schema !== 'tbw-signature-evidence-v1' || evidence.report !== report ||
                !evidence.publicTest || !evidence.returnedArtifact || !Object.isFrozen(evidence))
                throw new Error('Unexpected public evidence binding');
            const json=JSON.stringify(evidence), bytes=new TextEncoder().encode(json), status=this.retentionStatus();
            if (status.retained>=TBW_RETENTION_LIMITS.payloads) this.#retentionFault='payload-limit';
            else if (bytes.length>TBW_RETENTION_LIMITS.bytes-status.bytes) this.#retentionFault='byte-limit';
            if (this.#retentionFault) return {_retention:this.#retentionFault};
            return {_retention:'retained',_attachment:Object.freeze({json,bytes:bytes.length,sha256:K.encode(ns(bytes))})};
        } catch { this.#retentionFault='retention-error'; return {_retention:this.#retentionFault}; }
    }
    recordCapture({test, outcome, code, transport}) {
        if (!this.#retain) return false;
        if (this.#entries.filter(e=>e.type==='capture-attempt').length>=TBW_RETENTION_LIMITS.captures) {
            this.#captureOmitted=Math.min(this.#captureOmitted+1,Number.MAX_SAFE_INTEGER);return false;
        }
        if (!Number.isSafeInteger(test) || test<1 || !['received','failed','stopped'].includes(outcome)) return false;
        this.#append({type:'capture-attempt',test,createdAt:new Date().toISOString(),outcome,
            code:typeof code==='string'&&/^[A-Z][A-Z0-9_]{0,63}$/.test(code)?code:null,
            transport:tbwDiagnosticCounts(transport)});
        return true;
    }
    operationFailureCount() {
        // A terminal guided capture records telemetry, then the existing control halt synchronously.
        // Keep both history events; do not count that pair as two stopped operations.
        return this.#entries.filter((row, i) => {
            if (row.type === 'check' || row.type === 'end') return false;
            if (row.type !== 'capture-attempt') return true;
            if (row.outcome !== 'failed') return false;
            const next=this.#entries[i+1];
            return !(row.sessionId && next?.type === 'capture-error' &&
                next.sessionId === row.sessionId && next.code === row.code);
        }).length;
    }
    evidenceBundle(context) {
        const status=this.retentionVerify();
        return tbwFreeze({schema:'tbw-session-evidence-v1',build:TBW_BUILD,walletSession:context.walletSession,
            history:context,coverage:status,events:this.#entries.map(entry=>({index:entry.index,
                type:entry.type,test:entry.test ?? null,retention:entry._retention ?? 'diagnostic-only',
                ...(entry._attachment ? {bytes:entry._attachment.bytes,sha256:entry._attachment.sha256,
                    evidenceJson:entry._attachment.json} : {})})),
            disclosure:'Only explicitly retained public result evidence is included. Missing responses are not reconstructed. Original returned data is untrusted and may contain hidden information. No locally held seed/private key is added. Reload or a new wallet clears this tab. Hashes do not authenticate the publisher or device.'});
    }
    get locked() { return !!this.#plan && this.#phase !== 'ended'; }
    get hasPlan() { return !!this.#plan; }
    get canAdvance() { return this.#phase === 'ready'; }
    get canReceive() { return !this.locked || this.#phase === 'receiving'; }
    checks(extra) {
        return extra?.completed ? tbwFreeze($p(this.#checks, this.#checkSummary(extra))) : this.#checks;
    }
    #checkSummary(report) {
        return {transactionId:report.evidence.transactionId, test:report.test, result:report.result,
            metadataStatus:report.metadata?.status ?? 'not-assessed',
            scenario:report.scenario, completedAt:report.createdAt};
    }
    #append(entry) {
        if (entry.type !== 'capture-attempt' && !this.canRecord) throw new Error('Session history limit reached. Save the reports and start a fresh disposable wallet.');
        this.#entries.push(tbwFreeze({...entry, index:this.#entries.length+1,
            sessionId:this.locked ? this.#plan.id : null,
            caseNumber:this.locked ? this.#cursor+1 : null}));
    }
    inspect() {
        const entries = this.#plan ? this.#entries.filter(e=>e.sessionId===this.#plan.id) : [];
        const checks = entries.filter(e=>e.type==='check' && e.completed);
        const outcomes = em(checks);
        return tbwFreeze({phase:this.#phase,active:this.locked,hasPlan:this.hasPlan,
            planId:this.#plan?.id ?? null,planSha256:this.#plan?.sha256 ?? null,
            current:this.#plan ? this.#cursor+1 : null,requested:this.#plan?.requested ?? 0,
            completed:checks.length,matched:outcomes.matched,review:outcomes.review,
            differed:outcomes.differed, countPolicy:TBW_SESSION_COUNT_POLICY,
            metadataWarnings:checks.filter(e=>e.metadataStatus==='unexpected').length,
            incomplete:entries.filter(e=>e.type==='check'&&!e.completed).length,
            captureFailures:entries.filter(e=>e.type==='capture-error').length,
            notCompleted:(this.#plan?.requested ?? 0)-checks.length,
            reason:this.#reason,canAdvance:this.canAdvance,canReceive:this.canReceive,
            evidenceScope:'Imported responses; physical signer origin is not attested.'});
    }
    status() { return this.inspect(); }
    history() { return Object.freeze(this.#entries.map(e=>this.#summary(e))); } // Public summaries only; attachments remain journal-owned.
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
    record(report, evidence = null) {
        if (!this.canReceive) throw new Error('The guided session is not accepting another response.');
        const entry={type:'check',createdAt:report.createdAt,test:report.test,scenario:report.scenario,
            completed:report.completed,result:report.result,
            transactionId:report.evidence?.transactionId ?? null,
            artifactSha256:report.evidence?.artifactSha256 ?? null,
            signaturesVerified:report.evidence?.signaturesVerified ?? 0,
            metadataStatus:report.metadata?.status ?? null,
            matchedAlgorithms:[...(report.matchedAlgorithms ?? [])],
            policy:report.signingPolicy.id,error:report.error ? String(report.error).slice(0,1000) : null};
        this.#append({...entry,...this.#attachment(report,evidence)});
        if (report.completed) this.#checks=tbwFreeze($p(this.#checks,this.#checkSummary(report)));
        if (this.locked) {
            if (!report.completed || tbwCheckOutcome(entry) !== 'matched') {
                this.#phase='halted';this.#reason=!report.completed ? 'The response could not be checked.' :
                    report.result !== 'match' ? 'The signatures differ from the required reference.' : 'The returned file requires review.';
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
            plan:this.#plan,status:this.inspect(),events:this.history().filter(e=>e.sessionId===this.#plan.id),
            evidenceScope:'This is a public plan and summary, not a full replay bundle. Save each current result separately with Save evidence before advancing when original responses are needed.',
            deviceOrigin:'not-attested',firmwareInspected:false,
            limitation:'Physical signing and approval are required but are not attested by the browser. Matching responses are not a firmware safety certificate. Counts measure imported checks, not proven hardware executions. No locally held seed or private key is exported.'});
    }
}
