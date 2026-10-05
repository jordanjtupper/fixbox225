const buttons = document.querySelectorAll('[data-filter]');
buttons.forEach(button => button.addEventListener('click', () => {
  buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  document.querySelectorAll('[data-game]').forEach(game => {
    game.hidden = button.dataset.filter !== 'all' && game.dataset.game !== button.dataset.filter;
  });
}));
const next = document.querySelector('[data-next-game]');
if (next) {
  const games = JSON.parse(document.querySelector('#games-data').textContent);
  const game = games.find(g => new Date(`${g.date}T${g.time}:00${g.date < '2026-11-01' || g.date >= '2027-03-14' ? '-05:00' : '-06:00'}`) > new Date());
  if (game) {
    next.querySelector('[data-opponent]').textContent = `${game.home ? 'vs.' : 'at'} ${game.opponent}`;
    const date = new Date(`${game.date}T12:00:00`);
    next.querySelector('[data-date]').textContent = date.toLocaleDateString('en-US', {month:'long',day:'numeric',weekday:'short'});
    next.querySelector('[data-venue]').textContent = game.venue;
  } else {
    next.querySelector('[data-opponent]').textContent = 'More hockey ahead';
    next.querySelector('[data-date]').textContent = 'Check the official schedule';
    next.querySelector('[data-venue]').textContent = 'More games will be added here.';
  }
}
const load = document.querySelector('[data-load-feed]');
if (load) load.addEventListener('click', () => {
  const iframe = document.createElement('iframe');
  iframe.title = 'Official Baton Rouge Kingfish Facebook timeline';
  iframe.src = `https://www.facebook.com/plugins/page.php?href=${encodeURIComponent(load.dataset.loadFeed)}&tabs=timeline&width=500&height=500&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false`;
  iframe.loading = 'lazy';
  iframe.referrerPolicy = 'strict-origin-when-cross-origin';
  load.parentElement.append(iframe);
  load.remove();
});
