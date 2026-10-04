/* src/15-qr-render.js: reconstructed from the reviewed v0.13.0-rc2 distribution.
 * Application symbols retained for traceability; this is not recovered original TypeScript.
 */
async function tv(canvas, text, width = 260, qrOptions = {}) {
    const content = qrOptions.alphanumeric ? [{ data: text, mode: 'alphanumeric' }] : text;
    const options = { errorCorrectionLevel: 'L', ...(qrOptions.version ? { version: qrOptions.version } : {}) };
    const modules = ev.create(content, options).modules.size;
    const scale = Math.max(8, Math.ceil(width / (modules + 8)));
    await ev.toCanvas(canvas, content, { ...options, margin: 4, scale });
    canvas.style.removeProperty('width');
    canvas.style.removeProperty('height');
}
var nv = class {
    canvas;
    frames;
    intervalMs;
    width;
    onError;
    qrOptions;
    timer = null;
    frameIndex = 0;
    constructor(canvas, frames, intervalMs = 350, width = 260, onError = () => { }, qrOptions = {}) {
        this.canvas = canvas;
        this.frames = frames;
        this.intervalMs = intervalMs;
        this.width = width;
        this.onError = onError;
        this.qrOptions = qrOptions;
    }
    get frameCount() { return this.frames.length; }
    start() {
        this.stop();
        this.draw();
        if (this.frames.length > 1)
            this.timer = setInterval(() => void this.draw(), this.intervalMs);
    }
    stop() { if (this.timer !== null)
        clearInterval(this.timer); this.timer = null; }
    async draw() {
        const frame = this.frames[this.frameIndex % this.frames.length];
        this.frameIndex++;
        try {
            await tv(this.canvas, frame.toUpperCase(), this.width, this.qrOptions);
        }
        catch {
            this.stop();
            this.onError();
        }
    }
};
