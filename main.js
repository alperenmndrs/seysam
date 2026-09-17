(() => {
  'use strict';
  const articleEditor = document.querySelector('.article-editor');
  if (articleEditor) {
    const title = articleEditor.elements.title;
    const slug = articleEditor.elements.slug;
    let automaticSlug = articleEditor.dataset.new === 'true' && !slug.value;
    slug.addEventListener('input', () => { automaticSlug = false; });
    title.addEventListener('input', () => {
      if (automaticSlug) slug.value = title.value.toLocaleLowerCase('tr-TR').replace(/ı/g, 'i').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0,160).replace(/-$/, '');
    });
    const addHeading = articleEditor.querySelector('[data-add-heading]');
    addHeading.hidden = false;
    addHeading.addEventListener('click', () => {
      const body = articleEditor.elements.body;
      body.setRangeText('\n\n## Bölüm başlığı\n', body.selectionStart, body.selectionEnd, 'end');
      body.focus();
    });
  }
  const nav = document.getElementById('main-nav');
  const toggle = document.getElementById('menu-toggle');
  if (nav && toggle) {
    const mobile = window.matchMedia('(max-width: 1000px)');
    const setMenu = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? 'Kapat' : 'Menü';
      nav.hidden = mobile.matches && !open;
      document.body.classList.toggle('menu-open', mobile.matches && open);
    };
    const syncMenu = () => { toggle.hidden = !mobile.matches; setMenu(false); };
    syncMenu();
    mobile.addEventListener('change', syncMenu);
    toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { setMenu(false); toggle.focus(); }
    });
    document.addEventListener('click', (event) => {
      if (!event.target.closest('.site-header')) setMenu(false);
    });
  }
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('.motion-toggle').forEach((button) => {
    const update = () => { button.hidden = motion.matches; };
    update();
    motion.addEventListener('change', update);
    button.addEventListener('click', () => {
      const paused = button.getAttribute('aria-pressed') !== 'true';
      document.querySelectorAll('[data-logo-strip]').forEach(el => el.classList.toggle('is-paused', paused));
      button.setAttribute('aria-pressed', String(paused));
      button.textContent = paused ? 'Hareketi başlat' : 'Hareketi durdur';
    });
  });
  const form = document.getElementById('contact-form');
  if (form) {
    document.getElementById('contact-fields').disabled = false;
    const status = document.getElementById('form-status');
    const panel = document.getElementById('draft-panel');
    try {
      const selectedService = new URLSearchParams(window.location.search).get('hizmet');
      if (selectedService && form.elements['service']) {
        for (const opt of form.elements['service'].options) {
          if (opt.value === selectedService) { opt.selected = true; break; }
        }
      }
    } catch (_) {}
    form.addEventListener('input', () => { panel.hidden = true; status.textContent = ''; });
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const data = new FormData(form);
      const name = data.get('name').trim();
      const message = data.get('message').trim();
      if (!name || !message) { status.textContent = 'Lütfen adınızı ve proje açıklamanızı doldurun.'; return; }
      const service = data.get('service') || 'Genel görüşme';
      const body = `Merhaba Seysa Medya,\n\nAdım: ${name}\nE-posta: ${data.get('email')}\nHizmet: ${service}\n\n${message}`;
      document.getElementById('draft-text').value = body;
      document.getElementById('draft-link').href = document.querySelector('.contact-email').getAttribute('href') + '?subject=' + encodeURIComponent('Teklif talebi — ' + service) + '&body=' + encodeURIComponent(body);
      panel.hidden = false;
      status.textContent = 'Taslağınız hazır. Göndermek için e-posta uygulamanızda açın.';
    });
  }

  // Public-site effects. Form and admin behavior above remains independent.
  if (document.body.classList.contains('admin-body')) return;

  const pageContent = document.getElementById('main');
  let pageAnimation;
  window.addEventListener('pageshow', () => pageAnimation?.cancel());
  document.addEventListener('visibilitychange', () => {
    if (document.hidden || motion.matches || !pageContent?.animate) return;
    pageAnimation?.cancel();
    pageAnimation = pageContent.animate([{opacity: .8, translate: '0 6px'}, {opacity: 1, translate: '0 0'}], {duration: 260, easing: 'ease-out'});
  });
  document.querySelectorAll('[data-project-filter]').forEach(button => {
    button.addEventListener('click', () => {
      document.querySelectorAll('[data-project-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      document.querySelectorAll('[data-project-service]').forEach(card => {
        card.hidden = !!button.dataset.projectFilter && card.dataset.projectService !== button.dataset.projectFilter;
      });
    });
  });

  const viewer = document.getElementById('image-viewer');
  if (viewer && typeof viewer.showModal === 'function') {
    const picture = viewer.querySelector('img');
    document.querySelectorAll('.gallery-open').forEach(button => {
      button.addEventListener('click', () => {
        picture.src = button.dataset.fullImage;
        picture.alt = button.dataset.caption;
        viewer.querySelector('p').textContent = button.dataset.caption;
        viewer.showModal();
      });
    });
    viewer.querySelector('.viewer-close').addEventListener('click', () => viewer.close());
    viewer.addEventListener('click', event => { if (event.target === viewer) viewer.close(); });
    viewer.addEventListener('close', () => picture.removeAttribute('src'));
  }

  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const stage = document.querySelector('[data-hero-motion]');
  if (stage) {
    let frame = 0;
    let point;
    const resetScene = () => {
      cancelAnimationFrame(frame);
      frame = 0;
      stage.style.removeProperty('--scene-x');
      stage.style.removeProperty('--scene-y');
    };
    stage.addEventListener('pointermove', event => {
      if (motion.matches || !finePointer.matches || event.pointerType !== 'mouse') return;
      point = {x: event.clientX, y: event.clientY};
      if (frame) return;
      frame = requestAnimationFrame(() => {
        frame = 0;
        const box = stage.getBoundingClientRect();
        stage.style.setProperty('--scene-x', `${(0.5 - (point.y - box.top) / box.height) * 24}deg`);
        stage.style.setProperty('--scene-y', `${((point.x - box.left) / box.width - 0.5) * 30}deg`);
      });
    }, {passive: true});
    stage.addEventListener('pointerleave', resetScene);
    stage.addEventListener('pointercancel', resetScene);
    window.addEventListener('blur', resetScene);
    window.addEventListener('scroll', resetScene, {passive: true});
    finePointer.addEventListener('change', resetScene);
    motion.addEventListener('change', resetScene);
    // Pause decorative loops when the hero leaves the viewport or tab is hidden.
    let inView = true;
    const syncScene = () => stage.classList.toggle('scene-idle', !inView || document.hidden);
    if ('IntersectionObserver' in window) {
      const sceneObserver = new IntersectionObserver(entries => {
        inView = entries[0].isIntersecting;
        syncScene();
      });
      sceneObserver.observe(stage);
    }
    document.addEventListener('visibilitychange', syncScene);
  }
  const resetCards = new Set();
  document.querySelectorAll('[data-tilt]').forEach((card) => {
    let rect = null;
    let frame = 0;
    let point = null;
    const limit = Math.min(Number(card.dataset.tilt) || 5, 6);
    const reset = () => {
      cancelAnimationFrame(frame);
      frame = 0;
      rect = null;
      point = null;
      card.classList.remove('is-tilting');
      ['--tilt-x', '--tilt-y', '--spot-x', '--spot-y'].forEach(key => card.style.removeProperty(key));
      resetCards.delete(reset);
    };
    card.addEventListener('pointermove', (event) => {
      if (motion.matches || !finePointer.matches || event.pointerType !== 'mouse') return;
      if (!rect) rect = card.getBoundingClientRect();
      point = { x: event.clientX, y: event.clientY };
      resetCards.add(reset);
      if (frame) return;
      frame = requestAnimationFrame(() => {
        frame = 0;
        const x = Math.max(0, Math.min(1, (point.x - rect.left) / rect.width));
        const y = Math.max(0, Math.min(1, (point.y - rect.top) / rect.height));
        card.classList.add('is-tilting');
        card.style.setProperty('--tilt-x', `${(0.5 - y) * limit * 2}deg`);
        card.style.setProperty('--tilt-y', `${(x - 0.5) * limit * 2}deg`);
        card.style.setProperty('--spot-x', `${x * 100}%`);
        card.style.setProperty('--spot-y', `${y * 100}%`);
      });
    }, { passive: true });
    card.addEventListener('pointerleave', reset);
    card.addEventListener('pointercancel', reset);
  });
  const resetActiveCards = () => [...resetCards].forEach(reset => reset());
  window.addEventListener('scroll', resetActiveCards, { passive: true });
  window.addEventListener('resize', resetActiveCards, { passive: true });
  window.addEventListener('blur', resetActiveCards);
  finePointer.addEventListener('change', resetActiveCards);

  // One observer, no scroll-position polling. Off-screen content stays readable
  // if JavaScript or the animation API is unavailable.
  const revealTargets = [...document.querySelectorAll(
    '.section-heading, .service-card, .service-directory, .scope-list li, ' +
    '.service-aside, .project-card, .reference-card, .package-card, ' +
    '.about-logo, .about-layout .prose, .contact-callout, .creative-cta .container'
  )];
  const animations = new Set();
  let observer;
  const reveal = (element) => {
    if (!element.classList.contains('reveal-pending')) return;
    element.classList.remove('reveal-pending');
    observer?.unobserve(element);
    if (motion.matches || element.matches(':focus-within')) return;
    const siblings = [...element.parentElement.children].filter(el => revealTargets.includes(el));
    const delay = (Math.max(0, siblings.indexOf(element)) % 3) * 75;
    // Animate the individual translate property so tilt's transform is untouched.
    const animation = element.animate([
      { opacity: 0, translate: '0 26px', filter: 'blur(4px)' },
      { opacity: 1, translate: '0 0', filter: 'blur(0)' }
    ], { duration: 650, delay, easing: 'cubic-bezier(.2,.8,.2,1)', fill: 'backwards' });
    animations.add(animation);
    animation.finished.then(() => animations.delete(animation)).catch(() => animations.delete(animation));
  };
  const prepareReveals = () => {
    observer?.disconnect();
    animations.forEach(animation => animation.cancel());
    animations.clear();
    revealTargets.forEach(el => el.classList.remove('reveal-pending'));
    if (motion.matches || !('IntersectionObserver' in window) || !Element.prototype.animate) return;
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { if (entry.isIntersecting) reveal(entry.target); });
    }, { threshold: 0, rootMargin: '0px 0px -20px 0px' });
    revealTargets.forEach(el => {
      if (el.getBoundingClientRect().top >= window.innerHeight) {
        el.classList.add('reveal-pending');
        observer.observe(el);
      }
    });
  };
  document.addEventListener('focusin', event => {
    const pending = event.target.closest('.reveal-pending');
    if (pending) reveal(pending);
  });
  motion.addEventListener('change', () => { resetActiveCards(); prepareReveals(); });
  // BFCache can restore a page at a different scroll position.
  window.addEventListener('pageshow', event => { if (event.persisted) prepareReveals(); });
  prepareReveals();
})();
