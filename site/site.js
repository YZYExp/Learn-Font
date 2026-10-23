(() => {
  const field = document.querySelector('#chapter-search');
  if (field) {
    const cards = [...document.querySelectorAll('[data-search]')];
    const parts = [...document.querySelectorAll('[data-part]')];
    const status = document.querySelector('#search-status');
    const empty = document.querySelector('#no-results');
    field.addEventListener('input', () => {
      const terms = field.value.trim().toLocaleLowerCase().split(/\s+/u).filter(Boolean);
      let count = 0;
      for (const card of cards) {
        const text = card.dataset.search.toLocaleLowerCase();
        card.hidden = !terms.every(term => text.includes(term));
        if (!card.hidden) count += 1;
      }
      for (const part of parts) part.hidden = !part.querySelector('.chapter-card:not([hidden])');
      status.textContent = terms.length ? `找到 ${count} 个相关章节` : '按顺序阅读，也可以从感兴趣的章节开始。';
      empty.hidden = count > 0;
    });
    field.addEventListener('keydown', event => {
      if (event.key === 'Escape') {
        field.value = '';
        field.dispatchEvent(new Event('input'));
      }
    });
  }
  const menu = document.querySelector('.chapter-menu');
  if (menu) {
    const smallScreen = matchMedia('(max-width: 800px)');
    const adaptMenu = () => { menu.open = !smallScreen.matches; };
    adaptMenu();
    smallScreen.addEventListener('change', adaptMenu);
  }
  const progress = document.querySelector('.reading-progress span');
  if (progress) {
    let scheduled = false;
    const draw = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      progress.style.transform = `scaleX(${max > 0 ? Math.min(1, Math.max(0, scrollY / max)) : 1})`;
      scheduled = false;
    };
    addEventListener('scroll', () => {
      if (!scheduled) { scheduled = true; requestAnimationFrame(draw); }
    }, { passive: true });
    addEventListener('resize', draw);
    draw();
  }
})();
