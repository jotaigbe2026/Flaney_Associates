/* Minimal ZIP writer — STORED (no compression).
 *
 * The publisher hands back a folder of files that mirror the repo layout, and
 * a single archive is far less error-prone than eight separate downloads. The
 * site ships no bundler and no dependencies, so the format is written by hand.
 * Everything here is already compressed (JPEG/PNG) or tiny (HTML/JSON), so
 * skipping DEFLATE costs almost nothing and removes the only hard part.
 */
window.FlaneyZip = (function () {
    'use strict';

    const CRC_TABLE = (function () {
        const table = new Uint32Array(256);
        for (let i = 0; i < 256; i++) {
            let c = i;
            for (let k = 0; k < 8; k++) {
                c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
            }
            table[i] = c >>> 0;
        }
        return table;
    })();

    function crc32(bytes) {
        let c = 0xFFFFFFFF;
        for (let i = 0; i < bytes.length; i++) {
            c = CRC_TABLE[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8);
        }
        return (c ^ 0xFFFFFFFF) >>> 0;
    }

    function toBytes(data) {
        if (typeof data === 'string') return new TextEncoder().encode(data);
        if (data instanceof Uint8Array) return data;
        return new Uint8Array(data);
    }

    /* MS-DOS packed date/time. Files carry a real timestamp so an unzipped
       bundle doesn't look like it came from 1980. */
    function dosStamp(d) {
        const time = (d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() >> 1);
        const date = ((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
        return { time, date };
    }

    function Writer() {
        this.chunks = [];
        this.length = 0;
    }
    Writer.prototype.push = function (bytes) {
        this.chunks.push(bytes);
        this.length += bytes.length;
    };
    Writer.prototype.header = function (fields) {
        // fields: array of [byteWidth, value]
        let size = 0;
        fields.forEach(f => { size += f[0]; });
        const buf = new Uint8Array(size);
        const view = new DataView(buf.buffer);
        let off = 0;
        fields.forEach(function (f) {
            if (f[0] === 2) view.setUint16(off, f[1] >>> 0, true);
            else view.setUint32(off, f[1] >>> 0, true);
            off += f[0];
        });
        this.push(buf);
    };

    /* files: [{ name: 'blog/post.html', data: string | Uint8Array }] */
    function build(files, when) {
        const stamp = dosStamp(when || new Date());
        const out = new Writer();
        const central = [];

        files.forEach(function (file) {
            const name = new TextEncoder().encode(file.name);
            const data = toBytes(file.data);
            const crc = crc32(data);
            const offset = out.length;

            out.header([
                [4, 0x04034b50],        // local file header signature
                [2, 20],                // version needed
                [2, 0x0800],            // flag: UTF-8 filenames
                [2, 0],                 // method: stored
                [2, stamp.time], [2, stamp.date],
                [4, crc], [4, data.length], [4, data.length],
                [2, name.length], [2, 0]
            ]);
            out.push(name);
            out.push(data);

            central.push({ name: name, crc: crc, size: data.length, offset: offset });
        });

        const cdOffset = out.length;
        central.forEach(function (e) {
            out.header([
                [4, 0x02014b50],        // central directory signature
                [2, 20], [2, 20],
                [2, 0x0800], [2, 0],
                [2, stamp.time], [2, stamp.date],
                [4, e.crc], [4, e.size], [4, e.size],
                [2, e.name.length], [2, 0], [2, 0],
                [2, 0], [2, 0], [4, 0],
                [4, e.offset]
            ]);
            out.push(e.name);
        });
        const cdSize = out.length - cdOffset;

        out.header([
            [4, 0x06054b50],            // end of central directory
            [2, 0], [2, 0],
            [2, central.length], [2, central.length],
            [4, cdSize], [4, cdOffset], [2, 0]
        ]);

        return new Blob(out.chunks, { type: 'application/zip' });
    }

    return { build: build, crc32: crc32 };
})();
