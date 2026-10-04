/* Optional physical-session planner. No signer, firmware runner, signing reference or
 * verification result is produced here. A failed plan is never applied to the app. */
function tbwSessionCount(value) {
    const text = String(value);
    if (!/^[1-9]\d{0,2}$/.test(text) || Number(text) > 200)
        throw new RangeError('Choose a whole number of transactions from 1 to 200.');
    return Number(text);
}
function tbwFormCase(form, psbtVersion) {
    // Explicit public allowlist: never copy the reactive app or its seed/state key.
    return {scenario:form.scenario ?? 'custom', psbtVersion:String(psbtVersion),
        lockTime:String(form.lockTime.value),
        inputs:form.inputs.map(row => ({utxoId:row.utxoId.value, amount:row.amount.value,
            pathSuffix:row.pathSuffix.value, sequence:row.sequence.value})),
        outputs:form.outputs.map(row => ({amount:row.amount.value, dest:row.dest.value}))};
}
function tbwCaseIdentity(form) {
    // Scenario labels and row IDs are presentation, not transaction identity.
    return K.encode(ns(new TextEncoder().encode(JSON.stringify([form.psbtVersion, form.lockTime,
        form.inputs.map(row => [row.utxoId, row.amount, row.pathSuffix, row.sequence]),
        form.outputs.map(row => [row.amount, row.dest])]))));
}
function tbwRestoreCase(item) {
    const f = item.form;
    return {scenario:f.scenario, lockTime:Sv(f.lockTime),
        inputs:f.inputs.map(row => ({id:Cv++,utxoId:Sv(row.utxoId),amount:Sv(row.amount),
            pathSuffix:Sv(row.pathSuffix),sequence:Sv(row.sequence)})),
        outputs:f.outputs.map(row => ({id:Cv++,amount:Sv(row.amount),dest:Sv(row.dest)}))};
}
function tbwMakeGuidedPlan(count, context, generate = jv) {
    count = tbwSessionCount(count);
    if (!['0','2'].includes(context.psbtVersion) || !TBW_SIGNING_POLICIES.includes(context.policy) ||
        !/^(02|03)[a-f0-9]{64}$/.test(context.rootPublicKey) || typeof context.walletSession !== 'string')
        throw new Error('A prepared disposable wallet and signing policy are required.');
    const cases = [], selected = [], identities = new Set();
    for (let index = 0; index < count; index++) {
        const form = tbwFormCase(generate(selected), context.psbtVersion), identity = tbwCaseIdentity(form);
        if (identities.has(identity)) throw new Error('The planner repeated a transaction. Start a fresh plan explicitly.');
        identities.add(identity); selected.push({scenario:form.scenario});
        cases.push({number:index+1,identity,form});
    }
    const data = {schema:'tbw-physical-session-plan-v1', id:tbwUUID(), createdAt:new Date().toISOString(),
        requested:count, walletSession:context.walletSession, rootPublicKey:context.rootPublicKey,
        fingerprint:context.fingerprint, policy:context.policy, psbtVersion:context.psbtVersion, cases};
    const sha256 = K.encode(ns(new TextEncoder().encode(JSON.stringify(data))));
    return tbwFreeze({...data,sha256});
}
