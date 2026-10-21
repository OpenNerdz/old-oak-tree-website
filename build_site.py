#!/usr/bin/env python3
"""Builds the Old Oak Tree site: python3 build_site.py [path/to/api.json]
Writes index.html and the other pages next to this script. All content comes from
the pub's current website (crawled 21 Oct 2026); nothing here is invented."""
import json, re, sys, os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
API = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "content", "api.json")
PHONE = "01845 523276"
EMAIL = "info@oldoaktreethirsk.co.uk"
BOOK_ROOMS = "https://via.eviivo.com/OldYO72NL"
MAPS = "https://www.google.com/maps/search/?api=1&query=Old+Oak+Tree+South+Kilvington+Thirsk+YO7+2NL"
FACEBOOK = "https://www.facebook.com/pages/Old-Oak-Tree/169152219800632"
TWITTER = "https://twitter.com/LauretteNick"
TRIPADVISOR = "https://www.tripadvisor.co.uk/Restaurant_Review-g499612-d720778-Reviews-The_Old_Oak_Tree-Thirsk_North_Yorkshire_England.html"
NOTICE = "Closed 9 to 15 November 2026 and 4 to 10 January 2027."

FONTS = "https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&display=swap"

CSS = r"""
/* Layout: full-bleed photo bands over a measured cream column. Burgundy is reserved for actions,
   brass for labels and rules, so the photographs carry the colour. */
:root{
  --bg:#f4eee2;--surface:#fbf8f2;--surface-2:#eae1cf;--ink:#2a1d17;--muted:#6b5b50;--line:#d8cbb3;
  --brand:#4b1118;--brand-hover:#601722;--on-brand:#f8f1e7;--brass:#8c6b3e;--brass-soft:#ebdfc6;
  --shade:rgba(22,10,6,.58);--focus:#b8862b;
  --font-display:'Cinzel',Georgia,'Times New Roman',serif;
  --font-head:'Libre Caslon Text',Georgia,'Times New Roman',serif;
  --font-body:'Source Sans 3','Segoe UI',Helvetica,Arial,sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#1a1210;--surface:#231915;--surface-2:#2f231d;--ink:#f0e7d8;--muted:#b9a995;--line:#3f3129;
  --brand:#6d1e29;--brand-hover:#842532;--on-brand:#fbf3e9;--brass:#cda75f;--brass-soft:#3b2e21;
  --shade:rgba(0,0,0,.62);--focus:#e0b25a;color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#1a1210;--surface:#231915;--surface-2:#2f231d;--ink:#f0e7d8;--muted:#b9a995;--line:#3f3129;
  --brand:#6d1e29;--brand-hover:#842532;--on-brand:#fbf3e9;--brass:#cda75f;--brass-soft:#3b2e21;
  --shade:rgba(0,0,0,.62);--focus:#e0b25a;color-scheme:dark}

*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-body);font-size:1.0625rem;line-height:1.6;-webkit-font-smoothing:antialiased}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:40;background:var(--brand)}
img{max-width:100%;height:auto;display:block}
a{color:var(--brand);text-underline-offset:.15em}
:focus-visible{outline:3px solid var(--focus);outline-offset:3px}
h1,h2,h3,h4{font-family:var(--font-head);font-weight:400;line-height:1.15;margin:0;text-wrap:balance}
h1{font-size:clamp(2.1rem,4.6vw,3.4rem)}
h2{font-size:clamp(1.65rem,3vw,2.35rem)}
h3{font-size:1.3rem}
p{margin:0 0 1em}
.wrap{max-width:1140px;margin-inline:auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.measure{max-width:62ch}
.eyebrow{font-family:var(--font-body);font-weight:600;font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;color:var(--brass);margin:0 0 .6rem}
.lede{font-size:1.2rem;color:var(--muted)}
.muted{color:var(--muted)}
.btn{display:inline-flex;align-items:center;gap:.5rem;padding:.8rem 1.25rem;border-radius:3px;font-weight:600;text-decoration:none;border:1.5px solid var(--brand);background:var(--brand);color:var(--on-brand);line-height:1.2;transition:background .15s,border-color .15s}
.btn:hover{background:var(--brand-hover);border-color:var(--brand-hover)}
.btn.ghost{background:transparent;color:var(--brand)}
.btn.ghost:hover{background:var(--brand);color:var(--on-brand)}
.btn.light{background:var(--on-brand);color:var(--brand);border-color:var(--on-brand)}
.btn.light:hover{background:#fff}
.btn.ghost-light{background:transparent;color:#fff;border-color:rgba(255,255,255,.75)}
.btn.ghost-light:hover{background:rgba(255,255,255,.12)}
.btn svg{width:1.05em;height:1.05em;flex:none}
.btns{display:flex;flex-wrap:wrap;gap:.75rem}
.acorn{width:22px;height:28px;fill:var(--brass);display:block;margin:0 0 .8rem}
.rule{border:0;border-top:1px solid var(--line);margin:0}

/* notice + header */
.notice{background:var(--brand);color:var(--on-brand);font-size:.9rem;text-align:center}
.notice .wrap{padding-block:.45rem}
.notice strong{font-weight:600}
.site-header{position:sticky;top:env(safe-area-inset-top,0px);z-index:30;background:var(--surface);border-bottom:1px solid var(--line)}
.site-header .wrap{display:flex;align-items:center;gap:1.5rem;min-height:72px;padding-block:.5rem}
.brand{display:flex;flex-direction:column;text-decoration:none;color:var(--ink);line-height:1.05;flex:none}
.brand .name{font-family:var(--font-display);font-weight:600;font-size:1.25rem;letter-spacing:.14em;color:var(--brand)}
.brand .sub{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--brass);margin-top:.25rem}
.nav{display:flex;align-items:center;gap:.1rem;margin-left:auto}
.nav a{padding:.5rem .55rem;text-decoration:none;color:var(--ink);font-weight:600;font-size:.9rem;border-radius:3px;white-space:nowrap}
.nav a:hover{background:var(--surface-2)}
.nav a[aria-current="page"]{color:var(--brand);box-shadow:inset 0 -2px 0 var(--brand)}
.nav .call{margin-left:.5rem;padding:.55rem .9rem}
.menu-toggle{display:none;margin-left:auto;background:none;border:1.5px solid var(--line);border-radius:3px;padding:.5rem .7rem;color:var(--ink);font:inherit;font-weight:600;cursor:pointer}
@media (max-width:1120px){
  .menu-toggle{display:inline-flex;align-items:center;gap:.5rem}
  .nav{display:none;position:absolute;left:0;right:0;top:100%;flex-direction:column;align-items:stretch;background:var(--surface);border-bottom:1px solid var(--line);padding:.5rem max(16px,env(safe-area-inset-left,0px)) 1rem;gap:.15rem;box-shadow:0 12px 24px -12px rgba(0,0,0,.3)}
  .nav.open{display:flex}
  .nav a{padding:.75rem .6rem;font-size:1.05rem}
  .nav .call{margin:.5rem 0 0;justify-content:center}
}

/* hero */
.hero{position:relative;display:grid;background:#2a1d17;color:#fff}
.hero img{grid-area:1/1;width:100%;aspect-ratio:16/7;max-height:640px;object-fit:cover;object-position:center 60%}
.hero::after{content:"";grid-area:1/1;background:linear-gradient(to top,rgba(20,10,6,.88) 0%,rgba(20,10,6,.58) 50%,rgba(20,10,6,.12) 100%)}
.hero .eyebrow,.hero .lede{text-shadow:0 1px 8px rgba(0,0,0,.45)}
.hero .copy{grid-area:1/1;position:relative;z-index:1;align-self:end;width:100%;padding-block:2.5rem 2.75rem}
.hero .copy .eyebrow{color:#e7c98a}
.hero h1{color:#fff;max-width:16ch;text-shadow:0 2px 14px rgba(0,0,0,.35)}
.hero .lede{color:rgba(255,255,255,.88);max-width:46ch;margin:.9rem 0 1.4rem}
@media (max-width:700px){.hero img{aspect-ratio:4/4.4;max-height:none}.hero .copy{padding-block:1.75rem 2rem}}
.hero.short img{aspect-ratio:16/5.2;min-height:300px;max-height:460px}
@media (max-width:700px){.hero.short img{aspect-ratio:4/3;min-height:0}}
.hero.short h1{font-size:clamp(2rem,4vw,3rem)}

/* strips & bands */
.infostrip{background:var(--surface);border-bottom:1px solid var(--line)}
.infostrip .wrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1rem 2rem;padding-block:1.1rem}
.infostrip .cell{display:flex;gap:.8rem;align-items:flex-start;min-width:0}
.infostrip svg{width:22px;height:22px;flex:none;fill:none;stroke:var(--brass);stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;margin-top:.2rem}
.infostrip .k{font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;color:var(--brass);font-weight:600}
.infostrip .v{font-size:.98rem;line-height:1.45}
section.band{padding-block:clamp(3rem,6vw,5rem)}
section.band.alt{background:var(--surface);border-block:1px solid var(--line)}
section.band.dark{background:var(--brand);color:var(--on-brand)}
section.band.dark .eyebrow{color:#e7c98a}
section.band.dark h2,section.band.dark h3{color:var(--on-brand)}
section.band.dark .lede,section.band.dark .muted{color:rgba(248,241,231,.8)}
section.band.dark a:not(.btn){color:#f3dcb0}
.two{display:grid;grid-template-columns:1.05fr 1fr;gap:clamp(1.5rem,4vw,4rem);align-items:center}
.two>*{min-width:0}
@media (max-width:820px){.two{grid-template-columns:1fr}}
.photo-pair{display:grid;grid-template-columns:1fr 1fr;gap:.75rem}
.photo-pair img{width:100%;aspect-ratio:5/4;object-fit:cover;border-radius:3px}
.photo-pair img:first-child{margin-top:2.5rem}
.photo-pair img:last-child{margin-bottom:2.5rem}
.frame{border-radius:3px;overflow:hidden;background:var(--surface-2)}
.frame img{width:100%;object-fit:cover}
figure{margin:0}
figcaption{font-size:.85rem;color:var(--muted);margin-top:.45rem}

/* cards */
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.25rem}
.card{display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:3px;overflow:hidden;min-width:0}
.card img{width:100%;aspect-ratio:5/3;object-fit:cover}
.card .body{padding:1.1rem 1.2rem 1.3rem;display:flex;flex-direction:column;gap:.5rem;flex:1}
.card h3{font-size:1.25rem}
.card p{margin:0;color:var(--muted);font-size:.98rem}
.card a.more{margin-top:auto;font-weight:600;text-decoration:none}
.card a.more::after{content:" \2192"}

/* photo strip for the pub's panoramic photographs (527x210 originals) */
.strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.75rem}
.strip figure img{width:100%;aspect-ratio:527/210;object-fit:cover;border-radius:3px}
.strip figcaption{font-size:.82rem}

/* menus */
.menu-intro{display:grid;grid-template-columns:1fr auto;gap:1rem 3rem;align-items:end;margin-bottom:2.5rem}
@media (max-width:700px){.menu-intro{grid-template-columns:1fr}}
.served{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--brass);padding:.9rem 1.1rem;font-size:.95rem;border-radius:3px}
.served .k{display:block;font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--brass);font-weight:600;margin-bottom:.2rem}
.menu-section{padding-block:1.75rem;border-top:1px solid var(--line)}
.menu-section h2{font-size:1.5rem;display:flex;align-items:baseline;gap:1rem;flex-wrap:wrap}
.menu-section h2 small{font-family:var(--font-body);font-size:.92rem;color:var(--muted);font-weight:400}
.menu-section .note{color:var(--muted);font-size:.95rem;margin:.35rem 0 1rem}
.items{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:.55rem 3rem}
@media (max-width:760px){.items{grid-template-columns:1fr}}
.item{display:flex;align-items:baseline;gap:.5rem;min-width:0}
.item .n{min-width:0}
.item .n em{font-style:italic;color:var(--muted)}
.item .dots{flex:1;min-width:1.5rem;border-bottom:1px dotted var(--line);transform:translateY(-.3em)}
.item .p{font-variant-numeric:tabular-nums;font-weight:600;white-space:nowrap}
.tag{display:inline-block;font-size:.66rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;background:var(--brass-soft);color:var(--brass);padding:.1rem .4rem;border-radius:2px;margin-left:.35rem;vertical-align:.1em}
.prices{display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem;margin:1.5rem 0}
.prices div{background:var(--surface);border:1px solid var(--line);border-radius:3px;padding:1rem;text-align:center}
.prices .big{font-family:var(--font-head);font-size:1.9rem;line-height:1;margin-top:.2rem}
@media (max-width:520px){.prices{grid-template-columns:1fr}}
.key{font-size:.85rem;color:var(--muted)}

/* lists */
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.75rem;margin:1.5rem 0}
.facts div{background:var(--surface);border:1px solid var(--line);border-radius:3px;padding:.8rem .9rem}
.facts .k{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--brass);font-weight:600}
.facts .v{font-weight:600}
.fixtures{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:.4rem 2rem}
.fixtures li{display:grid;grid-template-columns:11.5rem 1fr;gap:1rem;padding:.55rem 0;border-bottom:1px solid var(--line)}
.fixtures .d{font-weight:600;font-variant-numeric:tabular-nums}
@media (max-width:420px){.fixtures li{grid-template-columns:1fr}}
.places{display:grid;gap:1.25rem}
.place{display:grid;grid-template-columns:260px 1fr;gap:1.25rem;background:var(--surface);border:1px solid var(--line);border-radius:3px;overflow:hidden}
.place .pics{display:grid;grid-template-rows:1fr auto;min-width:0}
.place img{width:100%;height:100%;object-fit:cover;min-height:180px}
.place img.second{aspect-ratio:527/210;min-height:0;height:auto;border-top:2px solid var(--surface)}
.place img.second.logo{object-fit:contain;aspect-ratio:auto;max-height:110px;padding:.6rem;background:var(--surface-2)}
.place .body{padding:1.1rem 1.25rem 1.25rem;min-width:0}
.place dl{display:grid;grid-template-columns:auto 1fr;gap:.2rem 1rem;margin:.75rem 0 0;font-size:.95rem}
.place dt{color:var(--brass);font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;font-weight:600;align-self:baseline;padding-top:.2em}
.place dd{margin:0;word-break:break-word}
@media (max-width:640px){.place{grid-template-columns:1fr}.place img{aspect-ratio:16/9;min-height:0}.place img.second{aspect-ratio:527/210}}

/* news */
.notices{display:grid;gap:1rem}
.notice-card{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--brand);padding:1rem 1.2rem;border-radius:3px}
.notice-card .d{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--brass);font-weight:600}
.notice-card h3{font-size:1.15rem;margin:.2rem 0 .3rem}
.notice-card p{margin:0;color:var(--muted)}
.archive h2{font-size:1.4rem;margin:2.25rem 0 .75rem;padding-bottom:.4rem;border-bottom:1px solid var(--line)}
.post{display:grid;grid-template-columns:7.5rem 1fr;gap:1rem;padding:.9rem 0;border-bottom:1px solid var(--line)}
.post time{font-variant-numeric:tabular-nums;color:var(--muted);font-size:.92rem;padding-top:.15rem}
.post h3{font-size:1.08rem;font-family:var(--font-body);font-weight:600}
.post .c{color:var(--muted);font-size:.97rem}
.post .c p{margin:.3rem 0 0}
@media (max-width:520px){.post{grid-template-columns:1fr;gap:.2rem}}

/* contact */
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:2.5rem}
.contact-grid>*{min-width:0}
@media (max-width:820px){.contact-grid{grid-template-columns:1fr}}
.address{font-style:normal;line-height:1.5}
.big-tel{font-family:var(--font-head);font-size:1.9rem;color:var(--brand);text-decoration:none;display:inline-block;margin:.25rem 0}
.hours{list-style:none;margin:0;padding:0}
.hours li{display:flex;justify-content:space-between;gap:1rem;padding:.45rem 0;border-bottom:1px solid var(--line)}
.hours li span:last-child{font-variant-numeric:tabular-nums;text-align:right}
.social{display:flex;flex-wrap:wrap;gap:.6rem}
.social a{display:inline-flex;align-items:center;gap:.4rem;padding:.45rem .8rem;border:1px solid var(--line);border-radius:3px;text-decoration:none;color:var(--ink);font-weight:600;font-size:.92rem;background:var(--surface)}
form.enquiry{display:grid;gap:.9rem;background:var(--surface);border:1px solid var(--line);border-radius:3px;padding:1.4rem}
form.enquiry .row{display:grid;grid-template-columns:1fr 1fr;gap:.9rem}
@media (max-width:520px){form.enquiry .row{grid-template-columns:1fr}}
form.enquiry label{display:grid;gap:.3rem;font-weight:600;font-size:.92rem}
form.enquiry input,form.enquiry textarea{font:inherit;padding:.6rem .7rem;border:1px solid var(--line);border-radius:3px;background:var(--bg);color:var(--ink);width:100%;min-width:0}
form.enquiry textarea{min-height:110px;resize:vertical}
.form-note{font-size:.9rem;color:var(--muted);margin:0}
.form-done{background:var(--brass-soft);color:var(--ink);padding:.9rem 1rem;border-radius:3px;font-size:.95rem}

/* legal */
.prose{max-width:70ch}
.prose h2{font-size:1.35rem;margin:1.8rem 0 .5rem}
.prose ul{padding-left:1.2rem}

/* footer */
.site-footer{background:var(--surface);border-top:1px solid var(--line);color:var(--muted);font-size:.95rem}
.site-footer .wrap{display:grid;grid-template-columns:1.3fr 1fr 1fr 1fr;gap:2rem;padding-block:3rem 2rem}
.site-footer h4{font-family:var(--font-body);font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;color:var(--brass);margin-bottom:.6rem}
.site-footer ul{list-style:none;margin:0;padding:0;display:grid;gap:.3rem}
.site-footer a{color:var(--ink);text-decoration:none}
.site-footer a:hover{text-decoration:underline}
.site-footer .brand .name{font-size:1.1rem}
.site-footer .legal{border-top:1px solid var(--line)}
.site-footer .legal .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:.5rem 1.5rem;padding-block:1rem;font-size:.85rem}
@media (max-width:900px){.site-footer .wrap{grid-template-columns:1fr 1fr}}
@media (max-width:520px){.site-footer .wrap{grid-template-columns:1fr}}
"""

