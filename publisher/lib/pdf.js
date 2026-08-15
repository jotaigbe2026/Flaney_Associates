/* Minimal PDF writer for Flaney Associates article downloads.
 *
 * The publisher runs as a static page, so the gated PDF has to be built in the
 * browser. Only the three base-14 Helvetica faces are used, which means no font
 * embedding: a PDF viewer already has them. Layout mirrors generate_pdfs_v2.py
 * — Letter, navy headings, 11/17 justified body — so a PDF produced here sits
 * alongside the hand-written ones in articles/ without looking out of place.
 *
 *   FlaneyPDF.build({ title, categories, date, author, url, blocks })  -> Blob
 *
 * `blocks` is a flat list of { type, runs }, where type is one of
 * h2 | h3 | p | li | quote and each run is { text, bold, italic }.
 */
window.FlaneyPDF = (function () {
    'use strict';

    // ---------------------------------------------------------------- metrics

    /* Base-14 advance widths (1/1000 em) for WinAnsi 32..126. Anything outside
       that range falls back to FALLBACK below — accented characters are close
       enough to their ASCII counterparts that wrapping stays correct. */
    const W_REGULAR = ('278 278 355 556 556 889 667 191 333 333 389 584 278 333 278 278 ' +
        '556 556 556 556 556 556 556 556 556 556 278 278 584 584 584 556 ' +
        '1015 667 667 722 722 667 611 778 722 278 500 667 556 833 722 778 ' +
        '667 778 722 667 611 722 667 944 667 667 611 278 278 278 469 556 ' +
        '333 556 556 500 556 556 278 556 556 222 222 500 222 833 556 556 ' +
        '556 556 333 500 278 556 500 722 500 500 500 334 260 334 584').split(' ').map(Number);

    const W_BOLD = ('278 333 474 556 556 889 722 238 333 333 389 584 278 333 278 278 ' +
        '556 556 556 556 556 556 556 556 556 556 333 333 584 584 584 611 ' +
        '975 722 722 722 722 667 611 778 722 278 556 722 611 833 722 778 ' +
        '667 778 722 667 611 722 667 944 667 667 611 333 278 333 584 556 ' +
        '333 556 611 556 611 556 333 611 611 278 278 556 278 889 611 611 ' +
        '611 611 389 556 333 611 556 778 556 556 500 389 280 389 584').split(' ').map(Number);

    /* Punctuation the editor produces that has no ASCII width above. */
    const W_EXTRA_REGULAR = { 133: 1000, 145: 222, 146: 222, 147: 333, 148: 333, 149: 350, 150: 556, 151: 1000 };
    const W_EXTRA_BOLD = { 133: 1000, 145: 278, 146: 278, 147: 500, 148: 500, 149: 350, 150: 556, 151: 1000 };
    const FALLBACK_REGULAR = 556;
    const FALLBACK_BOLD = 611;

    /* Unicode the browser gives us -> WinAnsi byte. Curly quotes, dashes and
       bullets are common in pasted copy; everything unmapped degrades to a
       plain ASCII equivalent rather than a blank box. */
    const WINANSI = {
        '‘': 145, '’': 146, '“': 147, '”': 148,
        '–': 150, '—': 151, '•': 149, '…': 133,
        ' ': 32, '′': 39, '″': 34, '­': 45,
        '−': 45, '·': 183, '™': 153, '©': 169, '®': 174
    };
    const ASCII_FOLD = {
        'Ā': 'A', 'ā': 'a', '⁄': '/', 'ˆ': '^', '˜': '~'
    };

    function toWinAnsi(text) {
        const out = [];
        for (const ch of String(text)) {
            const code = ch.codePointAt(0);
            if (code < 128) { out.push(code); continue; }
            if (WINANSI[ch] !== undefined) { out.push(WINANSI[ch]); continue; }
            if (code <= 255) { out.push(code); continue; }
            const folded = ASCII_FOLD[ch] || '';
            for (let i = 0; i < folded.length; i++) out.push(folded.charCodeAt(i));
        }
        return out;
    }

    function widthOf(text, size, bold) {
        const widths = bold ? W_BOLD : W_REGULAR;
        const extra = bold ? W_EXTRA_BOLD : W_EXTRA_REGULAR;
        const fallback = bold ? FALLBACK_BOLD : FALLBACK_REGULAR;
        let total = 0;
        toWinAnsi(text).forEach(function (code) {
            if (code >= 32 && code <= 126) total += widths[code - 32];
            else if (extra[code] !== undefined) total += extra[code];
            else total += fallback;
        });
        return total * size / 1000;
    }

    /* PDF string literal: escape the three special bytes, and emit anything
       non-printable as a three-digit octal code. */
    function pdfString(text) {
        let out = '';
        toWinAnsi(text).forEach(function (code) {
            if (code === 0x28 || code === 0x29 || code === 0x5C) out += '\\' + String.fromCharCode(code);
            else if (code < 32 || code > 126) out += '\\' + code.toString(8).padStart(3, '0');
            else out += String.fromCharCode(code);
        });
        return '(' + out + ')';
    }

    // ------------------------------------------------------------- page setup

    const PAGE_W = 612, PAGE_H = 792;
    const MARGIN = 64;
    const CONTENT_W = PAGE_W - MARGIN * 2;
    const TOP = PAGE_H - 72;
    const BOTTOM = 92;

    const NAVY = '0.102 0.227 0.361';       // #1a3a5c
    const DARK = '0.059 0.153 0.251';       // #0f2740
    const BLUE = '0.176 0.549 0.941';       // #2d8cf0
    const BODY = '0.200 0.200 0.200';
    const MUTED = '0.400 0.400 0.400';
    const RULE = '0.886 0.906 0.929';       // #e2e8f0
    const TINT = '0.969 0.976 0.988';       // #f7f9fc

    const STYLE = {
        h2: { size: 15.5, leading: 21, before: 20, after: 8, bold: true, color: NAVY },
        h3: { size: 12.5, leading: 18, before: 15, after: 6, bold: true, color: DARK },
        p: { size: 11, leading: 17, before: 0, after: 10, bold: false, color: BODY, justify: true },
        li: { size: 11, leading: 17, before: 0, after: 6, bold: false, color: BODY, indent: 22 },
        quote: { size: 11, leading: 18, before: 12, after: 12, bold: false, color: NAVY, indent: 20, italic: true }
    };

    // -------------------------------------------------------- line breaking

    /* Split runs into words, then greedily fill lines. Words carry the space
       that follows them so justification can widen every gap with a single Tw.

       A word is a list of styled segments, not a single string, because a style
       can change mid-word: "<strong>…to ask</strong>." is one word ending in a
       bold run and a regular full stop. Treating each run as its own word would
       put a space in front of the period. Whether a run actually began after
       whitespace is what decides it, so that is tracked across run boundaries. */
    function layoutLines(runs, size, avail, forceBold, forceItalic) {
        const words = [];
        let open = false;       // the last word can still be extended

        runs.forEach(function (run) {
            const bold = forceBold || !!run.bold;
            const italic = forceItalic || !!run.italic;
            const text = String(run.text);
            const parts = text.split(/\s+/).filter(part => part !== '');

            if (!parts.length) {
                if (text.length) open = false;   // a run of pure whitespace
                return;
            }
            const startsMidWord = open && !/^\s/.test(text);
            parts.forEach(function (part, i) {
                const segment = { text: part, bold: bold, italic: italic };
                if (i === 0 && startsMidWord) words[words.length - 1].segments.push(segment);
                else words.push({ segments: [segment] });
            });
            open = !/\s$/.test(text);
        });

        words.forEach(function (word) {
            word.width = word.segments.reduce(
                (sum, s) => sum + widthOf(s.text, size, s.bold), 0);
            word.bold = word.segments[0].bold;
        });

        const lines = [];
        let line = [], lineWidth = 0;

        words.forEach(function (word) {
            const gap = line.length ? widthOf(' ', size, word.bold) : 0;
            if (line.length && lineWidth + gap + word.width > avail) {
                lines.push({ words: line, width: lineWidth });
                line = [word];
                lineWidth = word.width;
            } else {
                line.push(word);
                lineWidth += gap + word.width;
            }
        });
        if (line.length) lines.push({ words: line, width: lineWidth });
        return lines;
    }

    // -------------------------------------------------------------- document

    function Doc() {
        this.pages = [];
        this.ops = null;
        this.y = 0;
        this.newPage();
    }

    Doc.prototype.newPage = function () {
        this.ops = [];
        this.pages.push(this.ops);
        this.y = TOP;
    };

    Doc.prototype.space = function (needed) {
        if (this.y - needed < BOTTOM) {
            this.newPage();
            return true;
        }
        return false;
    };

    Doc.prototype.rect = function (x, y, w, h, color) {
        this.ops.push(color + ' rg', [x, y, w, h].join(' ') + ' re f');
    };

    Doc.prototype.rule = function (x, y, w, color, thickness) {
        this.ops.push((color || RULE) + ' RG', (thickness || 0.75) + ' w',
            x + ' ' + y + ' m ' + (x + w) + ' ' + y + ' l S');
    };

    /* A small filled diamond — the site's ◆ logo mark. Helvetica has no glyph
       for it, so it is drawn as a path. */
    Doc.prototype.diamond = function (cx, cy, r, color) {
        this.ops.push(color + ' rg',
            (cx) + ' ' + (cy + r) + ' m ' +
            (cx + r) + ' ' + cy + ' l ' +
            (cx) + ' ' + (cy - r) + ' l ' +
            (cx - r) + ' ' + cy + ' l h f');
    };

    Doc.prototype.textLine = function (x, y, line, size, color, wordSpacing) {
        const ops = this.ops;
        ops.push('BT', color + ' rg', '1 0 0 1 ' + x + ' ' + y + ' Tm');
        ops.push((wordSpacing || 0).toFixed(3) + ' Tw');
        let current = null;
        line.words.forEach(function (word, i) {
            const lastWord = i === line.words.length - 1;
            word.segments.forEach(function (segment, j) {
                const font = segment.bold ? '/F2' : (segment.italic ? '/F3' : '/F1');
                if (font !== current) {
                    ops.push(font + ' ' + size + ' Tf');
                    current = font;
                }
                const trailing = (!lastWord && j === word.segments.length - 1) ? ' ' : '';
                ops.push(pdfString(segment.text + trailing) + ' Tj');
            });
        });
        ops.push('0 Tw', 'ET');
    };

    /* Centre a single-style string — used by the letterhead and footers. */
    Doc.prototype.centred = function (text, y, size, bold, color) {
        const width = widthOf(text, size, bold);
        this.ops.push('BT', color + ' rg', (bold ? '/F2 ' : '/F1 ') + size + ' Tf',
            '1 0 0 1 ' + ((PAGE_W - width) / 2).toFixed(2) + ' ' + y + ' Tm',
            pdfString(text) + ' Tj', 'ET');
    };

    Doc.prototype.plain = function (text, x, y, size, bold, color) {
        this.ops.push('BT', color + ' rg', (bold ? '/F2 ' : '/F1 ') + size + ' Tf',
            '1 0 0 1 ' + x + ' ' + y + ' Tm', pdfString(text) + ' Tj', 'ET');
    };

    Doc.prototype.block = function (type, runs) {
        const style = STYLE[type] || STYLE.p;
        const indent = style.indent || 0;
        const avail = CONTENT_W - indent;
        const lines = layoutLines(runs, style.size, avail, style.bold, style.italic);
        if (!lines.length) return;

        this.y -= style.before;

        lines.forEach(function (line, i) {
            // Keep a heading with at least one line of what follows it.
            this.space(style.leading * (style.bold && i === 0 ? 2 : 1));
            this.y -= style.leading;

            const last = i === lines.length - 1;
            const gaps = line.words.length - 1;
            let wordSpacing = 0;
            if (style.justify && !last && gaps > 0) {
                wordSpacing = (avail - line.width) / gaps;
                if (wordSpacing > style.size * 0.6) wordSpacing = 0;   // avoid rivers
            }

            if (type === 'li' && i === 0) {
                this.plain('•', MARGIN + 6, this.y, style.size, false, BLUE);
            }
            this.textLine(MARGIN + indent, this.y, line, style.size, style.color, wordSpacing);
        }, this);

        if (type === 'quote') {
            // Left accent bar spanning the quote, drawn after its height is known.
            const height = lines.length * STYLE.quote.leading;
            this.ops.push(BLUE + ' RG', '2 w',
                (MARGIN + 4) + ' ' + (this.y - 3) + ' m ' + (MARGIN + 4) + ' ' + (this.y + height - 4) + ' l S');
        }

        this.y -= style.after;
    };

    // ------------------------------------------------------------- letterhead

    function letterhead(doc, meta) {
        doc.rect(0, PAGE_H - 46, PAGE_W, 46, TINT);
        doc.diamond(MARGIN, PAGE_H - 26, 4.5, NAVY);
        doc.plain('FLANEY ASSOCIATES', MARGIN + 12, PAGE_H - 29, 10.5, true, NAVY);
        doc.plain('Materials Engineering & Innovation', PAGE_W - MARGIN - widthOf('Materials Engineering & Innovation', 9, false), PAGE_H - 28.5, 9, false, MUTED);
        doc.rule(0, PAGE_H - 46, PAGE_W, BLUE, 2);

        doc.y = PAGE_H - 92;

        if (meta.categories && meta.categories.length) {
            doc.plain(meta.categories.join('  ·  ').toUpperCase(), MARGIN, doc.y, 9, true, BLUE);
            doc.y -= 20;
        }

        const titleLines = layoutLines([{ text: meta.title }], 21, CONTENT_W, true, false);
        titleLines.forEach(function (line) {
            doc.y -= 27;
            doc.textLine(MARGIN, doc.y, line, 21, NAVY, 0);
        });

        doc.y -= 20;
        const byline = [meta.author, meta.date].filter(Boolean).join('  ·  ');
        doc.plain(byline, MARGIN, doc.y, 10, false, MUTED);
        doc.y -= 14;
        doc.rule(MARGIN, doc.y, CONTENT_W, RULE, 1);
        doc.y -= 16;
    }

    function contactBlock(doc) {
        const height = 92;
        if (doc.y - height - 20 < BOTTOM) doc.newPage();
        doc.y -= 24;

        const top = doc.y;
        doc.rect(MARGIN, top - height, CONTENT_W, height, TINT);
        doc.ops.push(BLUE + ' RG', '3 w',
            (MARGIN + 1.5) + ' ' + (top - height) + ' m ' + (MARGIN + 1.5) + ' ' + top + ' l S');

        doc.plain('Talk to us about your materials challenge', MARGIN + 20, top - 26, 12, true, NAVY);
        doc.plain('Joshua U. Otaigbe, PhD  ·  Materials Engineering Consultant', MARGIN + 20, top - 44, 10, false, BODY);
        doc.plain('info@flaneyassociates.com  ·  +1 (601) 402-7282', MARGIN + 20, top - 60, 10, false, BODY);
        doc.plain('flaneyassociates.com', MARGIN + 20, top - 76, 10, false, BLUE);
        doc.y = top - height;
    }

    function footers(doc, meta) {
        doc.pages.forEach(function (ops, i) {
            const saved = doc.ops;
            doc.ops = ops;
            doc.rule(MARGIN, 62, CONTENT_W, RULE, 0.75);
            doc.plain('© ' + new Date(meta.dateISO || Date.now()).getFullYear() +
                ' Flaney Associates', MARGIN, 48, 8.5, false, MUTED);
            const label = 'Page ' + (i + 1) + ' of ' + doc.pages.length;
            doc.plain(label, PAGE_W - MARGIN - widthOf(label, 8.5, false), 48, 8.5, false, MUTED);
            doc.ops = saved;
        });
    }

    // ------------------------------------------------------------ serialising

    function serialise(doc) {
        const objects = [];
        const push = body => objects.push(body);

        const pageCount = doc.pages.length;
        const firstPageObj = 6;
        const kids = [];
        for (let i = 0; i < pageCount; i++) kids.push((firstPageObj + i * 2) + ' 0 R');

        push('<< /Type /Catalog /Pages 2 0 R >>');
        push('<< /Type /Pages /Kids [' + kids.join(' ') + '] /Count ' + pageCount + ' >>');
        push('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>');
        push('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>');
        push('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>');

        doc.pages.forEach(function (ops, i) {
            const contentObj = firstPageObj + i * 2 + 1;
            push('<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ' + PAGE_W + ' ' + PAGE_H + '] ' +
                '/Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R >> >> ' +
                '/Contents ' + contentObj + ' 0 R >>');
            // Ops are pure ASCII (pdfString octal-escapes everything else), so
            // character length is byte length — which is what /Length must be.
            const stream = ops.join('\n');
            push('<< /Length ' + stream.length + ' >>\nstream\n' + stream + '\nendstream');
        });

        let pdf = '%PDF-1.4\n%âãÏÓ\n';
        const offsets = [];
        objects.forEach(function (body, i) {
            offsets.push(pdf.length);
            pdf += (i + 1) + ' 0 obj\n' + body + '\nendobj\n';
        });

        const xref = pdf.length;
        pdf += 'xref\n0 ' + (objects.length + 1) + '\n0000000000 65535 f \n';
        offsets.forEach(function (off) {
            pdf += String(off).padStart(10, '0') + ' 00000 n \n';
        });
        pdf += 'trailer\n<< /Size ' + (objects.length + 1) + ' /Root 1 0 R >>\nstartxref\n' + xref + '\n%%EOF';

        // Latin-1 rather than UTF-8: byte offsets in the xref table must match.
        const bytes = new Uint8Array(pdf.length);
        for (let i = 0; i < pdf.length; i++) bytes[i] = pdf.charCodeAt(i) & 0xFF;
        return new Blob([bytes], { type: 'application/pdf' });
    }

    function build(meta) {
        const doc = new Doc();
        letterhead(doc, meta);
        (meta.blocks || []).forEach(function (block) {
            doc.block(block.type, block.runs);
        });
        contactBlock(doc);
        footers(doc, meta);
        return serialise(doc);
    }

    return { build: build, widthOf: widthOf };
})();
