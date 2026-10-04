/* Explicit allowlist for public evidence. Never serialize the private prepared object,
 * mnemonic, HD root, child private key or the reactive application object.
 */
const TBW_SIGNING_POLICIES = Object.freeze(['compatible', 'plain', 'grind-core', 'grind-embit']);
const TBW_SIGNING_POLICY_VERSION = 'deterministic-ecdsa-v1';
function tbwPolicyReferences(references, policy) {
    if (!TBW_SIGNING_POLICIES.includes(policy)) tbwFail('SIGNING_POLICY', 'Choose a supported signing policy.');
    return policy === 'compatible' ? references : references.filter(reference => reference.ids.includes(policy));
}
function tbwPublicTest(spec, root, psbtHex, references) {
    const tx = wp(spec, root);
    return tbwFreeze({ psbtHex, psbtVersion: spec.psbtVersion, unsignedTransactionHex: K.encode(tx.unsignedTx),
        version: 2, lockTime: spec.lockTime,
        inputs: spec.inputs.map((input, index) => {
            const publicKey = fp(root, input.account, input.change, input.addressIndex).publicKey;
            return { txid: input.txid, vout: input.vout, sequence: input.sequence,
                amountSats: input.amountSats.toString(), publicKeyHex: K.encode(publicKey),
                previousScriptHex: K.encode(Af(publicKey, _d).script), digestHex: K.encode(kp(tx, index, spec, root)),
                path: pp(input.account, input.change, input.addressIndex) };
        }),
        outputs: spec.outputs.map((output, index) => ({ amountSats: output.amountSats.toString(),
            scriptHex: K.encode(tx.getOutput(index).script) })),
        references: references.map(reference => ({ ids: [...reference.ids], txHex: reference.txHex, label: reference.label, wallets: reference.wallets })) });
}
function tbwPublicCopy(value) { return JSON.parse(JSON.stringify(value, (key, item) => typeof item === 'bigint' ? item.toString() : item)); }
// One scope classification shared by the report and the UI; no signing logic here.
function tbwFindingState(signatureResult, metadata) {
    return signatureResult === 'match' && metadata?.status === 'unexpected' ? 'review' : signatureResult;
}
function tbwResultSnapshot({ stateKey, artifactText, analysis, error, prepared, publicTest, intake, context, timestamp }) {
    const completed = !!analysis?.ok, time = timestamp ?? new Date().toISOString();
    const report = {
        schema: 'tbw-signature-result-v2', tool: 'The Bitcoin Way Signature Lab', version: Zp,
        edition: 'v' + Zp, build: TBW_BUILD, createdAt: time, ...tbwPublicCopy(Object.fromEntries(['test','walletSession','session','sessionChecks','scenario','scenarioCoverage','step','inputs','outputs','supported','device','firmware','physicalSession'].map(key => [key, context[key]]))),
        completed, result: error || !analysis?.ok ? 'incomplete' : analysis.matched ? 'match' : 'mismatch',
        psbtVersion: String(prepared?.spec.psbtVersion ?? context.psbtVersion ?? ''),
        signingPolicy: { id: context.signingPolicy, version: TBW_SIGNING_POLICY_VERSION, deviceQualified: false },
        matchedAlgorithms: completed ? [...(analysis.matched?.ids ?? [])] : [],
        evidence: completed ? tbwPublicCopy(analysis.evidence) : null,
        metadata: analysis?.metadata ? tbwPublicCopy(analysis.metadata) : null,
        error: error ?? (analysis?.ok === false ? analysis.error : null),
        deviceOrigin: 'not-attested', firmwareInspected: false,
        limitation: 'Signature spot check only. A match is not firmware certification. Public evidence cannot independently reproduce secret-key-derived nonces or prove hardware origin. Operator device/firmware labels are unverified. Twenty tests is not a safety threshold.'
    };
    report.overallStatus = tbwFindingState(report.result, report.metadata);
    report.transport = tbwPublicCopy(intake?.transport ?? intake?.artifact?.transport ?? {});
    const artifact = intake?.artifact;
    const evidence = artifact && publicTest ? {
        schema: 'tbw-signature-evidence-v1', report,
        publicTest,
        returnedArtifact: { kind: artifact.kind, hex: K.encode(artifact.bytes), sha256: K.encode(ns(artifact.bytes)) },
        submission: { method: intake.method ?? 'text', transport: tbwPublicCopy(intake.transport ?? artifact.transport ?? {}),
            ...(intake.method !== 'camera' ? { text: artifactText } : {}),
            ...(intake.originalFileHex ? { originalFileHex: intake.originalFileHex } : {}) },
        analysis: tbwPublicCopy(analysis),
        disclosure: 'No locally held seed or private key is added to this export. Original returned data is untrusted and could itself carry hidden or unexpected information. Use disposable tests only; review before sharing.'
    } : null;
    return tbwFreeze({ stateKey, artifactText, completedAt: completed ? time : null,
        analysis: analysis ? tbwPublicCopy(analysis) : null, error: report.error, report, evidence });
}