JS = r"""
(function(){
  var t=document.querySelector('.menu-toggle'),n=document.querySelector('.nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});}
  var f=document.querySelector('form.enquiry');
  if(f){f.addEventListener('submit',function(e){e.preventDefault();var d=document.getElementById('form-done');if(d){d.hidden=false;d.focus();}f.querySelector('button').disabled=true;});}
})();
"""

ACORN = '<svg class="acorn" viewBox="0 0 22 28" aria-hidden="true"><path d="M11 1.2c.4 0 .8.4.8.9v1.6h-1.6V2.1c0-.5.4-.9.8-.9z"/><path d="M3.2 9.5c0-3.4 3.6-5.6 7.8-5.6s7.8 2.2 7.8 5.6c0 .6-.4 1-1 1H4.2c-.6 0-1-.4-1-1z"/><path d="M4.6 12.1h12.8c0 6.2-2.6 11.2-6.4 14.7-3.8-3.5-6.4-8.5-6.4-14.7z"/></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ICON_PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'
ICON_PHONE_FILL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25c1.1.37 2.3.57 3.6.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1L6.6 10.8z"/></svg>'
ICON_BED = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18V8M3 14h18v4M21 14v-3a2 2 0 0 0-2-2h-6v5M7 11h4"/><circle cx="7.5" cy="9" r="1.5"/></svg>'

