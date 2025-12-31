(() => {
  const overlay = document.getElementById('mobileSidebarOverlay');
  const sidebar = document.getElementById('mobileSidebar');
  const openBtn = document.querySelector('[data-sidebar-open]');
  const closeBtns = document.querySelectorAll('[data-sidebar-close]');

  if (!overlay || !sidebar || !openBtn) return;

  const focusableSelector = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
  ].join(',');

  let lastActiveElement = null;

  const show = (el) => el.classList.remove('hidden');
  const hide = (el) => el.classList.add('hidden');

  const setOpenState = (isOpen) => {
    openBtn.setAttribute('aria-expanded', String(isOpen));

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
      }
      lastActiveElement = null;
    }
  };

  const isOpen = () => !sidebar.classList.contains('hidden');

  openBtn.addEventListener('click', () => setOpenState(true));

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
