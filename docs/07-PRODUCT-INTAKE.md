# 07 — Product intake (what to send per product)

Send all of this in one go per product. The Strategist refuses to start if a **required**
field is missing (CLAUDE.md rule 10). Put photos in `assets/products/{product_id}/`.

## Photos (most important — the video can only be as accurate as these)
Required: **6–8 real photos**, at least 2000 px on the long side, no watermarks, no
heavy retouching, true-to-life colour.
- [ ] Full product, straight on, neutral light (e.g. full bedsheet laid flat / on bed)
- [ ] Product in a real room (any decent phone photo is fine)
- [ ] Print / pattern close-up showing the true scale of the repeat
- [ ] Fabric / material macro (weave, pile, sheen)
- [ ] Logo, label, tag and embroidery, close and sharp
- [ ] Every item in the set (fitted sheet, flat sheet, pillow covers — count them)
- [ ] Optional: packaging, folded stack, colour variants
Tip: shoot by a window in daylight, no flash, colour card in one frame if you have one.

## Facts
| Field | Required | Example |
|---|---|---|
| product_id (slug) | yes | `bedsheet-aurora-king` |
| name | yes | Aurora Printed Cotton Bedsheet Set |
| brand | yes | Bianca Home / Nautica / Bianca Maison |
| category | yes | bedding / bath / dining / fragrance / other |
| product URL | yes | https://www.biancahome.com/products/... |
| material | yes | 100% cotton, 210 TC, percale |
| size / contents | yes | King 274×274 cm + 2 pillow covers 46×69 cm |
| print / colour name | yes | Aurora — sage + ivory botanical |
| logo notes | yes | woven label bottom-left of flat sheet; none on pillow covers |
| selling points (3–5) | yes | breathable, softens with wash, colour-fast |
| price point | yes | MRP ₹3,499, sale ₹1,799 |
| audience | yes | 28–45, urban India, first home / upgrading |
| platform + length | yes | instagram_reel, 15 s |
| mood / look you want | nice to have | calm Sunday morning, warm daylight |
| must avoid | nice to have | no kids, no pets, no dark rooms |
| reference video | nice to have | a Reel whose style you like (URL) |
| caption / CTA preference | nice to have | "Shop the Aurora set — link in bio" |

These map 1:1 to `schemas/product_brief.json`.
