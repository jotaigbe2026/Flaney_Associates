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

    apply();
})();
