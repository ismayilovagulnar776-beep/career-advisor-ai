"""
2-ci addim: uygunluq alqoritmini test edir (Quality testing ucun).
Isletmek:  python evaluate.py
Netice: konsolda cedvel + results.csv (formda 'ne sinaq etdik' hissesine).
"""
import csv, json, math
from pathlib import Path

HERE = Path(__file__).parent
MAJORS = json.loads((HERE / "majors.json").read_text(encoding="utf-8"))

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)

def recommend(scores, top=3):
    ranked = sorted(
        ((cosine(scores, m["riasec"]), m["name"]) for m in MAJORS), reverse=True
    )
    return [(name, round(sim * 100)) for sim, name in ranked[:top]]

# (profil adi, [R,I,A,S,E,C], gozlenilen ixtisaslardan en azi biri top-3-de olmalidir)
TESTS = [
    ("Texniki sagird",      [5,4,2,1,2,3], ["Mexanika muhendisliyi","Komputer elmleri","Insaat muhendisliyi"]),
    ("Alim tipli",          [2,5,1,2,1,3], ["Riyaziyyat ve statistika","Biologiya ve biotexnologiya","Komputer elmleri"]),
    ("Yaradici",            [2,2,5,3,3,1], ["Dizayn","Memarliq","Jurnalistika ve media"]),
    ("Insansever",          [1,2,3,5,2,2], ["Pedaqogika","Psixologiya","Tibb"]),
    ("Biznes meyilli",      [1,2,2,3,5,3], ["Biznesin idare edilmesi","Marketinq ve reklam","Iqtisadiyyat"]),
    ("Nizam ve hesab",      [1,3,1,2,3,5], ["Maliyye ve muhasibat","Iqtisadiyyat"]),
    ("Natiq / diplomat",    [1,3,2,4,5,3], ["Beynelxalq munasibetler","Huquqsunasliq"]),
    ("Hamisi 5 (ekstrem)",  [5,5,5,5,5,5], None),   # gozlenilen yoxdur, yalniz xeta olmamalidir
    ("Hamisi 1 (ekstrem)",  [1,1,1,1,1,1], None),
    ("Hamisi 0 (bos)",      [0,0,0,0,0,0], None),
]

def main():
    rows, passed, checked = [], 0, 0
    print(f"{'Profil':<22} {'Top-3 netice':<70} Status")
    print("-" * 105)
    for name, scores, expected in TESTS:
        top = recommend(scores)
        top_names = [n for n, _ in top]
        text = "; ".join(f"{n} ({p}%)" for n, p in top)
        if expected is None:
            status = "N/A (xeta yoxdur)"
        else:
            checked += 1
            ok = any(e in top_names for e in expected)
            passed += ok
            status = "OK" if ok else "UYGUN DEYIL"
        rows.append([name, scores, text, status])
        print(f"{name:<22} {text:<70} {status}")

    print("-" * 105)
    print(f"Gozlenilen nailiyyet: {passed}/{checked}")

    # Eyni istiqametli profiller cosine ile eyni netice verir -> zeiflik
    a, b = recommend([5,5,5,5,5,5]), recommend([1,1,1,1,1,1])
    if a == b:
        print("DIQQET: 'Hamisi 5' ve 'Hamisi 1' EYNI netice verir (cosine yalniz istiqamete baxir).")
        print("        Bu, formda 'ne sindi' sualina yaza bileceyiniz real tapintidir.")

    with open(HERE / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["profil", "RIASEC", "top3", "status"])
        w.writerows(rows)
    print("results.csv yazildi")

if __name__ == "__main__":
    main()
