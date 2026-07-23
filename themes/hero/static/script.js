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

  const toggle = document.getElementById('mobileMenuToggle');
  const nav = document.getElementById('navMenu');
  const closeMenu = () => {
    if (!toggle || !nav) return;
    toggle.classList.remove('active');
    nav.classList.remove('active');
    toggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  };
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('active');
      toggle.classList.toggle('active', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', closeMenu));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeMenu();
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

  // Focus catalog search when arriving from header search icon
  const params = new URLSearchParams(window.location.search);
  if (params.get('focus') === 'search') {
    const searchInput =
      document.querySelector('.catalog-search input[type="search"], .catalog-search input[name="search"], input[name="search"]');
    if (searchInput) {
      searchInput.focus();
      searchInput.select?.();
    }
  }
});
