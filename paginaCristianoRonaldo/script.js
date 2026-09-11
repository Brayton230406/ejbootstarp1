const timelineItems = document.querySelectorAll('.timeline-item');
const progressBar = document.querySelector('#progress-bar');
const currentYear = document.querySelector('#current-year');

function toggleTimelineItem(item) {
  const trigger = item.querySelector('.timeline-trigger');
  const content = item.querySelector('.timeline-content');
  const isOpen = item.classList.contains('is-active');

  timelineItems.forEach((otherItem) => {
    otherItem.classList.remove('is-active');
    otherItem.querySelector('.timeline-trigger').setAttribute('aria-expanded', 'false');
    otherItem.querySelector('.timeline-content').hidden = true;
  });

  if (!isOpen) {
    item.classList.add('is-active');
    trigger.setAttribute('aria-expanded', 'true');
    content.hidden = false;
  }
}

timelineItems.forEach((item) => {
  item.querySelector('.timeline-trigger').addEventListener('click', () => toggleTimelineItem(item));
});

function updateReadingProgress() {
  const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = scrollableHeight > 0 ? (window.scrollY / scrollableHeight) * 100 : 0;
  progressBar.style.width = `${progress}%`;
}

window.addEventListener('scroll', updateReadingProgress, { passive: true });
updateReadingProgress();
currentYear.textContent = new Date().getFullYear();
