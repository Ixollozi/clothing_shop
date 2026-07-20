document.addEventListener('DOMContentLoaded', function () {
  const languageBtn = document.getElementById('languageBtn');
  if (languageBtn) {
    languageBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      this.closest('.language-switcher')?.classList.toggle('active');
    });
  }
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.language-switcher')) {
      document.querySelector('.language-switcher')?.classList.remove('active');
    }
  });

  const toggle = document.getElementById('mobileMenuToggle');
  const nav = document.getElementById('navMenu');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('active');
      nav.classList.toggle('active');
      document.body.style.overflow = nav.classList.contains('active') ? 'hidden' : '';
    });
    nav.querySelectorAll('a').forEach((a) =>
      a.addEventListener('click', () => {
        toggle.classList.remove('active');
        nav.classList.remove('active');
        document.body.style.overflow = '';
      })
    );
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
});