NAV = [("index.html", "Home"), ("menu.html", "Menu"), ("sunday-lunch.html", "Sunday Lunch"), ("rooms.html", "Rooms"),
       ("private-dining.html", "Private Dining"), ("race-days.html", "Race Days"), ("local-area.html", "Local Area"),
       ("news.html", "News"), ("contact.html", "Contact")]

def header(current):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in NAV if h != "index.html")
    return f"""
<div class="notice"><div class="wrap"><strong>Please note.</strong> {NOTICE}</div></div>
<header class="site-header"><div class="wrap">
  <a class="brand" href="index.html" aria-label="Old Oak Tree, home"><span class="name">OLD OAK TREE</span><span class="sub">Freehold public house &middot; Thirsk</span></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav">Menu <span aria-hidden="true">&#9776;</span></button>
  <nav class="nav" id="nav" aria-label="Main">{links}<a class="btn call" href="tel:+441845523276">{ICON_PHONE_FILL}{PHONE}</a></nav>
</div></header>"""

def footer():
    year = datetime.date.today().year
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div><a class="brand" href="index.html"><span class="name">OLD OAK TREE</span><span class="sub">Freehold public house</span></a>
      <p style="margin-top:1rem">Nick, Laurette, Mollie and Elliot welcome you to our freehouse with home-cooked food and real ales.</p>
      <p>Old Oak Tree, South Kilvington, Thirsk, North Yorkshire YO7 2NL</p></div>
    <div><h4>Food served</h4><ul><li>Mon to Sat: 12 to 2pm, 5 to 8.30pm</li><li>Sunday: 12 to 7.30pm</li><li>Sunday lunch: 12 to 2.30pm</li></ul></div>
    <div><h4>Bookings</h4><ul><li><a href="tel:+441845523276">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{BOOK_ROOMS}" target="_blank" rel="noopener">Book a room online</a></li></ul></div>
    <div><h4>Find us</h4><ul><li><a href="menu.html">Menu</a></li><li><a href="rooms.html">Rooms</a></li><li><a href="race-days.html">Race days</a></li><li><a href="news.html">News</a></li><li><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a></li><li><a href="{TRIPADVISOR}" target="_blank" rel="noopener">TripAdvisor</a></li></ul></div>
  </div>
  <div class="legal"><div class="wrap"><span>&copy; {year} Old Oak Tree. All rights reserved.</span><span><a href="privacy.html">Privacy policy</a> &middot; <a href="terms.html">Terms &amp; conditions</a></span></div></div>
</footer>
<script>{JS}</script>"""

def page(fname, title, body, current=None, desc=""):
    """Full HTML document. Also returns the body-only variant used for the artifact's main page."""
    head_bits = f"""<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{html.escape(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<style>{CSS}</style>"""
    inner = head_bits + "\n" + header(current or fname) + "\n<main>" + body + "\n</main>" + footer()
    full = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head_bits}
