/* Sole camera lifecycle owner. No wallet or verification logic here. */
var iv = class {
    video; onCode; onError; onState; stream = null; rafId = null;
    lastDecodeTime = 0; lastText = null; lastTextTime = 0; generation = 0;
    phase = 'stopped'; failure = null; promise = null; resolveStart = null; rejectStart = null;
    startupTimer = null; captureTimer = null; healthTimer = null; listeners = [];
    lastFrameAt = 0; lastVideoTime = -1; stallSince = null;
    canvas = document.createElement('canvas');
    constructor(video, onCode, onError = () => {}, onState = () => {}, limits = {}) {
        this.video = video; this.onCode = onCode; this.onError = onError; this.onState = onState;
        this.limits = Object.freeze({ startup: 30000, capture: 120000, stall: 10000, ...limits });
        for (const value of Object.values(this.limits)) if (!Number.isSafeInteger(value) || value < 1)
            throw new TypeError('Camera deadlines must be positive whole milliseconds');
    }
    get running() { return this.status().active; }
    inspect() { return this.status(); }
    plan() { return Object.freeze({ supported: !!navigator.mediaDevices?.getUserMedia,
        startupMs: this.limits.startup, captureMs: this.limits.capture, stallMs: this.limits.stall }); }
    status() { return Object.freeze({ phase: this.phase,
        active: ['awaiting-permission', 'awaiting-video', 'scanning', 'stalled'].includes(this.phase),
        error: this.failure?.message ?? null, code: this.failure?.code ?? null }); }
    publish(phase) { this.phase = phase; this.onState(this.status()); }
    listen(target, type, handler) {
        target?.addEventListener?.(type, handler);
        this.listeners.push(() => target?.removeEventListener?.(type, handler));
    }
    settle(error) {
        if (error) this.rejectStart?.(error); else this.resolveStart?.();
        this.resolveStart = this.rejectStart = null;
    }
    cleanup() {
        this.generation++;
        for (const timer of [this.startupTimer, this.captureTimer, this.healthTimer]) if (timer !== null) clearTimeout(timer);
        this.startupTimer = this.captureTimer = this.healthTimer = null;
        if (this.rafId !== null) cancelAnimationFrame(this.rafId);
        this.rafId = null;
        for (const remove of this.listeners.splice(0)) remove();
        const stream = this.stream; this.stream = null;
        if (stream) for (const track of stream.getTracks()) { try { track.stop(); } catch {} }
        try { this.video.pause?.(); this.video.srcObject = null; } catch {}
        this.lastText = null; this.lastTextTime = 0; this.stallSince = null;
    }
    fail(error) {
        if (this.phase === 'failed' || this.phase === 'stopped') return;
        this.failure = error instanceof TBWFailure ? error
            : new TBWFailure('CAMERA_FAILURE', error?.message ?? String(error));
        this.cleanup(); this.publish('failed'); this.settle(this.failure); this.onError(this.failure);
    }
    stop() {
        const preserveFailure = this.phase === 'failed';
        this.cleanup(); this.settle(new TBWFailure('CAMERA_CANCELLED', 'Camera startup was cancelled.'));
        if (!preserveFailure) { this.failure = null; this.publish('stopped'); }
        this.promise = null;
    }
    rollback() { this.stop(); this.failure = null; this.publish('stopped'); return this.status(); }
    verify() { if (this.phase !== 'scanning') tbwFail('CAMERA_NOT_READY', 'The camera is not scanning.'); return this.status(); }
    apply() { return this.start(); }
    start() {
        if (this.running) return this.promise;
        if (this.phase === 'failed') return Promise.reject(new TBWFailure('CAMERA_FAILED', 'Start a new scan explicitly.'));
        const token = ++this.generation;
        this.failure = null; this.lastVideoTime = -1; this.lastDecodeTime = 0;
        const promise = new Promise((resolve, reject) => { this.resolveStart = resolve; this.rejectStart = reject; });
        this.promise = promise;
        this.publish('awaiting-permission');
        this.startupTimer = setTimeout(() => this.fail(new TBWFailure('CAMERA_START_TIMEOUT',
            'Camera permission or startup timed out. Start a new scan explicitly, or import a file.')), this.limits.startup);
        this.listen(document, 'visibilitychange', () => {
            if (document.visibilityState === 'hidden') this.fail(new TBWFailure('CAMERA_HIDDEN',
                'Camera stopped because the page was hidden. Return here and start a new scan.'));
        });
        const current = () => token === this.generation && this.running;
        const acquired = async (stream) => {
            if (!current()) { stream.getTracks().forEach(track => track.stop()); return; }
            this.stream = stream;
            const tracks = stream.getVideoTracks?.() ?? stream.getTracks();
            if (!tracks.length || tracks.every(track => track.readyState === 'ended'))
                throw new TBWFailure('CAMERA_ENDED', 'The camera stream ended. Start a new scan.');
            const ended = () => this.fail(new TBWFailure('CAMERA_ENDED', 'The camera stream ended. Start a new scan or import a file.'));
            const stalled = () => { if (this.phase === 'scanning') { this.stallSince ??= performance.now(); this.publish('stalled'); } };
            const resume = () => { if (this.phase === 'stalled') { this.stallSince = null; this.lastFrameAt = performance.now(); this.publish('scanning'); } };
            for (const track of tracks) { this.listen(track, 'ended', ended); this.listen(track, 'mute', stalled); this.listen(track, 'unmute', resume); }
            this.listen(stream, 'inactive', ended);
            this.listen(this.video, 'error', () => this.fail(new TBWFailure('CAMERA_VIDEO', 'The camera video failed. Start a new scan or import a file.')));
            for (const type of ['waiting', 'stalled']) this.listen(this.video, type, stalled);
            for (const type of ['playing', 'canplay']) this.listen(this.video, type, resume);
            this.video.srcObject = stream; this.video.setAttribute('playsinline', 'true');
            this.publish('awaiting-video');
            await this.video.play();
            if (!current()) return;
            clearTimeout(this.startupTimer); this.startupTimer = null;
            this.lastFrameAt = performance.now(); this.publish('scanning'); this.settle();
            this.captureTimer = setTimeout(() => this.fail(new TBWFailure('CAMERA_SCAN_TIMEOUT',
                'The two-minute scan limit was reached. Start a new scan explicitly or import a file.')), this.limits.capture);
            const health = () => {
                if (!current()) return;
                if (stream.active === false || tracks.every(track => track.readyState === 'ended')) { ended(); return; }
                const now = performance.now();
                if ((this.stallSince !== null && now - this.stallSince >= this.limits.stall) || now - this.lastFrameAt >= this.limits.stall) {
                    this.fail(new TBWFailure('CAMERA_STALLED', 'Camera video stopped updating. Start a new scan or import a file.')); return;
                }
                this.healthTimer = setTimeout(health, Math.min(1000, this.limits.stall));
            };
            this.healthTimer = setTimeout(health, Math.min(1000, this.limits.stall));
            const loop = () => {
                if (!current()) return;
                try {
                    if (this.video.readyState >= this.video.HAVE_ENOUGH_DATA && this.video.videoWidth &&
                        this.video.videoHeight && this.video.currentTime !== this.lastVideoTime) {
                        this.lastVideoTime = this.video.currentTime; this.lastFrameAt = performance.now();
                        if (!tracks.some(track => track.muted)) resume();
                    }
                    this.decodeFrame();
                } catch (error) {
                    this.fail(new TBWFailure('CAMERA_FRAME', 'The camera frame could not be read. Start a new scan or import a file.')); return;
                }
                if (current()) this.rafId = requestAnimationFrame(loop);
            };
            loop();
        };
        try {
            if (!navigator.mediaDevices?.getUserMedia) throw new TBWFailure('CAMERA_UNAVAILABLE', 'Camera unavailable here. Import the signed file or paste the QR text instead.');
            Promise.resolve(navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false }))
                .then(acquired).catch(error => {
                    if (!current()) return;
                    const message = error.name === 'NotAllowedError' ? 'Camera permission was denied. Allow camera access and try again.'
                        : error.name === 'NotFoundError' ? 'No camera was found on this device.'
                        : error.message ?? String(error);
                    this.fail(error instanceof TBWFailure ? error : new TBWFailure('CAMERA_START', message));
                });
        } catch (error) { this.fail(error); }
        return promise;
    }
    decodeFrame() {
        const now = performance.now(); if (now - this.lastDecodeTime < 100) return;
        this.lastDecodeTime = now; const video = this.video;
        if (video.readyState < video.HAVE_ENOUGH_DATA || !video.videoWidth || !video.videoHeight) return;
        const scale = Math.min(1, 1280 / Math.max(video.videoWidth, video.videoHeight));
        this.canvas.width = Math.max(1, Math.round(video.videoWidth * scale));
        this.canvas.height = Math.max(1, Math.round(video.videoHeight * scale));
        const context = this.canvas.getContext('2d', { willReadFrequently: true });
        if (!context) throw new Error('Camera canvas unavailable');
        context.drawImage(video, 0, 0, this.canvas.width, this.canvas.height);
        const image = context.getImageData(0, 0, this.canvas.width, this.canvas.height);
        const code = (0, rv.default)(image.data, image.width, image.height, { inversionAttempts: 'dontInvert' });
        if (!code || (!code.data && !code.binaryData?.length) || (code.data === this.lastText && now - this.lastTextTime < 400)) return;
        this.lastText = code.data; this.lastTextTime = now;
        this.onCode({ text: code.data, binary: new Uint8Array(code.binaryData ?? []) });
    }
};
