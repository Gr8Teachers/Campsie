"""Turn the St Leonards template (template.html) into the Campsie template.
Run after make_template.py:  python3 campsie_patch.py
"""
import re
p = '/home/claude/campsie/build/template.html'
t = open(p, encoding='utf-8').read()

def rep(old, new, count=None):
    global t
    assert old in t, old[:80]
    t = t.replace(old, new) if count is None else t.replace(old, new, count)

# --- Brand colours: navy (from the Campsie flyer) instead of red ---
for old, new in [('#a8012f', '#2b4a78'), ('#7d0023', '#1e3557'), ('#c3133f', '#3d6299'),
                 ('rgba(168,1,47,.35)', 'rgba(43,74,120,.35)'), ('#fbeef2', '#e8eef7'),
                 ('#ffd7e1', '#d3e0f2'), ('#ffe3ea', '#dfe8f5'), ('#f6dbe3', '#d9e3f1'),
                 ('#f1c9d4', '#c7d5ea'), ('#f3dfe5', '#dde6f3')]:
    rep(old, new)

# --- Campus name, links, contact details ---
rep('<span class="eyebrow">TAFE NSW St Leonards</span>', '<span class="eyebrow">TAFE NSW Campsie</span>')
MAP = 'https://www.google.com/maps/search/?api=1&query=59-63+Evaline+Street+Campsie+NSW+2194'
rep('https://www.google.com/maps/search/?api=1&query=213+Pacific+Hwy+St+Leonards+NSW+2065', MAP)
rep('<a href="tel:+61279206475" dir="ltr">7920 6475</a>', '<a href="tel:+61279208992" dir="ltr">7920 8992</a>')
rep('<a dir="ltr" href="mailto:esolstleonards@tafensw.edu.au">esolstleonards<wbr>@tafensw.edu.au</a>',
    '<a dir="ltr" href="mailto:amepcampsie@tafensw.edu.au">amepcampsie<wbr>@tafensw.edu.au</a>')
rep('>Building P, Level 4, P4.02<br>213 Pacific Hwy, St Leonards NSW 2065</a>',
    '>Level 1, 59/63 Evaline Street<br>Campsie NSW 2194</a>')
rep('gr8teachers.github.io/StLeonards{{PATH}}', 'gr8teachers.github.io/Campsie{{PATH}}')

# --- Office hours card instead of info-day date ---
rep('<a class="btn btn-white" href="#info-day">{{btn_info}}</a>', '<a class="btn btn-white" href="#hours">{{btn_info}}</a>')
rep('<li class="link"><a href="#info-day">{{nav_info}}</a></li>', '<li class="link"><a href="#hours">{{nav_info}}</a></li>')
rep('<!-- Info day -->\n  <div class="wrap infoday" id="info-day">', '<!-- Office hours -->\n  <div class="wrap infoday" id="hours">')
rep('<div class="cal" aria-hidden="true"><div class="m">{{cal_top}}</div><div class="d{{CAL_CLS}}">{{cal_mid}}</div><div class="y">{{cal_bot}}</div></div>',
    '<div class="cal" aria-hidden="true"><div class="m">{{cal_top}}</div><div class="d clock"><svg viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2a10 10 0 1 1 0 20 10 10 0 0 1 0-20zm0 2a8 8 0 1 0 0 16 8 8 0 0 0 0-16zm1 3v5.4l3.8 2.3-1 1.7L11 13.5V7z"/></svg></div></div>')
# no second badge for Campsie (office hours only)
rep('\n          <span class="pill pill-y"><svg viewBox="0 0 24 24"><path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>{{free_test}}</span>', '')

# --- Contact section: no QR code / online form for Campsie ---
s = t.index('      <div class="qr-box print-qr">')
e = t.index('    </div>\n  </section>\n</main>')
t = t[:s] + t[e:]
rep('<a class="btn btn-ghost" href="#enquiry">{{btn_contact}}</a>', '<a class="btn btn-ghost" href="#contact">{{btn_contact}}</a>')

rep('<p>{{dc_where}}</p>', '<div class="dc-loc"><p>{{dc_where}}</p>\n        <p class="walk"><svg viewBox="0 0 24 24"><path d="M12 2c-4 0-8 .5-8 4v9.5A3.5 3.5 0 0 0 7.5 19L6 20.5v.5h12v-.5L16.5 19a3.5 3.5 0 0 0 3.5-3.5V6c0-3.5-4-4-8-4zM7.5 17a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm3.5-7H6V6h5zm2 0V6h5v4zm3.5 7a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/></svg><span>{{walk}}</span></p></div>')
CSS = '''
/* ---- Campsie ---- */
.date-card p.walk{display:flex;align-items:center;gap:.45em;margin-top:6px;font-weight:600;color:#fff}
.date-card p.walk svg{width:1.15em;height:1.15em;fill:currentColor;flex:none}
.date-card p.walk span{min-width:0;overflow-wrap:break-word}
.cal .d.clock{display:flex;justify-content:center;padding:16px 0 10px}
.cal .d.clock svg{width:72px;height:72px;fill:var(--red)}
.contact{grid-template-columns:1fr !important}
.contact-box{display:grid;grid-template-columns:1fr 1.6fr;gap:12px 40px;align-items:center}
.contact-box > h2, .contact-box > p{grid-column:1}
.contact-box > .cl{grid-column:2;grid-row:1 / span 2}
@media (max-width:900px){.contact-box{display:block}.contact-box > .cl{margin-top:8px}}
@media (max-width:380px){.nav img{height:auto !important;width:100px}.nav ul{gap:4px !important}}
@media print{
  .cal .d.clock svg{width:58px;height:58px}
  /* use the empty right side of the office-hours card for the address */
  .dc-main{display:grid;grid-template-columns:auto 1fr;column-gap:30px;align-items:center}
  .dc-main > .dc-eyebrow,.dc-main > h2,.dc-main > .dc-row{grid-column:1}
  .dc-main > .dc-loc{grid-column:2;grid-row:1 / span 3;border-inline-start:1.5px solid rgba(255,255,255,.35);padding-inline-start:28px;align-self:stretch;display:flex;flex-direction:column;justify-content:center}
  .dc-loc p{font-size:1.35rem !important;line-height:1.4;color:#fff !important}
  .dc-loc p.walk{font-size:1.25rem !important;margin-top:10px}
  .contact-box{display:grid !important;grid-template-columns:1fr 1.15fr;gap:6px 28px;align-items:center}
  .contact-box > h2, .contact-box > p{grid-column:1}
  .contact-box > .cl{grid-column:2;grid-row:1 / span 2;margin-top:0 !important}
  .contact-box > h2{align-self:end}
  .contact-box > p{align-self:start;margin-top:6px !important}
}
'''
rep('</style>', CSS + '</style>', 1)
open(p, 'w', encoding='utf-8').write(t)
left = [x for x in ['St Leonards', 'StLeonards', '7920 6475', 'esolstleonards', 'Pacific', 'qr.png', 'forms.office'] if x in t]
print('St Leonards leftovers:', left)
