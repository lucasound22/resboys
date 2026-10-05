# RES BOYS — LIVE ECOM — READY FOR ORDERS

This build is GitHub Pages ready + Shopify Buy SDK + Stripe Checkout live.

## 1. Deploy to GitHub Pages (30 sec)
Upload `index.html` + `assets/` to your repo root > Settings > Pages > Deploy from main branch.

## 2. Choose your checkout mode

Open `index.html` and edit the top `LIVE_CONFIG` object:

### OPTION A: SHOPIFY (recommended for clothing)
You already have inventory management, sizes, AUD shipping.

1. Create Shopify store (res-boys.myshopify.com)
2. Shopify Admin > Products > Import > Upload `shopify_products.csv` (sample, then add all 19 products manually for best images)
3. Create custom app: Apps > Develop apps > Create app > Configure Storefront API > Enable all read scopes > Install > Copy Storefront Access Token
4. For each product, get Variant GID: In Shopify Admin, open product, right-click variant > inspect network, or use GraphQL. Easiest: Use Shopify's Storefront API explorer. Format `gid://shopify/ProductVariant/123456789`
5. Paste into `LIVE_CONFIG.shopify.variants` map in index.html
6. Set:
```
mode: 'shopify',
shopify: { domain: 'res-boys.myshopify.com', storefrontAccessToken: 'YOUR_TOKEN', variants: {...} }
```

Live checkout will redirect to Shopify's secure checkout (AUD, Apple Pay, etc). Orders appear in Shopify.

### OPTION B: STRIPE (fastest, no Shopify needed)
1. Stripe Dashboard > Payment Links > Create 19 links (one per product) OR use Worker for multi-item cart.
2. For multi-item cart (so customer can buy hoodie + cap together):
   - Deploy included `stripe-worker.js` to Cloudflare Workers:
     ```
     npm i -g wrangler
     wrangler login
     wrangler init res-boys-checkout
     // paste stripe-worker.js into src/index.js
     wrangler secret put STRIPE_SECRET_KEY (sk_live_...)
     wrangler deploy
     ```
   - Copy worker URL e.g. https://res-boys-checkout.yourname.workers.dev
   - Paste into `LIVE_CONFIG.stripe.checkoutWorkerUrl`
   - Set `mode: 'stripe'`

3. Optional: also paste per-product Payment Links into `paymentLinks` as fallback for single-item buys.

Stripe will handle AUD payments, shipping address collection (AU only), promotion codes.

## 2b. 15% popup + discount code (NEVERBLEND15)
- The popup (timed / exit-intent / scroll) unlocks code `NEVERBLEND15` and applies it to the cart automatically; shoppers can also type it in the cart.
- SHOPIFY: Admin > Discounts > Create > Discount code `NEVERBLEND15`, 15% off products, limit one use per customer. The site sends it via `?discount=` on the cart link.
- STRIPE: Dashboard > Product catalogue > Coupons > create a 15% coupon with ID `NEVERBLEND15`. The Worker applies it and checks it server-side.
- Email capture: paste a Formspree/Klaviyo/Mailchimp endpoint into `LIVE_CONFIG.newsletter.endpoint` (receives JSON `{email, source, consent}`). Without it the code still unlocks but emails are not stored.
- SHOPIFY variants: in `LIVE_CONFIG.shopify.variants` use either one variant ID per product, or per size: `hoodie_black: {S:'123', M:'456', L:'789', XL:'...', XXL:'...'}`.
- STRIPE: set Worker secrets `STRIPE_SECRET_KEY` and `ALLOWED_ORIGIN` (https://resboys.com.au). Prices live in `stripe-worker.js` (CATALOG) — change them there too if you change them on the site.

## 3. Go live checklist
- [ ] Update contact email in footer (crew@resboys.com.au)
- [ ] Replace demo ABN in footer
- [ ] Add real Instagram link
- [ ] Set shipping rates in Shopify/Stripe (Standard $10, Express $18, Free over $200)
- [ ] Review `policies.html` (14-day returns etc. are defaults — edit to match your real policy)
- [ ] Test order with 100% discount code or Stripe test card 4242 4242 4242 4242

## Files included
- index.html — production site with LIVE_CONFIG
- assets/ — vector (SVG) artwork: sharp at any resolution, named after Reservoir streets
- stripe-worker.js — Cloudflare Worker for Stripe Checkout Sessions
- shopify_products.csv — starter import (expand to 19 products)

All prices in AUD. Swap any SVG for real photography by keeping the same filename and updating the extension in index.html.

Never Blend In. Est. 2026


## Images (v4)
- Hero = four-guys crew shot (background softened, crew enlarged, extra cap brim removed, film grain added) (3200px + 1600px versions via srcset). Lookbook = Broadway couple. Popup = male portrait. Story = female portrait. Each photo is used once.
- Photos and product crops were upscaled with an AI super-resolution pass. For truly sharp results, export the originals at 2400px+ wide and drop them in `assets/` using the same filenames (hero_crew.jpg 3200w, hero_crew_1600.jpg 1600w, model_male.jpg, model_female.jpg, crew_broadway.jpg).
- The four detail tiles (detail_*.jpg) are rendered graphics of the RES BOYS logo, woven label, tab and postcode — not photographs. Replace them with real macro photos when you have them (same filenames).
- Product quick-view, size guide, FAQ, trust bar and Product schema (Google) are built in. Edit `LINES`, `DESC` and `DESC_BY_ID` in index.html to change product copy.


## v5 notes
- Product images are now consistent 4:5 studio-style packshots (soft grey seamless backdrop, contact shadow) generated from your lookbook pieces. They are as sharp as the source allows. For true ASOS-grade shots, re-shoot or re-generate each product at 1500px+ using `PHOTO_SHOT_LIST.md` and drop the files in `assets/` with the same names.
- Tracking: paste a GA4 ID and/or Meta Pixel ID in `LIVE_CONFIG.analytics` to track add_to_cart, begin_checkout and purchase.
- Sold out: add product ids to `LIVE_CONFIG.soldOut` and they show SOLD OUT with the button disabled.
- Sort (featured / price) and "Complete the look" cart suggestions are built in. The duplicate cap strip has been removed; caps live in the main grid.


## v6 notes
- Product shots rebuilt: crisp real logo placed on every garment (no more smudged lettering), bone hoodie cutout fixed, blotchy fabric smoothed, consistent studio backdrop.
- Menu/filter strip, trust bar, header and cards enlarged; the layout scales up on 1800px+ screens. Filter bar now sticks only while you're in the shop.
- Product cards: hover "quick add" with sizes on desktop; tap opens quick view on touch.


## v7 notes (final push)
- On-model photos: the site now supports male/female model images per product (gallery in quick view, hover swap on the grid). Prompts, filenames and the 3-step setup are in `PHOTO_SHOT_LIST.md`. No model photos are included — they need to be generated or shot.
- New: deep links (`index.html#p-hoodie_black` opens that product), Fit & sizing / Delivery & returns accordions, statement marquee, "Join the crew" signup band, scroll reveals, keyboard focus trapping in dialogs, `_headers` (security + caching for Netlify / Cloudflare Pages), `.nojekyll` for GitHub Pages.
- Tested end to end in test mode: add to cart, discount code, checkout form, order confirmation, deep link, crew signup.
