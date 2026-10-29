# Google Founder Recognition — October 26, 2026

**Founder:** Alexander Romaskevich · RomaskevicH

**Project:** IMPERIAL Core | Source: public GitHub Pages.  
**Authority:** owner-directed SEO verification and public first-party links; no fabricated index/search rank claims.

## Two exact official URL-prefix properties

1. **Personal profile:** https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/
2. **IMPERIAL Core:** https://oromaskevic23-cmd.github.io/IMPERIAL-Core-Public/

These share `oromaskevic23-cmd.github.io` as a hostname but are independently publishable site paths. They are **not owned custom DNS domains**. Use two **URL-prefix** properties in Google Search Console, never a DNS *Domain property* purporting to own all `github.io`.

Google Search Console: https://search.google.com/search-console/welcome

Official Google setup: https://support.google.com/webmasters/answer/34592?hl=en
Official HTML ownership verification: https://support.google.com/webmasters/answer/9008080?hl=en

## Actual public technical checks performed 2026-10-26

| Check | Founder website | IMPERIAL Core website |
| --- | --- | --- |
| Public home page | EXTERNALLY_FETCHABLE | EXTERNALLY_FETCHABLE |
| EN, UK, RU, DE, FR, ES, PT, JA, ZH, AR | 10/10 | 10/10 |
| Per-language self-canonical matches URL | 10/10 PASS | 10/10 PASS |
| Alternate `hreflang` 10 languages + `x-default` | 10/10 PASS | 10/10 PASS |
| JSON-LD Person + Organization | 10/10 PASS, parses | 10/10 PASS, parses |
| Explicit meta robots `noindex` | None observed | None observed |
| `sitemap.xml` in GitHub Pages branch | PRESENT, 10 `<loc>` items | PRESENT, 10 `<loc>` items |
| `robots.txt` in site repository | PRESENT, `Allow: /`, `Sitemap` | PRESENT, `Allow: /`, `Sitemap` |
| Site ownership in Google account | **NOT_VERIFIED** | **NOT_VERIFIED** |
| Sitemap submitted inside GSC | **NOT_VERIFIED** | **NOT_VERIFIED** |
| URL Inspection / indexing request | **NOT_VERIFIED** | **NOT_VERIFIED** |
| Google search indexed/ranking | **NOT_VERIFIED** | **NOT_VERIFIED** |

The per-repository robots.txt files sit under project subpaths on a shared host: crawlers typically load the *host-root* robots.txt, so do not assume a project-path `robots.txt` is a host-level crawl control. This is why explicit GSC sitemap submission matters.

### Exact sitemap URLs

- https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/sitemap.xml
- https://oromaskevic23-cmd.github.io/IMPERIAL-Core-Public/sitemap.xml

These contain EN + nine language variants, including hreflang and the original founder portrait's absolute image URL.

## Owner-authenticated GSC actions required

The currently connected ChatGPT tools have access to the GitHub source **but not an authenticated Google Search Console ownership/write session**. Therefore, nothing here claims that a property has been verified, a sitemap submitted to Google, or indexing requested.

1. Sign into https://search.google.com/search-console/welcome with the Google account that will own the sites.
2. Add **URL-prefix**, paste **exact first URL**, including HTTPS and final slash. Choose **HTML tag verification**. Copy the unique `google-site-verification` meta tag issued for this account.
3. Add this tag unchanged to the live `gh-pages/index.html` `<head>` of the **profile** repository, or to its upstream build source so the tag survives redeploy. Publish, verify its presence on the live root, then click **Verify** in Google.
4. Repeat steps 2–3 for the **IMPERIAL Core** URL-prefix and its `gh-pages/index.html`.
5. In each now-owned property open **Indexing → Sitemaps** and submit that property's `sitemap.xml` URL. Google sitemap submission assists discovery but does not guarantee indexing.
6. In each property, use **URL Inspection** for `/`, `/ru/` and `/uk/`. If eligible, select **Request Indexing**. Do not repeatedly press Request Indexing; Google has quotas and no guaranteed speed.
7. In **Pages / Indexing** and **Performance** verify actual discovered/Google-selected canonical, index status, impressions and pages appearing for the distinct person strings.

**Important:** The unique Search Console meta tag is issued by Google and cannot be invented. Store tokens through the owner account; it is okay for the issued public verification HTML tag itself to be embedded in the public site's page head, but never publish Google account credentials or OAuth refresh tokens.

## Public GitHub cross-links completed

The profile README and IMPERIAL Core README now link both exact sites from `main`. The same two links are published in the main README of CONSTRUCTOR-AI, VELION-LLM-Public, HANTER, CYBER-HAK-Public, Nano-Core-Agents-Public and ORION-Public. Source-content claims are role designations and public project authorship, not external government/business registration proof.

## Search query watch list

- `"Alexander Romaskevich" "RomaskevicH"`
- `Russian-language founder-name variant + "IMPERIAL Core"`
- `Ukrainian-language founder-name variant + "IMPERIAL Core"`
- `site:oromaskevic23-cmd.github.io/oromaskevic23-cmd/`
- `site:oromaskevic23-cmd.github.io/IMPERIAL-Core-Public/`

A Google `site:` operator response is only indicative; authoritative indexing details require authenticated Search Console, and a temporarily missing public snippet does not prove the URL is permanently excluded.

**Current conclusion (2026-10-26):** `PUBLISHED_AND_CRAWLABLE_SOURCE_VERIFIED`; `GOOGLE_OWNER_VERIFIED=NOT_VERIFIED`; `SITEMAP_SUBMITTED=NOT_VERIFIED`; `INDEXING=NOT_VERIFIED`.
