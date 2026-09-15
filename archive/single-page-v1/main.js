(() => {
  'use strict';
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.getElementById('main-nav');
  const mobile = window.matchMedia('(max-width: 1000px)');
  const setMenu = (open) => {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.innerHTML = open ? 'Kapat <span aria-hidden="true">−</span>' : 'Menü <span aria-hidden="true">＋</span>';
    nav.hidden = mobile.matches && !open;
  };
  const syncMenu = () => {
    toggle.hidden = !mobile.matches;
    setMenu(false);
  };
  syncMenu();
  mobile.addEventListener('change', syncMenu);
  toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      toggle.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.site-header')) setMenu(false);
  });
  document.getElementById('year').textContent = new Date().getFullYear();
  const serviceSelect = document.getElementById('service-select');
  document.querySelectorAll('[data-package]').forEach((link) => {
    link.addEventListener('click', () => {
      serviceSelect.value = link.dataset.package;
      serviceSelect.dispatchEvent(new Event('input', { bubbles: true }));
    });
  });
  const form = document.getElementById('contact-form');
  document.getElementById('contact-fields').disabled = false;
  form.addEventListener('input', () => {
    document.getElementById('draft-panel').hidden = true;
    document.getElementById('form-status').textContent = '';
  });
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const name = data.get('name').trim();
    const message = data.get('message').trim();
    if (!name || !message) {
      document.getElementById('form-status').textContent = 'Lütfen adınızı ve proje açıklamanızı doldurun.';
      return;
    }
    const subject = 'Proje görüşmesi — ' + data.get('service');
    const body = `Merhaba Seysa Medya,\n\nAdım: ${name}\nE-posta: ${data.get('email')}\nİlgilendiğim hizmet: ${data.get('service')}\n\n${message}`;
    document.getElementById('draft-text').value = body;
    document.getElementById('draft-link').href = 'mailto:info@seysamedya.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    document.getElementById('draft-panel').hidden = false;
    document.getElementById('form-status').textContent = 'Taslağınız hazır. Henüz gönderilmedi; aşağıdaki bağlantıdan e-posta uygulamanızda açabilirsiniz.';
  });
})();
