# RES BOYS — on-model photo shot list (male + female)

I (Claude) can't generate photographs, so this is the production pack for your image generator or a real shoot. The site is already wired up to show these as extra product images (gallery in quick view + hover swap on the shop grid).

## How to add the photos
1. Save each image as `assets/models/<product_id>_m.jpg` (male) and/or `assets/models/<product_id>_f.jpg` (female). 1600 x 2000 px, JPG, under ~400 KB each.
2. In `index.html`, list them in `LIVE_CONFIG.modelShots`, e.g. `modelShots: { hoodie_black: ['m','f'], cap_black: ['m','f'] }`.
3. Done — no other code changes. Products without model photos keep the studio packshot.

AI generators often misspell logos. If the lettering comes out wrong, send me the images and I'll swap in the real RES BOYS logo, or fix it in an editor. Keep the same model, styling and grade across the whole set.

## Style block (paste at the end of every prompt)
```
Street-style lookbook photograph shot on location in Reservoir, Melbourne (VIC, Australia). Gritty, low-key, slightly desaturated colour grade, overcast or dusk light, direct on-camera flash feel, visible 35mm film grain, shallow depth of field, candid street-cast model with a confident, unsmiling expression, not a studio, no gloss. Natural skin texture, correct hands and fabric folds. 4:5 portrait, 1600 x 2000 px minimum, photorealistic. The ONLY text visible is the RES BOYS logo exactly as described (two lines, "RES" over "BOYS", bold italic uppercase sans-serif, spelled correctly). No other words, no other logos, no watermarks.
```

## Locations to rotate (keep them recognisably local)
- wet street outside Reservoir shopfronts at dusk
- concrete underpass with graffiti
- tram stop on a wet road, overcast
- suburban park path by the lake, golden hour
- brick wall and roller door, side lane
- car park, sodium streetlights, night

## Casting + styling notes
- Male and female models, mixed ages 20–30, street-cast look. Same two models across the full set if your tool supports reference images / seeds.
- Style around the piece: black cargos or jeans, clean white sneakers. Keep colours muted so the garment is the hero.
- Shot mix: 1 full-length or 3/4 per product per model; add a close-up of the logo for hero items (hoodie_black, cap_black, hoodie_back_black).

## Prompts
Append the style block to each.

### Henty Snapback — `cap_black`
- `assets/models/cap_black_m.jpg` — Male: Close portrait, shoulders up, wearing the black flat-brim snapback, RES BOYS embroidered on the front in white (two lines: RES / BOYS, bold italic uppercase). Location: wet street outside Reservoir shopfronts at dusk. Subject: male model.
- `assets/models/cap_black_f.jpg` — Female: Close portrait, shoulders up, wearing the black flat-brim snapback, RES BOYS embroidered on the front in white (two lines: RES / BOYS, bold italic uppercase). Location: suburban park path by the lake, golden hour. Subject: female model.

### Ruthven Snapback — `cap_charcoal`
- `assets/models/cap_charcoal_m.jpg` — Male: Close portrait, shoulders up, wearing the charcoal flat-brim snapback, RES BOYS embroidered on the front in white (two lines, bold italic uppercase). Location: concrete underpass with graffiti. Subject: male model.
- `assets/models/cap_charcoal_f.jpg` — Female: Close portrait, shoulders up, wearing the charcoal flat-brim snapback, RES BOYS embroidered on the front in white (two lines, bold italic uppercase). Location: brick wall and roller door, side lane. Subject: female model.

### Edwardes Snapback — `cap_olive`
- `assets/models/cap_olive_m.jpg` — Male: Close portrait, shoulders up, wearing the olive green flat-brim snapback, RES BOYS embroidered on the front in white (two lines, bold italic uppercase). Location: tram stop on a wet road, overcast. Subject: male model.
- `assets/models/cap_olive_f.jpg` — Female: Close portrait, shoulders up, wearing the olive green flat-brim snapback, RES BOYS embroidered on the front in white (two lines, bold italic uppercase). Location: car park, sodium streetlights, night. Subject: female model.

