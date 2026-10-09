"""
1-ci addim: ixtisas bazasini (majors.json) yaradir.
Isletmek:  python build_majors.py

RIASEC sirasi: [R, I, A, S, E, C], her biri 1-5.
Bu ballar KOMANDA QIYMETLENDIRMESIDIR (rasmi data deyil).
"group" ve "universities" sahelerini DIM saytindan yoxlayib doldurun,
bilmediyiniz yeri BOS saxlayin, uydurmayin.
"""
import json
from pathlib import Path

MAJORS = [
    # (ad, [R,I,A,S,E,C], fenler, peseler, tesvir)
    ("Komputer elmleri", [3,5,2,1,2,3], ["Riyaziyyat","Informatika"],
     ["Proqramci","Data analitik","Kibertehlukesizlik mutexessisi"],
     "Proqramlasdirma, alqoritmler, verilenler bazasi ve suni intellekt."),
    ("Informasiya tehlukesizliyi", [3,5,1,1,2,4], ["Riyaziyyat","Informatika"],
     ["Tehlukesizlik analitiki","Sizma testcisi","Sistem administratoru"],
     "Sebekelerin ve melumatlarin muhafizesi."),
    ("Tibb", [3,5,1,5,2,2], ["Biologiya","Kimya"],
     ["Hekim","Cerrah","Tibbi tedqiqatci"],
     "Insan orqanizmi, diaqnostika ve mualice."),
    ("Stomatologiya", [4,4,2,4,2,3], ["Biologiya","Kimya"],
     ["Stomatoloq","Ortodont","Dis texnikasi"],
     "Agiz bosluğu xestelikleri ve mualicesi."),
    ("Əczaçılıq", [3,5,1,3,2,4], ["Kimya","Biologiya"],
     ["Eczaci","Dermanlarin tedqiqatcisi","Keyfiyyet nezaretcisi"],
     "Dermanlarin hazirlanmasi ve istifadesi."),
    ("Huquqsunasliq", [1,3,2,4,4,4], ["Tarix","Azerbaycan dili"],
     ["Vekil","Hakim","Huquq meslehetcisi"],
     "Qanunlar, mehkeme prosesleri ve huquqi meslehet."),
    ("Iqtisadiyyat", [1,4,1,2,4,5], ["Riyaziyyat","Cografiya"],
     ["Iqtisadci","Maliyye analitiki","Bank mutexessisi"],
     "Iqtisadi proseslerin tehlili ve proqnozu."),
    ("Maliyye ve muhasibat", [1,3,1,2,3,5], ["Riyaziyyat"],
     ["Muhasib","Auditor","Maliyye meneceri"],
     "Maliyye hesabatlari, vergi ve audit."),
    ("Biznesin idare edilmesi", [1,2,2,3,5,3], ["Riyaziyyat","Cografiya"],
     ["Menecer","Sahibkar","Marketoloq"],
     "Teskilatlarin ve layihelerin idare edilmesi."),
    ("Marketinq ve reklam", [1,2,4,3,5,2], ["Azerbaycan dili","Tarix"],
     ["Marketoloq","SMM mutexessisi","Brend meneceri"],
     "Mehsul ve xidmetlerin teqdimati ve satisi."),
    ("Mexanika muhendisliyi", [5,4,2,1,2,3], ["Riyaziyyat","Fizika"],
     ["Mexanik muhendis","Layihe muhendisi","Texnoloq"],
     "Masin ve mexanizmlerin layihelendirilmesi."),
    ("Insaat muhendisliyi", [5,4,2,1,3,3], ["Riyaziyyat","Fizika"],
     ["Insaat muhendisi","Layihe rehberi","Texniki nezaretci"],
     "Bina, korpu ve yol layihelerinin qurulmasi."),
    ("Neft ve qaz muhendisliyi", [5,4,1,1,2,4], ["Riyaziyyat","Fizika","Kimya"],
     ["Neft muhendisi","Geoloq","Quyu muhendisi"],
     "Neft ve qazin cixarilmasi ve emali."),
    ("Elektrik ve elektronika muhendisliyi", [5,5,2,1,2,3], ["Riyaziyyat","Fizika"],
     ["Elektrik muhendisi","Embedded muhendis","Avtomatika muhendisi"],
     "Elektrik sistemleri ve elektron qurgular."),
    ("Memarliq", [3,3,5,2,3,3], ["Riyaziyyat","Rəsm"],
     ["Memar","Seher planlasdiricisi","Interyer dizayneri"],
     "Bina ve seher muhitinin layihelendirilmesi."),
    ("Dizayn", [2,2,5,3,3,1], ["Rəsm","Informatika"],
     ["Qrafik dizayner","UX dizayner","Moda dizayneri"],
     "Vizual kommunikasiya ve mehsul dizayni."),
    ("Jurnalistika ve media", [1,3,5,4,4,2], ["Azerbaycan dili","Tarix"],
     ["Jurnalist","Redaktor","Kontent produseri"],
     "Xeber hazirlama, media ve kommunikasiya."),
    ("Psixologiya", [1,5,3,5,2,2], ["Biologiya","Azerbaycan dili"],
     ["Psixoloq","Karyera meslehetcisi","HR mutexessisi"],
     "Insan davranisi ve dusuncesinin tedqiqi."),
    ("Pedaqogika", [1,2,3,5,3,3], ["Azerbaycan dili","Tarix"],
     ["Muellim","Terbiyeci","Tehsil meneceri"],
     "Tedris metodlari ve usaq inkisafi."),
    ("Beynelxalq munasibetler", [1,3,2,4,5,3], ["Tarix","Xarici dil"],
     ["Diplomat","Beynelxalq analitik","Tercumeci"],
     "Dovletlerarasi elaqeler ve diplomatiya."),
    ("Biologiya ve biotexnologiya", [3,5,2,2,1,3], ["Biologiya","Kimya"],
     ["Bioloq","Laborant","Biotexnoloq"],
     "Canli orqanizmlerin tedqiqi ve texnologiyalari."),
    ("Riyaziyyat ve statistika", [1,5,2,1,1,4], ["Riyaziyyat"],
     ["Statistik","Aktuari","Tedqiqatci"],
     "Riyazi modellesdirme ve melumat tehlili."),
    ("Turizm ve otelcilik", [2,2,3,5,4,3], ["Cografiya","Xarici dil"],
     ["Otel meneceri","Tur operatoru","Bələdçi"],
     "Turizm xidmetlerinin teskili."),
]

def main():
    out = []
    for i, (name, riasec, subjects, careers, desc) in enumerate(MAJORS, 1):
        assert len(riasec) == 6 and all(1 <= x <= 5 for x in riasec), name
        out.append({
            "id": i, "name": name,
            "group": "",            # DIM saytindan yoxlayib doldurun
            "riasec": riasec,
            "subjects": subjects,
            "careers": careers,
            "universities": [],     # yoxlayib doldurun, bilmirsinizse bos qalsin
            "description": desc,
        })
    path = Path(__file__).parent / "majors.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {len(out)} ixtisas yazildi -> {path}")

if __name__ == "__main__":
    main()