</head>
<body>
{header(current or fname)}
<main>{body}
</main>
{footer()}
</body>
</html>"""
    return full, inner

# ---------------------------------------------------------------- menu data (from oldoaktreethirsk.co.uk/our-menu, Oct 2026)
def it(name, price=None, tags=(), desc=None):
    return (name, price, tags, desc)

MENU = [
 ("Starters", None, [
  it("Homemade soup of the day with warm roll", "6.75"), it("Yorkshire pudding with rich onion gravy", "6.75"),
  it("Magic mushrooms", "8.75", desc="in a parsley and garlic sauce topped with mature cheddar"),
  it("Cheesy garlic bread topped with mature cheddar", "6.95"), it("Deep-fried brie with a redcurrant and orange jelly", "8.50"),
  it("Loaded meat or veggie nachos", "8.95", desc="topped with jalapeños, sour cream and cheese"),
  it("Salmon and haddock fishcake with salad and tartare sauce", "8.50"), it("Battered chicken goujons with garlic mayo", "8.50"),
  it("Whitebait, deep fried, with tartare sauce", "7.75"),
  it("Sautéed duck with pancakes", "9.95", desc="spring onion, cucumber and hoisin sauce"),
  it("Black pudding fritters with apple and red onion chutney", "7.95")]),
 ("Main courses", "Served with a selection of vegetables and homemade chips or buttered new potatoes.", [
  it("Steak and ale pie", "17.95", desc="braised steak and Oak Tree ale with homemade shortcrust"),
  it("Oak Tree fish pie", "17.95", ("GF",), desc="haddock, salmon and prawns in a creamy sauce, topped with cheesy mash"),
  it("Chicken breast in a creamy mushroom sauce", "15.95", ("GF",)),
  it("Homemade beef chilli with rice and cheesy nachos", "14.50"),
  it("Honey roast ham, served cold", "14.50", desc="with two fried eggs, Branston pickle, pickled onions and chips"),
  it("Proper pork sausages with creamy mash and red onion gravy", "14.00"),
  it("Our own lasagne with homemade chips and salad", "14.95"),
  it("Breaded wholetail Whitby scampi, homemade chips and tartare sauce", "16.50"),
  it("Fish-and-chip-shop style haddock and chips with mushy peas", "16.95"),
  it("Moby Dick", "21.95", desc="1lb of fresh haddock, chips and mushy peas"),
  it("Two homemade fishcakes with salad and tartare sauce", "15.95"),
  it("Half a roast duck on an orange sauce", "24.95", ("GF",)),
  it("Medallions of pork fillet", "19.95", desc="topped with caramelised onions and Stilton on a red wine sauce"),
  it("Chicken breast stuffed with Wensleydale cheese", "21.95", desc="wrapped in bacon on a creamy Wensleydale sauce"),
  it("Baked salmon fillet on wilted spinach in a white wine sauce", "18.95"),
  it("Grilled salmon and feta on mixed salad, house dressing", "18.50"),
  it("Seafood platter", "22.50", desc="poached salmon, fishcake, battered king prawns, smoked salmon and mini prawn cocktail"),
  it("Two bean and lentil chilli", "14.50", ("GF", "Vegan option"), desc="with rice, sour cream and cheesy nachos"),
  it("Vegetable lasagne topped with tomato sauce and mature cheddar", "14.50", ("V",)),
  it("Thai green vegetable curry in a creamy coconut sauce with rice", "15.95", ("Vegan",)),
  it("Roast spinach, feta and pepper Wellington", "16.95", ("V",), desc="with a tomato and pepper sauce"),
  it("Mushroom stroganoff with rice", "14.95", ("GF", "V")),
  it("Creamy butternut squash linguine with spinach", "16.95", ("Vegan",))]),
 ("Burgers", "Two Oak Tree burgers in each, served with salad and house coleslaw.", [
  it("Classic bacon cheeseburger", "15.50", desc="topped with bacon and cheddar"),
  it("Chilli burger", "16.50", desc="topped with house chilli, cheddar and jalapeños"),
  it("Pulled pork burger", "16.95", desc="with house BBQ pulled pork and cheddar")]),
 ("Parmos", "Served with salad and house coleslaw.", [
  it("Classic parmo", "14.95", desc="topped with béchamel sauce and mature cheddar"),
  it("Hot Shot parmo", "16.50", desc="topped with house chilli, jalapeños, béchamel and cheddar"),
  it("Pulled pork parmo", "16.50", desc="topped with BBQ pulled pork, béchamel and mature cheddar")]),
 ("From the grill", "Served with mushrooms, onion rings and tomato.", [
  it("14oz prime gammon centre-cut steak", "17.00", desc="with fried egg or pineapple"),
  it("12oz local sirloin steak", "29.95"),
  it("Mixed grill", "21.95", desc="pork chop, gammon, beef burger, sausage, black pudding and fried egg")]),
 ("Little Acorns", "For children: £8.50 each, served with mash or chips and vegetables. Just ask when ordering.", [
  it("Our own cheeseburger with chips and tomato sauce"), it("Sausages, egg and chips"), it("Haddock, chips and mushy peas"),
  it("Homemade fishcake and chips"), it("Our own chicken nuggets and chips"), it("Ham, egg and chips"),
  it("Vegetable lasagne", tags=("V",)), it("Butternut squash and spinach linguine", tags=("V", "GF", "Vegan")),
  it("Classic parmo"), it("Chicken stroganoff with rice", tags=("GF",))]),
 ("Sandwiches", "Lunchtime only. In white or brown bread or a white baguette, with dressed leaves, homemade chips and coleslaw.", [
  it("Proper pork sausage and fried egg", "9.95"), it("Hand-carved honey roast ham", "9.95"),
  it("Mature cheddar and Branston pickle", "9.95"), it("Warm tomato, mozzarella and green pesto", "9.95"),
  it("Grilled halloumi, sriracha mayo and salad", "9.95"), it("Roast beef and horseradish", "11.95"),
  it("Warm BLT with mayo", "10.95"), it("Prawn salad and Marie Rose sauce", "12.95"),
  it("Breaded chicken breast with coleslaw and salad", "12.50"), it("Our own fish finger sarnie with breaded haddock", "12.50"),
  it("Oak Tree Club", "13.50", desc="chicken or haddock, lettuce, bacon, tomato and mayo")]),
 ("Light bites", "Lunchtime only.", [
  it("Fresh grilled chicken Caesar salad, dressing and crispy croutons", "14.50"),
  it("Cajun spiced salmon fillet with sour cream and salad", "16.00"),
  it("Sliced smoked salmon with scrambled egg and salad", "16.00"),
  it("Prawn salad with Marie Rose and a warm roll", "16.50"),
  it("Ploughman's with a warm baguette", "14.50", desc="a selection of cheeses and pickles; add ham for £16.50"),
  it("Omelette with salad", "12.95", desc="cheese, cheese and onion, tomato (V) or cheese and ham"),
  it("Hand-carved honey roast ham or roast beef salad with roll and butter", "15.00")]),
]

SUNDAY = {
 "starters": ["Fan of Galia melon with fruit coulis", "Sautéed mushrooms in a creamy garlic sauce", "Chef's soup of the day",
              "Our own fishcake with tartare sauce", "Large homemade Yorkshire pudding in rich gravy"],
 "mains": [("Roast sirloin of beef with homemade Yorkshire pudding", None), ("Roast pork, sausagemeat stuffing and homemade Yorkshire pudding", None),
           ("Chicken breast with a creamy mushroom sauce", None), ("Steak and ale pie with homemade shortcrust", None),
           ("Half a roast duck on an orange sauce", "£4 supplement"), ("Our own lasagne, homemade chips and salad", None),
           ("Oak Tree fish pie", "haddock, salmon and prawns in a creamy sauce topped with cheesy mash"),
           ("Fish and chips", "large chip-shop style fresh haddock and chips with mushy peas"),
           ("Baked salmon fillet on wilted spinach in a white wine sauce", None),
           ("Roast spinach, feta and pepper Wellington with a tomato and pepper sauce (V)", None)],
 "pudding": "A selection of chef's sweets from the board",
}

FIXTURES_2026 = [("Fri 10 April", "Season opener"), ("Sat 18 April", "Afternoon racing"), ("Sat 2 May", "Thirsk Hunt Cup"),
 ("Sat 16 May", "Irish Day"), ("Sun 31 May", "Sunday Series"), ("Fri 5 June", "Afternoon racing"),
 ("Tue 16 June", "Afternoon racing, with coverage of Royal Ascot"), ("Wed 1 July", "Afternoon racing"), ("Thu 16 July", "Afternoon racing"),
 ("Fri 24 July", "Family Day"), ("Sat 1 August", "Summer Cup"), ("Fri 7 August", "Family Day"), ("Fri 14 August", "Evening meeting"),
 ("Fri 28 August", "Family Day"), ("Sat 5 September", "Ladies Day"), ("Mon 14 September", "Season finale")]

PLACES = [
 ("Hambleton Ales", "Microbrewery near Thirsk producing bottled and cask-conditioned ales. You will find their beers on our bar.", "Melmerby", "01765 640108", "https://hambletonbrewery.co.uk", "images/hambleton-brewery.jpg", "Hambleton Brewery bottles", "images/hambleton-logo.png", "Hambleton Brewery logo"),
 ("Mouseman Visitor Centre", "An amazing journey through the life and times of the Mouseman, from humble beginnings to furniture legend, with a tearoom and gift shop stocked with handmade Mouseman pieces.", "Kilburn, Thirsk", "01347 869102", "https://www.robertthompsons.co.uk", "images/mouseman-centre.jpg", "The Mouseman Visitor Centre at Kilburn", "images/mouseman-carving.jpg", "The carved mouse signature on Mouseman furniture"),
 ("The World of James Herriot", "One of the country's premier attractions, paying a unique tribute to the life and times of the author Alf Wight, otherwise known as James Herriot.", "Thirsk", "01845 524234", "https://worldofjamesherriot.com", "images/herriot-museum.jpg", "Inside the World of James Herriot in Thirsk", "images/herriot-sign.jpg", "The brass plate for Mr J A Wight, veterinary surgeon"),
 ("Monk Park Farm", "Children's farm and visitor centre at Bagby, with animals from sheep and horses to wallabies and alpacas, an adventure playground, tea room and gift shop.", "Bagby, Thirsk", "01845 597730", "https://www.monkparkfarm.co.uk", "images/wallaby.jpg", "Feeding a wallaby at Monk Park Farm", "images/monk-park-pony.jpg", "A pony at the fence at Monk Park Farm"),
 ("Thirsk Racecourse", "Country racing at its best, with high-quality racing, good facilities and attractive surroundings. We are on the main road in from the A19.", "Thirsk", "01845 522276", "https://www.thirskracecourse.net", "images/racecourse-stand.jpg", "The grandstand at Thirsk Racecourse", "images/racecourse-paddock.jpg", "Racegoers by the parade ring"),
]

def menu_items(items):
    out = []
    for name, price, tags, desc in items:
        t = "".join(f'<span class="tag">{x}</span>' for x in tags)
        d = f' <em>{desc}</em>' if desc else ""
        p = f'<span class="dots"></span><span class="p">£{price}</span>' if price else ""
        out.append(f'<li class="item"><span class="n">{name}{d}{t}</span>{p}</li>')
    return "\n".join(out)

def strip(photos):
    return '<div class="strip">' + "".join(f'<figure><img src="{s}" alt="{a}" loading="lazy" width="527" height="210"><figcaption>{c}</figcaption></figure>' for s, a, c in photos) + "</div>"

# ---------------------------------------------------------------- pages
def home():
    return f"""
