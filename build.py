#!/usr/bin/env python3
"""Assemble data/*.json into index.html and report data holes."""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
D = ROOT / "data"
THEMES = ["economie_fiscalite", "budget_dette", "retraites", "travail_salaires", "sante", "education", "immigration",
          "securite_justice", "defense_international", "europe", "energie_climat", "ia_numerique", "logement",
          "agriculture", "institutions"]


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def non_libre(logo):
    lic = ((logo or {}).get("licence") or "").lower()
    return "marque" in lic or "contest" in lic


def check(c):
    """Return a list of warnings for one candidate."""
    w = []
    for k in ("nom", "parti", "famille", "position", "photo", "bio", "programme", "parrainages", "fonds"):
        if not c.get(k) and c.get(k) != 0:
            w.append(f"champ manquant: {k}")
    if c.get("photo", {}).get("fichier") and not (ROOT / c["photo"]["fichier"]).exists():
        w.append("photo absente du disque")
    if c.get("logo_parti", {}).get("fichier") and not (ROOT / c["logo_parti"]["fichier"]).exists():
        w.append("logo absent du disque")
    vides = [t for t in THEMES if not c.get("programme", {}).get(t)]
    if vides:
        w.append(f"{len(vides)} thème(s) vide(s)")
    uniq = 0
    for f in [*sum((c.get("bio", {}).get(k, []) for k in ("etudes", "carriere_hors_politique", "mandats", "autres")), []),
              *c.get("financement", []), *sum((p.get("details", []) for p in c.get("programme", {}).values()), []),
              *c.get("affaires", [])]:
        if len(f.get("sources", [])) < 2:
            uniq += 1
    f = c.get("fonds") or {}
    if (f.get("alerte", "aucune") != "aucune" or f.get("alerte_etranger")) and len(f.get("sources", [])) < 2:
        w.append("alerte financement avec moins de 2 sources")
    if uniq:
        w.append(f"{uniq} fait(s) à source unique")
    return w


def main():
    cands = [load(p) for p in sorted((D / "candidats").glob("*.json"))]
    for c in cands:  # logos non libres : pas de republication sur le site public
        if non_libre(c.get("logo_parti")):
            c["logo_parti"] = {}
    meta = load(D / "meta.json")
    data = {"maj": meta["maj"], "methode": meta.get("methode", ""), "candidats": cands, "sondages": load(D / "sondages.json")}
    data["sondages"]["avis"] = meta.get("avis_sondages", "")
    data["retires"] = [c for c in load(D / "candidats_liste.json") if c["statut"] == "retire"]
    for c in cands:
        for w in check(c):
            print(f"[{c['id']}] {w}")
    html = (ROOT / "template.html").read_text(encoding="utf-8")
    js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    (ROOT / "index.html").write_text(html.replace("/*DATA*/null", js), encoding="utf-8")
    print(f"index.html écrit : {len(cands)} candidats")


if __name__ == "__main__":
    main()
