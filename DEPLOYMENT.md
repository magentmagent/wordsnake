# wordsnake Public Release Guide

This project is ready to publish as a static website. The game currently runs from `index.html` and loads dictionary data from `public/words-data.js`, so no backend server is required.

## Before Publishing

Check these files before the first public release:

- `index.html`
- `public/words-data.js`
- `public/words.txt`
- `NOTICE.md`
- `privacy.html`
- `.nojekyll`

Keep `NOTICE.md` and `privacy.html` linked from the first screen. They help with dictionary attribution and ad-network review.

## Recommended Hosting: GitHub Pages

1. Create a GitHub repository for this folder.
2. Upload or push the full project.
3. In GitHub, open the repository settings.
4. Go to Pages.
5. Set the source to the main branch and root folder.
6. Save and wait for the Pages URL to become available.
7. Open the published URL on a phone and confirm the game starts and the dictionary loads.

The `.nojekyll` file is included so GitHub Pages serves the static files as-is.

## Other Good Static Hosts

Netlify:

1. Create a new site from the repository.
2. Leave the build command empty.
3. Set the publish directory to the project root.

Cloudflare Pages:

1. Connect the repository.
2. Leave the build command empty.
3. Set the output directory to the project root.

Vercel:

1. Import the repository.
2. Use a static project with no build command.
3. Set the output directory to the project root if asked.

## AdSense Preparation

Google AdSense site review generally expects:

- You own or control the site and can edit the HTML.
- The site has original, useful content and works without broken pages.
- The site complies with AdSense policies.
- The applicant is at least 18 years old.
- Privacy and attribution pages are reachable.

For this project, do not add real ad code until the site has a public URL and an AdSense publisher ID.

## Adding AdSense Later

1. Publish the site first.
2. Create or open a Google AdSense account.
3. Add the published domain in AdSense.
4. Copy the AdSense verification or auto-ads script.
5. Paste that script into the `<head>` of `index.html`.
6. Replace the placeholder in `ads.txt.template` with your real publisher ID.
7. Rename `ads.txt.template` to `ads.txt`.
8. Publish again.
9. Confirm that `https://YOUR_DOMAIN/ads.txt` opens in the browser.
10. Request review in AdSense.

Example `ads.txt` line:

```txt
google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0
```

Replace `pub-0000000000000000` with the publisher ID shown in your AdSense account.

## Ad Placement Notes

For a mobile game, start gently:

- Prefer one banner or anchor ad outside the active board area.
- Do not cover the board, start button, undo button, or typed letters.
- Do not ask users to click ads.
- Avoid placing ads where accidental taps are likely.

Auto ads may be convenient, but manual placement is usually safer for a game UI because the board needs stable touch space.

## Dictionary Data and Commercial Use

The code can be published as a static game, but the dictionary data has separate source and license considerations. Keep `NOTICE.md` with the release, and review the current terms for the National Institute of Korean Language data and Kaikki/Wiktionary-derived data before treating the dictionary bundle as a commercial asset.

This document is practical deployment guidance, not legal advice.

## Optional Word Suggestion Server

GitHub Pages cannot store user submissions by itself. To let players suggest missing words and require admin approval, deploy the Cloudflare Worker example in `server/cloudflare-worker.js`.

High-level setup:

1. Create a Cloudflare account.
2. Install Wrangler locally.
3. Create a KV namespace for suggestions.
4. Copy `server/wrangler.toml.example` to `server/wrangler.toml`.
5. Replace `YOUR_KV_NAMESPACE_ID` with the real KV namespace ID.
6. Set an admin token with `wrangler secret put ADMIN_TOKEN`.
7. Deploy the worker with `wrangler deploy`.
8. Put the worker URL in `public/suggest-config.js`.
9. Visit `admin.html`, enter the worker URL and admin token, then approve or reject pending words.

The worker keeps one record per word. Duplicate player submissions increase the record count instead of creating duplicate pending rows.
