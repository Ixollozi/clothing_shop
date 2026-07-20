(function () {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initNav() {
    const languageBtn = document.getElementById('languageBtn');
    const languageSwitcher = languageBtn?.closest('.language-switcher');

    languageBtn?.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = !languageSwitcher?.classList.contains('active');
      languageSwitcher?.classList.toggle('active', open);
      languageBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.language-switcher')) {
        languageSwitcher?.classList.remove('active');
        languageBtn?.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        languageSwitcher?.classList.remove('active');
        languageBtn?.setAttribute('aria-expanded', 'false');
        closeMobileNav();
      }
    });

    const burger = document.getElementById('mobileMenuToggle');
    const nav = document.getElementById('navMenu');
    if (!burger || !nav) return;

    function closeMobileNav() {
      nav.classList.remove('active');
      burger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
      window.__lbLenis?.start();
    }

    burger.addEventListener('click', () => {
      const open = !nav.classList.contains('active');
      nav.classList.toggle('active', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
      window.__lbLenis?.[open ? 'stop' : 'start']();
    });

    nav.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', closeMobileNav);
    });
  }

  function initHeader() {
    const header = document.getElementById('lbHeader');
    const hero = document.querySelector('.lb-hero');
    if (!header) return;

    const sync = () => {
      if (!document.body.classList.contains('is-home') || !hero) {
        header.classList.add('is-solid');
        return;
      }
      const y = window.__lbLenis ? window.__lbLenis.scroll : (window.scrollY || document.documentElement.scrollTop);
      const threshold = Math.max(hero.offsetHeight * 0.42, window.innerHeight * 0.42);
      header.classList.toggle('is-solid', y > threshold);
    };

    sync();
    if (window.__lbLenis) {
      window.__lbLenis.on('scroll', sync);
    }
    window.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync, { passive: true });
  }

  function initLenis() {
    if (reduceMotion || typeof Lenis === 'undefined' || typeof gsap === 'undefined') return;
    gsap.registerPlugin(ScrollTrigger);
    const lenis = new Lenis({ autoRaf: false, lerp: 0.1 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    window.__lbLenis = lenis;
  }

  function initHero() {
    if (typeof gsap === 'undefined') return;
    const media = document.querySelector('.lb-hero-media');
    const brand = document.querySelector('[data-hero="brand"] .lb-mask > span');
    const kicker = document.querySelector('[data-hero="kicker"]');
    const line = document.querySelector('[data-hero="line"]');
    const cta = document.querySelector('[data-hero="cta"]');

    if (reduceMotion) {
      if (media) media.style.transform = 'none';
      return;
    }

    const tl = gsap.timeline({ defaults: { ease: 'expo.out' } });
    if (media) {
      gsap.set(media, { scale: 1.12 });
      tl.to(media, { scale: 1, duration: 2.1 }, 0);
    }
    if (brand) {
      gsap.set(brand, { yPercent: 110 });
      tl.to(brand, { yPercent: 0, duration: 1.1 }, 0.18);
    }
    [kicker, line, cta].forEach((el, i) => {
      if (!el) return;
      gsap.set(el, { autoAlpha: 0, y: 18 });
      tl.to(el, { autoAlpha: 1, y: 0, duration: 0.8 }, 0.42 + i * 0.09);
    });
  }

  function initReveals() {
    if (typeof gsap === 'undefined') {
      document.querySelectorAll('.reveal').forEach((el) => {
        el.style.opacity = '1';
        el.style.transform = 'none';
      });
      return;
    }
    if (reduceMotion) {
      gsap.set('.reveal', { clearProps: 'all', opacity: 1, y: 0 });
      return;
    }
    ScrollTrigger.batch('.reveal', {
      start: 'top 92%',
      onEnter: (els) => {
        gsap.to(els, {
          opacity: 1,
          y: 0,
          duration: 0.9,
          ease: 'power3.out',
          stagger: 0.07,
          overwrite: true,
        });
      },
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initNav();
    initLenis();
    initHeader();
    initHero();
    initReveals();
  });
})();
