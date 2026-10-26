# Two official multilingual websites

Release prepared on **26 October 2026 (Europe/Kyiv)** for GitHub Pages, with no paid services.

| Site | Prepared public address | Repository / publication branch |
|---|---|---|
| Alexander Romaskevich — founder | https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/ | `oromaskevic23-cmd/oromaskevic23-cmd` / `gh-pages` |
| IMPERIAL Core — ecosystem | https://oromaskevic23-cmd.github.io/IMPERIAL-Core-Public/ | `oromaskevic23-cmd/IMPERIAL-Core-Public` / `gh-pages` |

These are free GitHub Pages addresses on one `github.io` subdomain, with a separate project path for each site. They are not purchased custom domains. A prepared branch does not mean that Pages is enabled or that Google has indexed a URL. See [release status](REPORT.md) and [evidence](evidence/search-console.json).

Both sites have complete **English, Ukrainian, Russian, German, French, Spanish, Portuguese, Japanese, Chinese and Arabic** versions. English is at the site root; the other versions use `/uk/`, `/ru/`, `/de/`, `/fr/`, `/es/`, `/pt/`, `/ja/`, `/zh/`, `/ar/`. Arabic uses right-to-left layout. Language links work without JavaScript. The translations have not received independent native-speaker editorial review.

## Build and verify

Python 3.10+ and the standard library are sufficient; no package installation, account, build service or API key is required.

```sh
python3 websites/tools/build.py
python3 websites/tools/verify.py
python3 tools/verify_public_docs.py
```

`source/content.json` holds all copy and both canonical base URLs. `assets/` holds shared styles, a small menu enhancement and the original owner-published portrait. `founder/dist/` and `ecosystem/dist/` contain only public static files. The generator handles the GitHub repository prefix in navigation, assets, canonical URLs, JSON-LD and sitemaps. Each release has a SHA-256 publication manifest beside its `dist` directory.

## Enable the free addresses

Once the reviewed `gh-pages` branches exist, the repository owner can select **Settings → Pages → Build and deployment → Deploy from a branch → gh-pages → /(root) → Save** in each repository. Leave the custom-domain field empty; GitHub supplies the free address. Keep HTTPS enforced when available. No DNS purchase is needed.

- Founder Pages settings: https://github.com/oromaskevic23-cmd/oromaskevic23-cmd/settings/pages
- Ecosystem Pages settings: https://github.com/oromaskevic23-cmd/IMPERIAL-Core-Public/settings/pages

Only the matching `dist` directory belongs at the root of its publication branch. Keep the original default branch and Git history. Source changes remain in a Draft PR for review; publishing the prepared static branch does not require merging unrelated changes.

After GitHub finishes its deployment, run the public-byte verifier:

```sh
python3 websites/tools/verify_live.py
```

It requests each published HTML page and asset, compares the SHA-256 value with its manifest, checks root-level robots policies, and writes a dated result. It never reports Google indexing.

GitHub Pages controls HTTP response headers; Netlify `_headers` and `_redirects` files are intentionally absent. Project-level `robots.txt` files document the sitemap locations, but robots policy is governed by the origin-root `https://oromaskevic23-cmd.github.io/robots.txt`. Inspect that root policy after enabling Pages.

## Google Search Console

After the sites return the expected public content:

1. Open https://search.google.com/search-console using the founder's Google account.
2. Add each full site address from the table as a **URL-prefix** property. A `github.io` project site does not grant DNS ownership of `github.io`.
3. Use Google's HTML-file verification option: place the exact provided verification file in the matching publication branch. Alternatively add the exact Google-provided meta tag to the generator and rebuild. Never put passwords or account tokens into public source or chat.
4. Select Verify in Search Console. Preserve the verification file/tag afterward.
5. Submit `sitemap.xml` in each property. It contains all 10 locales, reciprocal language alternates and the unchanged portrait URL.
6. Inspect each English root plus the Ukrainian and Russian profiles. Run **Test live URL**; request indexing once for a new/changed key URL. Record Google's reported canonical, last crawl and actual indexing verdict.
7. Check Page indexing and Search performance after data becomes available. Record impressions, clicks, CTR and average position for the approved name/brand queries. A rich-results test or HTTP 200 is not an indexing verdict.

## Sources and limits

- [GitHub Pages availability and default URL format](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [GitHub Pages publishing-source settings](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Google ProfilePage documentation](https://developers.google.com/search/docs/appearance/structured-data/profile-page)
- [Google multilingual-page guidance](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Google image guidance](https://developers.google.com/search/docs/appearance/google-images)

The original ChatGPT-hosted reference websites are unchanged. No external profile, award, legal identifier, customer claim, market valuation or independent endorsement has been invented. The two unused Netlify project shells from the earlier preparation are not canonical destinations and have no deployment in this release.
