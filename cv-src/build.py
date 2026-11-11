#!/usr/bin/env python3
"""Generate cv_en.html / cv_fr.html. Export to PDF with:
chromium --headless --no-pdf-header-footer --print-to-pdf=../CV_VEDANI_EN.pdf cv_en.html
"""
from pathlib import Path

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Montserrat:wght@300;400;500;600;700&display=swap');
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --teal:#1d4851; --text:#2b4e57; --soft:#5f7d83; }
html, body { width:210mm; height:296mm; background:#fff; overflow:hidden; }
body { font-family:'Montserrat',sans-serif; font-weight:400; color:var(--text);
       font-size:9pt; line-height:1.4; position:relative; overflow:hidden;
       -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.deco { position:absolute; background:var(--teal); z-index:0; }
.d1 { left:-20mm; top:-30mm; width:78mm; height:110mm; transform:rotate(38deg); border-radius:0 0 0 60mm; }
.d1b{ left:-14mm; top:-34mm; width:80mm; height:112mm; transform:rotate(38deg); border-radius:0 0 0 60mm;
      background:transparent; border-left:1.6mm solid #fff; }
.d2 { right:-10mm; top:-14mm; width:30mm; height:30mm; border-radius:50%; }
.d3 { right:6mm; top:-6mm; width:16mm; height:16mm; border-radius:50%; background:#3d6670; }
.d4 { left:-14mm; bottom:-16mm; width:38mm; height:38mm; border-radius:50%; }
.d5 { left:16mm; bottom:-8mm; width:16mm; height:16mm; border-radius:50%; background:#3d6670; }
.photo { position:absolute; left:20mm; top:10mm; width:40mm; height:40mm; border-radius:50%;
         overflow:hidden; border:1.2mm solid #fff; z-index:2; background:#fff; }
.photo img { width:100%; height:100%; object-fit:cover; }
.name { position:absolute; left:74mm; right:12mm; top:7mm; text-align:center; z-index:2;
        font-family:'Archivo Black',sans-serif; color:var(--teal); font-size:24pt; letter-spacing:3.5pt; line-height:1.15; }
.summary { position:absolute; left:74mm; right:12mm; top:36mm; text-align:center; font-size:8.8pt; z-index:2; }
.left  { position:absolute; left:0; width:59mm; top:%LEFTTOP%; z-index:2; }
.right { position:absolute; left:62mm; right:6mm; top:%RIGHTTOP%; z-index:2; }
h2 { background:var(--teal); color:#fff; font-weight:600; font-size:9pt; letter-spacing:3pt;
     text-align:center; padding:1.6mm 0; margin:0 0 2.6mm; text-transform:uppercase; }
.left h2 { margin-top:6mm; }
.left h2:first-child { margin-top:0; }
.left .blk { padding:0 4mm 0 7mm; }
.contact div { display:flex; align-items:center; gap:3mm; margin:2.4mm 0; font-size:8.8pt; }
.ico { width:6mm; height:6mm; border-radius:50%; background:var(--teal); color:#fff; flex:none;
       display:flex; align-items:center; justify-content:center; font-size:7pt; }
.left ul { list-style:disc; padding-left:4mm; }
.left li { margin:1.2mm 0; }
.right section { margin-bottom:4.4mm; }
.edu { margin-bottom:2.2mm; padding-left:1mm; }
.edu .s { text-decoration:underline; font-weight:500; }
.edu .y { font-weight:600; }
.edu .now { color:var(--teal); font-weight:600; }
.xp { margin:0 0 2.4mm; padding-left:3mm; position:relative; }
.xp::before { content:''; position:absolute; left:0; top:2.1mm; width:1.6mm; height:0.45mm; background:var(--text); }
.xp .t { font-weight:600; }
.xp .y { font-weight:600; color:var(--teal); }
.xp ul { padding-left:4mm; margin-top:0.4mm; }
.proj { display:flex; gap:4mm; align-items:flex-start; }
.proj .list { flex:1; }
.proj .k { text-decoration:underline; font-weight:500; margin-top:1.4mm; }
.proj ul { padding-left:8mm; }
.qr { width:22mm; height:22mm; margin-top:3mm; image-rendering:pixelated; }
"""

L = {
"en": dict(
 lang="en", leftTop="84mm", rightTop="58mm",
 summary="Currently a <b>second-year engineering student at ENSEEIHT</b> in a work-study program (FISA) and apprentice software engineer at Kyber, I am looking to <b>spend a semester (six months) studying abroad</b>. Passionate about electronics and embedded systems, I aim to deepen my technical skills in an international environment.",
 h_contact="Contact", h_skills="Skills", h_lang="Languages", h_hob="Hobbies and interests",
 h_edu="Education", h_xp="Experience", h_proj="Accomplished projects",
 skills=["Programming languages:<br>Rust, Python, Java, C, C++, OCaml, VHDL, Promela, CUDA, JavaScript, WebAssembly",
         "Tools: ROS, Docker, Git, embedded Linux, LaTeX", "Strong work ethic", "Team-oriented", "Curious"],
 langs=["English C1 / Spanish B2", "Working knowledge of Literary Arabic and Russian"],
 hobbies=["Swimming", "Tracking planes on FlightRadar", "Traveling"],
 edu=[("ENSEEIHT – Toulouse INP (31):", "2025 – present:", "Engineering degree in Digital Sciences – Computer Science &amp; Networks, work-study program (FISA). <span class='now'>Currently in 2nd year.</span>"),
      ("Université Toulouse III – Paul Sabatier (31):", "2024 – 2025:", "MSc Year 1 (Embedded and Connected Systems: Infrastructure and Software)"),
      ("Aix-Marseille Université (13):", "2022 – 2024:", "Double Major in Mathematics and Computer Science"),
      ("Classe préparatoire, Lycée Thiers, Marseille (13):", "2020 – 2022:", "Intensive Preparatory Classes for Grandes Écoles (BCPST track: Biology, Chemistry, Physics and Earth Sciences)")],
 xp=[("Kyber, Paris (75) – Apprentice Software Engineer (FISA)", "Since October 2025",
      ["Developing an SDK with ultra-low latency (&lt; 20 ms) remote control capabilities.",
       "Network protocols based on QUIC and WebTransport; Rust/WebAssembly codebase."]),
     ("IRIT, Toulouse (31)", "May – July 2025", ["Master's First Year (M1) Validation Project: Optimization of eXecution Decision Diagrams (XDD)"]),
     ("LIS (CNRS Joint Research Unit), Marseille (13)", "June – July 2023", ["Dual Bachelor's Degree Validation Internship: Research on Probabilistic Automata"]),
     ("Parkours Tutor, Marseille (13), Toulouse (31)", "Since October 2022", ["Academic support and homework assistance for high school students."])],
 proj=[(None, ["Integration of an MCP server with a local LLM", "Autonomous sailboat model"]),
       ("Python:", ["Design of an AI-based image classifier", "Implementation of a state-reduction algorithm for a probabilistic automaton"]),
       ("Java:", ["Implementation of a SAT solver [DPLL]", "Flashcard application based on double major courses"])]),
"fr": dict(
 lang="fr", leftTop="84mm", rightTop="58mm",
 summary="Actuellement en <b>deuxième année de cycle ingénieur à l'ENSEEIHT</b> en alternance (FISA) et apprentie ingénieure logiciel chez Kyber, je souhaite <b>effectuer un semestre d'études (6 mois) à l'étranger</b>. Passionnée par l'électronique et l'embarqué, je souhaite approfondir mes compétences techniques dans un environnement international.",
 h_contact="Contact", h_skills="Compétences", h_lang="Langues", h_hob="Loisirs et intérêts",
 h_edu="Études", h_xp="Expériences", h_proj="Projets menés",
 skills=["Langages de programmation :<br>Rust, Python, Java, C, C++, OCaml, VHDL, Promela, CUDA, JavaScript, WebAssembly",
         "Outils : ROS, Docker, Git, Linux embarqué, LaTeX", "Grande capacité de travail", "Esprit d'équipe", "Curieuse"],
 langs=["Anglais C1 / Espagnol B2", "Notions d'arabe littéraire et de russe"],
 hobbies=["Natation", "Suivre des avions sur FlightRadar", "Voyager"],
 edu=[("ENSEEIHT – Toulouse INP (31) :", "2025 – aujourd'hui :", "Cycle ingénieur Sciences du Numérique – Informatique et Réseaux, en alternance (FISA). <span class='now'>Actuellement en 2<sup>e</sup> année.</span>"),
      ("Université Toulouse III – Paul Sabatier (31) :", "2024 – 2025 :", "Master 1 Systèmes Embarqués et Connectés : Infrastructure et Logiciels (SECIL)"),
      ("Aix-Marseille Université (13) :", "2022 – 2024 :", "Double Licence en Mathématiques et Informatique"),
      ("Classe préparatoire, Lycée Thiers, Marseille (13) :", "2020 – 2022 :", "CPGE BCPST (Biologie, Chimie, Physique et Sciences de la Terre)")],
 xp=[("Kyber, Paris (75) – Apprentie ingénieure logiciel (FISA)", "Depuis octobre 2025",
      ["Développement d'un SDK de contrôle à distance à très faible latence (&lt; 20 ms).",
       "Protocoles réseau basés sur QUIC et WebTransport ; code Rust/WebAssembly."]),
     ("IRIT, Toulouse (31)", "Mai – juillet 2025", ["Stage de validation du M1 sur l'optimisation des XDD (eXecution Decision Diagrams)"]),
     ("LIS, sous tutelle du CNRS, Marseille (13)", "Juin – juillet 2023", ["Stage de validation de la double licence sur les automates probabilistes, sous la direction de M. Benjamin Monmege"]),
     ("Parkours, Marseille (13), Toulouse (31)", "Depuis octobre 2022", ["Tutrice Parkours : aide aux devoirs pour les lycéens."])],
 proj=[(None, ["Intégration d'un serveur MCP avec un LLM local", "Réalisation d'une maquette de voilier autonome"]),
       ("Python :", ["Conception d'un classifieur d'images basé sur l'IA", "Implémentation d'un algorithme de réduction d'états d'un automate probabiliste"]),
       ("Java :", ["Implémentation d'un SAT-solver [DPLL]", "Application de flashcards basée sur les cours de double licence"])]),
}

def ul(items, cls=""):
    return f"<ul{cls}>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

for code, d in L.items():
    edu = "".join(f"<div class='edu'><div class='s'>{s}</div><div class='y'>{y}</div><div>{t}</div></div>" for s, y, t in d["edu"])
    xp = "".join(f"<div class='xp'><div class='t'>{t}</div><div class='y'>{y}</div>{ul(b)}</div>" for t, y, b in d["xp"])
    proj = "".join((f"<div class='k'>{k}</div>" if k else "") + ul(items) for k, items in d["proj"])
    css = CSS.replace("%LEFTTOP%", d["leftTop"]).replace("%RIGHTTOP%", d["rightTop"])
    html = f"""<!doctype html><html lang="{d['lang']}"><head><meta charset="utf-8"><title>CV Camille Vedani</title><style>{css}</style></head><body>
<div class="deco d1"></div><div class="deco d2"></div><div class="deco d3"></div><div class="deco d4"></div><div class="deco d5"></div>
<div class="photo"><img src="cv-photo.png" alt=""></div>
<div class="name">CAMILLE<br>VEDANI</div>
<p class="summary">{d['summary']}</p>
<div class="left">
  <h2>{d['h_contact']}</h2>
  <div class="blk contact"><div><span class="ico">&#9742;</span>06 29 27 59 31</div><div><span class="ico">&#9993;</span>camille.vedani@outlook.fr</div></div>
  <h2>{d['h_skills']}</h2><div class="blk">{ul(d['skills'])}</div>
  <h2>{d['h_lang']}</h2><div class="blk">{ul(d['langs'])}</div>
  <h2>{d['h_hob']}</h2><div class="blk">{ul(d['hobbies'])}</div>
</div>
<div class="right">
  <section><h2>{d['h_edu']}</h2>{edu}</section>
  <section><h2>{d['h_xp']}</h2>{xp}</section>
  <section><h2>{d['h_proj']}</h2><div class="proj"><div class="list">{proj}</div><img class="qr" src="cv-qr.png" alt="QR"></div></section>
</div>
</body></html>"""
    Path(__file__).with_name(f"cv_{code}.html").write_text(html, encoding="utf-8")
print("ok")
