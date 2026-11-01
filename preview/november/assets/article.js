const links = [...document.querySelectorAll('.contents a')];
const sections = links.map(a => document.getElementById(a.hash.slice(1))).filter(Boolean);
const contents=document.querySelector('.contents');
if(contents && matchMedia('(max-width:720px)').matches) {
  const details=document.createElement('details');
  const summary=document.createElement('summary');
  summary.textContent='Contents';
  details.append(summary,contents.querySelector('nav'));
  contents.replaceChildren(details);
}
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    const entry = entries.find(e => e.isIntersecting);
    if (entry) links.forEach(a => a.classList.toggle('active', a.hash === '#' + entry.target.id));
  }, {rootMargin:'-5% 0px -75% 0px'});
  sections.forEach(s => observer.observe(s));
}
