/* Application coordinator. Private prepared test and immutable verification snapshot.
 * The camera controller owns its own lifecycle; the app projects its state only.
 * Former independent l/u references, verified ledgers and camera timer are retired.
 */
function Fv() {
    tbwReferenceSelfTest.apply();
    tbwReferenceSelfTest.verify();
    let e = '', t = null, n = null, r = '', i = '', a = null, s = null, c = null,
        d = '', f = 0, p = '', m = '';
    let prepared = null, failedPreparation = null, result = null, intake = null;
    let journal = new TbwSessionJournal(), installingGuided = false, seedRenderRequest = 0;
    let pendingWalletChange = null; // Transient operator intent; only randomizeAll changes the wallet.
    let captureReceipt = null;
    function finishCapture(app, outcome, code = null) {
        const receipt=captureReceipt; captureReceipt=null;
        if (!receipt) return;
        try {
            receipt.owner.recordCapture({test:receipt.test,outcome,code,transport:app.scan.diagnostics});
        } catch { /* Optional telemetry must not interfere with the camera or verifier. */ }
        app.sessionRevision++;
    }
    function h(mnemonic) {
        if (mnemonic !== e || !t) { t = up(mnemonic); e = mnemonic; }
        return t;
    }
    function renderSeed(app, mnemonic, explicit = false) {
        const payload = wm(mnemonic), canvas = app.$refs.seedQrCanvas;
        if (i === payload && !explicit) return;
        i = payload; const request = ++seedRenderRequest;
        app.seedQrVisible = false;
        if (!canvas) return;
        tv(canvas, payload, 840).then(() => {
            if (request === seedRenderRequest && e === mnemonic && sv(app.seed.value) === mnemonic)
                app.seedQrVisible = true;
        }).catch(() => {
            if (request !== seedRenderRequest || e !== mnemonic || sv(app.seed.value) !== mnemonic) return;
            app.seedQrVisible = false;
            app.qrProblem = 'Seed QR unavailable. Use the displayed test words.';
        });
    }
    function guidedHalt(app, message, type = 'control-error', code = null) {
        if (journal.halt(message, type, code)) {
            app.sessionRevision++; app.fileRequest++;
            n?.stop(); n = null; r = ''; app.psbtQrAvailable = false;
            Nv(app.$refs.psbtQrCanvas);
        }
    }
    function clearResult(app) { result = null; app.resultRevision++; }
    function preparationFailure(app, key, message) {
        prepared = null; failedPreparation = {key, message}; app.preparedRevision++;
        app.buildProblem = message; app.psbtQrAvailable = false;
        n?.stop(); n = null; r = ''; Nv(app.$refs.psbtQrCanvas);
        if (!sv(app.seed.value)) { app.seedQrVisible = false; i = ''; Nv(app.$refs.seedQrCanvas); app.accountXpub = ''; app.receiveAddressesText = ''; }
    }
    function commit(app, analysis, error, artifact) {
        const time = new Date().toISOString();
        const projected = journal.checks({completed:!!analysis?.ok,createdAt:time,test:app.testNumber,
            scenario:app.scenarioId,result:analysis?.matched ? 'match' : 'mismatch',evidence:analysis?.evidence,
            metadata:analysis?.metadata});
        const next = tbwResultSnapshot({ stateKey:app.stateSignature, artifactText:app.artifactText,
            analysis, error, prepared, publicTest:prepared?.publicTest,
            intake:{...intake, artifact}, timestamp:time,
            context:{test:app.testNumber, walletSession:app.walletSession, session:em(projected),
                sessionChecks:projected, scenario:app.scenarioId,
                scenarioCoverage:dm.map(scenario=>({...scenario,checked:projected.filter(check=>check.scenario===scenario.id).length})),
                step:app.step, inputs:app.inputs.length, outputs:app.outputs.length, psbtVersion:app.psbtVersion,
                supported:'BIP84 P2WPKH ECDSA only', device:String(app.device).slice(0,80),
                firmware:String(app.firmware).slice(0,80), signingPolicy:app.signingPolicy,
                physicalSession:journal.locked ? {planId:journal.status().planId,planSha256:journal.status().planSha256,
                    caseNumber:journal.status().current,requested:journal.status().requested,deviceOrigin:'not-attested'} : null} });
        journal.record(next.report, next.evidence); result = next; app.sessionRevision++;
        app.resultRevision++;
        if (analysis?.ok) {
            app.fileRequest++; app.stopScan(); n?.stop(); n = null; r = '';
            app.psbtQrAvailable = false; Nv(app.$refs.psbtQrCanvas);
            app.intakeOpen = app.pasteOpen = app.settingsOpen = false;
        }
    }
    const g = jv();
    return {
get referenceSelfCheck() { return tbwReferenceSelfTest.status(); },
githubUrl: `https://github.com/oren-z0/exfil-tester`,
step: 1,
acknowledged: !1,
device: ``,
firmware: ``,
settingsOpen: !1,
get releaseVersion() { return TBW_BUILD.version; },
get releaseSourceHash() { return TBW_BUILD.sourceSha256; },
workspaceView: 'test',
workspaceRequest: 0,
outputsOpen: false,
async showFileDetails() {
    this.cancelSectionFocus(); const request = ++this.workspaceRequest, state = this.stateSignature;
    this.workspaceView = 'test';
    const root = this.$refs.resultTools;
    if (root) root.open = true;
    await this.$nextTick?.();
    if (request !== this.workspaceRequest || this.workspaceView !== 'test' || state !== this.stateSignature) return;
    const item = root?.querySelector('#returned-file-details');
    if (item) { item.open = true; item.querySelector('summary')?.focus(); item.scrollIntoView?.({block:'nearest'}); }
},
async openWorkspace(view) {
    if (!['test', 'advanced', 'session'].includes(view)) throw new RangeError('Unknown workspace');
    // Do not hide a live capture or acquire a new camera as a side effect of navigation.
    if (this.scan.active) { this.notice = 'Stop the camera before opening another workspace.'; return false; }
    this.cancelSectionFocus(); const request = ++this.workspaceRequest, epoch = this.epoch; this.workspaceView = view;
    if (view === 'advanced' && this.$refs.advancedTools) this.$refs.advancedTools.open = true;
    await this.$nextTick?.();
    if (request !== this.workspaceRequest || epoch !== this.epoch || this.workspaceView !== view) return false;
    // Workspace changes keep the shared navigation in place; focus must not scroll it away.
    const ref = view === 'advanced' ? 'advancedTitle' : view === 'session' ? 'sessionTitle'
        : this.step === 1 ? 'prepareTitle' : this.step === 2 ? 'signTitle' : 'resultTitle';
    this.$refs?.[ref]?.focus?.({preventScroll:true});
    return true;
},
async showAdvancedSettings() {
    if (!await this.openWorkspace('advanced')) return;
    const request = this.workspaceRequest; this.settingsOpen = true;
    await this.$nextTick?.();
    if (request !== this.workspaceRequest || this.workspaceView !== 'advanced') return;
    this.$refs.advancedTools?.querySelector('#transaction-editor > summary')?.focus();
},
get routineNotice() {
    return this.notice === 'New transaction ready. Use the test wallet already loaded on your device.' ||
        this.notice === 'Fresh test wallet created. Load this seed on your signing device.' ||
        this.notice === 'Session ended. Its record is in Session. Your current result is unchanged.';
},
get outputReview() {
    this.preparedRevision;
    if (!this.transactionReady || !prepared) return {ok:false,outputs:[],problem:''};
    try { return {ok:true,outputs:tbwOutputReview(prepared.publicTest,prepared.spec),problem:''}; }
    catch { return {ok:false,outputs:[],problem:'Output details are unavailable. Do not sign until the full destination list can be reviewed.'}; }
},
formatReviewAmount(value) { return Dv(BigInt(value), this.amountUnit); },
get sessionHistory() { this.sessionRevision; return journal.history(); },
get recordedReviewCount() { return this.sessionHistory.filter(row => row.type === 'check' && row.metadataStatus === 'unexpected').length; },
get recordedIncompleteCount() { return this.sessionHistory.filter(row => row.type === 'check' && !row.completed).length; },
get recordedOperationFailureCount() { this.sessionRevision; return journal.operationFailureCount(); },
historyLabel(row) {
    if (row.type === 'capture-attempt') return ({received:'Response captured',failed:'Capture failed',stopped:'Capture stopped'})[row.outcome];
    if (row.type !== 'check') return row.type === 'end' ? 'Session ended' : 'Operation stopped';
    return !row.completed ? 'Incomplete' : row.result !== 'match' ? 'Signatures differ' : row.metadataStatus === 'unexpected' ? 'File review needed' : 'Signatures matched';
},
historyTone(row) {
    if (row.type === 'capture-attempt') return row.outcome === 'failed' ? 'incomplete' : 'ended';
    if (row.type === 'end' && row.previousPhase !== 'halted') return 'ended';
    return row.type !== 'check' || !row.completed ? 'incomplete' : tbwFindingState(row.result,{status:row.metadataStatus});
},
scenarioName(id) { return dm.find(item => item.id === id)?.label ?? 'Custom transaction'; },
exportHistory() {
    // Detach public projection data before freezing. Freezing reactive proxies can break JSON export.
    return tbwFreeze(JSON.parse(JSON.stringify({schema:'tbw-session-history-v1',tool:'The Bitcoin Way Signature Lab',build:TBW_BUILD,
        walletSession:this.walletSession,summary:this.sessionSummary,scenarioCoverage:this.scenarioCoverage,
        recordedReviewFindings:this.recordedReviewCount,recordedIncompleteChecks:this.recordedIncompleteCount,
        events:this.sessionHistory,
        guidedSession:this.hasGuidedSession ? this.exportSessionReport() : null,
        deviceOrigin:'not-attested',firmwareInspected:false,
        scope:'Recorded response summaries, not an archive of every original response. Camera attempt summaries appear only when evidence retention was enabled. Save each current result before advancing for public replay evidence. A matching session does not certify firmware.'})));
},
downloadHistory() {
    try { tbwSaveJson(this.exportHistory(),'journal'); }
    catch { this.notice = 'Session download unavailable. The session remains in this tab.'; }
},
downloadResult() {
    // Reuse the existing authoritative exporter. Never rebuild or alter a result here.
    if (this.hasEvidence) return this.downloadEvidence();
    return this.downloadReport();
},
diagnosticIncludeResponse: false,
get retentionStatus() { this.sessionRevision; return journal.retentionStatus(); },
get retentionNotice() {
    const r=this.retentionStatus;
    return r.fault ? 'Session evidence retention stopped. Earlier evidence is intact; save new results separately.' : '';
},
setEvidenceRetention(enabled) {
    try { journal.retentionApply(enabled); this.sessionRevision++; }
    catch (error) { this.notice=error.message; }
},
exportSessionEvidence() { return journal.evidenceBundle(this.exportHistory()); },
downloadSessionEvidence() {
    try { tbwSaveJson(this.exportSessionEvidence(), 'journal'); }
    catch { this.notice='Session evidence download failed. Retained evidence is still in this tab.'; }
},
diagnosticPackage(includeResponse = false) {
    if (typeof includeResponse !== 'boolean') throw new TypeError('Choose whether to include the response.');
    const report=result?.report;
    const status=report ? {result:report.result,overallStatus:report.overallStatus,completed:report.completed,
        transactionId:report.evidence?.transactionId ?? null,artifactSha256:report.evidence?.artifactSha256 ?? null,
        metadataPolicy:report.metadata?.policy ?? null,metadataStatus:report.metadata?.status ?? null,
        unexpectedFields:report.metadata?.unexpected ?? 0} : null;
    const code=typeof this.scan.code==='string'&&/^[A-Z][A-Z0-9_]{0,63}$/.test(this.scan.code)?this.scan.code:null;
    return tbwFreeze({schema:'tbw-diagnostic-package-v1',build:TBW_BUILD,test:this.testNumber,
        walletSession:this.walletSession,operatorNotes:{device:String(this.device).slice(0,80),firmware:String(this.firmware).slice(0,80),verified:false},
        status,scan:{phase:this.scan.phase,code,...tbwDiagnosticCounts(this.scan.diagnostics)},
        retention:journal.retentionStatus(),captureAttempts:journal.history().filter(e=>e.type==='capture-attempt'),
        includedResponse:!!(includeResponse && result?.evidence),
        ...(includeResponse && result?.evidence ? {evidence:result.evidence} : {}),
        disclosure:includeResponse ? 'May include the original untrusted response; review before sharing. No locally held seed/private key is added.' :
            'Diagnostic-only: no response bytes, QR frames, private keys, local seed or exception text. Operator notes are unverified. Does not diagnose firmware.'});
},
downloadDiagnosticPackage(includeResponse = false) {
    try { tbwSaveJson(this.diagnosticPackage(includeResponse), 'notes'); }
    catch { this.notice='Diagnostic download failed. Your test is unchanged.'; }
},
pasteOpen: !1,
intakeOpen: !1,
wordCount: `12`,
testNumber: 1,
walletSession: tbwUUID(),
sessionRevision: 0,
get sessionChecks() { this.sessionRevision; return journal.checks(); },
get sessionSummary() { return em(this.sessionChecks); },
get walletFingerprint() {
    this.preparedRevision;
    try {
        const mnemonic = sv(this.seed.value);
        if (!mnemonic || !t || e !== mnemonic || !this.seedQrVisible || i !== wm(mnemonic)) return '';
        const fingerprint = t.fingerprint;
        return Number.isSafeInteger(fingerprint) && fingerprint >= 0 && fingerprint <= 0xffffffff
            ? fingerprint.toString(16).padStart(8,'0').toUpperCase() : '';
    } catch { return ''; }
},
generatedScenario: g.scenario,
generatedShape: Mv(g.lockTime, g.inputs, g.outputs),
get scenarioId() { return this.generatedScenario && this.generatedShape === Mv(this.lockTime, this.inputs, this.outputs) ? this.generatedScenario : `custom`; },
get scenarioLabel() { return dm.find(e => e.id === this.scenarioId)?.label ?? `Custom transaction`; },
get scenarioCoverage() { return dm.map(e => ({ ...e, checked: this.sessionChecks.filter(t => t.scenario === e.id).length })); },
get coveredScenarios() { return this.scenarioCoverage.filter(e => e.checked > 0).length; },
get completedAt() { this.resultRevision; return result?.completedAt ?? null; },
get isTestComplete() { return this.completedAt !== null; },
get testNumberDisplay() { return String(this.testNumber).padStart(3, `0`); },
epoch: 0,
fileRequest: 0,
notice: ``,
qrProblem: ``,
psbtQrAvailable: !1,
psbtQrMode: `ur`,
psbtQrCaption: ``,
get verifiedSignature() { this.resultRevision; return result?.stateKey ?? ''; },
get verifiedArtifact() { this.resultRevision; return result?.artifactText ?? ''; },
get builtStateSignature() { this.preparedRevision; return prepared?.stateKey ?? ''; },
get summary() { this.preparedRevision; return prepared?.summary ?? null; },
seed: Sv(rm(12)),
lockTime: g.lockTime,
psbtVersion: `0`,
amountUnit: `btc`,
inputs: g.inputs,
outputs: g.outputs,
get psbtBase64() { this.preparedRevision; return prepared?.psbt64 ?? ''; },
get variants() { this.preparedRevision; return prepared?.publicTest.references ?? []; },
get signedVsize() { this.preparedRevision; return prepared?.signedVsize ?? null; },
get signedTxid() { this.preparedRevision; return prepared?.signedTxid ?? null; },
buildProblem: `Enter a seed phrase to build the PSBT.`,
seedQrVisible: !1,
seedQrExpanded: !1,
accountXpub: ``,
receiveAddressesText: ``,
copiedKey: null,
artifactText: ``,
get analysis() { this.resultRevision; return result?.analysis ?? null; },
get parseProblem() { this.resultRevision; return result?.error ?? null; },
dragOver: !1,
scan: {diagnostics:null, active:false, phase:'stopped', code:null, progress:0, format:null, error:null, supported:typeof navigator !== 'undefined' && !!navigator.mediaDevices?.getUserMedia},
init() {
    this.$watch('stateSignature', () => this.scheduleRecompute());
    this.$watch('artifactText', () => {
        if (result && (this.artifactText !== result.artifactText || this.stateSignature !== result.stateKey) && !this.isTestComplete)
            clearResult(this);
    });
    window.addEventListener('pagehide', event => event.persisted ? this.pause() : this.destroy());
    window.addEventListener('pageshow', event => { if (event.persisted && !this.isTestComplete) this.recompute(); });
    this.recompute();
},
async focusSection(e, { scroll = true } = {}) { let t = ++f, n = this.epoch, r = this.step, view = this.workspaceView; try {
            if (await this.$nextTick?.(), t !== f || n !== this.epoch || r !== this.step || view !== this.workspaceView)
                return;
            let i = this.$refs?.[e];
            la(i?.ownerDocument); i?.focus?.({ preventScroll: !0 });
            // Navigation keeps the common controls stationary; explicit task actions may reveal their target.
            if (scroll) (i?.closest?.(`[data-scroll-anchor]`) ?? i)?.scrollIntoView?.({ block: `start`, behavior: `auto` });
        }
        catch { } },
cancelSectionFocus() { f++; },
focusCurrentSection(options = {}) {
    const target = this.workspaceView !== 'test' ? (this.workspaceView === 'advanced' ? 'advancedTitle' : 'sessionTitle')
        : this.step === 1 ? 'prepareTitle' : this.step === 2 ? 'signTitle'
        : this.resultState === 'unverified' ? 'intakeSection' : 'resultTitle';
    return this.focusSection(target, options);
},
get stateSignature() { return JSON.stringify([this.seed.value, this.lockTime.value, this.psbtVersion, this.signingPolicy, this.inputs.map(e => [e.utxoId.value, e.amount.value, e.pathSuffix.value, e.sequence.value]), this.outputs.map(e => [e.amount.value, e.dest.value])]); },
blurField(e, t) { e.error = t(e.value); },
inputField(e, t) { e.error && t(e.value) === null && (e.error = null); },
syncLastOutputBudgetError(e) { if (!this.outputs.length)
            return; let t = this.outputs[this.outputs.length - 1].amount, n = xv(t.value, this.parsedTotalIn(), this.parsedOtherOutputsTotal()), r = n && /exceed/i.test(n) ? n : null; e ? r ? t.error = r : t.error && /exceed/i.test(t.error) && (t.error = null) : t.error && /exceed/i.test(t.error) && !r && (t.error = null); },
blurTxField(e, t) { this.blurField(e, t), this.syncLastOutputBudgetError(!0); },
inputTxField(e, t) { this.inputField(e, t), this.syncLastOutputBudgetError(!1); },
otherUtxoIds(e) { return this.inputs.filter((t, n) => n !== e).map(e => cv(e.utxoId.value)).filter(e => e !== null).map(e => `${e.txid}:${e.vout}`); },
utxoValidator(e) { return t => gv(t, this.otherUtxoIds(e)); },
outputAmountValidator(e) { return t => e === this.outputs.length - 1 ? xv(t, this.parsedTotalIn(), this.parsedOtherOutputsTotal()) : _v(t); },
validateMnemonicText: mv,
validateLockTime: hv,
validateAmount: _v,
validateInputPathSuffix: vv,
validateSequence: yv,
validateOutputDest: bv,
parsedTotalIn() { let e = 0n; for (let t of this.inputs) {
            let n = lv(t.amount.value);
            if (n === null)
                return null;
            e += n;
        } return e; },
parsedOtherOutputsTotal() { let e = 0n; for (let t of this.outputs.slice(0, -1)) {
            let n = lv(t.amount.value);
            if (n === null)
                return null;
            e += n;
        } return e; },
setRandomLockTime() { if (journal.locked) { this.notice = 'End the guided session before editing its plan.'; return; } if (this.isTestComplete)
            return; let e; try {
            e = String(im());
        }
        catch {
            this.notice = `Could not randomize locktime. The current test is unchanged. Try again explicitly.`;
            return;
        } this.invalidate(), this.notice = ``, this.lockTime.value = e, this.lockTime.error = null; },
addInputRow() { if (journal.locked) { this.notice = 'End the guided session before editing its plan.'; return; } if (this.isTestComplete || this.inputs.length >= 20)
            return; let e; try {
            e = Ov();
        }
        catch {
            this.notice = `Could not add an input. The current test is unchanged. Try again explicitly.`;
            return;
        } this.invalidate(), this.notice = ``, this.inputs.push(e); },
removeInputRow(e) { if (journal.locked) { this.notice = 'End the guided session before editing its plan.'; return; } this.isTestComplete || this.inputs.length > 1 && (this.invalidate(), this.inputs.splice(e, 1)); },
generateRandomInputs() { if (journal.locked) { this.notice = 'End the guided session before editing its plan.'; return; } if (this.isTestComplete)
            return; let e; try {
            e = kv();
        }
        catch {
            this.notice = `Could not randomize inputs. The current test is unchanged. Try again explicitly.`;
            return;
        } this.invalidate(), this.notice = ``, this.inputs = e; },
addOutputRow() { if (journal.locked) { this.notice = 'End the guided session before editing its plan.'; return; } if (this.isTestComplete || this.outputs.length >= 20)
            return; let e; try {
            e = om();
        }
        catch {
            this.notice = `Could not add an output. The current test is unchanged. Try again explicitly.`;
            return;
        } this.invalidate(), this.notice = ``, this.outputs.push({ id: Cv++, amount: Sv(``), dest: Sv(e) }); },
removeOutputRow(e) { if (journal.locked) { this.notice = 'End the guided session before editing its plan.'; return; } this.isTestComplete || this.outputs.length > 1 && (this.invalidate(), this.outputs.splice(e, 1)); },
get canGenerateRandomOutputs() { let e = this.parsedTotalIn(); return e !== null && e <= 2100000000000000n && e >= BigInt(1342); },
generateRandomOutputs() { if (journal.locked) { this.notice = 'End the guided session before editing its plan.'; return; } if (this.isTestComplete)
            return; let e = this.parsedTotalIn(); if (e === null || e > 2100000000000000n || e < BigInt(1342))
            return; let t; try {
            t = Av(e);
        }
        catch {
            this.notice = `Could not randomize outputs. The current test is unchanged. Try again explicitly.`;
            return;
        } this.invalidate(), this.notice = ``, this.outputs = t; },
scheduleRecompute() {
    if (this.isTestComplete || this.stateSignature === d) return;
    this.invalidate(); if (c !== null) clearTimeout(c);
    c = setTimeout(() => { c = null; this.recompute(); }, 150);
},
buildSpec() { if (this.inputs.length < 1 || this.inputs.length > 20 || this.outputs.length < 1 || this.outputs.length > 20)
            return { problem: `Use 1 to 20 inputs and outputs.` }; if (![`0`, `2`].includes(this.psbtVersion))
            return { problem: `Choose PSBT v0 or v2.` }; let e = sv(this.seed.value); if (!e)
            return { problem: `Enter a valid seed phrase to build the PSBT.` }; let t = fv(this.lockTime.value); if (t === null)
            return { problem: `Fix the nLockTime field to build the PSBT.` }; let n = [], r = new Set; for (let e = 0; e < this.inputs.length; e++) {
            let t = this.inputs[e], i = cv(t.utxoId.value), a = lv(t.amount.value), o = uv(t.pathSuffix.value), s = dv(t.sequence.value);
            if (!i || a === null || !o || s === null)
                return { problem: `Fix input #${e + 1} to build the PSBT.` };
            let c = `${i.txid}:${i.vout}`;
            if (r.has(c))
                return { problem: `Input #${e + 1} spends the same UTXO as another input.` };
            r.add(c), n.push({ txid: i.txid, vout: i.vout, amountSats: a, account: o.account, change: o.change, addressIndex: o.addressIndex, sequence: s });
        } let i = []; for (let e = 0; e < this.outputs.length; e++) {
            let t = this.outputs[e], n = lv(t.amount.value), r = pv(t.dest.value);
            if (n === null || !r)
                return { problem: `Fix output #${e + 1} to build the PSBT.` };
            i.push({ amountSats: n, dest: r });
        } let a = xp(n); if (a > 2100000000000000n)
            return { problem: `Total inputs exceed the 21 million BTC monetary limit. Reduce the test amounts.` }; let o = i.reduce((e, t) => e + t.amountSats, 0n); return o > a ? { problem: `Total outputs (${o} sats) exceed total inputs (${a} sats).` } : { spec: { mnemonic: e, lockTime: t, psbtVersion: this.psbtVersion === `0` ? 0 : 2, inputs: n, outputs: i } }; },
setPsbtQrMode(mode) {
            if (this.isTestComplete || !['ur', 'bbqr'].includes(mode) || mode === this.psbtQrMode)
                return;
            this.psbtQrMode = mode;
            if (this.transactionReady)
                this.renderPsbtQr(Ra.decode(this.psbtBase64));
        },
renderPsbtQr(bytes) {
            if (journal.locked && !this.checkGuidedBinding()) return;
            if (this.isTestComplete || (journal.locked && !journal.canReceive))
                return;
            const canvas = this.$refs.psbtQrCanvas;
            if (!canvas)
                return;
            const key = this.psbtQrMode + ':' + Ra.encode(bytes);
            if (r === key)
                return; // Also latches a failed render until explicit mode/test change.
            r = key;
            n?.stop();
            n = null;
            this.psbtQrAvailable = false;
            this.psbtQrCaption = '';
            this.qrProblem = '';
            try {
                if (!Nv(canvas))
                    throw Error('QR canvas unavailable');
                let frames, options = {}, interval = 350, caption;
                if (this.psbtQrMode === 'bbqr') {
                    const plan = tbwBBQrCodec().plan(bytes, 'P');
                    frames = plan.frames;
                    const longest = frames.reduce((a, b) => a.length >= b.length ? a : b);
                    const version = ev.create([{ data: longest, mode: 'alphanumeric' }], { errorCorrectionLevel: 'L' }).version;
                    options = { version, alphanumeric: true };
                    interval = 250;
                    caption = `BBQr · PSBT · ${plan.encoding === 'Z' ? 'compressed' : 'Base32'}`;
                }
                else {
                    frames = w_(bytes);
                    caption = 'BC-UR · crypto-psbt';
                }
                const animator = new nv(canvas, frames, interval, 280, () => {
                    if (n !== animator)
                        return;
                    this.psbtQrAvailable = false;
                    this.psbtQrCaption = '';
                    this.qrProblem = 'Transaction QR unavailable. Change QR format or save/copy the PSBT instead.';
                }, options);
                n = animator;
                this.psbtQrCaption = `${caption} · ${frames.length} frame${frames.length === 1 ? '' : 's'}`;
                this.psbtQrAvailable = true;
                animator.start();
            }
            catch {
                this.qrProblem = 'Transaction QR unavailable. Change QR format or save/copy the PSBT instead.';
            }
        },
recompute(options = {}) {
    if (this.isTestComplete) return;
    if (journal.locked && !installingGuided && !this.checkGuidedBinding()) return;
    const key = this.stateSignature; d = key;
    // Failure latch and the successful cache are keyed by the complete form and policy.
    if (failedPreparation?.key === key && !options.explicit) return;
    if (prepared?.stateKey === key) {
        this.buildProblem = '';
        renderSeed(this, prepared.spec.mnemonic, !!options.explicit);
        if (this.$refs.psbtQrCanvas) this.renderPsbtQr(K.decode(prepared.psbtHex));
        return;
    }
    const form = this.buildSpec();
    if ('problem' in form) { preparationFailure(this, key, form.problem); return; }
    try {
        const spec = tbwFreeze(form.spec), root = h(spec.mnemonic);
        const psbt = Tp(spec, root), psbtHex = K.encode(psbt), references = Np(spec, root);
        const selectedReferences = tbwPolicyReferences(references, this.signingPolicy);
        if (!selectedReferences.length) throw new Error('No reference is available for the selected signing policy.');
        const publicTest = tbwPublicTest(spec, root, psbtHex, references);
        prepared = tbwFreeze({ stateKey:key, spec, psbtHex, psbt64:Ra.encode(psbt),
            references, selectedReferences, publicTest, summary:Cm(spec),
            signedVsize:Sp(references[0].txHex), signedTxid:Cp(references[0].txHex) });
        failedPreparation = null; this.preparedRevision++; this.buildProblem = '';
        renderSeed(this, spec.mnemonic, !!options.explicit);
        this.accountXpub = gp(root, 0); this.receiveAddressesText = _p(root, 0, 5).join('\n');
        if (this.$refs.psbtQrCanvas) this.renderPsbtQr(psbt);
    } catch (error) { preparationFailure(this, key, 'Cannot build the PSBT: ' + (error?.message ?? String(error)));
        if (journal.locked) guidedHalt(this, this.buildProblem, 'preparation-error'); }
},
verify() {
    if (this.isTestComplete || !this.canReceiveResponse()) return;
    if (!this.acknowledged) { this.notice = 'Confirm you are using a disposable test wallet first.'; return; }
    this.policyLocked = true;
    if (c !== null) { clearTimeout(c); c = null; }
    this.recompute();
    if (journal.locked && !this.canReceiveResponse()) return;
    this.step = 3; this.workspaceView = 'test'; this.intakeOpen = false;
    this.focusSection('resultTitle');
    const submission = this.artifactText;
    if (!submission.trim()) { commit(this, null, 'Paste, scan or import the signed test transaction first.'); return; }
    if (submission.length > TBW_LIMITS.text) { commit(this, null, 'The supplied data exceeds the 1 MiB limit.'); return; }
    if (!prepared || prepared.stateKey !== this.stateSignature || this.buildProblem) {
        commit(this, null, 'Fix the transaction form before checking the signed response.'); return;
    }
    let artifact;
    try {
        artifact = Pv(submission);
        const analysis = zp(prepared.spec, artifact, prepared.selectedReferences, h(prepared.spec.mnemonic), prepared.psbtHex);
        commit(this, analysis, null, artifact);
    } catch (error) { commit(this, null, error?.message ?? String(error), artifact); }
},
selectAll(e) { e.target.select(); },
async copyText(e, t) { try {
            await navigator.clipboard.writeText(e);
        }
        catch {
            let t = document.createElement(`textarea`);
            t.value = e, t.style.position = `fixed`, t.style.left = `-9999px`;
            try {
                if (document.body.appendChild(t), t.select(), !document.execCommand(`copy`))
                    throw Error(`Copy unsupported`);
            }
            catch {
                this.notice = `Copy unavailable. Select the text and copy it manually.`;
                return;
            }
            finally {
                t.remove();
            }
        } this.showCopied(t); },
async copyPsbt() { if (!this.checkGuidedBinding() || (journal.locked && !journal.canReceive)) return; if (!this.isTestComplete) {
            if (!this.transactionReady) {
                this.notice = `Wait for a valid, updated transaction before copying its PSBT.`;
                return;
            }
            await this.copyText(this.psbtBase64, `psbt`);
        } },
async copyTxid() { this.transactionReady && this.signedTxid && await this.copyText(this.signedTxid, `txid`); },
showCopied(e) { this.copiedKey = e, setTimeout(() => { this.copiedKey === e && (this.copiedKey = null); }, 1600); },
editArtifact() {
    if (this.isTestComplete || (journal.locked && !journal.canReceive)) return;
    this.fileRequest++; this.stopScan(); intake = null; clearResult(this);
},
acceptArtifact(text, details = {}) {
    if (this.isTestComplete || !this.canReceiveResponse()) return;
    if (details.method === 'camera') finishCapture(this, 'received');
    this.workspaceRequest++; this.workspaceView = 'test'; this.editArtifact(); this.artifactText = text;
    intake = { method:details.method ?? 'text', transport:details.transport ?? null,
        originalFileHex:details.originalFileHex ?? null };
    this.notice = ''; this.verify(); this.intakeOpen = false;
},
failImport(message) {
    if (this.isTestComplete || !this.canReceiveResponse()) return;
    this.artifactText = ''; intake = null; commit(this, null, message);
    this.intakeOpen = false; this.focusSection('resultTitle');
},
pasteArtifact(e) { if (this.isTestComplete)
            return; let t = e.clipboardData?.getData(`text/plain`); t && this.acceptArtifact(t); },
async scanSignedTransaction() { await this.startScan(); },
async openPaste() { this.isTestComplete || (this.step = 3, this.intakeOpen = !0, this.pasteOpen = !0, await this.focusSection(`artifactInput`)); },
async handleFileInput(e) { let t = e.target, n = t.files?.[0]; n && await this.loadFile(n), t.value = ``; },
async handleDrop(e) { this.dragOver = !1; let t = e.dataTransfer?.files?.[0]; t && await this.loadFile(t); },
async loadFile(file) {
    if (this.isTestComplete || !this.canReceiveResponse()) return;
    this.editArtifact(); this.step = 3; this.intakeOpen = true; this.focusSection('intakeSection');
    const epoch = this.epoch, state = this.stateSignature, request = ++this.fileRequest;
    if (file.size > TBW_LIMITS.bytes) { this.failImport('This file exceeds the 512 KiB limit.'); return; }
    try {
        const bytes = new Uint8Array(await file.arrayBuffer());
        if (this.epoch !== epoch || request !== this.fileRequest || this.stateSignature !== state) return;
        if (bytes.length > TBW_LIMITS.bytes) { this.failImport('This file exceeds the 512 KiB limit.'); return; }
        this.acceptArtifact(Lp(bytes), {method:'file', originalFileHex:K.encode(bytes)});
    } catch {
        if (this.epoch === epoch && request === this.fileRequest && this.stateSignature === state)
            this.failImport('The file could not be read. Select it again or paste the data.');
    }
},
async startScan() {
    if (this.isTestComplete || this.scan.active || !this.acknowledged || !this.canReceiveResponse()) return;
    this.recompute();
    if (this.buildProblem) { this.notice = this.buildProblem; return; }
    this.editArtifact(); this.policyLocked = true; this.step = 3; this.intakeOpen = true;
    this.scan.progress = 0; this.scan.format = null; this.scan.diagnostics = null;
    const epoch = this.epoch, state = this.stateSignature;
    s = new E_({source:'camera'});
    if (journal.retentionStatus().enabled) captureReceipt={owner:journal,test:this.testNumber};
    const controller = new iv(this.$refs.scanVideo,
        code => { if (a === controller && this.epoch === epoch && this.stateSignature === state) this.onScanHit(code); },
        () => { if (a === controller) { s = null; this.scan.progress = 0; this.focusSection('intakeSection'); } },
        status => { if (a === controller) { this.scan.active = status.active; this.scan.phase = status.phase;
            this.scan.error = status.error; this.scan.code = status.code;
            if (status.phase === 'failed') { finishCapture(this, 'failed', status.code); guidedHalt(this, status.error, 'capture-error', status.code); }
            else if (status.phase === 'stopped') finishCapture(this, 'stopped'); } });
    a = controller; this.focusSection('scanSection');
    try { await controller.start(); }
    catch { /* The sole lifecycle controller already published the terminal/cancelled state. */ }
},
onScanHit(code) {
    if (this.isTestComplete || !s) return;
    try {
        if (typeof code.text !== 'string' || code.text.length > TBW_LIMITS.frame || code.binary.length > TBW_LIMITS.bytes)
            tbwFail('QR_PAYLOAD_SIZE', 'QR payload exceeds the size limit.');
        if (code.binary.length && Pp(code.binary, sp)) {
            if (s.active) tbwFail('QR_MIXED', 'Mixed QR sequence formats. Start a new scan explicitly.');
            this.scan.progress = 1;
            this.acceptArtifact(K.encode(code.binary), {method:'camera', transport:{family:'binary',frames:1}}); return;
        }
        const state = s.feed(code.text); this.scan.diagnostics = state;
        this.scan.progress = state.done ? 1 : Math.min(state.progress, .99); this.scan.format = state.format;
        if (state.done) {
            const decoded = s.verify();
            this.acceptArtifact(decoded.kind === 'bytes' ? K.encode(decoded.bytes) : decoded.text,
                {method:'camera', transport:{...state, completeSubmission:false}});
        }
    } catch (error) {
        if (s) this.scan.diagnostics = s.status();
        a?.fail(error);
    }
},
scanDiagnostics() {
    return tbwFreeze({schema:'tbw-scan-diagnostics-v1',build:TBW_BUILD,
        phase:this.scan.phase,code:this.scan.code,error:this.scan.error,
        transport:this.scan.diagnostics ? tbwPublicCopy(this.scan.diagnostics) : null,
        signatureTestCompleted:this.isTestComplete,
        disclosure:'Capture diagnostics only. No raw QR content, seed or private key is included. This does not identify a device or establish firmware safety.'});
},
downloadScanDiagnostics() {
    try { tbwSaveJson(this.scanDiagnostics(), 'notes'); }
    catch { this.notice = 'Diagnostics download unavailable. Your test is unchanged.'; }
},
stopScan() {
    finishCapture(this, 'stopped');
    a?.stop(); a = null; s = null;
    this.scan.active = false;
    if (this.scan.phase !== 'failed') this.scan.phase = 'stopped';
},
get scanPercent() { return Math.min(this.scan.active ? 99 : 100, Math.floor(this.scan.progress * 100)); },
invalidate() {
    if (this.isTestComplete) return;
    this.epoch++; clearResult(this); intake = null; this.artifactText = ''; this.stopScan(); this.scan.diagnostics = null;
},
confirmWalletLoaded() {
    if (this.isTestComplete) return;
    this.recompute();
    if (this.buildProblem) { this.notice = this.buildProblem; return; }
    this.acknowledged = true;
    // This is a task action, not a navigation tab: reveal the review on a long mobile wallet page.
    return this.goToStep(2, { scroll: true });
},
beginPreparedTest(form, wallet) {
    if (journal.locked && !installingGuided) { this.notice = 'End the guided session before changing the test.'; return; }
    this.cancelSectionFocus(); this.workspaceRequest++; this.workspaceView = 'test'; this.outputsOpen = false;
    this.diagnosticIncludeResponse=false;
    clearResult(this); this.policyLocked = false; this.invalidate();
    if (wallet) {
        this.seed = Sv(wallet.mnemonic); this.wordCount = String(wallet.words);
        this.walletSession = wallet.session; journal = new TbwSessionJournal(); this.sessionRevision++;
        this.testNumber = 1; this.acknowledged = false;
    } else this.testNumber++;
    this.lockTime = form.lockTime; this.inputs = form.inputs; this.outputs = form.outputs;
    this.generatedScenario = form.scenario; this.generatedShape = Mv(form.lockTime,form.inputs,form.outputs);
    this.intakeOpen = this.pasteOpen = this.settingsOpen = false;
    this.step = this.acknowledged ? 2 : 1;
    this.notice = wallet ? 'Fresh test wallet created. Load this seed on your signing device.' :
        this.acknowledged ? 'New transaction ready. Use the test wallet already loaded on your device.' : '';
    this.recompute(); if (journal.locked) this.policyLocked = true;
    this.focusSection(this.step === 2 ? 'signTitle' : 'prepareTitle');
},
randomizeTransaction(e) { if (journal.locked) {
    if (e !== undefined) { this.notice = 'End the guided session before choosing another scenario.'; return; }
    return this.advanceGuidedSession();
} let t; try {
            t = jv(this.sessionChecks, e);
        }
        catch {
            this.notice = `Could not generate the next transaction. The current test is unchanged. Try again explicitly.`;
            return;
        } this.beginPreparedTest(t); },
walletChangeRevision: 0,
walletChangeWords: 12,
walletChangeError: '',
get walletChangePending() { this.walletChangeRevision; return pendingWalletChange !== null; },
requestWalletChange(words = this.wordCount === '24' ? 24 : 12, replaceSameLength = true) {
    if (words !== 12 && words !== 24) throw new RangeError('Choose 12 or 24 test words.');
    if (!replaceSameLength && String(words) === this.wordCount) return false;
    if (journal.locked) { this.notice = 'End the guided session before creating another test wallet. Its record remains in Session.'; return false; }
    if (this.scan.active) { this.notice = 'Stop the camera before replacing the test wallet.'; return false; }
    if (pendingWalletChange) return false;
    const used = this.acknowledged || this.hasGuidedSession || this.sessionHistory.length > 0 ||
        !!this.artifactText || !!this.parseProblem || !!this.scan.diagnostics;
    if (!used) {
        const previous = this.walletSession; this.randomizeAll(words);
        return this.walletSession !== previous;
    }
    const dialog = this.$refs?.walletChangeDialog;
    if (!dialog || dialog.isConnected === false || dialog.open || typeof dialog.showModal !== 'function') {
        this.notice = 'Wallet replacement confirmation is unavailable. Your wallet and records are unchanged.'; return false;
    }
    pendingWalletChange = Object.freeze({words, epoch:this.epoch, walletSession:this.walletSession,
        stateKey:this.stateSignature, resultRevision:this.resultRevision, sessionRevision:this.sessionRevision,
        fileRequest:this.fileRequest, wordCount:this.wordCount});
    this.walletChangeWords = words; this.walletChangeError = ''; this.walletChangeRevision++;
    this.cancelSectionFocus();
    try {
        dialog.showModal(); dialog.scrollTop = 0;
        this.$refs?.keepWallet?.focus?.({preventScroll:true});
        return true;
    } catch {
        this.cancelWalletChange();
        this.notice = 'Wallet replacement confirmation could not open. Your wallet and records are unchanged.'; return false;
    }
},
cancelWalletChange() {
    pendingWalletChange = null; this.walletChangeRevision++;
    try { if (this.$refs?.walletChangeDialog?.open) this.$refs.walletChangeDialog.close(); } catch {}
},
confirmWalletChange() {
    const intent = pendingWalletChange;
    if (!intent) return false;
    const unchanged = !journal.locked && !this.scan.active && intent.epoch === this.epoch &&
        intent.walletSession === this.walletSession && intent.stateKey === this.stateSignature &&
        intent.resultRevision === this.resultRevision && intent.sessionRevision === this.sessionRevision &&
        intent.fileRequest === this.fileRequest && intent.wordCount === this.wordCount;
    // Consume before applying: double clicks and stale/replayed callbacks cannot reset twice.
    this.cancelWalletChange();
    if (!unchanged) { this.notice = 'The test changed while confirmation was open. Nothing was replaced. Review the current result before trying again.'; return false; }
    this.randomizeAll(intent.words);
    return this.walletSession !== intent.walletSession;
},
saveBeforeWalletChange(kind) {
    if (!pendingWalletChange) return false;
    if (kind !== 'result' && kind !== 'session' && kind !== 'bundle') throw new RangeError('Unknown export choice');
    this.notice = ''; this.walletChangeError = '';
    try {
        if (kind === 'result') this.downloadResult(); else if (kind === 'bundle') this.downloadSessionEvidence(); else this.downloadHistory();
        if (this.notice) this.walletChangeError = this.notice;
    } catch { this.walletChangeError = 'Download unavailable. Keep this wallet to preserve its result and record.'; }
    return !this.walletChangeError;
},
selectSeedLength(e) { if (e !== 12 && e !== 24)
            throw RangeError(`Choose 12 or 24 test words.`); String(e) !== this.wordCount && this.randomizeAll(e); },
randomizeAll(e = this.wordCount === `24` ? 24 : 12) { if (journal.locked) { this.notice = 'Save the session report and end the session before creating another wallet.'; return; } if (e !== 12 && e !== 24)
            throw RangeError(`Choose 12 or 24 test words.`); let t, n; try {
            t = { mnemonic: rm(e), session: tbwUUID(), words: e }, n = jv();
        }
        catch {
            this.notice = `Could not generate a new wallet. The current test is unchanged. Try again explicitly.`;
            return;
        } this.beginPreparedTest(n, t); },
nextStep() { this.goToStep(Math.min(3, this.step + 1)); },
goToStep(e, { scroll = false } = {}) {
    if (![1, 2, 3].includes(e)) throw new RangeError('Unknown test step');
    if (e !== 1 && !this.acknowledged) {
        this.notice = 'Confirm you are using a disposable test wallet first.';
        return false;
    }
    // Re-selecting Results is a no-op during capture: do not cancel a live/starting camera.
    if (e === 3 && this.step === 3 && this.workspaceView === 'test' && this.scan.active) return true;
    this.cancelSectionFocus();
    this.stopScan();
    if (e !== 1) {
        this.recompute();
        if (this.buildProblem) { this.notice = this.buildProblem; return false; }
    }
    this.workspaceRequest++;
    this.workspaceView = 'test'; this.step = e; this.notice = '';
    // Reopening intake is presentation only. Keep errors, evidence, paste content and guided holds.
    if (e === 3) this.intakeOpen = !this.isTestComplete;
    this.focusCurrentSection({ scroll });
    return true;
},
get resultState() {
    this.resultRevision;
    if (!result || result.stateKey !== this.stateSignature || result.artifactText !== this.artifactText) return 'unverified';
    return result.report.result;
},
inspect() { return { test: this.testNumber, walletSession: this.walletSession, session: this.sessionSummary, scenario: this.scenarioId, scenarioCoverage: this.scenarioCoverage, completed: this.isTestComplete, step: this.step, result: this.resultState, inputs: this.inputs.length, outputs: this.outputs.length, supported: `BIP84 P2WPKH ECDSA only`, signingPolicy: this.signingPolicy, metadataStatus: this.metadataSummary?.status ?? null, physicalSession:this.guidedStatus }; },
status() { return this.inspect(); },
plan() { let e = this.buildSpec(); return `problem` in e ? { ok: !1, error: e.problem } : { ok: !0, inputs: e.spec.inputs.length, outputs: e.spec.outputs.length }; },
apply() { this.recompute({explicit:true}); return this.plan(); },
rollback() { return this.randomizeAll(), this.inspect(); },
demonstration: { analysis: null, error: `` },
openExample() {
    if (this.scan.active) { this.notice = 'Stop the camera before opening the example.'; return false; }
    const dialog = this.$refs?.exampleDialog;
    if (!dialog || dialog.isConnected === false || typeof dialog.showModal !== 'function') {
        this.notice = 'The example is unavailable in this view. Your test is unchanged.'; return false;
    }
    if (dialog.open) { dialog.scrollTop = 0; this.$refs?.exampleTitle?.focus?.({preventScroll:true}); return true; }
    this.cancelSectionFocus();
    try {
        dialog.showModal();
        dialog.scrollTop = 0;
        this.runDemonstration();
        this.$refs?.exampleTitle?.focus?.({preventScroll:true});
        return true;
    } catch {
        try { dialog.close(); } catch {}
        this.notice = 'The example could not open. Your test is unchanged.'; return false;
    }
},
runDemonstration() { if (!(this.demonstration.analysis?.ok && !this.demonstration.error))
            try {
                let e = Up();
                !e.ok || e.matched || e.evidence?.signaturesVerified !== 2 ? (this.demonstration.error = `The example did not produce its expected result. Do not treat this as a successful check. Retry explicitly or use a verified release.`, this.demonstration.analysis = null) : (this.demonstration.analysis = e, this.demonstration.error = ``);
            }
            catch {
                this.demonstration.analysis = null, this.demonstration.error = `The example could not run. Your active test is unchanged. You can retry explicitly.`;
            } },
report() {
    this.resultRevision;
    if (!result || this.resultState === 'unverified') throw new Error('No current verified result is available.');
    return result.report;
},
downloadReport() { if (this.resultState === `unverified`) {
            this.notice = `Verify a signed test transaction before saving a report.`;
            return;
        } try {
            tbwSaveJson(this.report(), 'record');
        }
        catch {
            this.notice = `Report download unavailable. Your result is still visible on this page.`;
        } },
downloadPsbt() { if (!this.checkGuidedBinding() || (journal.locked && !journal.canReceive)) return; if (!this.isTestComplete && !(!this.transactionReady || !this.acknowledged))
            try {
                if (p !== this.psbtBase64) {
                    let e = Sm(this.scenarioId);
                    p = this.psbtBase64, m = e;
                }
                Qp(Ra.decode(this.psbtBase64), m, `application/octet-stream`);
            }
            catch {
                this.notice = `Download unavailable. Copy the PSBT or scan its QR code.`;
            } },
pause() { this.cancelWalletChange(); this.cancelSectionFocus(), this.fileRequest++, c !== null && clearTimeout(c), c = null, n?.stop(), n = null, r = ``, this.psbtQrAvailable = !1, this.stopScan(); },
destroy() {
    this.epoch++; this.pause(); seedRenderRequest++; this.seedQrVisible = false; i = ''; prepared = null; failedPreparation = null;
    clearResult(this); this.preparedRevision++; t = null; e = ''; intake = null;
},
parsedTotalOut() { let e = 0n; for (let t of this.outputs) {
            let n = lv(t.amount.value);
            if (n === null)
                return null;
            e += n;
        } return e; },
get transactionReady() { return !!this.psbtBase64 && !!this.summary && !this.buildProblem && this.builtStateSignature === this.stateSignature; },
get reviewSummary() { return this.transactionReady ? this.summary : null; },
get totalInDisplay() { return this.reviewSummary ? Dv(this.reviewSummary.inputSats, this.amountUnit) : `?`; },
get feeAmountDisplay() { return this.reviewSummary ? Dv(this.reviewSummary.feeSats, this.amountUnit) : `?`; },
get feeSatsDisplay() { return this.reviewSummary ? Dv(this.reviewSummary.feeSats, `sats`) : `?`; },
get feeRateDisplay() { return !this.reviewSummary || !this.signedVsize || this.signedVsize <= 0 ? `?` : (Number(this.reviewSummary.feeSats) / this.signedVsize).toFixed(2) + ` sat/vB`; },
get paymentsDisplay() { return this.reviewSummary ? Dv(this.reviewSummary.paymentSats, this.amountUnit) : `?`; },
get walletBalanceChangeDisplay() { return this.reviewSummary ? Dv(this.reviewSummary.walletDeltaSats, this.amountUnit) : `?`; },
get changeDisplay() { return this.reviewSummary ? Dv(this.reviewSummary.returnSats, this.amountUnit) : `?`; },
get outputRolesDisplay() { let e = this.reviewSummary; if (!e)
            return ``; let t = [`${e.recipientOutputs} recipient${e.recipientOutputs === 1 ? `` : `s`}`, `${e.changeOutputs} change`]; return e.selfTransferOutputs && t.push(`${e.selfTransferOutputs} self-transfer${e.selfTransferOutputs === 1 ? `` : `s`}`), t.join(` · `); },
get txidDisplay() { return this.transactionReady ? this.signedTxid ?? `?` : `?`; },
preparedRevision: 0,
resultRevision: 0,
signingPolicy: 'compatible',
policyLocked: false,
setSigningPolicy(policy) {
    if (!TBW_SIGNING_POLICIES.includes(policy)) throw new RangeError('Choose a supported signing policy.');
    if (this.isTestComplete || this.policyLocked || journal.locked) { this.notice = 'Start a new transaction before changing its signing policy.'; return; }
    if (policy === this.signingPolicy) return;
    this.invalidate(); this.signingPolicy = policy; this.recompute();
},
get signingPolicyLabel() { return this.signingPolicy === 'compatible' ? 'Compatibility: any supported reference' : Ap[this.signingPolicy]?.label ?? 'Unsupported policy'; },
get metadataSummary() { this.resultRevision; return result?.report.metadata ?? null; },
get metadataDetailCount() { return this.metadataSummary?.fields.filter(field => field.classification === 'unexpected').length ?? 0; },
get metadataDetails() {
    // Display only; the complete field records remain in the immutable report/evidence.
    return (this.metadataSummary?.fields.filter(field => field.classification === 'unexpected') ?? [])
        .slice(0, 32).map((field, index) => ({...field, displayId:index,
            key:field.key.length > 128 ? field.key.slice(0, 128) + '…' : field.key}));
},
get metadataDetailNotice() {
    return `Showing ${Math.min(this.metadataDetailCount, 32)} of ${this.metadataDetailCount} unexpected changes. Long keys are shortened here; Save result preserves the full details.`;
},
get metadataOrderExplanation() {
    const metadata = this.metadataSummary;
    if (!metadata?.fieldOrderAssessed) return '';
    const count = metadata.fieldOrderChanged;
    return count ? `Retained fields changed order in ${count} map${count === 1 ? '' : 's'}. This can be a normal file-format change; it is not proof of leakage. Original positions are saved in the evidence.`
        : 'No relative reordering of retained fields was observed. Added-field placement and omitted data can still carry information; full positions are saved in the evidence.';
},
get resultDisplayState() { return tbwFindingState(this.resultState, this.metadataSummary); },
get metadataExplanation() {
    const metadata = this.metadataSummary;
    if (metadata?.status === 'unexpected') return 'Signatures and transaction data were checked separately. These extra file changes are not explained by the supported signing formats. Save the evidence and inspect the changes. This is not, by itself, a malware or seed-leakage finding.';
    if (metadata?.status === 'not-applicable') return 'A raw transaction has no PSBT supporting fields to compare. Its transaction data and signatures were still checked.';
    if (metadata?.reducedResponse) return 'The signer returned the transaction and signatures without the original supporting fields. The Lab checked the signatures against its original test data. This recognized reduced format is not a file-change warning, but it does not prove the absence of hidden information.';
    return 'Only supported signing or finalization changes were found. This file check is separate from the signature result and is not a guarantee against every hidden-information channel.';
},
metadataFieldLabel(field) {
    const names = {witnessUtxo:'Previous-output amount and script',bip32Derivation:'Public-key derivation',partialSig:'Signature',finalScriptWitness:'Finalized signature data',proprietary:'Application-specific field',witnessScript:'Witness script',redeemScript:'Redeem script',xpub:'Extended public key'};
    return (field.scope === 'global' ? 'File' : field.scope[0].toUpperCase()+field.scope.slice(1)+' '+(field.index+1))+': '+(names[field.field] ?? field.field);
},
get completedScanNote() {
    this.resultRevision; const count = result?.report.transport?.rejectedFrames ?? 0;
    return count ? `${count} unreadable QR frame${count===1?' was':'s were'} not used. The complete response passed transport checks before signature verification.` : '';
},
get hasEvidence() { this.resultRevision; return this.resultState !== 'unverified' && !!result?.evidence; },
exportEvidence() {
    this.resultRevision;
    if (!this.hasEvidence) throw new Error('No current evidence is available.');
    return result.evidence;
},
downloadEvidence() {
    try { tbwSaveJson(this.exportEvidence(), 'detail'); }
    catch (error) { this.notice = 'Evidence download unavailable. Your result remains on this page. ' + (error?.message ?? ''); }
},
sessionCount: '20',
sessionEndReason: '',
get guidedStatus() { this.sessionRevision; return journal.status(); },
get guidedLocked() { this.sessionRevision; return journal.locked; },
get hasGuidedSession() { this.sessionRevision; return journal.hasPlan; },
get canStartGuided() { this.sessionRevision; return typeof tbwMakeGuidedPlan === 'function' && !journal.hasPlan && !this.policyLocked && !this.isTestComplete && !this.sessionChecks.length; },
get guidedPhaseLabel() { return ({receiving:'Awaiting signed response',ready:'Ready for the next transaction',
    halted:'Stopped: review required',complete:'Requested checks completed',ended:'Session ended',manual:'Individual checks'})[this.guidedStatus.phase]; },
checkGuidedBinding() {
    if (!journal.locked || installingGuided) return true;
    try {
        const mnemonic = sv(this.seed.value);
        if (!t || !mnemonic || e !== mnemonic) throw new Error('The test wallet changed during the session.');
        journal.verify({caseNumber:this.testNumber,walletSession:this.walletSession,rootPublicKey:K.encode(t.publicKey),policy:this.signingPolicy,
            psbtVersion:this.psbtVersion,caseIdentity:tbwCaseIdentity(tbwFormCase({lockTime:this.lockTime,inputs:this.inputs,outputs:this.outputs},this.psbtVersion))});
        return true;
    } catch (error) {
        guidedHalt(this,error?.message ?? 'The session plan changed.');
        this.notice = journal.status().reason; return false;
    }
},
canReceiveResponse() {
    if (!journal.canRecord) { this.notice = 'Session history limit reached. Save the reports and create a fresh disposable wallet.'; return false; }
    if (!this.checkGuidedBinding()) return false;
    if (!journal.canReceive) { this.notice = 'This session is not accepting another response. Save the evidence and end it explicitly.'; return false; }
    return true;
},
startGuidedSession() {
    try {
        // No change to core state on bad count, unavailable planner or failed generation.
        if (typeof tbwSessionCount !== 'function' || typeof tbwMakeGuidedPlan !== 'function') throw new Error('Guided planning is unavailable. Individual checks remain available.');
        const count = tbwSessionCount(this.sessionCount);
        if (!this.canStartGuided) throw new Error('Start a fresh disposable wallet before planning another session.');
        if (!this.transactionReady || !t || e !== sv(this.seed.value)) throw new Error('Prepare a valid disposable wallet first.');
        const plan = journal.plan(count,{walletSession:this.walletSession,rootPublicKey:K.encode(t.publicKey),
            fingerprint:t.fingerprint.toString(16).padStart(8,'0').toUpperCase(),policy:this.signingPolicy,psbtVersion:this.psbtVersion});
        const first = tbwRestoreCase(plan.cases[0]);
        journal.apply(plan); this.sessionRevision++;
        installingGuided = true;
        try { this.testNumber = 0; this.beginPreparedTest(first); }
        finally { installingGuided = false; }
        if (this.buildProblem) guidedHalt(this,this.buildProblem,'preparation-error');
        else this.notice = 'Session plan fixed. Review and sign each transaction on your physical device. Nothing is signed automatically.';
    } catch (error) { this.notice = error?.message ?? 'Session planning failed. The current test is unchanged.'; }
},
advanceGuidedSession() {
    if (!this.checkGuidedBinding()) return;
    if (!journal.canAdvance) { this.notice = 'Check this transaction first. A stopped or completed session must be ended explicitly.'; return; }
    try {
        // Copy the next case before changing the cursor, then use the sole test transition.
        const next = journal.report().plan.cases[journal.status().current];
        const form = tbwRestoreCase(next);
        journal.advance(); this.sessionRevision++; installingGuided = true;
        try { this.beginPreparedTest(form); } finally { installingGuided = false; }
        if (this.buildProblem) guidedHalt(this,this.buildProblem,'preparation-error');
    } catch (error) { installingGuided=false; guidedHalt(this,error?.message ?? 'Could not prepare the next planned transaction.');this.notice=journal.status().reason; }
},
endGuidedSession() {
    if (!journal.locked) return;
    this.pause();this.epoch++;journal.rollback(this.sessionEndReason.trim() || 'Ended by the operator.');this.sessionRevision++;
    this.notice = 'Session ended. Its record is in Session. Your current result is unchanged.';
    // Focus a stable visible control when the ended banner leaves the active workspace.
    this.$refs?.sessionNav?.focus?.({preventScroll:true});
},
exportSessionReport() { this.sessionRevision; return journal.report(); },
downloadSessionReport() {
    try { tbwSaveJson(this.exportSessionReport(), 'journal'); }
    catch (error) { this.notice = 'Session report download unavailable. '+(error?.message ?? 'Your session is still visible.'); }
}
    };
}
