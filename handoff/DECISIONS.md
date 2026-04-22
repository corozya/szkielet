# Key Project Decisions

**Last Updated:** 2026-04-21

---

## Decision 1: Target Audience

**Decided:** Software Houses (not end-users directly)

**Why:**
- Real market need: SH struggle with client communication and trust
- Better business model: per-project fees scale better than per-user
- Larger deal size: SH manages 10-50+ projects
- Revenue alignment: SH benefits = we benefit

---

## Decision 2: Revenue Model

**Decided:** Per-Project SaaS fees (not per-user, not per-feature)

**Why:**
- Aligns with how SH operate (projects = clients)
- Easy to understand for customer
- Predictable recurring revenue
- Scales as customer grows

---

## Decision 3: MVP Integrations

**Decided:** Start with Kanboard + Email (not 11 adapters)

**Why:**
- Kanboard: ~40% of self-hosted teams use it
- Email: Works everywhere, no integration complexity
- Delivery risk: 2 integrations = doable in 6-8 weeks
- More is not better: Start small, add by demand

---

## Decision 4: Marketing Message

**Decided:** Focus on financial ROI + ecosystem (not just "easier bug reporting")

**Why:**
- Real pain: Dev wastes 2-3 hours on info gathering per bug
- Real money: 50 clients × 2.5h saved = 125h/month = thousands saved
- SH understands: "Your developers will spend less time on support questions"
- Emotional layer: "Your clients will feel cared for" = retention

---

## Decision 5: Desktop First, Browser Support

**Decided:** Chrome, Firefox, Edge, Safari (desktop only for MVP)

**Why:**
- Covers 95%+ of desktop market
- Mobile Phase 3 (lower priority)
- Faster MVP delivery
- Store employees primarily use desktop

---

## Decision 6: Deployment Model

**Decided:** Full SaaS (We Host) — **TEMPORARY**
- MVP Launch: SaaS-only (us hosting, recurring fees)
- Pending: Validate market fit before investing in infrastructure
- Future: Can pivot to Hybrid (OSS + managed tier) in Phase 2 if market prefers

**Why:**
- Simpler MVP scope (no Docker/open source docs overhead)
- Clear revenue model (recurring SaaS fees)
- Plan to validate with beta customers before committing to ops burden

---

## Decision 7: Pricing Structure

**Decided (Temporary):** $20/month per project
- Example: SH with 50 projects = $1,000/month recurring
- Justification: Midpoint between conservative ($10) and premium ($29)
- Allows volume discounts later (5+ projects = discount)
- **Will validate with first 3-5 beta customers**

**Pending Research:**
- Competitor pricing (BugHerd $42/mo, Marker.io $99/mo)
- Customer willingness-to-pay survey
- Discount structure for high-volume SH

---

## Decision 8: First Customer Targets

**Decided (Temporary):** Beta testers = Anyone interested
- Not restricting to industry vertical yet
- Goal: Validate core hypothesis (does tool solve real problem?)
- Plan: 3-5 beta SH partners, measure actual time saved

**Pending Research:**
- E-commerce vs web agencies — which has bigger pain?
- Geographic focus (EU-first vs global?)
- Niche positioning (which SH vertical has most traction?)

---

## MVP Launch Readiness Checklist

**Code Quality:**
- ✅ Add HTTP timeouts to all adapters
- ✅ Add unit tests for 7 integrations
- ✅ Verify webhook secret_token encryption in DB

**Deployment Preparation:**
- ⏳ Choose hosting (AWS, DigitalOcean, Vercel?)
- ⏳ Setup payment processing (Stripe, Paddle?)
- ⏳ Privacy policy + ToS templates
- ⏳ Customer onboarding flow (emails, docs, video?)

**Go-to-Market:**
- ⏳ Beta customer outreach (who do you know?)
- ⏳ Pricing page + docs
- ⏳ Launch announcement (ProductHunt? Twitter?)
- ⏳ Support channel setup

---

## Assumptions to Validate

✓ SH actually waste 2-3 hours per bug on info gathering
✓ Kanboard covers enough of the market
✓ Email routing is reliable enough for MVP
✓ Extension is easy enough for store employees to use
✓ SH would pay for this tool

---

## Next Steps

1. Build MVP (backend + extension)
2. Find 3-5 beta SH partners
3. Validate assumptions with real usage
4. Measure actual time saved (not theoretical)
5. Decide Phase 2 integrations based on feedback

---

## Decision 9: Alternative Feedback Submission (Mobile)

**Decided:** Start with in-app feedback form (web) first; mobile-friendly/PWA/public links deferred.

**Why:**
- Lowest scope / fastest delivery (no extension required)
- Immediate value for admins who want to submit feedback manually
- Mobile approach needs product validation (PWA vs public link vs responsive-only) before committing
