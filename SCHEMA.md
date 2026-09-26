# Format des données (data/*.json)

`fact` = `{"texte": "...", "sources": [{"media": "Le Monde", "titre": "...", "url": "https://...", "date": "AAAA-MM-JJ"}]}`
Un fait avec 1 seule source apparaît avec le badge « ⚠ source unique ».

`data/candidats/<id>.json` :
```json
{
  "id": "lisnard", "nom": "David Lisnard", "naissance": "AAAA-MM-JJ", "lieu_naissance": "...",
  "parti": "Nouvelle Énergie", "parti_sigle": "NE",
  "famille": "extreme_gauche|gauche|centre_gauche|centre|centre_droit|droite|extreme_droite",
  "position": 4.5,                       // -10 (extrême gauche) … +10 (extrême droite)
  "position_justif": fact,
  "statut": "declare|investi|primaire|pressenti|retire",
  "photo": {"fichier": "img/candidats/lisnard.jpg", "source_url": "...", "auteur": "...", "licence": "..."},
  "logo_parti": {"fichier": "img/partis/ne.svg", "source_url": "...", "licence": "..."},
  "bio": {"etudes": [fact], "carriere_hors_politique": [fact], "mandats": [fact], "autres": [fact]},
  "programme": {"<theme>": {"resume": "une phrase", "origine": "programme 2027|déclarations 2025-2026|programme 2022", "details": [fact]}},
  "affaires": [{"intitule": "...", "statut": "condamnation_definitive|condamnation_non_definitive|proces_en_cours|mis_en_examen|enquete|accusation|classe_sans_suite|relaxe_ou_non_lieu", "date": "...", "description": "...", "sources": [...]}],
  "financement": [fact]
}
```
Thèmes : economie_fiscalite, budget_dette, retraites, travail_salaires, sante, education, immigration, securite_justice, defense_international, europe, energie_climat, ia_numerique, logement, agriculture, institutions.

Pour régénérer la page : `python3 build.py`.
