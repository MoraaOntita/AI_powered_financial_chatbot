const CACHE_NAME = 'bcg-chatbot-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/images/static-bcg-logo.png',
  '/styles/main.css',
  '/scripts/main.js',
  '/images/loading-spinner.gif',
  '/images/og-image.jpg'
  // Add other assets as needed
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});
