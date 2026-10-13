# 73 — LIVE ECOM — READY FOR ORDERS

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
- STRIPE: set Worker secrets `STRIPE_SECRET_KEY` and `ALLOWED_ORIGIN` (https://shop73.com.au). Prices live in `stripe-worker.js` (CATALOG) — change them there too if you change them on the site.

## 3. Go live checklist
- [ ] Update contact email in footer (crew@shop73.com.au)
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
- The four detail tiles (detail_*.jpg) are rendered graphics of the 73 logo, woven label, tab and postcode — not photographs. Replace them with real macro photos when you have them (same filenames).
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


## v8 — Track 73 (new line)
- 6 new products: Broadway / Dundas / Darebin Track Jackets and Henty / Gilbert / Ruthven Track Pants, in Black/Rose, Black/Bone and Olive/Bone. Prices ($169.95 jacket, $129.95 pant) and names are suggestions — edit `PRODUCTS` in index.html, `CATALOG` in stripe-worker.js and the CSV together.
- New: Track 73 banner, filter, "ADD THE FULL SET" button in quick view (adds jacket + pant in the same size), on-model gallery.
- IMPORTANT: Black/Bone and Olive/Bone images are recolours of the one design photo. Swap in real photos of the made samples before selling those colourways.
- `shopify_products.csv` was rebuilt from scratch: all 25 products, every size, SKUs and image rows (the old file only had 10 products). Check Product Category values against your Shopify taxonomy when importing.
- Shopify: add the new ids and their size variant IDs to `LIVE_CONFIG.shopify.variants`.


## v9 — shop redesign + track jacket logo
- Track jacket: the chest patch is gone. 73 now sits evenly across the front ("RES" left, "BOYS" right) with the zip running straight through the middle, and the chevrons meet in a clean V at the zip. Done by editing your photo, so it is a digital edit, not a photo of a real garment — confirm the sample matches before selling.
- Shop grid rebuilt in an ASOS-style layout: smaller 4:5 cards (6 across on desktop, 2 on mobile), no borders, compact name / price / colour, hover quick-add, heart-to-save with a "Saved" filter (kept in the browser).
- Performance: grid loads 500px thumbnails (`*_s.jpg`) and the full image only in quick view. If you replace a product photo, also replace its `_s.jpg` (500 x 625).
- Track pant cards now crop to the pants; jackets crop to the jacket and logo.


## v10 — rebrand to "73"
- Brand is now **73**. New logo: a stylised 73 (sliced and offset, no zip line). Files: `assets/logo_white.png`, `assets/logo_black.png`; full brand pack (SVG, PNG, lockups) in `brand/`.
- Every garment image carries the street name in small lettering centred under a big 73 (e.g. HENTY / 73). The tracksuit is the **Edwardes Tracksuit** (Edwardes Lake, Reservoir): jacket has a big 7 | 3 split by the real zip with EDWARDES under it.
- New **Originals** line: original RES BOYS logo + small 73 in oxblood (hoodie and snapback). Prices ($149.95 / $59.95) are suggestions.
- New sections: **Shop the 73** (illustrated Reservoir street map, each pin lists the pieces named after that street), **The 73 Code** (7 rules, 3 promises — edit these to promises you can keep).
- Lifestyle photos and the hero had their printed lettering replaced with 73 digitally. Real garments must match before you sell.

## Trust, safety and legal (web-safe checklist)
- Pages: shipping, returns, privacy, terms of sale, cookies, contact, size guide, about. They are Australian-law based DRAFTS — have them reviewed by a lawyer before launch and fill in the [bracketed] business details (legal name, ABN) in `tools/build_seo.py` (BIZ block), then run `python3 tools/build_seo.py`.
- Cookie consent banner appears only when you set GA4 / Meta Pixel IDs; analytics never load until the visitor accepts.
- Checkout assurance text, payment badges, HTTPS reminder, `.well-known/security.txt`, security headers in `_headers`.
- Still your job: HTTPS on your host (GitHub Pages / Netlify / Cloudflare all provide it), Stripe or Shopify live keys, a monitored crew@ email, real business details.

## SEO
- `tools/build_seo.py` generates 27 product pages (`products/`), 7 category pages (`hoodies.html`, `caps.html`, `tracksuits.html` …), `sitemap.xml` (with image entries), `robots.txt`, and structured data (Product with price, shipping and 14-day return policy; Organization; WebSite; Breadcrumbs; ItemList).
- Set `DOMAIN` at the top of `tools/build_seo.py` (and find/replace `shop73.com.au` in `index.html`) to your real domain, then rebuild.
- Titles / descriptions target "73 Melbourne streetwear", Reservoir 3073, hoodies, caps, tracksuits. "Streetware" (the alternate spelling) appears in the meta description, keywords and the about text.
- After launch: add the site in Google Search Console, submit `sitemap.xml`, create a Google Business Profile only if you have a public address, and keep Instagram @73reservoir (placeholder) consistent.


## v11 — unified seal, colour families, esoteric voice
- Logo: the 73 is now one fused symbol inside a ring (the "seal") with no lettering. The wordmark (fused 73 alone) is `assets/logo_white.png` / `logo_black.png`; the seal is `assets/seal_white.png` / `seal_black.png`. Brand pack in `brand/`.
- On clothes the seal is small and subtle with the product name in tiny lettering beneath. Tracksuit seal sits just under the left collar.
- One name per product type: all caps = Henty Snapback, all hoodies = Gilbert Hoodie, all tees = Plenty Tee. Colours are variants, shown as swatches on one card (like White Fox / ASOS). Colour filter, sort and saved items are built in.
- Tracksuit: Edwardes Track Jacket / Pant / Short in Rose, Ice, Bone, Olive, Oxblood (short in 3). Card images show tops only / bottoms only; the full model photo is in the gallery.
- Bottoms redesigned: cargos removed. New Edwardes track shorts, a garment-washed Broadway sweatshort, and the Lakeside jogger.
- Darebin is gone as a name. Copy is now esoteric (no Reservoir wording); the street map was replaced by "The Spread" — draw a cap, a layer and a ground, lock what you like, add all three to the cart.
- Hero is graded sepia-grey with subtle seals. Product sources were re-extracted with a higher-quality upscaler (EDSR) — still limited by the original small crops; real photography is the only way to reach full ASOS quality.
- White Fox research: Australian online fashion label built on a staple (hoodies), many colours per style, granular filters, "you may also like" and fast-shipping clarity. Applied here: colour families, colour filter, related items, shipping clarity. Not copied: influencer-driven fast-fashion tactics.
- Shopify CSV is now one product per style with Colour x Size variants.