### Dundas Snapback — `cap_white`
- `assets/models/cap_white_m.jpg` — Male: Close portrait, shoulders up, wearing the cream-white flat-brim snapback, RES BOYS embroidered on the front in black (two lines, bold italic uppercase). Location: suburban park path by the lake, golden hour. Subject: male model.
- `assets/models/cap_white_f.jpg` — Female: Close portrait, shoulders up, wearing the cream-white flat-brim snapback, RES BOYS embroidered on the front in black (two lines, bold italic uppercase). Location: wet street outside Reservoir shopfronts at dusk. Subject: female model.

### Gilbert Hoodie — `hoodie_black`
- `assets/models/hoodie_black_m.jpg` — Male: Three-quarter-length standing shot wearing the black heavyweight oversized hoodie, small white RES BOYS chest logo on the left chest (two lines, bold italic uppercase). Location: brick wall and roller door, side lane. Subject: male model.
- `assets/models/hoodie_black_f.jpg` — Female: Three-quarter-length standing shot wearing the black heavyweight oversized hoodie, small white RES BOYS chest logo on the left chest (two lines, bold italic uppercase). Location: concrete underpass with graffiti. Subject: female model.

### Broadway Hoodie — `hoodie_charcoal`
- `assets/models/hoodie_charcoal_m.jpg` — Male: Three-quarter-length standing shot wearing the charcoal grey heavyweight oversized hoodie, small white RES BOYS chest logo on the left chest. Location: car park, sodium streetlights, night. Subject: male model.
- `assets/models/hoodie_charcoal_f.jpg` — Female: Three-quarter-length standing shot wearing the charcoal grey heavyweight oversized hoodie, small white RES BOYS chest logo on the left chest. Location: tram stop on a wet road, overcast. Subject: female model.

### Darebin Hoodie — `hoodie_olive`
- `assets/models/hoodie_olive_m.jpg` — Male: Three-quarter-length standing shot wearing the olive green heavyweight oversized hoodie, small white RES BOYS chest logo on the left chest. Location: wet street outside Reservoir shopfronts at dusk. Subject: male model.
- `assets/models/hoodie_olive_f.jpg` — Female: Three-quarter-length standing shot wearing the olive green heavyweight oversized hoodie, small white RES BOYS chest logo on the left chest. Location: suburban park path by the lake, golden hour. Subject: female model.

### Summerhill Hoodie — `hoodie_bone`
- `assets/models/hoodie_bone_m.jpg` — Male: Three-quarter-length standing shot wearing the bone / cream heavyweight oversized hoodie, small black RES BOYS chest logo on the left chest. Location: concrete underpass with graffiti. Subject: male model.
- `assets/models/hoodie_bone_f.jpg` — Female: Three-quarter-length standing shot wearing the bone / cream heavyweight oversized hoodie, small black RES BOYS chest logo on the left chest. Location: brick wall and roller door, side lane. Subject: female model.

### Cuthbert Hoodie — `hoodie_back_black`
- `assets/models/hoodie_back_black_m.jpg` — Male: Full-length shot from behind, looking over the shoulder, wearing the black heavyweight oversized hoodie, large white RES BOYS print across the back (shot from behind, over the shoulder). Location: tram stop on a wet road, overcast. Subject: male model.
- `assets/models/hoodie_back_black_f.jpg` — Female: Full-length shot from behind, looking over the shoulder, wearing the black heavyweight oversized hoodie, large white RES BOYS print across the back (shot from behind, over the shoulder). Location: car park, sodium streetlights, night. Subject: female model.

### Plenty Tee — `tee_black`
- `assets/models/tee_black_m.jpg` — Male: Three-quarter-length standing shot wearing the black regular-fit cotton tee, small white RES BOYS chest logo on the left chest. Location: suburban park path by the lake, golden hour. Subject: male model.
- `assets/models/tee_black_f.jpg` — Female: Three-quarter-length standing shot wearing the black regular-fit cotton tee, small white RES BOYS chest logo on the left chest. Location: wet street outside Reservoir shopfronts at dusk. Subject: female model.

### Cheddar Tee — `tee_charcoal`
- `assets/models/tee_charcoal_m.jpg` — Male: Three-quarter-length standing shot wearing the charcoal regular-fit cotton tee, small white RES BOYS chest logo on the left chest. Location: brick wall and roller door, side lane. Subject: male model.
- `assets/models/tee_charcoal_f.jpg` — Female: Three-quarter-length standing shot wearing the charcoal regular-fit cotton tee, small white RES BOYS chest logo on the left chest. Location: concrete underpass with graffiti. Subject: female model.

