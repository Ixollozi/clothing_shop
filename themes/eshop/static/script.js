document.addEventListener('DOMContentLoaded', function () {
  const languageBtn = document.getElementById('languageBtn');
  const languageSwitch = document.querySelector('.language-switcher');
  if (languageBtn && languageSwitch) {
    languageBtn.setAttribute('aria-expanded', 'false');
    languageBtn.setAttribute('aria-haspopup', 'true');
    languageBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      const open = languageSwitch.classList.toggle('active');
      languageBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.language-switcher')) {
        languageSwitch.classList.remove('active');
        languageBtn.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && languageSwitch.classList.contains('active')) {
        languageSwitch.classList.remove('active');
        languageBtn.setAttribute('aria-expanded', 'false');
        languageBtn.focus();
      }
    });
  }

  const toggle = document.getElementById('mobileMenuToggle');
  const nav = document.getElementById('navMenu');
  if (toggle && nav) {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-controls', 'navMenu');
    toggle.addEventListener('click', () => {
      const open = toggle.classList.toggle('active');
      nav.classList.toggle('active', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach((a) =>
      a.addEventListener('click', () => {
        toggle.classList.remove('active');
        nav.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
      })
    );
  }

  const header = document.querySelector('.ag-header');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  gsap.registerPlugin(ScrollTrigger);

  const heroStage = document.querySelector('.ag-hero__stage');
  if (heroStage) {
    gsap.fromTo(
      '.ag-hero__bg',
      { scale: 1.06, opacity: 0.65 },
      { scale: 1, opacity: 1, duration: 1.25, ease: 'power2.out' }
    );
    gsap.from('.ag-hero__content > *', {
      y: 22,
      opacity: 0,
      duration: 0.85,
      stagger: 0.1,
      delay: 0.12,
      ease: 'power3.out',
    });
  }

  ScrollTrigger.batch('.ag-organic', {
    start: 'top 90%',
    onEnter: (elements) => {
      gsap.fromTo(
        elements,
        { y: 28, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.75, stagger: 0.08, ease: 'power3.out', overwrite: true }
      );
    },
  });
});
