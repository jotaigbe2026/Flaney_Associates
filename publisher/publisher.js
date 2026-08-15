/* Flaney Publisher — compose the monthly post, preview it, and download a
 * bundle of files that drop straight into the repository.
 *
 * The site is static and served from GitHub Pages, so nothing here can write to
 * the repo. Instead every file that a publish touches is rebuilt in the browser
 * and handed back: the new article page, the regenerated archive, the homepage
 * strip, the updated posts.json, the image and the gated PDF. Committing that
 * set is equivalent to running generate_blog.py — which stays the source of
 * truth, and can still be re-run at any time to rebuild everything.
 *
 * Requires a local server (fetch is blocked on file://):
 *     python3 -m http.server 8000  ->  http://localhost:8000/publisher/
 */
(function () {
    'use strict';

    const T = window.FlaneyTemplate;
    const TEMPLATE_KEY = 'flaney_publisher_template';

    const state = {
        posts: [],
        assets: { css: '', js: '' },
        defaults: {},         // publisher/template.json, the committed baseline
        homepageHTML: '',
        categories: [],
        selected: new Set(),
        image: null,          // { name, ext, bytes, url, type }
        pdfUpload: null,      // { name, bytes }
        bundle: null,
        ready: false
    };

    const $ = id => document.getElementById(id);
    const el = {};
    ['titlePattern', 'defaultAuthor', 'publishDay', 'standingByline', 'saveTemplate',
        'exportTemplate', 'templateStatus', 'title', 'titleError', 'slug', 'slugError', 'slugPreview',
        'categoryChips', 'categoryError', 'pubDate', 'dateHelp', 'author', 'scheduleNotice',
        'body', 'bodyError', 'bodyStats', 'bodyHint', 'summary', 'imageDrop', 'imageInput',
        'imageThumb', 'imagePreview', 'imageName', 'imageSize', 'imageRemove', 'imageAlt',
        'pdfUploadWrap', 'pdfDrop', 'pdfInput', 'pdfTargetName', 'pdfUploadInfo',
        'generate', 'generateFeedback', 'queueList', 'queueHint', 'previewFrame', 'cardFrame',
        'shareUrl', 'shareText', 'fileList', 'bundleActions', 'downloadZip', 'commitBlock',
        'commitCommands', 'toast', 'startNextMonth', 'resetForm'
    ].forEach(id => { el[id] = $(id); });

    // ------------------------------------------------------------------ utils

    function toast(message) {
        el.toast.textContent = message;
        el.toast.classList.add('on');
        clearTimeout(toast.timer);
        toast.timer = setTimeout(() => el.toast.classList.remove('on'), 2600);
    }

    function notice(target, kind, html) {
        target.className = 'notice notice-' + kind;
        target.innerHTML = '<span>' + html + '</span>';
        target.hidden = false;
    }

    function humanSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }

    function todayISO() {
        const d = new Date();
        return [d.getFullYear(),
            String(d.getMonth() + 1).padStart(2, '0'),
            String(d.getDate()).padStart(2, '0')].join('-');
    }

    function readFile(file) {
        return file.arrayBuffer().then(buf => new Uint8Array(buf));
    }

    function download(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(url), 4000);
    }

    // ------------------------------------------------------------ monthly template

    /* Two layers: publisher/template.json is the committed baseline, and
       localStorage is a per-device override on top of it. Keeping the baseline
       in the repo means the template survives a cleared cache and is the same
       on every machine — a monthly template that only exists in one browser
       profile is not much of a template. */
    function currentTemplate() {
        let saved = {};
        try { saved = JSON.parse(localStorage.getItem(TEMPLATE_KEY) || '{}'); } catch (e) {}
        return { merged: Object.assign({}, state.defaults, saved), overridden: !!Object.keys(saved).length };
    }

    function loadTemplate() {
        const { merged, overridden } = currentTemplate();
        el.titlePattern.value = merged.titlePattern || '';
        el.defaultAuthor.value = merged.author || '';
        el.publishDay.value = merged.publishDay || 15;
        // `closing` is the old key for this field, kept so a per-device override
        // saved before the rename still loads.
        el.standingByline.value = merged.byline || merged.closing || '';
        el.templateStatus.textContent = overridden
            ? 'Edited on this device' : 'From template.json';
        return merged;
    }

    function templateFromForm() {
        return {
            titlePattern: el.titlePattern.value.trim(),
            author: el.defaultAuthor.value.trim(),
            publishDay: Math.min(28, Math.max(1, parseInt(el.publishDay.value, 10) || 15)),
            categories: Array.from(state.selected),
            byline: el.standingByline.value.trim()
        };
    }

    function saveTemplate() {
        try {
            localStorage.setItem(TEMPLATE_KEY, JSON.stringify(templateFromForm()));
            el.templateStatus.textContent = 'Edited on this device';
            toast('Saved for this browser');
        } catch (e) {
            toast('Could not save — browser storage is blocked');
        }
    }

    /* Write the template back out so the change can be committed and picked up
       by every other machine, rather than living in one browser forever. */
    function exportTemplate() {
        const data = Object.assign(
            { _comment: state.defaults._comment || '' }, templateFromForm());
        download(new Blob([JSON.stringify(data, null, 2) + '\n'],
            { type: 'application/json' }), 'template.json');
        toast('Replace publisher/template.json with this, then commit');
    }

    const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December'];

    /* The first slot on or after today that no post already occupies. Lets you
       queue several months in one sitting without picking dates by hand. */
    function nextOpenSlot(day) {
        const taken = new Set(state.posts.map(p => String(p.date).slice(0, 7)));
        const now = new Date();
        let year = now.getFullYear(), month = now.getMonth();
        if (now.getDate() >= day) month += 1;
        for (let i = 0; i < 36; i++) {
            const y = year + Math.floor(month / 12);
            const m = ((month % 12) + 12) % 12;
            const key = y + '-' + String(m + 1).padStart(2, '0');
            if (!taken.has(key)) {
                return { year: y, month: m, iso: key + '-' + String(day).padStart(2, '0') };
            }
            month += 1;
        }
        return { year: year, month: month % 12, iso: todayISO() };
    }

    function startNextMonth() {
        const template = loadTemplate();
        const day = Math.min(28, Math.max(1, parseInt(el.publishDay.value, 10) || 15));
        const slot = nextOpenSlot(day);
        const seriesCount = state.posts.filter(p => p.local).length + 1;
        const pattern = el.titlePattern.value.trim();

        el.pubDate.value = slot.iso;
        el.author.value = el.defaultAuthor.value.trim();

        // An empty pattern is the deliberate setting, not a missing one: it
        // means "write a real headline this month". Everything else is filled
        // in, and the cursor lands on the one field only you can write.
        if (pattern) {
            el.title.value = pattern
                .replace(/\{month\}/g, MONTHS[slot.month])
                .replace(/\{month_short\}/g, MONTHS[slot.month].slice(0, 3))
                .replace(/\{year\}/g, slot.year)
                .replace(/\{n\}/g, seriesCount);
            el.slug.value = T.slugify(el.title.value);
        } else {
            el.title.value = '';
            el.slug.value = '';
        }

        state.selected.clear();
        (template.categories || []).forEach(c => state.selected.add(c));
        renderCategories();

        (pattern ? el.body : el.title).focus();
        toast('Ready for ' + MONTHS[slot.month] + ' ' + slot.year);
        render();
    }

    // -------------------------------------------------------------- categories

    function renderCategories() {
        el.categoryChips.innerHTML = '';
        state.categories.forEach(function (name) {
            const chip = document.createElement('button');
            chip.type = 'button';
            chip.className = 'chip' + (state.selected.has(name) ? ' on' : '');
            chip.textContent = name;
            chip.addEventListener('click', function () {
                if (state.selected.has(name)) state.selected.delete(name);
                else state.selected.add(name);
                renderCategories();
                render();
            });
            el.categoryChips.appendChild(chip);
        });

        const add = document.createElement('button');
        add.type = 'button';
        add.className = 'chip chip-add';
        add.textContent = '+ New category';
        add.addEventListener('click', function () {
            const name = (prompt('Category name') || '').trim();
            if (!name) return;
            if (state.categories.indexOf(name) === -1) {
                state.categories.push(name);
                state.categories.sort();
            }
            state.selected.add(name);
            renderCategories();
            render();
        });
        el.categoryChips.appendChild(add);
    }

    // ----------------------------------------------------------- post assembly

    function currentPost() {
        const title = el.title.value.trim();
        const slug = (el.slug.value.trim() || T.slugify(title));
        const date = el.pubDate.value || todayISO();
        const byline = el.standingByline.value.trim();

        let content = T.parseBody(el.body.value);
        if (byline && content) {
            // <em> rather than a class: clean() in generate_blog.py strips class
            // attributes, so styling that way would vanish on the first
            // regeneration. An inline tag survives, and toBlocks() carries the
            // italics through to the PDF as well.
            content += '\n<p><em>' + T.esc(byline) + '</em></p>';
        }

        const cats = Array.from(state.selected);
        const words = T.countWords(content);
        const summary = el.summary.value.trim() || T.summarise(content, title);
        const wantsPdf = document.querySelector('input[name=pdfSource]:checked').value !== 'none';

        return {
            id: state.posts.reduce((max, p) => Math.max(max, p.id || 0), 16000) + 1,
            slug: slug,
            date: date + 'T09:00:00',
            modified: date + 'T09:00:00',
            link: T.SITE + '/blog/' + slug + '.html',
            title: title,
            excerpt: summary,
            content: content,
            gated: false,
            words: words,
            categories: cats,
            author: el.author.value.trim() || 'Joshua Otaigbe',
            image: state.image ? T.SITE + '/blog/images/' + slug + state.image.ext : '',
            image_alt: el.imageAlt.value.trim(),
            local_image: state.image ? slug + state.image.ext : '',
            pdf: wantsPdf ? 'articles/' + slug + '.pdf' : '',
            summary: summary,
            local: true
        };
    }

    // ---------------------------------------------------------------- preview

    /* An iframe written with srcdoc resolves relative URLs against this page,
       so blog-relative paths land in publisher/ and 404. Repoint them, then
       swap the post's own image for the blob it only exists as until the
       bundle is unpacked. */
    function fixPreviewPaths(html, post) {
        html = html.split('src="images/').join('src="../blog/images/');
        if (state.image) {
            html = html.split('../blog/images/' + post.local_image).join(state.image.url);
        }
        return html;
    }

    function previewArticle(post) {
        const related = T.pickRelated(post, state.posts, 3);
        let html = fixPreviewPaths(T.article(post, related, state.assets), post);
        // blog.js sits one directory over and would 404 too; it has nothing to
        // do in a preview anyway.
        html = html.replace(/<script src="blog\.js[^"]*"><\/script>/, '');
        el.previewFrame.srcdoc = html;
    }

    function previewCard(post) {
        const card = fixPreviewPaths(T.card(post), post);
        el.cardFrame.srcdoc = `<!DOCTYPE html><html><head>
<link rel="stylesheet" href="../styles.css">
<link rel="stylesheet" href="../blog/blog.css${state.assets.css}">
<style>body{background:transparent;padding:2px}.post-grid{display:block}</style>
</head><body><div class="post-grid">${card}</div></body></html>`;
    }

    const HASHTAGS = {
        'Advanced Materials Engineering': '#MaterialsEngineering',
        'Materials Engineering Innovations': '#MaterialsInnovation',
        'Glasses and Optical Devices': '#Photonics',
        'Sustainable Materials': '#SustainableMaterials',
        'Polymers': '#Polymers',
        'Composites': '#Composites',
        'Nanotechnology': '#Nanotechnology'
    };

    function previewShare(post) {
        const url = T.SITE + '/blog/' + post.slug + '.html';
        el.shareUrl.textContent = url;

        const tags = post.categories
            .map(c => HASHTAGS[c] || '#' + c.replace(/[^A-Za-z0-9]/g, ''))
            .filter((t, i, a) => t.length > 2 && a.indexOf(t) === i)
            .slice(0, 4);

        const parts = [];
        parts.push(post.title || 'Your headline goes here');
        parts.push('');
        parts.push(post.summary || 'A one-paragraph hook — this is what stops the scroll.');
        parts.push('');
        if (post.pdf) {
            parts.push('The full article is on our site, and you can download it as a PDF at the bottom of the page.');
        } else {
            parts.push('The full article is on our site:');
        }
        parts.push('');
        parts.push(url);
        parts.push('');
        parts.push(tags.concat(['#FlaneyAssociates']).join(' '));

        el.shareText.textContent = parts.join('\n');
    }

    function renderStats(post) {
        const scheduled = T.parseDate(post.date) > new Date(todayISO() + 'T23:59:59');
        el.bodyStats.innerHTML =
            `<span class="stat-pill"><strong>${post.words}</strong> words</span>` +
            `<span class="stat-pill"><strong>${T.readTime(post.words)}</strong> min read</span>` +
            `<span class="stat-pill"><strong>${(post.content.match(/<h[234]/g) || []).length}</strong> headings</span>` +
            `<span class="stat-pill"><strong>${(post.content.match(/<li>/g) || []).length}</strong> list items</span>`;
        el.bodyHint.textContent = post.words ? T.readTime(post.words) + ' min read' : 'Paste and go';

        if (!el.pubDate.value) {
            el.scheduleNotice.hidden = true;
        } else if (scheduled) {
            notice(el.scheduleNotice, 'info',
                'Scheduled for <strong>' + T.fmtDate(post.date) + '</strong>. Commit the bundle whenever you like — ' +
                'the card stays hidden on the archive and homepage until that morning, then appears on its own. ' +
                'The page itself is reachable at its URL straight away, so you can check it before it goes public.');
        } else {
            notice(el.scheduleNotice, 'ok',
                'Goes live as soon as you commit and push. Dated <strong>' + T.fmtDate(post.date) + '</strong>.');
        }
    }

    let renderTimer;
    function render() {
        if (!state.ready) return;
        clearTimeout(renderTimer);
        renderTimer = setTimeout(function () {
            const post = currentPost();
            renderStats(post);
            previewArticle(post);
            previewCard(post);
            previewShare(post);
            el.slugPreview.innerHTML = 'Page URL: ' + T.SITE + '/blog/<strong>' +
                T.esc(post.slug || '…') + '</strong>.html';
            el.pdfTargetName.textContent = 'articles/' + (post.slug || '<slug>') + '.pdf';
        }, 250);
    }

    // ------------------------------------------------------------- validation

    function validate(post) {
        const problems = [];
        const flag = (input, errorEl, message) => {
            if (message) {
                input.classList.add('invalid');
                errorEl.textContent = message;
                errorEl.hidden = false;
                problems.push(message);
            } else {
                input.classList.remove('invalid');
                errorEl.hidden = true;
            }
        };

        flag(el.title, el.titleError, post.title ? '' : 'Give the article a title.');

        let slugProblem = '';
        if (!post.slug) slugProblem = 'A URL slug is required.';
        else if (!/^[a-z0-9-]+$/.test(post.slug)) slugProblem = 'Use lower-case letters, numbers and hyphens only.';
        else if (state.posts.some(p => p.slug === post.slug)) slugProblem = 'That slug is already used by another post — change it.';
        flag(el.slug, el.slugError, slugProblem);

        flag(el.pubDate, el.categoryError, '');
        if (!post.categories.length) {
            el.categoryError.textContent = 'Choose at least one category.';
            el.categoryError.hidden = false;
            problems.push('category');
        } else {
            el.categoryError.hidden = true;
        }

        flag(el.body, el.bodyError,
            post.words >= 50 ? '' : 'Paste the article — at least a few paragraphs.');

        if (document.querySelector('input[name=pdfSource]:checked').value === 'upload' && !state.pdfUpload) {
            problems.push('Attach the PDF, or switch to generating one.');
            notice(el.pdfUploadInfo, 'err', 'Attach a PDF, or switch back to generating one.');
        }

        return problems;
    }

    // ------------------------------------------------------------ bundle build

    function buildBundle() {
        const post = currentPost();
        const problems = validate(post);
        if (problems.length) {
            notice(el.generateFeedback, 'err',
                'Not ready yet: ' + problems[0] + (problems.length > 1 ? ' (and ' + (problems.length - 1) + ' more above)' : ''));
            return null;
        }

        const files = [];

        // 1. the article page
        const related = T.pickRelated(post, state.posts, 3);
        files.push({
            name: 'blog/' + post.slug + '.html',
            data: T.article(post, related, state.assets),
            status: 'new'
        });

        // 2. the featured image
        if (state.image) {
            files.push({
                name: 'blog/images/' + post.local_image,
                data: state.image.bytes,
                status: 'new'
            });
        }

        // 3. the gated PDF
        const mode = document.querySelector('input[name=pdfSource]:checked').value;
        let pdfPromise = Promise.resolve(null);
        if (mode === 'upload' && state.pdfUpload) {
            pdfPromise = Promise.resolve(state.pdfUpload.bytes);
        } else if (mode === 'auto') {
            const blob = window.FlaneyPDF.build({
                title: post.title,
                categories: post.categories,
                date: T.fmtDate(post.date),
                dateISO: post.date,
                author: post.author,
                blocks: T.toBlocks(post.content)
            });
            pdfPromise = blob.arrayBuffer().then(b => new Uint8Array(b));
        }

        return pdfPromise.then(function (pdfBytes) {
            if (pdfBytes) {
                files.push({ name: post.pdf, data: pdfBytes, status: 'new' });
            }

            // 4. posts.json, with the new entry slotted in by date
            const merged = state.posts.concat([post])
                .sort((a, b) => String(b.date).localeCompare(String(a.date)));
            files.push({
                name: 'blog/data/posts.json',
                data: JSON.stringify(merged, null, 1),
                status: 'replace'
            });

            // 5. the regenerated archive
            files.push({
                name: 'blog/index.html',
                data: T.archive(merged, state.assets),
                status: 'replace'
            });

            // 6. the homepage "latest posts" strip
            if (state.homepageHTML) {
                const updated = T.homepage(state.homepageHTML, merged, 6);
                if (updated) {
                    files.push({ name: 'index.html', data: updated, status: 'replace' });
                }
            }

            return { post: post, files: files };
        });
    }

    function renderBundle(bundle) {
        state.bundle = bundle;

        el.fileList.innerHTML = '';
        bundle.files.forEach(function (file) {
            const bytes = typeof file.data === 'string'
                ? new TextEncoder().encode(file.data).length : file.data.length;
            const li = document.createElement('li');
            li.innerHTML = `<span class="tag ${file.status === 'replace' ? 'replace' : ''}">${file.status}</span>` +
                `<span class="path">${T.esc(file.name)}</span>` +
                `<span class="size">${humanSize(bytes)}</span>`;
            const btn = document.createElement('button');
            btn.className = 'btn btn-outline btn-sm';
            btn.type = 'button';
            btn.textContent = 'Save';
            btn.addEventListener('click', function () {
                const blob = typeof file.data === 'string'
                    ? new Blob([file.data], { type: 'text/plain;charset=utf-8' })
                    : new Blob([file.data]);
                download(blob, file.name.split('/').pop());
            });
            li.appendChild(btn);
            el.fileList.appendChild(li);
        });

        el.bundleActions.hidden = false;
        el.commitBlock.hidden = false;
        el.commitCommands.innerHTML =
            '<span class="c"># unzip the bundle over the repository root, then</span>\n' +
            'git add -A\n' +
            'git commit -m ' + JSON.stringify('Publish: ' + bundle.post.title) + '\n' +
            'git push origin main';

        document.querySelector('.tab[data-view=files]').click();
    }

    // ------------------------------------------------------------------ wiring

    function wire() {
        ['title', 'slug', 'pubDate', 'author', 'body', 'summary', 'imageAlt', 'standingByline']
            .forEach(id => el[id].addEventListener('input', render));

        // Keep the slug following the title until the slug is edited by hand.
        let slugTouched = false;
        el.slug.addEventListener('input', () => { slugTouched = true; });
        el.title.addEventListener('input', function () {
            if (!slugTouched) el.slug.value = T.slugify(el.title.value);
        });

        el.saveTemplate.addEventListener('click', saveTemplate);
        el.exportTemplate.addEventListener('click', exportTemplate);
        el.startNextMonth.addEventListener('click', function () {
            slugTouched = false;
            startNextMonth();
        });

        el.resetForm.addEventListener('click', function () {
            if (!confirm('Clear the form? The saved monthly template is kept.')) return;
            ['title', 'slug', 'body', 'summary', 'imageAlt'].forEach(id => { el[id].value = ''; });
            state.selected.clear();
            (currentTemplate().merged.categories || []).forEach(c => state.selected.add(c));
            clearImage();
            state.pdfUpload = null;
            state.bundle = null;
            slugTouched = false;
            el.pdfUploadInfo.hidden = true;
            el.generateFeedback.innerHTML = '';
            el.fileList.innerHTML = '<li><span class="path">Nothing generated yet</span></li>';
            el.bundleActions.hidden = true;
            el.commitBlock.hidden = true;
            renderCategories();
            render();
        });

        // --- tabs
        document.querySelectorAll('.tab').forEach(function (tab) {
            tab.addEventListener('click', function () {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('on'));
                tab.classList.add('on');
                document.querySelectorAll('.viewport').forEach(function (v) {
                    v.classList.toggle('on', v.dataset.view === tab.dataset.view);
                });
            });
        });

        // --- copy buttons
        document.querySelectorAll('[data-copy]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                const text = $(btn.dataset.copy).textContent;
                navigator.clipboard.writeText(text)
                    .then(() => toast('Copied to clipboard'))
                    .catch(() => toast('Copy failed — select the text instead'));
            });
        });

        // --- image
        el.imageInput.addEventListener('change', e => acceptImage(e.target.files[0]));
        el.imageRemove.addEventListener('click', function (e) {
            e.preventDefault();
            clearImage();
            render();
        });
        dropTarget(el.imageDrop, acceptImage);

        // --- pdf
        document.querySelectorAll('input[name=pdfSource]').forEach(function (radio) {
            radio.addEventListener('change', function () {
                document.querySelectorAll('.choice-option').forEach(function (opt) {
                    opt.classList.toggle('on', opt.querySelector('input').checked);
                });
                el.pdfUploadWrap.hidden = radio.value !== 'upload';
                render();
            });
        });
        el.pdfInput.addEventListener('change', e => acceptPdf(e.target.files[0]));
        dropTarget(el.pdfDrop, acceptPdf);

        // --- generate
        el.generate.addEventListener('click', function () {
            el.generateFeedback.innerHTML = '';
            el.generate.disabled = true;
            el.generate.textContent = 'Building…';

            Promise.resolve()
                .then(buildBundle)
                .then(function (bundle) {
                    if (bundle) {
                        renderBundle(bundle);
                        notice(el.generateFeedback, 'ok',
                            'Bundle ready — <strong>' + bundle.files.length + ' files</strong>. ' +
                            'Open the <strong>Files</strong> tab to download them.');
                        toast('Bundle ready');
                    }
                })
                .catch(function (err) {
                    notice(el.generateFeedback, 'err', 'Something went wrong: ' + T.esc(err.message));
                    console.error(err);
                })
                .finally(function () {
                    el.generate.disabled = false;
                    el.generate.textContent = 'Generate the publish bundle';
                });
        });

        el.downloadZip.addEventListener('click', function () {
            if (!state.bundle) return;
            const blob = window.FlaneyZip.build(state.bundle.files.map(f => ({ name: f.name, data: f.data })));
            download(blob, 'flaney-' + state.bundle.post.slug + '.zip');
            toast('Downloaded — unzip over the repository root');
        });
    }

    function dropTarget(node, accept) {
        ['dragenter', 'dragover'].forEach(type => node.addEventListener(type, function (e) {
            e.preventDefault();
            node.classList.add('over');
        }));
        ['dragleave', 'drop'].forEach(type => node.addEventListener(type, function (e) {
            e.preventDefault();
            node.classList.remove('over');
        }));
        node.addEventListener('drop', function (e) {
            if (e.dataTransfer.files.length) accept(e.dataTransfer.files[0]);
        });
    }

    const IMAGE_EXT = { 'image/jpeg': '.jpg', 'image/png': '.png', 'image/webp': '.webp', 'image/gif': '.gif' };

    function acceptImage(file) {
        if (!file) return;
        if (!IMAGE_EXT[file.type]) { toast('Use a JPG, PNG, WebP or GIF'); return; }
        readFile(file).then(function (bytes) {
            if (state.image) URL.revokeObjectURL(state.image.url);
            state.image = {
                name: file.name,
                ext: IMAGE_EXT[file.type],
                type: file.type,
                bytes: bytes,
                url: URL.createObjectURL(new Blob([bytes], { type: file.type }))
            };
            el.imagePreview.src = state.image.url;
            el.imageName.textContent = file.name;
            el.imageSize.textContent = humanSize(bytes.length);
            el.imageThumb.classList.add('on');
            if (!el.imageAlt.value.trim()) el.imageAlt.value = el.title.value.trim();
            render();
        });
    }

    function clearImage() {
        if (state.image) URL.revokeObjectURL(state.image.url);
        state.image = null;
        el.imageInput.value = '';
        el.imagePreview.removeAttribute('src');
        el.imageThumb.classList.remove('on');
    }

    function acceptPdf(file) {
        if (!file) return;
        if (file.type !== 'application/pdf') { toast('That is not a PDF'); return; }
        readFile(file).then(function (bytes) {
            state.pdfUpload = { name: file.name, bytes: bytes };
            notice(el.pdfUploadInfo, 'ok',
                'Using <strong>' + T.esc(file.name) + '</strong> (' + humanSize(bytes.length) + ').');
            render();
        });
    }

    // -------------------------------------------------------------- the queue

    function renderQueue() {
        const today = todayISO();
        const upcoming = state.posts
            .filter(p => String(p.date).slice(0, 10) > today)
            .sort((a, b) => String(a.date).localeCompare(String(b.date)));

        el.queueList.innerHTML = '';
        if (!upcoming.length) {
            el.queueList.innerHTML = '<li><span class="empty">Nothing scheduled — the next post you date in the future will show up here.</span></li>';
            el.queueHint.textContent = '';
            return;
        }
        el.queueHint.textContent = upcoming.length + ' waiting';
        upcoming.forEach(function (p) {
            const li = document.createElement('li');
            li.innerHTML = `<span class="when">${T.fmtDate(p.date)}</span>` +
                `<span class="what">${T.esc(T.stripTags(p.title))}</span>`;
            el.queueList.appendChild(li);
        });
    }

    // ------------------------------------------------------------------- boot

    /* Reuse whatever ?v= the deployed archive is already using. Recomputing a
       hash here would disagree with generate_blog.py's md5 and churn the URLs
       on every publish. */
    function readAssetVersions(html) {
        const css = html.match(/blog\.css(\?v=[a-z0-9]+)?/);
        const js = html.match(/blog\.js(\?v=[a-z0-9]+)?/);
        return { css: (css && css[1]) || '', js: (js && js[1]) || '' };
    }

    function boot() {
        Promise.all([
            fetch('../blog/data/posts.json').then(r => r.json()),
            fetch('../blog/index.html').then(r => r.text()),
            fetch('../index.html').then(r => r.text()),
            // Optional: the dashboard still works on localStorage alone.
            fetch('template.json').then(r => r.ok ? r.json() : {}).catch(() => ({}))
        ]).then(function (results) {
            state.posts = results[0];
            state.assets = readAssetVersions(results[1]);
            state.homepageHTML = results[2];
            state.defaults = results[3] || {};

            state.categories = Array.from(new Set(
                state.posts.flatMap(p => p.categories || [])
                    .concat(state.defaults.categories || [])
            )).sort();

            const template = loadTemplate();
            (template.categories || []).forEach(c => state.selected.add(c));
            renderCategories();
            renderQueue();

            el.author.value = el.defaultAuthor.value;
            el.pubDate.value = nextOpenSlot(
                Math.min(28, Math.max(1, parseInt(el.publishDay.value, 10) || 15))).iso;
            el.dateHelp.textContent = 'Posts dated ahead stay hidden until that day.';

            state.ready = true;
            render();
        }).catch(function (err) {
            state.ready = false;
            notice(el.generateFeedback, 'err',
                'Could not read the site files. The dashboard needs a local server — run ' +
                '<code>python3 -m http.server 8000</code> in the repository root and open ' +
                '<code>http://localhost:8000/publisher/</code>. (' + T.esc(err.message) + ')');
            console.error(err);
        });
    }

    loadTemplate();
    wire();
    boot();
})();
