const topControl = document.querySelector('.back-to-top');
const pageTop = document.getElementById('page-top');
if (topControl && pageTop) {
  const updateVisibility = () => { topControl.hidden = window.scrollY < 600; };
  window.addEventListener('scroll', updateVisibility, { passive: true });
  updateVisibility();
  document.querySelectorAll('.back-to-top, .back-to-top-link').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      pageTop.focus({ preventScroll: true });
      window.scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
    });
  });
}