### Merri Tee — `tee_olive`
- `assets/models/tee_olive_m.jpg` — Male: Three-quarter-length standing shot wearing the olive green regular-fit cotton tee, small white RES BOYS chest logo on the left chest. Location: car park, sodium streetlights, night. Subject: male model.
- `assets/models/tee_olive_f.jpg` — Female: Three-quarter-length standing shot wearing the olive green regular-fit cotton tee, small white RES BOYS chest logo on the left chest. Location: tram stop on a wet road, overcast. Subject: female model.

### High St Tee — `tee_white`
- `assets/models/tee_white_m.jpg` — Male: Three-quarter-length standing shot wearing the white regular-fit cotton tee, small black RES BOYS chest logo on the left chest. Location: wet street outside Reservoir shopfronts at dusk. Subject: male model.
- `assets/models/tee_white_f.jpg` — Female: Three-quarter-length standing shot wearing the white regular-fit cotton tee, small black RES BOYS chest logo on the left chest. Location: suburban park path by the lake, golden hour. Subject: female model.

### Settlement Work Jacket — `jacket_work`
- `assets/models/jacket_work_m.jpg` — Male: Three-quarter-length standing shot wearing the black collared work jacket with full zip and a small white RES BOYS logo on the chest. Location: concrete underpass with graffiti. Subject: male model.
- `assets/models/jacket_work_f.jpg` — Female: Three-quarter-length standing shot wearing the black collared work jacket with full zip and a small white RES BOYS logo on the chest. Location: brick wall and roller door, side lane. Subject: female model.

### Boldrewood Puffer — `vest_puffer`
- `assets/models/vest_puffer_m.jpg` — Male: Three-quarter-length standing shot wearing the black quilted puffer vest with a small white RES BOYS logo on the chest, worn over a black hoodie. Location: tram stop on a wet road, overcast. Subject: male model.
- `assets/models/vest_puffer_f.jpg` — Female: Three-quarter-length standing shot wearing the black quilted puffer vest with a small white RES BOYS logo on the chest, worn over a black hoodie. Location: car park, sodium streetlights, night. Subject: female model.

### Dundas Cargo — `pants_cargo_black`
- `assets/models/pants_cargo_black_m.jpg` — Male: Full-length standing shot wearing the black relaxed cargo pants with side cargo pockets, cuffed hem (full-length shot, with a plain black tee). Location: suburban park path by the lake, golden hour. Subject: male model.
- `assets/models/pants_cargo_black_f.jpg` — Female: Full-length standing shot wearing the black relaxed cargo pants with side cargo pockets, cuffed hem (full-length shot, with a plain black tee). Location: wet street outside Reservoir shopfronts at dusk. Subject: female model.

### Lakeside Jogger — `pants_joggers_charcoal`
- `assets/models/pants_joggers_charcoal_m.jpg` — Male: Full-length standing shot wearing the charcoal tapered joggers with cuffed ankles (full-length shot, with a plain black tee). Location: brick wall and roller door, side lane. Subject: male model.
- `assets/models/pants_joggers_charcoal_f.jpg` — Female: Full-length standing shot wearing the charcoal tapered joggers with cuffed ankles (full-length shot, with a plain black tee). Location: concrete underpass with graffiti. Subject: female model.

### Merri Cargo Short — `shorts_cargo_olive`
- `assets/models/shorts_cargo_olive_m.jpg` — Male: Full-length standing shot wearing the olive relaxed cargo shorts with side pockets (full-length shot, with a plain black tee). Location: car park, sodium streetlights, night. Subject: male model.
- `assets/models/shorts_cargo_olive_f.jpg` — Female: Full-length standing shot wearing the olive relaxed cargo shorts with side pockets (full-length shot, with a plain black tee). Location: tram stop on a wet road, overcast. Subject: female model.

### Broadway Short — `shorts_black`
- `assets/models/shorts_black_m.jpg` — Male: Full-length standing shot wearing the black relaxed shorts with a small white RES BOYS logo on the lower left leg (full-length shot, with a plain white tee). Location: wet street outside Reservoir shopfronts at dusk. Subject: male model.
- `assets/models/shorts_black_f.jpg` — Female: Full-length standing shot wearing the black relaxed shorts with a small white RES BOYS logo on the lower left leg (full-length shot, with a plain white tee). Location: suburban park path by the lake, golden hour. Subject: female model.
