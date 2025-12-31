(() => {
  const overlay = document.getElementById('mobileSidebarOverlay');
  const sidebar = document.getElementById('mobileSidebar');
  const openBtns = Array.from(document.querySelectorAll('[data-sidebar-open]'));
  const closeBtns = document.querySelectorAll('[data-sidebar-close]');

  if (!overlay || !sidebar || openBtns.length === 0) return;

  const focusableSelector = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
  ].join(',');

  let lastActiveElement = null;
  let lastOpenBtn = null;

  const show = (el) => el.classList.remove('hidden');
  const hide = (el) => el.classList.add('hidden');

  const setOpenState = (isOpen) => {
    openBtns.forEach((btn) => btn.setAttribute('aria-expanded', String(isOpen)));

    if (isOpen) {
      lastActiveElement = document.activeElement;
      show(overlay);
      show(sidebar);

      document.body.classList.add('overflow-hidden');

      const firstFocusable = sidebar.querySelector(focusableSelector);
      if (firstFocusable) firstFocusable.focus();
    } else {
      hide(overlay);
      hide(sidebar);

      document.body.classList.remove('overflow-hidden');

      if (lastActiveElement && typeof lastActiveElement.focus === 'function') {
        lastActiveElement.focus();
      } else if (lastOpenBtn && typeof lastOpenBtn.focus === 'function') {
        lastOpenBtn.focus();
      }
      lastActiveElement = null;
      lastOpenBtn = null;
    }
  };

  const isOpen = () => !sidebar.classList.contains('hidden');

  openBtns.forEach((btn) =>
    btn.addEventListener('click', () => {
      lastOpenBtn = btn;
      setOpenState(true);
    })
  );

  closeBtns.forEach((btn) => btn.addEventListener('click', () => setOpenState(false)));

  overlay.addEventListener('click', () => setOpenState(false));

  sidebar.addEventListener('click', (e) => {
    const target = e.target;
    if (!(target instanceof Element)) return;
    if (target.closest('a[href]')) setOpenState(false);
  });

  document.addEventListener('keydown', (e) => {
    if (!isOpen()) return;

    if (e.key === 'Escape') {
      e.preventDefault();
      setOpenState(false);
      return;
    }

    if (e.key !== 'Tab') return;

    const focusables = Array.from(sidebar.querySelectorAll(focusableSelector));
    if (focusables.length === 0) return;

    const first = focusables[0];
    const last = focusables[focusables.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  setOpenState(false);
})();
