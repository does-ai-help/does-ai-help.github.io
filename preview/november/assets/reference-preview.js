(() => {
  const templates = document.getElementById('reference-preview-templates');
  if (!templates) return;
  const desktop = matchMedia('(hover: hover) and (pointer: fine) and (min-width: 721px)');
  const entries = new Map([...templates.content.children].map(t => [t.dataset.referenceId, t]));
  const links = [...document.querySelectorAll('.citations a[data-reference-id]')];
  const titles = new Map(links.map(link => [link, link.getAttribute('title')]));
  const tooltip = document.createElement('div');
  tooltip.id = 'reference-preview';
  tooltip.className = 'reference-preview';
  tooltip.setAttribute('role', 'tooltip');
  tooltip.hidden = true;
  document.body.append(tooltip);
  let current = null;
  let timer;
  let pending = null;

  function hide() {
    clearTimeout(timer);
    pending = null;
    if (current) {
      const ids = (current.getAttribute('aria-describedby') || '').split(/\s+/).filter(id => id && id !== tooltip.id);
      if (ids.length) current.setAttribute('aria-describedby', ids.join(' '));
      else current.removeAttribute('aria-describedby');
    }
    tooltip.hidden = true;
    current = null;
  }

  function show(link) {
    if (!desktop.matches || !entries.has(link.dataset.referenceId)) return;
    hide();
    current = link;
    tooltip.replaceChildren(entries.get(link.dataset.referenceId).content.cloneNode(true));
    tooltip.hidden = false;
    const anchor = link.getBoundingClientRect();
    const box = tooltip.getBoundingClientRect();
    const margin = 16;
    const left = Math.max(margin, Math.min(anchor.left, innerWidth - box.width - margin));
    const below = anchor.bottom + 10;
    const preferred = below + box.height <= innerHeight - margin ? below : anchor.top - box.height - 10;
    const top = Math.max(margin, Math.min(preferred, innerHeight - box.height - margin));
    tooltip.style.left = `${left}px`;
    tooltip.style.top = `${top}px`;
    const ids = new Set((link.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean));
    ids.add(tooltip.id);
    link.setAttribute('aria-describedby', [...ids].join(' '));
  }

  function queueShow(link) {
    clearTimeout(timer);
    pending = link;
    if (desktop.matches) timer = setTimeout(() => {
      if (link.matches(':hover') || document.activeElement === link) show(link);
    }, 200);
  }

  function queueHide() {
    if (pending?.matches(':focus-visible') || current?.matches(':focus-visible')) return;
    clearTimeout(timer);
    pending = null;
    timer = setTimeout(hide, 160);
  }

  function updateMode() {
    hide();
    for (const link of links) {
      if (desktop.matches) link.removeAttribute('title');
      else if (titles.get(link)) link.setAttribute('title', titles.get(link));
    }
  }

  for (const link of links) {
    link.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'touch') queueShow(link);
    });
    link.addEventListener('pointerleave', queueHide);
    link.addEventListener('focus', () => queueShow(link));
    link.addEventListener('blur', () => {
      if (!tooltip.matches(':hover')) queueHide();
    });
    link.addEventListener('click', hide);
  }
  tooltip.addEventListener('pointerenter', () => clearTimeout(timer));
  tooltip.addEventListener('pointerleave', queueHide);
  document.addEventListener('keydown', event => { if (event.key === 'Escape') hide(); });
  document.addEventListener('scroll', event => {
    if (!tooltip.hidden && !tooltip.contains(event.target)) hide();
  }, true);
  window.addEventListener('resize', hide);
  desktop.addEventListener('change', updateMode);
  updateMode();
})();
