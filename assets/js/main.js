'use strict';

const themeButton = document.querySelector('.theme-toggle');
function updateThemeButton() {
  const dark = document.documentElement.dataset.theme === 'dark';
  const label = dark ? 'Switch to light theme' : 'Switch to dark theme';
  themeButton.setAttribute('aria-label', label);
  themeButton.title = label;
}
themeButton.hidden = false;
updateThemeButton();
themeButton.addEventListener('click', () => {
  const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = theme;
  try { localStorage.setItem('homepage-theme', theme); } catch (error) {}
  updateThemeButton();
});

const filterBar = document.querySelector('.filters');
const filters = [...filterBar.querySelectorAll('button')];
const papers = [...document.querySelectorAll('.paper')];
filterBar.hidden = false;
filters.forEach(button => {
  button.addEventListener('click', () => {
    const topic = button.dataset.filter;
    filters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
    papers.forEach(paper => { paper.hidden = topic !== 'all' && paper.dataset.topic !== topic; });
    document.querySelectorAll('.paper-section').forEach(section => {
      const visible = section.querySelectorAll('.paper:not([hidden])').length;
      section.querySelector('.count').textContent = visible;
      section.querySelector('.empty-state').hidden = visible !== 0;
      section.querySelectorAll('.year-heading').forEach(heading => {
        let next = heading.nextElementSibling;
        let hasVisiblePaper = false;
        while (next && !next.classList.contains('year-heading')) {
          if (next.classList.contains('paper') && !next.hidden) hasVisiblePaper = true;
          next = next.nextElementSibling;
        }
        heading.hidden = !hasVisiblePaper;
      });
    });
    const count = papers.filter(paper => !paper.hidden).length;
    document.querySelector('.filter-status').textContent = `${count} ${count === 1 ? 'paper' : 'papers'} shown. ${button.textContent}.`;
  });
});

const dialog = document.querySelector('.figure-dialog');
let figureTrigger;
if (typeof dialog.showModal === 'function') {
  document.querySelectorAll('.paper-figure').forEach(button => {
    button.addEventListener('click', () => {
      figureTrigger = button;
      const image = dialog.querySelector('.dialog-image');
      image.src = button.dataset.figure;
      image.alt = button.querySelector('img').alt;
      dialog.querySelector('#figure-title').textContent = button.dataset.title;
      dialog.querySelector('.dialog-source').href = button.closest('.paper').querySelector('h3 a').href;
      dialog.showModal();
      document.body.style.overflow = 'hidden';
    });
  });
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.style.overflow = '';
    if (figureTrigger) figureTrigger.focus();
  });
} else {
  document.querySelectorAll('.paper-figure').forEach(button => {
    button.addEventListener('click', () => window.open(button.dataset.figure, '_blank', 'noopener'));
  });
}
