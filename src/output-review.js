/* Read-only view of the exact prepared transaction; no signer, ledger or network. */
function tbwOutputReview(publicTest, spec) {
    if (!publicTest || !spec || publicTest.outputs.length !== spec.outputs.length) throw new Error('Output review unavailable');
    return tbwFreeze(publicTest.outputs.map((output, index) => {
        const item = spec.outputs[index], destination = item.dest;
        if (!['address','change'].includes(destination.kind) || String(item.amountSats) !== output.amountSats)
            throw new Error('Prepared output identity differs');
        const address = Lf(_d).encode(Df.decode(K.decode(output.scriptHex)));
        if (!address || !/^\d+$/.test(output.amountSats)) throw new Error('Invalid prepared output');
        return {index,amountSats:output.amountSats,address,scriptHex:output.scriptHex,
            role:destination.kind === 'address' ? 'Recipient' : destination.change === 1 ? 'Change' : 'Self-transfer',
            path:destination.kind === 'address' ? null : mp(destination.account,destination.change,destination.addressIndex)};
    }));
}