<section class="hero">
  <img src="images/hero-exterior.jpg" alt="The Old Oak Tree, a cream-rendered village pub with a red pantile roof, on a sunny day" fetchpriority="high">
  <div class="copy"><div class="wrap">
    <p class="eyebrow">South Kilvington &middot; Thirsk &middot; North Yorkshire</p>
    <h1>A pub with passion.</h1>
    <p class="lede">A family-run freehouse with home-cooked food, real ales and five en-suite rooms, a mile and a half from Thirsk and just off the A19.</p>
    <div class="btns"><a class="btn light" href="tel:+441845523276">{ICON_PHONE_FILL}Book a table &middot; {PHONE}</a><a class="btn ghost-light" href="{BOOK_ROOMS}" target="_blank" rel="noopener">{ICON_BED}Book a room</a></div>
  </div></div>
</section>
<div class="infostrip"><div class="wrap">
  <div class="cell">{ICON_CLOCK}<div><div class="k">Food served</div><div class="v">Mon to Sat 12 to 2pm and 5 to 8.30pm<br>Sunday 12 to 7.30pm</div></div></div>
  <div class="cell">{ICON_CLOCK}<div><div class="k">Sunday lunch</div><div class="v">Served 12 till 2.30pm<br>One, two or three courses from £19</div></div></div>
  <div class="cell">{ICON_PIN}<div><div class="k">Find us</div><div class="v">Beck Lane, South Kilvington, YO7 2NL<br><a href="contact.html">Map and directions</a></div></div></div>
</div></div>

<section class="band"><div class="wrap two">
  <div>{ACORN}<p class="eyebrow">Totally Yorkshire</p>
    <h2>Nick, Laurette, Mollie and Elliot welcome you to our freehouse.</h2>
    <p class="lede" style="margin-top:1rem">Home-cooked food and real ales in a proper village pub.</p>
    <p>We source our food locally: Nidderdale poultry, beef and lamb, fresh seafood from Redcar and Whitby, and seasonal vegetables from Hambleton Produce. The bar keeps an ever-changing line of guest ales alongside Hambleton beers brewed down the road at Melmerby.</p>
    <p>Alongside the everyday menu there are ever-changing specials boards, sandwiches and light bites over lunch, and a south-facing beer garden for the summer.</p>
    <div class="btns"><a class="btn" href="menu.html">See the menu</a><a class="btn ghost" href="sunday-lunch.html">Sunday lunch</a></div>
  </div>
  <div class="photo-pair">
    <img src="images/bar-ales.jpg" alt="Hand pumps and bottled beers on the bar" loading="lazy">
    <img src="images/food-roast.jpg" alt="Roast duck with green beans and roasted tomatoes" loading="lazy">
  </div>
</div></section>

<section class="band alt"><div class="wrap">
  <p class="eyebrow">Eat, drink, stay</p>
  <h2 style="margin-bottom:1.5rem">What we do</h2>
  <div class="cards">
    <article class="card"><img src="images/pie.jpg" alt="Steak and ale pie with golden shortcrust" loading="lazy"><div class="body"><h3>Our menu</h3><p>Classic pub favourites done properly: steak and ale pie, Whitby scampi, parmos, burgers from the grill and a proper children's menu.</p><a class="more" href="menu.html">Full menu and prices</a></div></article>
    <article class="card"><img src="images/yorkshire-pudding.jpg" alt="A large homemade Yorkshire pudding" loading="lazy"><div class="body"><h3>Sunday lunch</h3><p>Farm-fresh meat and vegetables, homemade Yorkshire puddings and chef's sweets from the board. Served 12 till 2.30pm; takeaway available if you pre-order.</p><a class="more" href="sunday-lunch.html">Sunday menu</a></div></article>
    <article class="card"><img src="images/room-bedroom.jpg" alt="A double bedroom with a flat-screen television" loading="lazy"><div class="body"><h3>Rooms</h3><p>Five modern, bright en-suite rooms and a one-bedroom luxury barn. Bed and breakfast from £70 single and £90 for two. Dogs welcome.</p><a class="more" href="rooms.html">Rooms and rates</a></div></article>
    <article class="card"><img src="images/restaurant-tables.jpg" alt="The restaurant set for a party, with views over the garden" loading="lazy"><div class="body"><h3>Private dining</h3><p>Weddings, birthdays, christenings and anniversaries. The restaurant can be booked exclusively for up to 50 guests.</p><a class="more" href="private-dining.html">Parties and functions</a></div></article>
  </div>
</div></section>

<section class="band dark"><div class="wrap two">
  <div class="frame"><img src="images/racing-finish.jpg" alt="Horses racing to the line at Thirsk" loading="lazy" style="aspect-ratio:527/210"></div>
  <div><p class="eyebrow">Thirsk Races</p><h2>The ideal race-day base.</h2>
    <p class="lede" style="margin-top:.8rem">We are on the main access road into Thirsk, the perfect place for a drink or a meal before and after racing.</p>
    <p>Race-day offers, rooms for the weekend and a restaurant that can be booked for groups. Book early for the big meetings.</p>
    <div class="btns"><a class="btn light" href="race-days.html">Fixtures and offers</a></div></div>
</div></section>

<section class="band"><div class="wrap two" style="align-items:start">
  <div><p class="eyebrow">News</p><h2>Latest from the pub</h2>
    <div class="notices" style="margin-top:1.25rem">
      <div class="notice-card"><div class="d">Closures</div><h3>Closed 9 to 15 November 2026 and 4 to 10 January 2027</h3><p>We will be closed from Monday 9 November and re-open on Monday 16 November 2026. We are also closed from Monday 4 January and re-open on Monday 11 January 2027.</p></div>
      <div class="notice-card"><div class="d">Event</div><h3>Chinese Banquet 2027</h3><p>Limited tables now available for Sunday 31 January 2027 at 8pm. Our annual banquet has run since 2011; call to book.</p></div>
    </div>
    <p style="margin-top:1.25rem"><a href="news.html">All news and past events</a></p>
  </div>
  <div><p class="eyebrow">Around the pub</p><h2>In pictures</h2>
    <div class="strip" style="margin-top:1.25rem;grid-template-columns:1fr 1fr">
      <figure><img src="images/specials-board.jpg" alt="The daily specials chalkboard" loading="lazy"><figcaption>Daily specials</figcaption></figure>
      <figure><img src="images/pub-seating.jpg" alt="Tables and chairs in the pub bar" loading="lazy"><figcaption>Seating in the pub and bar</figcaption></figure>
      <figure><img src="images/room-tray.jpg" alt="Tea tray with kettle, cups and glasses in a bedroom" loading="lazy"><figcaption>In the rooms</figcaption></figure>
      <figure><img src="images/exterior-sign.jpg" alt="The pub sign and frontage from the road" loading="lazy"><figcaption>Find us just off the A19</figcaption></figure>
    </div>
  </div>
</div></section>"""

def menu_page():
    sections = "".join(f"""
<section class="menu-section" id="{re.sub('[^a-z]+','-',h.lower()).strip('-')}"><h2>{h}{f'<small>{note}</small>' if note else ''}</h2><ul class="items">{menu_items(items)}</ul></section>""" for h, note, items in MENU)
    return f"""
<section class="hero short"><img src="images/specials-board.jpg" alt="The specials chalkboard listing the day's dishes" fetchpriority="high"><div class="copy"><div class="wrap"><p class="eyebrow">Served every day except Sunday lunch</p><h1>Our menu</h1></div></div></section>
<section class="band"><div class="wrap">
  <div class="menu-intro"><div class="measure"><p class="lede">Classic pub favourites, home-cooked. In addition to the everyday menu below we have ever-changing specials boards, and sandwiches and light bites over lunch.</p>
    <p class="key"><span class="tag" style="margin-left:0">GF</span> gluten free &nbsp; <span class="tag" style="margin-left:0">V</span> vegetarian &nbsp; <span class="tag" style="margin-left:0">Vegan</span> vegan. Please tell us about any allergies when you order.</p></div>
    <div class="served"><span class="k">Food served</span>Mon to Sat 12 to 2pm and 5 to 8.30pm<br>Sunday 12 to 7.30pm (see <a href="sunday-lunch.html">Sunday lunch</a>)<br><span class="k" style="margin-top:.6rem">Takeaway</span>Pre-order for collection during food service: phone {PHONE} with your order and collection time.</div></div>
  {sections}
  <section class="menu-section"><h2>Something sweet</h2><p class="note">Ask to see the sweets board. Chef's puddings change daily.</p></section>
  <div style="margin-top:2.5rem">{strip([("images/pie.jpg","Steak and ale pie","Steak and ale pie"),("images/fish-and-chips.jpg","Battered haddock, chips, mushy peas and tartare sauce","Fish and chips"),("images/veg-pasta.jpg","Butternut squash pasta with rocket","Fresh vegetarian options"),("images/pint-and-pie.jpg","A pint of ale and a pie on the bar","Pie and a pint")])}</div>
