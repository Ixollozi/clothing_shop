document.addEventListener('DOMContentLoaded', function () {
  const languageBtn = document.getElementById('languageBtn');
  const languageSwitcher = languageBtn?.closest('.language-switcher');
  if (languageBtn && languageSwitcher) {
    languageBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      const open = languageSwitcher.classList.toggle('active');
      languageBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.language-switcher') && languageSwitcher) {
      languageSwitcher.classList.remove('active');
      languageBtn?.setAttribute('aria-expanded', 'false');
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && languageSwitcher?.classList.contains('active')) {
      languageSwitcher.classList.remove('active');
      languageBtn?.setAttribute('aria-expanded', 'false');
      languageBtn?.focus();
    }
  });

  const menuToggle = document.getElementById('mobileMenuToggle');
  const menuClose = document.getElementById('mobileMenuClose');
  const nav = document.getElementById('navMenu');
  const backdrop = document.getElementById('navBackdrop');
  const searchToggle = document.getElementById('mobileSearchToggle');
  const searchSheet = document.getElementById('mobileSearchSheet');
  const searchClose = document.getElementById('mobileSearchClose');
  const searchBackdrop = document.getElementById('searchBackdrop');
  const searchInput = document.getElementById('mobileSearchInput');

  const setMenuOpen = (open) => {
    document.body.classList.toggle('is-menu-open', open);
    menuToggle?.setAttribute('aria-expanded', open ? 'true' : 'false');
    backdrop?.setAttribute('aria-hidden', open ? 'false' : 'true');
    if (open) setSearchOpen(false);
    document.body.style.overflow = open || document.body.classList.contains('is-search-open') ? 'hidden' : '';
  };

  const setSearchOpen = (open) => {
    document.body.classList.toggle('is-search-open', open);
    if (searchSheet) searchSheet.hidden = !open;
    searchToggle?.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) {
      setMenuOpen(false);
      setTimeout(() => searchInput?.focus(), 50);
    }
    document.body.style.overflow = open || document.body.classList.contains('is-menu-open') ? 'hidden' : '';
  };

  menuToggle?.addEventListener('click', () => {
    setMenuOpen(!document.body.classList.contains('is-menu-open'));
  });
  menuClose?.addEventListener('click', () => setMenuOpen(false));
  backdrop?.addEventListener('click', () => setMenuOpen(false));
  nav?.querySelectorAll('.h-nav__links a').forEach((a) => a.addEventListener('click', () => setMenuOpen(false)));

  searchToggle?.addEventListener('click', () => {
    setSearchOpen(Boolean(searchSheet?.hidden));
  });
  searchClose?.addEventListener('click', () => setSearchOpen(false));
  searchBackdrop?.addEventListener('click', () => setSearchOpen(false));

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      setMenuOpen(false);
      setSearchOpen(false);
    }
  });

  const filtersToggle = document.getElementById('filtersToggle');
  const filtersSidebar = document.getElementById('filtersSidebar');
  if (filtersToggle && filtersSidebar) {
    filtersToggle.addEventListener('click', () => {
      const open = filtersSidebar.classList.toggle('is-open');
      filtersToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  const scrollRow = (el, dir) => {
    if (!el) return;
    const card = el.querySelector('.pcard, a');
    const amount = card ? card.getBoundingClientRect().width + 16 : 240;
    el.scrollBy({ left: dir * amount, behavior: 'smooth' });
  };
  document.getElementById('sellersNext')?.addEventListener('click', () =>
    scrollRow(document.getElementById('sellersTrack'), 1)
  );
  document.getElementById('igNext')?.addEventListener('click', () =>
    scrollRow(document.getElementById('igTrack'), 1)
  );

  const params = new URLSearchParams(window.location.search);
  if (params.get('focus') === 'search') {
    if (window.matchMedia('(max-width: 920px)').matches) {
      setSearchOpen(true);
    } else {
      const searchInputDesktop =
        document.querySelector('.catalog-search input[type="search"], .catalog-search input[name="search"], input[name="search"]');
      if (searchInputDesktop) {
        searchInputDesktop.focus();
        searchInputDesktop.select?.();
      }
    }
  }
});
