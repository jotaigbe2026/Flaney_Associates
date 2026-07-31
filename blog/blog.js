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

    // Everything below is archive-only.
    const grid = document.getElementById('postGrid');
    if (!grid) return;

    const cards = Array.from(grid.querySelectorAll('.post-card'));
    const search = document.getElementById('postSearch');
    const chips = Array.from(document.querySelectorAll('.filter-chip'));
    const count = document.getElementById('resultsCount');
    const noResults = document.getElementById('noResults');
    const clearBtn = document.getElementById('clearFilters');

    let activeCat = 'all';
    let query = '';

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
        const value = e.target.value.trim().toLowerCase();
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
