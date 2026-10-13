# 73 — product photo shot list (ASOS-style + on-model)

I can't generate photographs. Use this as the brief for a shoot or an image generator. The site already supports extra images per product.

## Packshots (replace `assets/<id>.jpg`, 1000 x 1250, plus a 500 x 625 `<id>_s.jpg`)
Ghost-mannequin or flat-lay on a seamless light-grey (#EEEDE9) backdrop, soft even light, subtle contact shadow, sharp stitching, logo exactly as described, 4:5.

## On-model
Save as `assets/models/<id>_m.jpg` (male) / `<id>_f.jpg` (female) and list in `LIVE_CONFIG.modelShots` in index.html.

### Style block (append to every prompt)
```
Editorial streetwear photograph, muted sepia-grey colour grade, overcast light, visible film grain, street-cast model with a calm unsmiling expression, natural skin texture, correct hands and fabric folds. 4:5 portrait, 1600 x 2000 px minimum. The ONLY marks on the clothing are the 73 seal (a ring containing a fused 73, NO lettering around the ring) with the product name in tiny letters beneath it, exactly as described.
```

## Styles

- **Edwardes Track Jacket** (`trk_jacket_*`): track jacket with chevron colour-block panels, contrast sleeve stripes, stand collar, full zip; small 73 seal under the left collar.
- **Edwardes Track Pant** (`trk_pant_*`): straight-leg track pant with contrast side stripes and a front crease.
- **Edwardes Track Short** (`trk_short_*`): track short with contrast side stripes, elastic waist.
- **Henty Snapback** (`cap_black/charcoal/olive/white`): flat-brim snapback, small 73 seal on the front, HENTY in tiny lettering beneath.
- **Gilbert Hoodie** (`hoodie_black/charcoal/olive/bone/back_black`): heavyweight oversized hoodie, small 73 seal on the chest (or large on the back for back_black), GILBERT beneath.
- **Plenty Tee** (`tee_black/charcoal/olive/white`): regular-fit cotton tee, small 73 seal on the chest, PLENTY beneath.
- **Settlement Work Jacket / Boldrewood Puffer** (`jacket_work / vest_puffer`): collared work jacket / quilted puffer vest, small 73 seal on the chest.
- **Lakeside Jogger / Broadway Sweatshort** (`pants_joggers_charcoal / shorts_black`): tapered jogger / garment-washed sweatshort, small 73 seal.
- **Original Hoodie / Original Snapback** (`hoodie_oxblood / cap_oxblood`): oxblood; original RES BOYS mark with a small 73 beneath.

## Tracksuit note
The Black/Rose colourway in `assets/models/trk_rose_*` comes from your design photo; Ice, Bone, Olive and Oxblood are digital recolours. Replace them with photos of the real samples before selling those colourways.