</div></section>"""

def sunday_page():
    starters = "".join(f'<li class="item"><span class="n">{s}</span></li>' for s in SUNDAY["starters"])
    mains = "".join(f'<li class="item"><span class="n">{n}{f" <em>{d}</em>" if d else ""}</span></li>' for n, d in SUNDAY["mains"])
    return f"""
<section class="hero short"><img src="images/roast-beef.jpg" alt="Slices of pink roast beef" fetchpriority="high"><div class="copy"><div class="wrap"><p class="eyebrow">Served 12 till 2.30pm</p><h1>Sunday lunch</h1></div></div></section>
<section class="band"><div class="wrap">
  <div class="two" style="align-items:start"><div class="measure"><p class="lede">Farm-fresh meat and vegetables in a traditional Sunday lunch, with large homemade Yorkshire puddings and chef's sweets from the board.</p>
    <p>Sunday lunch is popular, so please book. Everything on the Sunday menu is available to take away if you pre-order.</p>
    <div class="prices"><div><div class="eyebrow" style="margin:0">One course</div><div class="big">£19</div></div><div><div class="eyebrow" style="margin:0">Two courses</div><div class="big">£26</div></div><div><div class="eyebrow" style="margin:0">Three courses</div><div class="big">£33</div></div></div>
    <div class="btns"><a class="btn" href="tel:+441845523276">{ICON_PHONE_FILL}Book &middot; {PHONE}</a></div></div>
    <div>{strip([("images/yorkshire-pudding.jpg","A large homemade Yorkshire pudding","Homemade Yorkshire puddings"),("images/salmon.jpg","Salmon fillet with a fork","Fresh seafood from Redcar and Whitby"),("images/veg-pasta.jpg","Butternut squash pasta","Fresh and tasty vegetarian options"),("images/food-roast.jpg","Roast duck with vegetables","Delicious locally sourced produce")]).replace('class="strip"','class="strip" style="grid-template-columns:1fr 1fr"')}</div></div>
  <section class="menu-section" style="margin-top:2rem"><h2>To start</h2><ul class="items">{starters}</ul></section>
  <section class="menu-section"><h2>Main courses<small>with farm-fresh vegetables</small></h2><ul class="items">{mains}</ul></section>
  <section class="menu-section"><h2>To finish</h2><ul class="items"><li class="item"><span class="n">{SUNDAY["pudding"]}</span></li></ul></section>
  <p class="key" style="margin-top:1.5rem">On Sundays the everyday menu is not served over lunch; it returns after 2.30pm until 7.30pm.</p>
</div></section>"""

def rooms_page():
    return f"""
<section class="hero short"><img src="images/exterior.jpg" alt="The Old Oak Tree pub frontage with hanging baskets" fetchpriority="high" style="object-position:center 55%"><div class="copy"><div class="wrap"><p class="eyebrow">Bed and breakfast in South Kilvington</p><h1>Rooms</h1></div></div></section>
<section class="band"><div class="wrap">
  <div class="two" style="align-items:start">
    <div class="measure"><p class="lede">Five en-suite rooms, modern and bright with the very best of facilities, in the delightful village of South Kilvington just 1.5 miles from Thirsk.</p>
      <p><strong>One-bedroom luxury barn now available.</strong> The barn is let on direct bookings only, so please call us.</p>
      <p>Dogs are welcome at £10 per night. And you have the added benefit of being on the doorstep of a great pub and restaurant: browse <a href="menu.html">our menu</a> or find out more about the <a href="private-dining.html">restaurant</a>.</p>
      <div class="facts">
        <div><div class="k">Rooms</div><div class="v">5 en-suite, plus the barn</div></div><div><div class="k">Children</div><div class="v">Welcome</div></div>
        <div><div class="k">Internet</div><div class="v">Yes</div></div><div><div class="k">Parking</div><div class="v">Yes, on site</div></div>
        <div><div class="k">Dogs</div><div class="v">£10 per night</div></div><div><div class="k">Smoking</div><div class="v">No</div></div>
      </div>
      <h2 style="font-size:1.5rem;margin:1.5rem 0 .5rem">Rates</h2>
      <p>Bed and breakfast for two is from <strong>£90</strong> and from <strong>£70</strong> for single occupancy, with a full Yorkshire breakfast. For the best available rates, give us a call and book direct on {PHONE}.</p>
      <div class="btns"><a class="btn" href="{BOOK_ROOMS}" target="_blank" rel="noopener">{ICON_BED}Check availability and book</a><a class="btn ghost" href="tel:+441845523276">{ICON_PHONE_FILL}{PHONE}</a></div>
    </div>
    <div>{strip([("images/room-bedroom.jpg","A double room with a television and bedside lamps","Modern, bright rooms"),("images/room-bathroom.jpg","An en-suite bathroom with bath, basin and toilet","Every room is en suite"),("images/room-tray.jpg","A hospitality tray with kettle, cups and bottled water","Tea and coffee in the room")]).replace('class="strip"','class="strip" style="grid-template-columns:1fr"')}</div>
  </div>
</div></section>
<section class="band alt"><div class="wrap two" style="align-items:start">
  <div><p class="eyebrow">Motorhomes and campervans</p><h2 style="font-size:1.6rem">Free stopovers for diners</h2><p style="margin-top:.75rem">We are happy to welcome motorhomes and campervans for free overnight stopovers. You must dine with us, and please book in advance.</p></div>
  <div><p class="eyebrow">Race weekends</p><h2 style="font-size:1.6rem">Book early for Thirsk Races</h2><p style="margin-top:.75rem">The rooms fill quickly around race meetings. See the <a href="race-days.html">fixture list</a> and book your accommodation as soon as the dates are out.</p></div>
</div></section>"""

def dining_page():
    return f"""
<section class="hero short"><img src="images/restaurant-tables.jpg" alt="Long tables set in the restaurant with garden views" fetchpriority="high"><div class="copy"><div class="wrap"><p class="eyebrow">Restaurant, parties and functions</p><h1>Private dining</h1></div></div></section>
<section class="band"><div class="wrap two" style="align-items:start">
  <div class="measure"><p class="lede">Our purpose-built restaurant seats up to 50, with open views across the garden and an emphasis on local, seasonal ingredients and traditional pub favourites.</p>
    <p>Whether it is a wedding, birthday, christening or special anniversary, we will do our best to cater for your individual requirements. The restaurant can be booked exclusively for up to 50 guests.</p>
    <p>Menus can be arranged to suit your budget, from a full sit-down meal to a buffet. Please call us to discuss what you have in mind.</p>
    <h2 style="font-size:1.5rem;margin:1.5rem 0 .5rem">Events through the year</h2>
    <p>Our <strong>Chinese Banquet</strong> has run every winter since 2011 and sells out; the next is Sunday 31 January 2027 at 8pm. <strong>Christmas</strong> party menus run through December and Christmas Day lunch books up well in advance. We also run theme nights and the occasional charity event; see <a href="news.html">news</a> for what is coming up.</p>
    <div class="btns"><a class="btn" href="tel:+441845523276">{ICON_PHONE_FILL}Book now &middot; {PHONE}</a><a class="btn ghost" href="contact.html">Send an enquiry</a></div>
  </div>
  <div>{strip([("images/restaurant-room.jpg","The restaurant with oak tables and chairs","Our newly built restaurant"),("images/pub-seating.jpg","Seating in the bar","Further seating in the pub and bar"),("images/food-roast.jpg","A plate of roast duck","Delicious locally sourced produce"),("images/bar-ales.jpg","Beer pumps on the bar","Ever-changing guest ales")]).replace('class="strip"','class="strip" style="grid-template-columns:1fr 1fr"')}</div>
</div></section>"""

def races_page():
    fx = "".join(f'<li><span class="d">{d}</span><span>{n}</span></li>' for d, n in FIXTURES_2026)
    return f"""
