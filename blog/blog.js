/* Blog archive: client-side search + category filtering.
   Everything is already in the DOM, so this only toggles visibility. */
(function () {
    // Mobile nav toggle — mirrors script.js, and runs on every blog page.
    const toggle = document.getElementById('navToggle');
    const links = document.getElementById('navLinks');
    if (toggle && links) {
        toggle.addEventListener('click', () => {
            links.classList.toggle('active');
            toggle.classList.toggle('active');
        });
    }

    // Solid navbar once scrolled past the hero — script.js does this on the
    // homepage, but blog pages don't load it.
    const navbar = document.getElementById('navbar');
    if (navbar && !navbar.classList.contains('navbar-solid')) {
        const onScroll = () => {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    // Scheduled posts: a future-dated card is committed like any other but stays
    // out of the listings until its morning. hideScheduledCards() lives in
    // lead-capture.js, which every article and archive page loads first.
    hideScheduledCards();

    // A scheduled article's own page still resolves, so you can proof it before
    // it goes public. Say so, rather than letting it look already-published.
    const page = document.querySelector('.article-page[data-publish]');
    if (page) {
        const today = new Date();
        const todayKey = [today.getFullYear(),
            String(today.getMonth() + 1).padStart(2, '0'),
            String(today.getDate()).padStart(2, '0')].join('-');
        if (page.dataset.publish > todayKey) {
            const banner = document.createElement('div');
            banner.className = 'scheduled-banner';
            banner.innerHTML = '<strong>Scheduled preview.</strong> This article is dated ' +
                page.dataset.publish + ' and is not yet listed on the blog or the homepage. ' +
                'It appears automatically on that date.';
            page.prepend(banner);
        }
    }

    // Everything below is archive-only.
    const grid = document.getElementById('postGrid');
    if (!grid) return;

    // Scheduled cards are excluded outright — they must not be findable by
    // search or category, and must not inflate any of the counts.
    const cards = Array.from(grid.querySelectorAll('.post-card'))
        .filter(card => card.dataset.scheduled !== 'true');
    const search = document.getElementById('postSearch');
    const chips = Array.from(document.querySelectorAll('.filter-chip'));
    const count = document.getElementById('resultsCount');
    const noResults = document.getElementById('noResults');
    const clearBtn = document.getElementById('clearFilters');

    // The hero total and the chip counts are baked in at build time and include
    // posts that are still scheduled. Recompute them from the cards that are
    // actually reachable, so the archive never advertises an article nobody can
    // open yet.
    (function recount() {
        const total = document.querySelector('.blog-hero-stats .stat-number[data-total]');
        if (total && +total.dataset.total !== cards.length) {
            total.textContent = cards.length;
            const sub = document.querySelector('.blog-hero-sub');
            if (sub) sub.textContent = sub.textContent.replace(/^\d+/, cards.length);
        }
        document.querySelectorAll('.filter-chip').forEach(chip => {
            const badge = chip.querySelector('.chip-count');
            if (!badge) return;
            badge.textContent = chip.dataset.cat === 'all' ? cards.length : cards.filter(
                card => (card.dataset.cats || '').split('|').indexOf(chip.dataset.cat) !== -1
            ).length;
        });
    })();

    let activeCat = 'all';
    let query = '';

    // Fold typographic characters to ASCII so typing "didn't" matches "didn’t".
    // generate_blog.py applies the same folding when it writes data-title.
    const FOLD = { '‘': "'", '’': "'", '“': '"', '”': '"',
                   '–': '-', '—': '-', '…': '...', ' ': ' ' };
    const fold = s => s.replace(/[‘’“”–—… ]/g,
                                c => FOLD[c]).toLowerCase();

    function apply() {
        let shown = 0;
        cards.forEach(card => {
            const cats = (card.dataset.cats || '').split('|');
            const matchCat = activeCat === 'all' || cats.indexOf(activeCat) !== -1;
            const matchText = !query || (card.dataset.title || '').indexOf(query) !== -1;
            const visible = matchCat && matchText;
            card.hidden = !visible;
            if (visible) shown++;
        });

        count.textContent = shown === cards.length
            ? `Showing all ${cards.length} articles`
            : `Showing ${shown} of ${cards.length} articles`;
        noResults.hidden = shown !== 0;
    }

    let timer;
    search.addEventListener('input', e => {
        clearTimeout(timer);
        const value = fold(e.target.value.trim());
        timer = setTimeout(() => { query = value; apply(); }, 150);
    });

    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            chips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            activeCat = chip.dataset.cat;
            apply();
            // Re-run the clamp so the newly active chip is kept on screen.
            if (typeof window.__flaneyChipLayout === 'function') window.__flaneyChipLayout();
        });
    });

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            search.value = '';
            query = '';
            activeCat = 'all';
            chips.forEach(c => c.classList.toggle('active', c.dataset.cat === 'all'));
            apply();
        });
    }

    /* ---- Clamp the category chips to one row ----
     *
     * The toolbar is sticky, so its height is subtracted from every screen of
     * reading. Thirteen categories wrapped to three rows on a desktop window
     * and twelve on a phone, pinning 305px and 653px respectively — 40% and
     * 80% of the viewport — directly over the cards.
     *
     * Only the first wrapped row stays; the rest hide behind a toggle. The
     * split is measured from laid-out positions rather than assumed from a
     * chip count, because how many fit depends on window width and on the
     * category names, which change as the archive grows.
     */
    (function collapseChips() {
        const wrap = document.getElementById('filterChips');
        if (!wrap || chips.length < 2) return;

        const toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'chip-toggle';
        toggle.setAttribute('aria-controls', 'filterChips');
        wrap.appendChild(toggle);

        let expanded = false;

        function layout() {
            // Measure with everything shown: a hidden chip has no position.
            chips.forEach(c => c.classList.remove('chip-hidden'));

            const rowTop = chips[0].offsetTop;
            const overflow = chips.filter(c => c.offsetTop > rowTop);

            if (!overflow.length) {           // they all fit — nothing to collapse
                toggle.hidden = true;
                return;
            }
            toggle.hidden = false;

            if (expanded) {
                toggle.textContent = 'Show fewer';
                toggle.setAttribute('aria-expanded', 'true');
                return;
            }

            // The selected chip always stays on screen. Collapsing it away
            // left the archive filtered to one category with nothing marked
            // active — the grid showed 16 of 58 articles and no chip explained
            // why. It flows up into the first row once the rest are hidden.
            const active = wrap.querySelector('.filter-chip.active');
            overflow.forEach(c => { if (c !== active) c.classList.add('chip-hidden'); });

            // Hiding the overflow pulls the toggle up, but if the first row was
            // already full it lands on a second row — which is the one thing
            // this is meant to prevent. Give back chips until it fits, taking
            // from the end and never taking the active one.
            const visible = chips.filter(c => !c.classList.contains('chip-hidden'));
            let guard = chips.length;
            while (visible.length > 1 && toggle.offsetTop > rowTop && guard--) {
                let i = visible.length - 1;
                while (i >= 0 && visible[i] === active) i--;
                if (i < 0) break;
                visible.splice(i, 1)[0].classList.add('chip-hidden');
            }

            const n = chips.filter(c => c.classList.contains('chip-hidden')).length;
            toggle.textContent = '+' + n + ' more';
            toggle.setAttribute('aria-expanded', 'false');
        }

        toggle.addEventListener('click', () => {
            expanded = !expanded;
            layout();
            headroom();
        });

        /* Picking a category from the expanded list keeps it expanded: a chip
         * that collapsed out of sight the moment it was clicked would leave no
         * visible sign of which filter is active. */

        // scroll-padding-top belongs on the scrolling element, and blog.css is
        // loaded by the homepage too, so it is set here — on the archive only,
        // from the measured header rather than a hardcoded guess.
        function headroom() {
            const nav = document.getElementById('navbar');
            const bar = document.querySelector('.blog-toolbar');
            if (!bar) return;
            syncToolbarTop(nav, bar);
            const h = (nav ? nav.offsetHeight : 0) + bar.offsetHeight;
            document.documentElement.style.scrollPaddingTop = (h + 12) + 'px';
        }

        /* The navbar is not one height. It is 81px as a full bar at rest and
         * 73px scrolled; in drawer mode the links leave the flow and it is
         * 73px at rest and 65px scrolled. The toolbar is only pinned while
         * the page is scrolled, so that is the height to match — measured
         * here rather than guessed, because every hardcoded value tried so
         * far was right in one state and left a visible strip of page content
         * showing through in another. */
        function syncToolbarTop(nav, bar) {
            if (!nav || getComputedStyle(bar).position !== 'sticky') return;
            const wasScrolled = nav.classList.contains('scrolled');
            const saved = nav.style.transition;
            nav.style.transition = 'none';          // read the end state, not a frame of the fade
            nav.classList.add('scrolled');
            const h = nav.offsetHeight;
            nav.classList.toggle('scrolled', wasScrolled);
            nav.style.transition = saved;
            bar.style.top = h + 'px';
        }

        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => { layout(); headroom(); }, 120);
        });

        // Exposed so the chip click handler above can re-clamp after the
        // active chip changes.
        window.__flaneyChipLayout = function () { layout(); headroom(); };

        layout();
        headroom();

        /* Re-measure once the webfont lands. Chip widths depend on it, and the
         * first pass runs in the fallback face: everything measures narrower,
         * more chips appear to fit, and when Inter swaps in the row reflows and
         * pushes the toggle onto a second row — the exact thing this avoids.
         * Observed as a 190px toolbar that should have been 144px. */
        if (document.fonts && document.fonts.ready) {
            document.fonts.ready.then(() => { layout(); headroom(); });
        }
    })();

    apply();
})();
