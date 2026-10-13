#!/usr/bin/env python3
"""73 — builds the static SEO / trust pages from index.html's PRODUCTS list.
Run from the site folder after changing products, prices or business details:   python3 tools/build_seo.py
Edit DOMAIN and BIZ below (they appear on every generated page, in the sitemap and in structured data)."""
import re, os, html, datetime
DOMAIN = 'https://shop73.com.au'          # <- your real domain
BIZ = dict(trading='73', legal='[add your legal / trading name]', abn='[add your ABN]', email='crew@shop73.com.au',
           place='Melbourne VIC, Australia', insta='https://instagram.com/73official', response='1–2 business days')
TODAY = '2026-10-07'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s):
    full = os.path.join(ROOT, p); os.makedirs(os.path.dirname(full), exist_ok=True); open(full, 'w', encoding='utf-8').write(s)
E = html.escape
idx = rd('index.html')
prods = [dict(id=a, name=b, variant=c, category=d, group=e, price=float(f), img=g, tag=h) for a, b, c, d, e, f, g, h in
         re.findall(r"\{id:'(\w+)', name:'([^']+)', variant:'([^']+)', category:'(\w+)', group:'([^']+)', price:([\d.]+), img:'([^']+)', tag:'([^']*)'\}", idx)]
def block(name):
    m = re.search(r'const %s=\{(.*?)\};' % name, idx, flags=re.S); return dict(re.findall(r"(\w+):'((?:[^'\\]|\\.)*)'", m.group(1))) if m else {}
DESC_ID, DESC_CAT, FIT = block('DESC_BY_ID'), block('DESC'), block('FIT')
LINES = block('LINES')
def catkey(c): return {'caps': 'cap', 'hoodies': 'hoodie', 'tees': 'tee', 'jackets': 'jacket'}.get(c, 'bottom')
def desc(p): return DESC_ID.get(p['id']) or DESC_CAT.get(catkey(p['category']), '')
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def purl(p): return 'products/%s-%s.html' % (slug(p['name']), slug(p['variant']))
MODEL = {}
m = re.search(r'modelShots: \{(.*?)\},\n', idx, flags=re.S)
if m:
    for k, v in re.findall(r"(\w+): \[(.*?)\]", m.group(1)): MODEL[k] = re.findall(r"'([^']+)'", v)
GROUPS = {'TRACKSUITS': ('tracksuits', 'Tracksuits', 'Melbourne streetwear tracksuits — chevron track jackets, pants and shorts', "The Edwardes Tracksuit is 73's matching track jacket, pant and short. A matching track jacket, pant and short with chevron panels and contrast stripes, in five colours."),
          'ORIGINALS': ('originals', 'Originals', 'The original RES BOYS hoodie and snapback in oxblood', 'Before 73 there was RES BOYS. The Originals line brings the first design back in a new colour — oxblood — with a small 73 beneath it.'),
          'CAPS': ('caps', 'Caps', 'Melbourne streetwear snapbacks — flat-brim caps', 'Structured flat-brim snapbacks from Melbourne streetwear brand 73, marked with a small 73 seal and a name in tiny lettering beneath it. Four colours.'),
          'HOODIES': ('hoodies', 'Hoodies', 'Heavyweight oversized streetwear hoodies — Melbourne', 'Heavyweight, oversized hoodies from Melbourne streetwear brand 73. One hoodie, five colourways, a small 73 seal on the chest or across the back.'),
          'T-SHIRTS': ('tees', 'T-Shirts', 'Streetwear t-shirts — Melbourne', 'Regular-fit streetwear tees from 73 in Melbourne, with a small 73 seal on the chest. Four colours.'),
          'JACKETS & VESTS': ('jackets', 'Jackets & Vests', 'Work jackets and puffer vests — Melbourne streetwear', 'The Settlement work jacket and Boldrewood puffer vest — layering pieces cut to sit over a hoodie.'),
          'BOTTOMS': ('bottoms', 'Bottoms', 'Joggers and sweatshorts — Melbourne streetwear', 'Relaxed joggers and garment-washed sweatshorts from Melbourne streetwear brand 73.')}