<section class="hero short"><img src="images/racing-finish.jpg" alt="Jockeys and horses in full flight at Thirsk" fetchpriority="high"><div class="copy"><div class="wrap"><p class="eyebrow">Thirsk Racecourse</p><h1>Race days</h1></div></div></section>
<section class="band"><div class="wrap two" style="align-items:start">
  <div class="measure"><p class="lede">Conveniently situated on the main access road into Thirsk, the Old Oak Tree is the ideal place for a pre- or post-race drink or meal.</p>
    <p>With special race-day offers and an ideal location, we are the perfect place to make a day of the races. Our restaurant can be booked for groups and private functions, and our <a href="rooms.html">rooms</a> make a comfortable base for a race weekend.</p>
    <div class="btns"><a class="btn" href="tel:+441845523276">{ICON_PHONE_FILL}Book &middot; {PHONE}</a><a class="btn ghost" href="contact.html">How to find us</a></div>
  </div>
  <div>{strip([("images/racecourse-paddock.jpg","Racegoers by the parade ring at Thirsk","Thirsk Races"),("images/racing-group.jpg","A tight finish on the turf","Top-class racing"),("images/racecourse-stand.jpg","The grandstand at Thirsk Racecourse","Country racing at its finest"),("images/map-area.jpg","Map showing South Kilvington just north of Thirsk on the A19","Just off the A19")]).replace('class="strip"','class="strip" style="grid-template-columns:1fr 1fr"')}</div>
</div></section>
<section class="band alt"><div class="wrap">
  <p class="eyebrow">Thirsk Racecourse</p><h2 style="margin-bottom:1.25rem">Fixtures 2026</h2>
  <ul class="fixtures">{fx}</ul>
  <p class="key" style="margin-top:1.25rem">Dates are set by Thirsk Racecourse; check <a href="https://www.thirskracecourse.net" target="_blank" rel="noopener">thirskracecourse.net</a> for the next season's list, and book your table or room early for the big meetings.</p>
</div></section>"""

def local_page():
    cards = "".join(f"""
<article class="place"><div class="pics"><img src="{img}" alt="{alt}" loading="lazy"><img src="{img2}" alt="{alt2}" loading="lazy" class="second{' logo' if img2.endswith('.png') else ''}"></div><div class="body"><h3>{n}</h3><p style="margin:.4rem 0 0;color:var(--muted)">{d}</p>
<dl><dt>Where</dt><dd>{loc}</dd><dt>Phone</dt><dd>{ph}</dd><dt>Website</dt><dd><a href="{url}" target="_blank" rel="noopener">{url.replace('https://','')}</a></dd></dl></div></article>""" for n, d, loc, ph, url, img, alt, img2, alt2 in PLACES)
    return f"""
<section class="hero short"><img src="images/herriot-sign.jpg" alt="The brass plate for Mr J A Wight, veterinary surgeon, at the World of James Herriot" fetchpriority="high"><div class="copy"><div class="wrap"><p class="eyebrow">Thirsk and the Hambleton hills</p><h1>Local area</h1></div></div></section>
<section class="band"><div class="wrap">
  <p class="lede measure">Why not explore some of the attractions close by? Thirsk, the market town of the James Herriot books, is a mile and a half down the road, with the North York Moors and the Dales within easy reach.</p>
  <div class="places" style="margin-top:2rem">{cards}</div>
</div></section>"""

def news_page(posts):
    def clean(h):
        h = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", h, flags=re.S | re.I)
        h = re.sub(r'<a\s', '<a target="_blank" rel="noopener" ', h)
        h = re.sub(r"<(?!/?(p|br|a|strong|em|b|i|ul|ol|li)\b)[^>]+>", "", h)
        h = re.sub(r"<p>\s*(&nbsp;|\s)*</p>", "", h)
        return h.strip()
    by_year = {}
    for p in sorted(posts, key=lambda p: p["date"], reverse=True):
        by_year.setdefault(p["date"][:4], []).append(p)
    out = []
    for y, ps in by_year.items():
        out.append(f'<h2 id="y{y}">{y}</h2>')
        for p in ps:
            d = datetime.date.fromisoformat(p["date"][:10]).strftime("%-d %b %Y")
            out.append(f'<article class="post"><time datetime="{p["date"][:10]}">{d}</time><div><h3>{p["title"]["rendered"]}</h3><div class="c">{clean(p["content"]["rendered"])}</div></div></article>')
    return f"""
<section class="band"><div class="wrap">
  <p class="eyebrow">News and notices</p><h1 style="font-size:clamp(2rem,4vw,2.8rem)">What's on at the Oak Tree</h1>
  <div class="notices" style="margin:1.5rem 0 0;max-width:70ch">
    <div class="notice-card"><div class="d">Closures</div><h3>Closed 9 to 15 November 2026 and 4 to 10 January 2027</h3><p>We will be closed from Monday 9 November and re-open on Monday 16 November 2026. We are also closed from Monday 4 January and re-open on Monday 11 January 2027.</p></div>
    <div class="notice-card"><div class="d">Event</div><h3>Chinese Banquet 2027</h3><p>Limited tables now available for Sunday 31 January 2027 at 8pm. Call {PHONE} to book.</p></div>
  </div>
  <div class="archive" style="max-width:70ch"><p class="eyebrow" style="margin-top:3rem">Archive</p><p class="muted">Every notice we have posted since the site began in 2011, newest first.</p>{"".join(out)}</div>
</div></section>"""

def contact_page():
    return f"""
<section class="band"><div class="wrap">
  <p class="eyebrow">Contact and directions</p><h1 style="font-size:clamp(2rem,4vw,2.8rem);margin-bottom:1.5rem">Find us</h1>
  <div class="contact-grid">
    <div>
      <address class="address"><strong>Old Oak Tree</strong><br>Beck Lane, South Kilvington<br>Thirsk, North Yorkshire<br>YO7 2NL</address>
      <a class="big-tel" href="tel:+441845523276">{PHONE}</a><br>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <p style="margin-top:1rem">To book a table, do it the old-fashioned personal way and give us a call. For rooms, use the <a href="{BOOK_ROOMS}" target="_blank" rel="noopener">online booking system</a> or call us for our best available rates.</p>
      <h2 style="font-size:1.35rem;margin:1.5rem 0 .5rem">Food served</h2>
      <ul class="hours"><li><span>Monday to Saturday</span><span>12 to 2pm, 5 to 8.30pm</span></li><li><span>Sunday</span><span>12 to 7.30pm</span></li><li><span>Sunday lunch menu</span><span>12 to 2.30pm</span></li></ul>
      <h2 style="font-size:1.35rem;margin:1.5rem 0 .5rem">Getting here</h2>
      <p>South Kilvington is just off the A19 on the main road into Thirsk, 1.5 miles from the town centre and the racecourse. There is parking at the pub.</p>
      <div class="btns" style="margin-bottom:1.5rem"><a class="btn ghost" href="{MAPS}" target="_blank" rel="noopener">{ICON_PIN.replace('aria-hidden="true"','aria-hidden="true" style="fill:none;stroke:currentColor;stroke-width:1.8"')}Open in Google Maps</a></div>
      <div class="social"><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a><a href="{TWITTER}" target="_blank" rel="noopener">Twitter</a><a href="{TRIPADVISOR}" target="_blank" rel="noopener">TripAdvisor</a></div>
    </div>
    <div>
      <figure class="frame"><img src="images/map-directions.jpg" alt="Map: South Kilvington sits on the A61 just north of Thirsk, between the A19 and the racecourse" width="558" height="340"><figcaption style="padding:.6rem .8rem">We are here: north of Thirsk on the road in from the A19, with the racecourse on the west side of town.</figcaption></figure>
      <form class="enquiry" style="margin-top:1.5rem" novalidate>
        <h2 style="font-size:1.35rem">Booking enquiry</h2>
        <div class="row"><label>Name<input id="f-name" name="name" type="text" autocomplete="name" required></label><label>Phone<input id="f-phone" name="phone" type="tel" autocomplete="tel"></label></div>
        <label>Email<input id="f-email" name="email" type="email" autocomplete="email" required></label>
        <div class="row"><label>Check-in date<input id="f-in" name="checkin" type="date"></label><label>Check-out date<input id="f-out" name="checkout" type="date"></label></div>
        <label>Comments<textarea id="f-comments" name="comments" placeholder="Number of guests, dogs, a table as well as a room, anything else we should know"></textarea></label>
        <button class="btn" type="submit">Send enquiry</button>
        <p class="form-note">Enquiries are not confirmed bookings. For same-day tables please phone.</p>
        <div class="form-done" id="form-done" hidden tabindex="-1">Thank you. This preview site does not send messages yet; please call {PHONE} or email {EMAIL} and we will get straight back to you.</div>
      </form>
    </div>
  </div>
