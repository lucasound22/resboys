// RES BOYS — Stripe Checkout Worker (Cloudflare Workers)
// Prices are defined HERE, server-side. The browser only sends {id, size, qty} so nobody can edit a price in dev tools.
// Setup:
//   wrangler secret put STRIPE_SECRET_KEY        (sk_live_...)
//   wrangler secret put ALLOWED_ORIGIN           (https://resboys.com.au)
//   Stripe Dashboard > Products > Coupons: create a 15% coupon with ID  NEVERBLEND15  (or set PROMO_COUPON_ID)
const CATALOG = {
  cap_black:['HENTY SNAPBACK — Black',5995], cap_charcoal:['RUTHVEN SNAPBACK — Charcoal',5995], cap_olive:['EDWARDES SNAPBACK — Olive',5995], cap_white:['DUNDAS SNAPBACK — White',5995],
  hoodie_black:['GILBERT HOODIE — Black',14995], hoodie_charcoal:['BROADWAY HOODIE — Charcoal',14995], hoodie_olive:['DAREBIN HOODIE — Olive',14995], hoodie_bone:['SUMMERHILL HOODIE — Bone',14995], hoodie_back_black:['CUTHBERT HOODIE — Black, Large Back Print',14995],
  tee_black:['PLENTY TEE — Black',6995], tee_charcoal:['CHEDDAR TEE — Charcoal',6995], tee_olive:['MERRI TEE — Olive',6995], tee_white:['HIGH ST TEE — White',6995],
  jacket_work:['SETTLEMENT WORK JACKET — Black',19995], vest_puffer:['BOLDREWOOD PUFFER — Black',18995],
  pants_cargo_black:['DUNDAS CARGO — Black',13995], pants_joggers_charcoal:['LAKESIDE JOGGER — Charcoal',12995], shorts_cargo_olive:['MERRI CARGO SHORT — Olive',10995], shorts_black:['BROADWAY SHORT — Black',8995],
};
const SIZES = ['One Size','S','M','L','XL','XXL'];
const PROMO = { code: 'NEVERBLEND15', percent: 15 };
const FREE_SHIP_OVER = 20000; // cents, applied AFTER discount

export default {
  async fetch(request, env) {
    const cors = corsHeaders(env);
    if (request.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (request.method !== 'POST') return new Response('RES BOYS Checkout Worker', { headers: cors });
    try {
      const { items, discount_code, success_url, cancel_url } = await request.json();
      if (!Array.isArray(items) || !items.length || items.length > 30) return json({ error: 'Invalid cart' }, 400, cors);
      if (env.ALLOWED_ORIGIN && (!success_url || new URL(success_url).origin !== env.ALLOWED_ORIGIN)) return json({ error: 'Bad origin' }, 400, cors);

      let subtotal = 0;
      const p = new URLSearchParams({ mode: 'payment', success_url, cancel_url, 'phone_number_collection[enabled]': 'true', 'shipping_address_collection[allowed_countries][0]': 'AU' });
      items.forEach((it, i) => {
        const row = CATALOG[it.id]; const qty = Math.floor(Number(it.qty));
        if (!row || !(qty >= 1 && qty <= 10) || !SIZES.includes(it.size)) throw new Error('Invalid item');
        subtotal += row[1] * qty;
        p.set(`line_items[${i}][price_data][currency]`, 'aud');
        p.set(`line_items[${i}][price_data][unit_amount]`, String(row[1]));
        p.set(`line_items[${i}][price_data][product_data][name]`, `${row[0]} [${it.size}]`);
        p.set(`line_items[${i}][price_data][product_data][images][0]`, new URL(`assets/${it.id}.jpg`, success_url).toString());
        p.set(`line_items[${i}][quantity]`, String(qty));
      });

      let net = subtotal;
      if (discount_code && String(discount_code).toUpperCase() === PROMO.code) {
        net = subtotal - Math.round(subtotal * PROMO.percent / 100);
        p.set('discounts[0][coupon]', env.PROMO_COUPON_ID || PROMO.code);
      } else {
        p.set('allow_promotion_codes', 'true');
      }

      const ship = net > FREE_SHIP_OVER ? [['Free shipping', 0]] : [['Standard (3-5 days)', 1000], ['Express (1-2 days)', 1800]];
      ship.forEach(([name, amt], i) => {
        p.set(`shipping_options[${i}][shipping_rate_data][type]`, 'fixed_amount');
        p.set(`shipping_options[${i}][shipping_rate_data][display_name]`, name);
        p.set(`shipping_options[${i}][shipping_rate_data][fixed_amount][amount]`, String(amt));
        p.set(`shipping_options[${i}][shipping_rate_data][fixed_amount][currency]`, 'aud');
      });

      const res = await fetch('https://api.stripe.com/v1/checkout/sessions', {
        method: 'POST',
        headers: { Authorization: `Bearer ${env.STRIPE_SECRET_KEY}`, 'Content-Type': 'application/x-www-form-urlencoded' },
        body: p,
      });
      const session = await res.json();
      if (session.error) return json({ error: session.error.message }, 400, cors);
      return json({ url: session.url, id: session.id }, 200, cors);
    } catch (e) {
      return json({ error: e.message }, 400, cors);
    }
  },
};
function corsHeaders(env) { return { 'Access-Control-Allow-Origin': env.ALLOWED_ORIGIN || '*', 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' }; }
function json(d, s, h) { return new Response(JSON.stringify(d), { status: s, headers: { 'Content-Type': 'application/json', ...h } }); }
