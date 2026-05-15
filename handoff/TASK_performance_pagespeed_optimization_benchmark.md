# TASK: PageSpeed Performance & SEO Optimization

## Status
- **Priority:** High
- **Type:** Performance / SEO
- **Created:** 2026-05-14
- **Last Benchmark:**
    - Mobile: **64/100** (LCP: 8.6s, FCP: 3.0s, TBT: 220ms, SI: 3.9s)
    - Desktop: **76/100** (LCP: 2.2s, FCP: 0.8s, TBT: 280ms, SI: 1.4s)

## Context
Initial PageSpeed Insights audit revealed critical performance bottlenecks on mobile, specifically a very high Largest Contentful Paint (LCP) of 8.6s. SEO audit also flagged an invalid `robots.txt` file.

## Requirements

### 1. Performance (Critical)
- [ ] **Improve LCP on Mobile:** Goal < 2.5s. Identify what is causing the 8.6s delay (likely heavy images or late-discovered hero element).
- [ ] **Eliminate render-blocking resources:** Focus on reducing the impact of CSS/JS that blocks initial paint (~730ms potential gain on mobile).
- [ ] **Optimize Image Delivery:** Improve compression and use modern formats (WebP/AVIF). Savings estimated at ~280 KiB.
- [ ] **Reduce Unused JavaScript:** Identify and split/lazy-load JS bundles. ~180 KiB estimated savings.

### 2. SEO
- [ ] **Fix robots.txt:** PageSpeed reports 1 error. Likely due to non-standard `Content-Signal` directives or formatting issues in the Cloudflare-managed section.
- [ ] **Verify Sitemap integrity:** Ensure all critical pages are present and returning 200 OK.

### 3. Accessibility
- [ ] **Fix color contrast:** Address "Kolory tła i pierwszego planu mają niewystarczający współczynnik kontrastu".
- [ ] **Improve link identification:** Ensure links are distinguishable not only by color.

### 4. Verification
- [ ] Run PageSpeed Insights again and document the new scores.
- [ ] Verify `robots.txt` using Google Search Console "Robots Testing Tool" (if available).

## Implementation Notes
- The `robots.txt` seems to be managed/injected partly by Cloudflare but also contains manual entries.
- LCP of 8.6s on mobile suggests a major bottleneck, possibly a large background image or a heavy blocking script before the main content renders.
- Speed Index of 3.9s on mobile is also high, indicating the "visual completion" is slow.

## Reference
- Audit URL: https://pagespeed.web.dev/analysis/http-reczniki-haftowane-pl/i7kjzo8iz4
