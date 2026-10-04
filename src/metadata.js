/* PSBT field inventory and ordered framing observations. The Bitcoin library remains
 * the semantic transaction/signature verifier. Key/value bytes and positions are recorded;
 * this is not a complete hidden-channel detector. Expected changes are versioned, not learned.
 */
function tbwPsbtMaps(bytes) {
    if (!(bytes instanceof Uint8Array) || bytes.length > TBW_LIMITS.bytes || !Pp(bytes, sp))
        tbwFail('PSBT_FRAME', 'Invalid or oversized PSBT envelope.');
    let pos = 5, fields = 0;
    const compact = (data, cursor) => {
        if (cursor.pos >= data.length) tbwFail('PSBT_TRUNCATED', 'Truncated PSBT length.');
        const marker = data[cursor.pos++]; if (marker < 253) return marker;
        const size = {253:2,254:4,255:8}[marker];
        if (cursor.pos + size > data.length) tbwFail('PSBT_TRUNCATED', 'Truncated PSBT length.');
        let result = 0n;
        for (let i = 0; i < size; i++) result |= BigInt(data[cursor.pos++]) << BigInt(i * 8);
        if (result < ({253:253n,254:65536n,255:4294967296n}[marker]) || result > BigInt(Number.MAX_SAFE_INTEGER))
            tbwFail('PSBT_COMPACT', 'Non-canonical or oversized PSBT integer.');
        return Number(result);
    };
    const readLength = () => { const cursor = {pos}; const value = compact(bytes, cursor); pos = cursor.pos; return value; };
    const read = length => {
        if (!Number.isSafeInteger(length) || length < 0 || pos + length > bytes.length)
            tbwFail('PSBT_TRUNCATED', 'Truncated PSBT key or value.');
        const value = bytes.slice(pos, pos + length); pos += length; return value;
    };
    const maps = [];
    while (pos < bytes.length) {
        if (maps.length >= TBW_LIMITS.psbtMaps) tbwFail('PSBT_MAP_LIMIT', 'PSBT has too many maps for this test flow.');
        const map = new Map();
        while (true) {
            const length = readLength(); if (length === 0) break;
            if (++fields > TBW_LIMITS.psbtFields) tbwFail('PSBT_FIELD_LIMIT', 'PSBT field-count limit reached.');
            const key = read(length), value = read(readLength()), hex = K.encode(key);
            if (map.has(hex)) tbwFail('PSBT_DUPLICATE', 'PSBT contains a duplicate key.');
            const cursor = {pos:0}, type = compact(key, cursor);
            map.set(hex, { key: hex, type, keyData: K.encode(key.slice(cursor.pos)), value: K.encode(value),
                valueBytes: value.length, sha256: K.encode(ns(value)) });
        }
        maps.push(map);
    }
    if (!maps.length) tbwFail('PSBT_EMPTY', 'PSBT global map is missing.');
    return maps;
}
const TBW_METADATA_POLICY = 'psbt-envelope-v3';
function tbwReducedResponse(maps, inputCount, version) {
    // Recognize a COMPLETE signature-only envelope, not arbitrary omissions or a device label.
    // The existing Bitcoin verifier must still bind the transaction and validate every signature.
    const globalTypes = version === 0 ? [0, 251] : [2, 3, 4, 5, 251];
    const inputTypes = version === 0 ? [] : [14, 15, 16];
    const outputTypes = version === 0 ? [] : [3, 4];
    if ([...maps[0].values()].some(f => !globalTypes.includes(f.type) || f.keyData)) return false;
    let kind = null;
    for (let index = 1; index <= inputCount; index++) {
        const fields = [...maps[index].values()];
        const partial = fields.filter(f => f.type === 2);
        const witness = fields.filter(f => f.type === 8 && !f.keyData);
        const thisKind = partial.length === 1 && !witness.length ? 'partial'
            : witness.length === 1 && !partial.length ? 'final' : null;
        if (!thisKind || (kind && kind !== thisKind)) return false;
        kind = thisKind;
        if (fields.some(f => !(inputTypes.includes(f.type) && !f.keyData) &&
            !(f.type === 3 && !f.keyData && f.value === '01000000') &&
            !(thisKind === 'partial' && f.type === 2) &&
            !(thisKind === 'final' && !f.keyData && (f.type === 8 || (f.type === 7 && f.value === ''))))) return false;
    }
    return maps.slice(inputCount + 1).every(map => [...map.values()].every(f => outputTypes.includes(f.type) && !f.keyData));
}
function tbwAssessMetadata(spec, artifact, root, preparedPsbtHex) {
    if (artifact.kind !== 'psbt') return tbwFreeze({ policy: TBW_METADATA_POLICY,
        status: 'not-applicable', label: 'No PSBT metadata', unexpected: 0, unchanged: 0,
        expected: 0, fields: [], fieldOrderAssessed: false, fieldOrderChanged: 0, fieldOrder: [], limitation: 'The returned artifact is a raw transaction, not a PSBT.' });
    const actual = tbwPsbtMaps(artifact.bytes);
    if (actual.length !== 1 + spec.inputs.length + spec.outputs.length)
        tbwFail('PSBT_MAP_COUNT', 'Returned PSBT contains missing or trailing maps. No complete-file result can be accepted.');
    const versionField = actual[0].get('fb');
    const version = versionField ? versionField.value === '02000000' ? 2 : versionField.value === '00000000' ? 0 : -1 : 0;
    if (version < 0) tbwFail('PSBT_VERSION', 'Unsupported PSBT version field.');
    const requestedBytes = preparedPsbtHex ? K.decode(preparedPsbtHex) : Tp(spec, root);
    const requested = tbwPsbtMaps(requestedBytes);
    const converted = version !== spec.psbtVersion;
    const expected = converted ? tbwPsbtMaps(wp(spec, root).toPSBT(version)) : requested;
    const reduced = tbwReducedResponse(actual, spec.inputs.length, version);
    const records = [], fieldOrder = []; let unchanged = 0, accepted = 0, unexpected = 0, supportingRemoved = 0, fieldOrderChanged = 0;
    const names = (index, field) => {
        const schema = index === 0 ? tf : index <= spec.inputs.length ? nf : of;
        return Object.entries(schema).find(([,info]) => info[0] === field.type)?.[0] ?? `unknown type ${field.type}`;
    };
    for (let mapIndex = 0; mapIndex < actual.length; mapIndex++) {
        const before = expected[mapIndex], after = actual[mapIndex];
        const isInput = mapIndex > 0 && mapIndex <= spec.inputs.length;
        const finalized = isInput && after.has('08');
        const scope = mapIndex === 0 ? 'global' : isInput ? 'input' : 'output';
        const index = mapIndex === 0 ? null : isInput ? mapIndex - 1 : mapIndex - spec.inputs.length - 1;
        // Compare relative order only among retained keys. Added signing fields and removed
        // supporting fields are not automatically reordering. Absolute positions retain the
        // complete returned sequence for independent inspection, including those new fields.
        const beforeKeys = [...before.keys()], afterKeys = [...after.keys()];
        const beforePositions = new Map(beforeKeys.map((key, pos) => [key, pos]));
        const afterPositions = new Map(afterKeys.map((key, pos) => [key, pos]));
        const retainedBefore = beforeKeys.filter(key => after.has(key));
        const retainedAfter = afterKeys.filter(key => before.has(key));
        const reordered = retainedBefore.some((key, pos) => key !== retainedAfter[pos]);
        if (reordered) fieldOrderChanged++;
        fieldOrder.push({scope, index, beforeCount: before.size, afterCount: after.size,
            comparedFields: retainedBefore.length, relativeOrderChanged: reordered});
        for (const key of new Set([...beforeKeys, ...afterKeys])) {
            const oldField = before.get(key), newField = after.get(key), field = newField ?? oldField;
            let change, classification, reason;
            if (oldField && newField && oldField.value === newField.value) {
                change = 'unchanged'; classification = 'unchanged'; reason = 'Preserved'; unchanged++;
            } else {
                change = !oldField ? 'added' : !newField ? 'removed' : 'changed';
                const signingAddition = isInput && !oldField && newField && (
                    field.type === 2 || (field.type === 8 && !field.keyData) ||
                    (field.type === 7 && !field.keyData && field.value === '') ||
                    (field.type === 3 && !field.keyData && field.value === '01000000'));
                const finalizedRemoval = isInput && finalized && !newField && [3,6].includes(field.type);
                const reducedRemoval = reduced && oldField && !newField &&
                    (isInput ? [1,3,6].includes(field.type) : scope === 'output' && field.type === 2);
                // Explicit v0 version=0 is a representational no-op. Unknown/proprietary data is not ignored.
                const explicitV0 = mapIndex === 0 && key === 'fb' && newField?.value === '00000000' && version === 0;
                if (signingAddition || finalizedRemoval || reducedRemoval || explicitV0) {
                    classification = 'expected'; reason = signingAddition ? 'Signing data checked by the signature verifier'
                        : reducedRemoval ? 'Supporting field omitted from a complete signature-only response; checked using the original prepared test'
                        : finalizedRemoval ? 'Input signing metadata removed during finalization' : 'Explicit PSBT version zero'; accepted++;
                    if (reducedRemoval) supportingRemoved++;
                } else {
                    classification = 'unexpected'; reason = 'Not an expected signing or finalization change'; unexpected++;
                }
            }
            records.push({ scope, index, field: names(mapIndex, field), key, type: field.type, change,
                classification, reason, beforePosition: beforePositions.get(key) ?? null, afterPosition: afterPositions.get(key) ?? null,
                beforeSha256: oldField?.sha256 ?? null, afterSha256: newField?.sha256 ?? null,
                beforeBytes: oldField?.valueBytes ?? null, afterBytes: newField?.valueBytes ?? null });
        }
    }
    return tbwFreeze({ policy: TBW_METADATA_POLICY, status: unexpected ? 'unexpected' : accepted || converted ? 'expected' : 'unchanged',
        label: unexpected ? 'File changes need review' : supportingRemoved ? 'Reduced signing response' : 'Only expected signing changes', unexpected, unchanged, expected: accepted,
        reducedResponse: !!supportingRemoved, supportingFieldsRemoved: supportingRemoved,
        requestedVersion: spec.psbtVersion, returnedVersion: version, versionConversion: converted,
        fields: records, fieldOrderAssessed: true, fieldOrderChanged, fieldOrder,
        fieldOrderBasis: converted ? 'same-version-local-reconstruction' : 'original-prepared-psbt',
        limitation: 'Field values and positions are recorded, not every hidden-information channel. Relative order compares retained keys; added-field placement is preserved in positions but not classified as reordering. Ordering can change legitimately and does not prove leakage. Reduced responses may omit supporting fields. Choices of order or retained data can carry information to a recipient of the PSBT, not necessarily to the blockchain. Unknown fields are not automatically malicious.' });
}