</div></section>"""

PRIVACY = f"""
<p>This privacy policy sets out how the Old Oak Tree uses and protects any information that you give the Old Oak Tree when you use this website.</p>
<p>The Old Oak Tree is committed to ensuring that your privacy is protected. Should we ask you to provide certain information by which you can be identified when using this website, then you can be assured that it will only be used in accordance with this privacy statement.</p>
<p>The Old Oak Tree may change this policy from time to time by updating this page. You should check this page from time to time to ensure that you are happy with any changes. This policy is effective from 1 March 2011.</p>
<h2>What we collect</h2><p>We may collect the following information:</p>
<ul><li>name</li><li>contact information including email address</li><li>demographic information such as postcode, preferences and interests</li><li>other information relevant to customer surveys and/or offers</li></ul>
<h2>What we do with the information we gather</h2><p>We require this information to understand your needs and provide you with a better service, and in particular for the following reasons:</p>
<ul><li>Internal record keeping.</li><li>We may use the information to improve our products and services.</li><li>We may periodically send promotional emails about new products, special offers or other information which we think you may find interesting using the email address which you have provided.</li><li>From time to time, we may also use your information to contact you for market research purposes. We may contact you by email, phone, fax or mail. We may use the information to customise the website according to your interests.</li></ul>
<h2>Security</h2><p>We are committed to ensuring that your information is secure. In order to prevent unauthorised access or disclosure, we have put in place suitable physical, electronic and managerial procedures to safeguard and secure the information we collect online.</p>
<h2>How we use cookies</h2><p>A cookie is a small file which asks permission to be placed on your computer's hard drive. Once you agree, the file is added and the cookie helps analyse web traffic or lets you know when you visit a particular site. Cookies allow web applications to respond to you as an individual. The web application can tailor its operations to your needs, likes and dislikes by gathering and remembering information about your preferences.</p>
<p>We use traffic log cookies to identify which pages are being used. This helps us analyse data about webpage traffic and improve our website in order to tailor it to customer needs. We only use this information for statistical analysis purposes and then the data is removed from the system.</p>
<p>Overall, cookies help us provide you with a better website by enabling us to monitor which pages you find useful and which you do not. A cookie in no way gives us access to your computer or any information about you, other than the data you choose to share with us.</p>
<p>You can choose to accept or decline cookies. Most web browsers automatically accept cookies, but you can usually modify your browser setting to decline cookies if you prefer. This may prevent you from taking full advantage of the website.</p>
<h2>Links to other websites</h2><p>Our website may contain links to other websites of interest. However, once you have used these links to leave our site, you should note that we do not have any control over that other website. Therefore, we cannot be responsible for the protection and privacy of any information which you provide whilst visiting such sites and such sites are not governed by this privacy statement. You should exercise caution and look at the privacy statement applicable to the website in question.</p>
<h2>Controlling your personal information</h2><p>You may choose to restrict the collection or use of your personal information in the following ways:</p>
<ul><li>whenever you are asked to fill in a form on the website, look for the box that you can click to indicate that you do not want the information to be used by anybody for direct marketing purposes</li><li>if you have previously agreed to us using your personal information for direct marketing purposes, you may change your mind at any time by writing to or emailing us at laurette@oldoaktreethirsk.co.uk</li></ul>
<p>We will not sell, distribute or lease your personal information to third parties unless we have your permission or are required by law to do so. We may use your personal information to send you promotional information about third parties which we think you may find interesting if you tell us that you wish this to happen.</p>
<p>You may request details of personal information which we hold about you under the Data Protection Act 1998. A small fee will be payable. If you would like a copy of the information held on you please send an email to laurette@oldoaktreethirsk.co.uk.</p>
<p>If you believe that any information we are holding on you is incorrect or incomplete, please write to or email us as soon as possible at the above email address. We will promptly correct any information found to be incorrect.</p>"""

TERMS = """
<p>Welcome to our website. If you continue to browse and use this website, you are agreeing to comply with and be bound by the following terms and conditions of use, which together with our privacy policy govern the Old Oak Tree's relationship with you in relation to this website. If you disagree with any part of these terms and conditions, please do not use our website.</p>
<p>The term 'Old Oak Tree' or 'us' or 'we' refers to the owner of the website. The term 'you' refers to the user or viewer of our website.</p>
<p>The use of this website is subject to the following terms of use:</p>
<ul><li>The content of the pages of this website is for your general information and use only. It is subject to change without notice.</li>
<li>Neither we nor any third parties provide any warranty or guarantee as to the accuracy, timeliness, performance, completeness or suitability of the information and materials found or offered on this website for any particular purpose. You acknowledge that such information and materials may contain inaccuracies or errors and we expressly exclude liability for any such inaccuracies or errors to the fullest extent permitted by law.</li>
<li>Your use of any information or materials on this website is entirely at your own risk, for which we shall not be liable. It shall be your own responsibility to ensure that any products, services or information available through this website meet your specific requirements.</li>
<li>This website contains material which is owned by or licensed to us. This material includes, but is not limited to, the design, layout, look, appearance and graphics. Reproduction is prohibited other than in accordance with the copyright notice, which forms part of these terms and conditions.</li>
<li>All trade marks reproduced in this website which are not the property of, or licensed to, the operator are acknowledged on the website.</li>
<li>Unauthorised use of this website may give rise to a claim for damages and/or be a criminal offence.</li>
<li>From time to time this website may also include links to other websites. These links are provided for your convenience to provide further information. They do not signify that we endorse the website(s). We have no responsibility for the content of the linked website(s).</li>
<li>Your use of this website and any dispute arising out of such use of the website is subject to the laws of England, Northern Ireland, Scotland and Wales.</li></ul>"""

def legal_page(title, body):
    return f'<section class="band"><div class="wrap"><p class="eyebrow">Legal</p><h1 style="font-size:clamp(2rem,4vw,2.8rem)">{title}</h1><div class="prose" style="margin-top:1.5rem">{body}</div></div></section>'

def main():
    api = json.load(open(API))
    pages = {
      "index.html": ("Old Oak Tree, Thirsk", home(), "Family-run freehouse in South Kilvington near Thirsk with home-cooked food, real ales, Sunday lunch and five en-suite rooms."),
      "menu.html": ("Menu · Old Oak Tree", menu_page(), "The everyday menu at the Old Oak Tree, South Kilvington: starters, mains, burgers, parmos, grill, children's menu, sandwiches and light bites."),
      "sunday-lunch.html": ("Sunday Lunch · Old Oak Tree", sunday_page(), "Traditional Sunday lunch at the Old Oak Tree, Thirsk, served 12 till 2.30pm. One, two or three courses."),
      "rooms.html": ("Rooms · Old Oak Tree", rooms_page(), "Five en-suite bed and breakfast rooms and a luxury barn at the Old Oak Tree, South Kilvington, 1.5 miles from Thirsk."),
      "private-dining.html": ("Private Dining · Old Oak Tree", dining_page(), "Weddings, parties and functions for up to 50 guests in the Old Oak Tree restaurant, Thirsk."),
      "race-days.html": ("Race Days · Old Oak Tree", races_page(), "Thirsk Racecourse fixtures and race-day food, drink and rooms at the Old Oak Tree, on the main road into Thirsk."),
      "local-area.html": ("Local Area · Old Oak Tree", local_page(), "Things to do near the Old Oak Tree: Hambleton Ales, the Mouseman Visitor Centre, the World of James Herriot, Monk Park Farm and Thirsk Racecourse."),
      "news.html": ("News · Old Oak Tree", news_page(api["posts"]), "Closures, events and notices from the Old Oak Tree, South Kilvington, with the full archive since 2011."),
      "contact.html": ("Contact · Old Oak Tree", contact_page(), "Phone, email, address, food times, map and a booking enquiry form for the Old Oak Tree, South Kilvington, Thirsk YO7 2NL."),
      "privacy.html": ("Privacy Policy · Old Oak Tree", legal_page("Privacy policy", PRIVACY), "How the Old Oak Tree uses information given through this website."),
      "terms.html": ("Terms & Conditions · Old Oak Tree", legal_page("Terms and conditions", TERMS), "Terms of use for the Old Oak Tree website."),
    }
    art = os.path.join(HERE, "..", "artifact"); os.makedirs(art, exist_ok=True)
    for fname, (title, body, desc) in pages.items():
        full, inner = page(fname, title, body, fname, desc)
        open(os.path.join(HERE, fname), "w").write(full)
        if fname == "index.html":
            open(os.path.join(art, "index.html"), "w").write(inner)
    print("built", len(pages), "pages")

if __name__ == "__main__":
    main()
