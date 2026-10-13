(() => {
  const link = document.querySelector('.github-star');
  if (!link) return;
  const repository = link.dataset.repository;
  if (!/^[\w.-]+\/[\w.-]+$/.test(repository)) return;
  const count = link.querySelector('.github-star-count');
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  fetch(`https://api.github.com/repos/${repository}`, {
    headers: { Accept: 'application/vnd.github+json' },
    signal: controller.signal,
    credentials: 'omit'
  }).then(response => {
    if (!response.ok) throw new Error('Star count unavailable');
    return response.json();
  }).then(data => {
    if (!Number.isSafeInteger(data.stargazers_count) || data.stargazers_count < 0) {
      throw new Error('Invalid star count');
    }
    count.textContent = new Intl.NumberFormat('en').format(data.stargazers_count);
    count.hidden = false;
    link.setAttribute('aria-label', `Star Does AI Help? on GitHub; ${data.stargazers_count} stars`);
  }).catch(() => {
    link.title = 'Give this repository a star on GitHub (live count unavailable)';
  }).finally(() => clearTimeout(timeout));
})();