CSS = """*{box-sizing:border-box}body{margin:0;font-family:'Instrument Sans',system-ui,sans-serif;background:#fafaf7;color:#0a0a0a;line-height:1.6}a{color:inherit}
header{display:flex;align-items:center;justify-content:space-between;padding:16px 28px;border-bottom:1px solid #0a0a0a;background:#fafaf7;position:sticky;top:0;z-index:5}
header img{height:38px;width:auto;display:block}nav{display:flex;gap:26px;font-family:'Space Mono',ui-monospace,monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:700}nav a{text-decoration:none}
main{max-width:980px;margin:0 auto;padding:48px 24px 80px}main.wide{max-width:1400px}h1{font-family:'Anton',Impact,'Arial Black',sans-serif;font-weight:400;font-size:clamp(40px,6vw,76px);line-height:.95;margin:0 0 18px;text-transform:uppercase}
h2{font-family:'Anton',Impact,'Arial Black',sans-serif;font-weight:400;font-size:28px;margin:40px 0 8px;text-transform:uppercase}p,li{font-size:16px;max-width:72ch}.mono{font-family:'Space Mono',ui-monospace,monospace;font-size:12px;letter-spacing:.08em;opacity:.7}
.crumbs{font-family:'Space Mono',monospace;font-size:11px;letter-spacing:.1em;opacity:.65;margin-bottom:18px}.crumbs a{text-decoration:underline}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:26px 14px;margin-top:28px}.card{text-decoration:none;display:block}.card img{width:100%;aspect-ratio:4/5;object-fit:cover;background:#eeede9;display:block}.card b{display:block;margin-top:10px;font-size:14px;text-transform:uppercase;letter-spacing:.03em}.card span{font-size:13px;opacity:.65}
.pdp{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}.pdp img{width:100%;background:#eeede9;display:block}.imgs{display:grid;gap:10px}.price{font-size:24px;font-weight:700;margin:6px 0 14px}
.btn{display:inline-block;background:#0a0a0a;color:#fafaf7;padding:18px 30px;font-family:'Space Mono',monospace;font-size:13px;font-weight:700;letter-spacing:.1em;text-decoration:none;margin:10px 0}.btn:hover{background:#333}
table{border-collapse:collapse;width:100%;max-width:720px;margin:12px 0}td,th{border:1px solid #0a0a0a;padding:10px 12px;text-align:left;font-size:15px}th{background:#eeede9}
footer{border-top:1px solid #0a0a0a;padding:36px 28px;background:#0a0a0a;color:#fafaf7;font-size:14px}footer .cols{display:flex;gap:48px;flex-wrap:wrap;margin-bottom:22px}footer ul{list-style:none;margin:8px 0 0;padding:0;display:grid;gap:6px}footer a{text-decoration:underline}footer small{opacity:.6;display:block;line-height:1.6}
@media(max-width:800px){.pdp{grid-template-columns:1fr}nav{gap:14px;font-size:11px}header{padding:12px 16px}}"""
def page(path, title, desc, body, schema='', og_img='assets/og_image.jpg', depth=0, wide=False, noindex=False):
    up = '../' * depth; canon = DOMAIN + '/' + path
    nav = [('Shop', 'index.html#shop'), ('Tracksuits', 'tracksuits.html'), ('About', 'about.html'), ('Contact', 'contact.html')]
    h = f"""<!DOCTYPE html><html lang="en-AU"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{canon}">{'<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'}
<meta property="og:type" content="website"><meta property="og:site_name" content="73"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMAIN}/{og_img}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{up}assets/favicon.png"><link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png"><meta name="theme-color" content="#0a0a0a">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Anton&family=Instrument+Sans:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style>{schema}</head><body>
<header><a href="{up}index.html" aria-label="73 home"><img src="{up}assets/logo_black.png" alt="73"></a><nav aria-label="Main">{''.join(f'<a href="{up}{u}">{n}</a>' for n, u in nav)}</nav></header>
<main{' class="wide"' if wide else ''}>{body}</main>
<footer><div class="cols"><div><b>Help</b><ul><li><a href="{up}shipping.html">Shipping &amp; delivery</a></li><li><a href="{up}returns.html">Returns &amp; exchanges</a></li><li><a href="{up}size-guide.html">Size guide</a></li><li><a href="{up}contact.html">Contact us</a></li></ul></div>
<div><b>Legal</b><ul><li><a href="{up}privacy.html">Privacy policy</a></li><li><a href="{up}terms.html">Terms of sale</a></li><li><a href="{up}cookies.html">Cookies</a></li></ul></div>
<div><b>Shop</b><ul><li><a href="{up}tracksuits.html">Tracksuits</a></li><li><a href="{up}hoodies.html">Hoodies</a></li><li><a href="{up}caps.html">Caps</a></li><li><a href="{up}originals.html">Originals</a></li></ul></div></div>
<small>© 2026 {BIZ['trading']} — Melbourne streetwear. {E(BIZ['legal'])} · ABN {E(BIZ['abn'])} · {E(BIZ['place'])}<br>All prices in AUD and include GST where applicable. Payments are processed securely by Stripe / Shopify — we never see or store your card details.</small></footer></body></html>"""
    wr(path, h)
