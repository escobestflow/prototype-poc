# Prototype POC

A single-file PWA prototype scaffold. Hosts on GitHub Pages, looks like a real app on iPhone when installed to the Home Screen (no browser chrome), and displays inside a phone bezel on desktop for demos.

## Files

- `index.html` — the entire app: sample screens (Home, Projects, Detail, Profile), bottom tab bar, device frame.
- `manifest.webmanifest` — PWA manifest (`display: standalone`).
- `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `apple-touch-icon.png` — app icons.

## Demo on desktop

Open `index.html` in a browser. A phone-shaped bezel wraps the app content for screenshots and stakeholder demos.

## Install on iPhone (chromeless)

1. Open the live URL in **Safari** on iPhone.
2. Tap the **Share** button.
3. Tap **Add to Home Screen**.
4. Launch from the Home Screen icon — no Safari address bar, no tabs.

## Customize

- Swap `ITEMS` and `TABS` arrays in the `<script>` block for your real content.
- Duplicate a `<section class="view" data-view="...">` block to add a new screen. Any element with `data-nav="viewName"` navigates to it.
- Edit the CSS variables at the top of the `<style>` block to retheme.

## Deploy

Pushed to GitHub Pages — any commit to `main` redeploys automatically.
