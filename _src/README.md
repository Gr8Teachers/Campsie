# Source for the Campsie Free English Classes pages

Built from the same template as the St Leonards site (Gr8Teachers/StLeonards), then adjusted
for Campsie by `campsie_patch.py` (navy colours, office hours, Campsie contact details,
no QR code / online form).

- `langs/en.json`, `langs/b*.json`, `langs/f_*.json` – shared text (English + 27 languages)
- `make_campsie_langs.py` → `langs/z_campsie.json` – Campsie-specific text (office hours etc.)
- Build: `python3 make_template.py && python3 campsie_patch.py && python3 build.py <output folder>`
- `zoom.json` – print scale per language so each prints on one A4 page
