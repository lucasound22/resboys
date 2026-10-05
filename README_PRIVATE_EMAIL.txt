# RES BOYS — DROP 01 / SS26 — PRO STREET BUILD + PRIVATE ORDER EMAIL

Design inspired by Lids (hat wall), Nike (tech), Elite 11 / Geedup / StreetX / HoMie (Melbourne street)

## LIVE MODE — Option B (Stripe) — How orders go to lucasound@gmail.com PRIVATELY

Your private email NEVER appears on the website. Footer still shows crew@resboys.com.au.

### Two workers (both hide your email):

1. **order-email-worker.js** — for manual/demo orders
   - Deploy to Cloudflare Workers: wrangler init res-boys-orders
   - No secrets needed (uses MailChannels free email)
   - Copy URL e.g. https://res-boys-orders.yourname.workers.dev
   - Paste into index.html LIVE_CONFIG.stripe.orderEmailWorkerUrl

2. **stripe-worker.js** — for real Stripe payments + email you
   - Deploy: wrangler init res-boys-checkout
   - wrangler secret put STRIPE_SECRET_KEY (sk_live_...)
   - wrangler deploy
   - Copy URL into LIVE_CONFIG.stripe.checkoutWorkerUrl
   - Set LIVE_CONFIG.mode = 'stripe'

When customer checks out:
- If Stripe worker URL set → creates Stripe Checkout Session + emails you at lucasound@gmail.com with items, customer name/email/address/shipping + Stripe session link
- If only orderEmailWorkerUrl set → demo checkout still emails you the order for manual processing
- If neither set → demo confirmation only (no email)

### GitHub Pages deploy:
Upload index.html + assets/ to repo root → Settings → Pages → Deploy main branch.

### Stripe Dashboard:
All payments appear in Stripe Dashboard. Email notification gives you head start to pack.

Never Blend In. Reservoir 3073.