def ld(obj):
    import json; return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'
def crumbs(items, depth=0):
    up = '../' * depth; return '<div class="crumbs">' + ' / '.join(f'<a href="{up}{u}">{E(n)}</a>' if u else E(n) for n, u in items) + '</div>'
def bl(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': DOMAIN + '/' + u} for i, (n, u) in enumerate(items)]}
# ---------------- product pages
def product_ld(p):
    url = DOMAIN + '/' + purl(p); imgs = [DOMAIN + '/' + p['img']] + [DOMAIN + '/assets/' + x for x in MODEL.get(p['id'], [])]
    return {'@context': 'https://schema.org', '@type': 'Product', 'name': f"{p['name'].title()} — {p['variant']}", 'image': imgs, 'description': desc(p), 'sku': p['id'], 'mpn': p['id'], 'color': p['variant'],
            'brand': {'@type': 'Brand', 'name': '73'}, 'category': 'Apparel & Accessories',
            'offers': {'@type': 'Offer', 'url': url, 'priceCurrency': 'AUD', 'price': '%.2f' % p['price'], 'itemCondition': 'https://schema.org/NewCondition', 'availability': 'https://schema.org/InStock', 'priceValidUntil': '2027-06-30',
                       'seller': {'@type': 'Organization', 'name': '73'},
                       'shippingDetails': {'@type': 'OfferShippingDetails', 'shippingRate': {'@type': 'MonetaryAmount', 'value': '10.00', 'currency': 'AUD'}, 'shippingDestination': {'@type': 'DefinedRegion', 'addressCountry': 'AU'},
                                           'deliveryTime': {'@type': 'ShippingDeliveryTime', 'handlingTime': {'@type': 'QuantitativeValue', 'minValue': 1, 'maxValue': 2, 'unitCode': 'DAY'}, 'transitTime': {'@type': 'QuantitativeValue', 'minValue': 3, 'maxValue': 5, 'unitCode': 'DAY'}}},
                       'hasMerchantReturnPolicy': {'@type': 'MerchantReturnPolicy', 'applicableCountry': 'AU', 'returnPolicyCategory': 'https://schema.org/MerchantReturnFiniteReturnWindow', 'merchantReturnDays': 14, 'returnMethod': 'https://schema.org/ReturnByMail', 'returnFees': 'https://schema.org/ReturnFeesCustomerResponsibility'}}}
for p in prods:
    gk = GROUPS.get(p['group'], ('shop', p['group'].title(), '', ''))
    cr = [('Home', 'index.html'), (gk[1], gk[0] + '.html'), (p['name'].title(), purl(p))]
    imgs = ''.join(f'<img src="../{u}" alt="{E(p["name"].title())} — {E(p["variant"])}" loading="{"eager" if i == 0 else "lazy"}">' for i, u in enumerate([p['img']] + ['assets/' + x for x in MODEL.get(p['id'], [])]))
    related = ''.join(f'<a class="card" href="../{purl(q)}"><img src="../{q["img"].replace(".jpg", "_s.jpg")}" alt="{E(q["name"].title())} {E(q["variant"])}" loading="lazy"><b>{E(q["name"].title())}</b><span>{E(q["variant"])} · ${q["price"]:.2f}</span></a>' for q in prods if q['group'] == p['group'] and q['id'] != p['id'])[:6000]
    body = f"""{crumbs(cr, 1)}<div class="pdp"><div class="imgs">{imgs}</div><div><h1>{E(p['name'].title())}</h1><div class="mono">{E(p['variant'])} · {E(gk[1])}</div><div class="price">${p['price']:.2f} AUD</div>
<p><em>{E(LINES.get(p['id'], ''))}</em></p><p>{E(desc(p))}</p><p class="mono">{E(FIT.get(p['category'], ''))}</p>
<a class="btn" href="../index.html#p-{p['id']}">CHOOSE SIZE &amp; BUY →</a>
<h2>Delivery &amp; returns</h2><p>Standard $10 (3–5 business days), Express $18 (1–2). Free shipping over $200. <a href="../returns.html">14-day returns</a> on unworn items with tags on. <a href="../shipping.html">Shipping details</a>. <a href="../size-guide.html">Size guide</a>.</p></div></div>
{('<h2>More from ' + E(gk[1]) + '</h2><div class="grid">' + related + '</div>') if related else ''}"""
    title = f"{p['name'].title()} — {p['variant']} | 73 Melbourne Streetwear"
    page(purl(p), title, f"{p['name'].title()} in {p['variant']} by 73, a Melbourne streetwear brand. ${p['price']:.2f} AUD. {desc(p)}"[:300], body,
         ld(product_ld(p)) + ld({'@context': 'https://schema.org', **bl([(n, u) for n, u in cr])}), og_img=p['img'], depth=1, wide=True)
# ---------------- category pages
for g, (slg, name, h1, intro) in GROUPS.items():
    items = [p for p in prods if p['group'] == g]
    cards = ''.join(f'<a class="card" href="{purl(p)}"><img src="{p["img"].replace(".jpg", "_s.jpg")}" alt="{E(p["name"].title())} {E(p["variant"])}" loading="lazy"><b>{E(p["name"].title())}</b><span>{E(p["variant"])} · ${p["price"]:.2f}</span></a>' for p in items)
    cr = [('Home', 'index.html'), (name, slg + '.html')]
    body = f'{crumbs(cr)}<h1>{E(h1)}</h1><p>{E(intro)}</p><p class="mono">{len(items)} {"piece" if len(items) == 1 else "pieces"} · free shipping over $200 · 14-day returns</p><div class="grid">{cards}</div><p style="margin-top:40px"><a class="btn" href="index.html#shop">SHOP EVERYTHING →</a></p>'
    il = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': h1, 'description': intro, 'url': DOMAIN + '/' + slg + '.html', 'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': DOMAIN + '/' + purl(p), 'name': p['name'].title() + ' — ' + p['variant']} for i, p in enumerate(items)]}}
    page(slg + '.html', f'{h1} | 73', intro[:290], body, ld(il) + ld({'@context': 'https://schema.org', **bl(cr)}), og_img=items[0]['img'], wide=True)
# ---------------- trust + legal pages
page('about.html', 'About 73 — Melbourne streetwear brand', '73 is a Melbourne streetwear brand making heavyweight hoodies, tees, caps, jackets and tracksuits, each marked with one small seal.',
 f"""{crumbs([('Home','index.html'),('About','about.html')])}<h1>About 73</h1>
<p>73 is a Melbourne streetwear brand. We make heavyweight hoodies, tees, snapbacks, work jackets, tracksuits and shorts in a handful of colours, designed to be worn hard and kept.</p>
<h2>The seal</h2><p>Every piece carries the same small mark: a fused 73 inside a ring, with the name of the piece in tiny lettering beneath it. That is all the branding there is.</p>
<h2>Before 73</h2><p>The label began as RES BOYS. The <a href="originals.html">Originals</a> line brings that first design back in oxblood, with a small 73 beneath it.</p>
<h2>The 73 code</h2><p>Seven rules: never blend in, weight over noise, say less, explain nothing, keep your own close, wear it like a decision, be seen. Three promises: honest sizing, fair returns and straight answers.</p>
<p><a class="btn" href="index.html#shop">SHOP 73 →</a></p><p class="mono">Questions? <a href="contact.html">Contact us</a>.</p>""",
 ld({'@context':'https://schema.org','@type':'AboutPage','name':'About 73','url':DOMAIN+'/about.html','about':{'@type':'Organization','name':'73','url':DOMAIN,'address':{'@type':'PostalAddress','addressLocality':'Melbourne','addressRegion':'VIC','addressCountry':'AU'}}}))
page('contact.html', 'Contact 73 — customer service', f"Contact 73 about orders, sizing or returns. We reply within {BIZ['response']}.",
 f"""{crumbs([('Home','index.html'),('Contact','contact.html')])}<h1>Contact us</h1><p>Questions about an order, sizing or a return? Email <a href="mailto:{BIZ['email']}">{BIZ['email']}</a> and a real person will reply within {BIZ['response']}.</p>
<p>Please include your order number and the email you ordered with.</p>
<form onsubmit="event.preventDefault();var f=this;location.href='mailto:{BIZ['email']}?subject='+encodeURIComponent(f.subject.value||'Order question')+'&body='+encodeURIComponent((f.order.value?'Order: '+f.order.value+'\\n\\n':'')+f.msg.value)" style="display:grid;gap:12px;max-width:520px">
<label>Order number (optional)<input name="order" style="width:100%;padding:12px;border:1px solid #0a0a0a"></label><label>Subject<input name="subject" style="width:100%;padding:12px;border:1px solid #0a0a0a"></label><label>Message<textarea name="msg" rows="6" required style="width:100%;padding:12px;border:1px solid #0a0a0a"></textarea></label><button class="btn" style="border:0;cursor:pointer;width:max-content">OPEN IN MY EMAIL →</button></form>
<h2>Business details</h2><p>{E(BIZ['trading'])} · {E(BIZ['legal'])} · ABN {E(BIZ['abn'])}<br>{E(BIZ['place'])}<br>Instagram: <a href="{BIZ['insta']}" rel="noopener">@73official</a></p>""")
page('size-guide.html', '73 size guide — fit notes for hoodies, tees, jackets and bottoms', 'How 73 pieces fit: oversized hoodies, regular tees, layering jackets and relaxed bottoms. Between sizes? Here is what to pick.',
 f"""{crumbs([('Home','index.html'),('Size guide','size-guide.html')])}<h1>Size guide</h1><p>Every 73 piece is cut for a streetwear fit. Use the notes below, and email us if you are unsure — we would rather help you pick than process a return.</p>
<table><tr><th>Piece</th><th>Fit</th><th>Between sizes?</th></tr><tr><td>Hoodies</td><td>Oversized, boxy</td><td>Size down for a closer fit</td></tr><tr><td>T-shirts</td><td>Regular</td><td>True to size</td></tr><tr><td>Jackets &amp; vests</td><td>Cut for layering over a hoodie</td><td>Size up</td></tr><tr><td>Tracksuit jacket</td><td>Regular</td><td>Size up</td></tr><tr><td>Tracksuit pant, cargos, joggers, shorts</td><td>Relaxed</td><td>Size down</td></tr><tr><td>Snapbacks</td><td>One size, adjustable</td><td>—</td></tr></table>
<h2>How to choose</h2><p>Measure a piece you already like, lay it flat and compare. For hoodies, think about whether you want the boxy oversized look (your normal size) or a closer fit (one size down). Garment measurements for any piece are available on request: <a href="contact.html">contact us</a>.</p>""")
page('shipping.html', 'Shipping & delivery — 73 Melbourne streetwear', 'Australia-wide shipping from Melbourne. Standard $10 (3–5 business days), Express $18 (1–2), free over $200. Tracked.',
 f"""{crumbs([('Home','index.html'),('Shipping','shipping.html')])}<h1>Shipping &amp; delivery</h1>
<p>We ship Australia-wide from Melbourne, Victoria. We do not ship internationally yet.</p>
<table><tr><th>Option</th><th>Cost</th><th>Delivery time</th></tr><tr><td>Standard</td><td>$10.00</td><td>3–5 business days</td></tr><tr><td>Express</td><td>$18.00</td><td>1–2 business days</td></tr><tr><td>Free shipping</td><td>$0.00</td><td>Orders over $200 (after discounts) — standard timing</td></tr></table>
<h2>Processing</h2><p>Orders are packed within 1–2 business days. Delivery times start once your order has been dispatched, and are estimates — weekends, public holidays, sale periods and carrier delays can add time.</p>
<h2>Tracking</h2><p>You will receive a confirmation email straight after checkout and tracking details once your order ships. Can't find it? Check your spam folder, then <a href="contact.html">contact us</a>.</p>
<h2>Wrong address</h2><p>Please check your delivery address at checkout. If you spot a mistake, email us straight away — we can only change an address before the order ships.</p>
<h2>Lost or damaged parcels</h2><p>If your parcel arrives damaged, or does not arrive, contact us with your order number and we will make it right. Under the Australian Consumer Law you are entitled to a remedy when goods do not arrive or arrive faulty.</p>""")
page('returns.html', 'Returns & exchanges — 73', '14-day returns on unworn items with tags on. Faulty or wrong item? We fix it at no cost. Your rights under Australian Consumer Law are never limited.',
 f"""{crumbs([('Home','index.html'),('Returns','returns.html')])}<h1>Returns &amp; exchanges</h1>
<h2>Changed your mind</h2><p>Return unworn, unwashed items with tags attached within 14 days of delivery for a refund or exchange. You cover return postage. Items that are worn, washed, altered or missing tags may be refused.</p>
<h2>Faulty or wrong item</h2><p>If an item is faulty or we sent the wrong thing, email us and we will arrange a repair, replacement or refund at no cost to you — your choice where the law gives you one.</p>
<h2>How to return</h2><ol><li>Email <a href="mailto:{BIZ['email']}">{BIZ['email']}</a> with your order number and what you are returning.</li><li>We will reply with the return address and instructions.</li><li>Post it back (we recommend a tracked service). Refunds go to your original payment method within 5–10 business days of us receiving and checking the item.</li></ol>
<h2>Exchanges</h2><p>Need a different size? Email us first so we can hold the size you want where stock allows.</p>
<h2>Your rights</h2><p>Our goods come with guarantees that cannot be excluded under the Australian Consumer Law. You are entitled to a replacement or refund for a major failure and compensation for any other reasonably foreseeable loss or damage. Nothing in this policy limits those rights.</p>""")
page('privacy.html', 'Privacy policy — 73', 'How 73 collects, uses and protects your personal information, in line with the Australian Privacy Principles.',
 f"""{crumbs([('Home','index.html'),('Privacy','privacy.html')])}<h1>Privacy policy</h1><p class="mono">Last updated 7 October 2026</p>
<p>{E(BIZ['trading'])} ({E(BIZ['legal'])}, ABN {E(BIZ['abn'])}) respects your privacy and handles personal information in line with the Privacy Act 1988 (Cth) and the Australian Privacy Principles.</p>
<h2>What we collect</h2><ul><li>Order details: name, email, phone, delivery and billing address, what you bought.</li><li>Email address if you join the crew list (with your consent).</li><li>Messages you send us.</li><li>If you accept analytics cookies: pages viewed, device and browser type, approximate location.</li></ul>
<h2>Payments</h2><p>Card payments are processed by Stripe or Shopify Payments. Your card number is entered on their secure pages — we never see or store it.</p>
<h2>How we use it</h2><p>To fulfil and deliver orders, provide customer service, prevent fraud, meet legal and tax obligations, and — only if you opted in — send marketing emails. You can unsubscribe at any time using the link in any email.</p>
<h2>Who we share it with</h2><p>Only the services needed to run the shop: payment processors, couriers, our email provider and (if you accept cookies) analytics providers. They may store data on servers outside Australia. We do not sell your personal information.</p>
<h2>Cookies</h2><p>See our <a href="cookies.html">cookie policy</a>.</p>
<h2>Security and retention</h2><p>We use reputable providers, HTTPS and access controls. We keep order records for as long as the law requires (generally 7 years for tax purposes) and delete marketing data when you unsubscribe or ask.</p>
<h2>Your rights</h2><p>You can ask to access, correct or delete the personal information we hold about you by emailing <a href="mailto:{BIZ['email']}">{BIZ['email']}</a>. If you are not satisfied with our response you can contact the Office of the Australian Information Commissioner (oaic.gov.au).</p>""")
page('terms.html', 'Terms of sale — 73', 'Terms of sale for 73 online orders: pricing, payment, shipping, discount codes, returns and your Australian Consumer Law rights.',
 f"""{crumbs([('Home','index.html'),('Terms','terms.html')])}<h1>Terms of sale</h1><p class="mono">Last updated 7 October 2026</p>
<h2>About these terms</h2><p>These terms apply to purchases from this website, operated by {E(BIZ['trading'])} ({E(BIZ['legal'])}, ABN {E(BIZ['abn'])}). By placing an order you agree to them.</p>
<h2>Prices and payment</h2><p>All prices are in Australian dollars (AUD) and include GST where applicable. Payment is taken at checkout through our payment provider. We may cancel and fully refund an order affected by a pricing or stock error.</p>
<h2>Orders</h2><p>Your order is accepted when we send a dispatch confirmation. We may decline or cancel orders where we reasonably suspect fraud or if an item is unavailable, and will refund you in full.</p>
<h2>Discount codes</h2><p>The code NEVERBLEND15 gives 15% off one order per customer, cannot be combined with other offers and has no cash value.</p>
<h2>Shipping and returns</h2><p>See our <a href="shipping.html">shipping</a> and <a href="returns.html">returns</a> policies, which form part of these terms.</p>
<h2>Consumer guarantees</h2><p>Our goods come with guarantees that cannot be excluded under the Australian Consumer Law. Nothing in these terms excludes, restricts or modifies those rights.</p>
<h2>Intellectual property</h2><p>The 73 name, seal, logos, photos and designs belong to us. Please do not copy or reuse them without written permission.</p>
<h2>Liability</h2><p>To the extent the law allows, our liability is limited to resupplying the goods or refunding the price paid.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of Victoria, Australia.</p><p>Questions? <a href="contact.html">Contact us</a>.</p>""")
page('cookies.html', 'Cookie policy — 73', 'What cookies and browser storage 73 uses, and how to change your choice.',
 f"""{crumbs([('Home','index.html'),('Cookies','cookies.html')])}<h1>Cookie policy</h1>
<h2>Essential storage</h2><p>This site stores your cart, saved items and discount code in your browser so the shop works. These are not used for tracking.</p>
<h2>Analytics (optional)</h2><p>If analytics are switched on, we ask first. If you accept, Google Analytics and/or the Meta Pixel measure which pages and products people view. If you decline, they never load.</p>
<h2>Change your choice</h2><p><button class="btn" style="border:0;cursor:pointer" onclick="try{{localStorage.removeItem('n73_consent')}}catch(e){{}};location.href='index.html'">RESET MY COOKIE CHOICE</button></p>
<p>You can also clear this site's data in your browser settings at any time. See our <a href="privacy.html">privacy policy</a> for more.</p>""")
# legacy policies page -> hub
page('policies.html', 'Policies — 73', 'Shipping, returns, privacy, terms and cookie policies for 73.', '<h1>Policies</h1><ul><li><a href="shipping.html">Shipping &amp; delivery</a></li><li><a href="returns.html">Returns &amp; exchanges</a></li><li><a href="privacy.html">Privacy policy</a></li><li><a href="terms.html">Terms of sale</a></li><li><a href="cookies.html">Cookie policy</a></li><li><a href="size-guide.html">Size guide</a></li><li><a href="contact.html">Contact</a></li></ul>', noindex=True)
# ---------------- sitemap, robots, security.txt
urls = [('', '1.0', 'daily'), ('about.html', '0.6', 'monthly'), ('contact.html', '0.5', 'yearly'), ('size-guide.html', '0.5', 'yearly'), ('shipping.html', '0.4', 'yearly'), ('returns.html', '0.4', 'yearly'), ('privacy.html', '0.3', 'yearly'), ('terms.html', '0.3', 'yearly'), ('cookies.html', '0.3', 'yearly')]
urls += [(v[0] + '.html', '0.8', 'weekly') for v in GROUPS.values()] + [(purl(p), '0.7', 'weekly') for p in prods]
imgmap = {purl(p): p for p in prods}
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
for u, pr, cf in urls:
    e = f'<url><loc>{DOMAIN}/{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority>'
    if u in imgmap: e += f'<image:image><image:loc>{DOMAIN}/{imgmap[u]["img"]}</image:loc><image:title>{E(imgmap[u]["name"].title())} — {E(imgmap[u]["variant"])}</image:title></image:image>'
    sm.append(e + '</url>')
sm.append('</urlset>'); wr('sitemap.xml', '\n'.join(sm))
wr('robots.txt', f'User-agent: *\nAllow: /\nDisallow: /policies.html\n\nSitemap: {DOMAIN}/sitemap.xml\n')
wr('.well-known/security.txt', f"Contact: mailto:{BIZ['email']}\nExpires: 2027-10-07T00:00:00.000Z\nPreferred-Languages: en\nCanonical: {DOMAIN}/.well-known/security.txt\n")
print('built', len(prods), 'product pages,', len(GROUPS), 'category pages, sitemap with', len(urls), 'urls')
