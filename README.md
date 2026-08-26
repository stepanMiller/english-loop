# English Loop — tutor test demo

Mobile-first React prototype for the homework practice loop:

1. Teacher creates homework for Ahav.
2. Switch to Student mode; the newest assignment appears immediately.
3. Open Speaking, tap Record, allow microphone access, Stop, Play, Re-record or Submit.
4. Switch to Teacher mode; the speaking submission appears under Needs review and can be played back.

Homework metadata is stored in `localStorage`. Audio recordings are stored locally in IndexedDB. Nothing is uploaded to a server.

## Local development

```bash
npm install
npm run dev
```

## Production build

```bash
npm run build
```

The static site is generated in `dist/` and uses relative asset paths, so it can be hosted on GitHub Pages or any static HTTPS host.

## GitHub Pages

Push the project to the `main` branch, then open **Settings → Pages → Source** and select **GitHub Actions**. The included workflow deploys every push to `main`.

## iPhone Safari notes

- Microphone access requires HTTPS (GitHub Pages provides it) or localhost.
- Permission is requested only after the student taps Record.
- If access is denied, enable Microphone for the site in Safari settings and try again.
- Audio stays on the same device and browser profile as the demo.
