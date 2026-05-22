// Dot Defense — 서비스워커 (오프라인 캐싱)
const CACHE = 'dot-defense-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-512-maskable.png',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(ASSETS).catch(() => {}))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(res => res || fetch(e.request).then(net => {
      // 캐시에 저장 (런타임)
      const copy = net.clone();
      caches.open(CACHE).then(c => c.put(e.request, copy)).catch(() => {});
      return net;
    }).catch(() => caches.match('./index.html')))
  );
});
