# CareerPath AI: Career and Major Advisor for Azerbaijani Students

An AI advisor that helps Azerbaijani high school students choose a university major. The student answers a short interest questionnaire, receives a personal interest profile, gets the top 3 matching majors with possible careers, and can ask follow-up questions to an AI advisor in Azerbaijani.

**Demo:** `PASTE_DEMO_LINK_HERE`
**Video:** `PASTE_VIDEO_LINK_HERE`

## The problem

Many students pick a major based on family pressure or entrance scores alone, without knowing what the major involves or which careers it leads to. A single school counselor cannot give personal guidance to hundreds of students. CareerPath AI gives every student a first, personalized orientation in their own language.

## How it works

1. **Interest questionnaire.** 12 questions on a 1-5 scale, based on the Holland (RIASEC) model: Realistic, Investigative, Artistic, Social, Enterprising, Conventional. Each type is the average of its 2 questions, giving a 6-number profile such as `[3.5, 5, 2, 3, 2.5, 4]`.
2. **Matching.** The student profile is compared with the RIASEC vector of each major in our database using cosine similarity. The top 3 majors are returned with a match percentage, description and possible careers.
3. **AI advisor.** A chat connected to an LLM through OpenRouter answers questions such as "What jobs can I find with this major?" in Azerbaijani. The prompt instructs the model to rely on the major list and not to invent information.

## Repository structure

```
.
├── frontend/              Web app (generated with Lovable, see Disclosure)
├── backend/               Spring Boot (Java): recommendation and chat API
├── data/
│   ├── build_majors.py    Builds majors.json (23 majors with RIASEC vectors)
│   ├── majors.json        Major database used by the backend
│   ├── evaluate.py        Tests the matching algorithm on sample profiles
│   └── results.csv        Output of evaluate.py
├── docs/                  Pitch deck and demo script
├── .env.example           Template for secrets (no real keys)
└── README.md
```

## Data

`data/majors.json` contains 23 majors. Each entry has: name, RIASEC vector `[R, I, A, S, E, C]` (1-5), school subjects, possible careers and a short description.

**Important:** the RIASEC vectors, careers and descriptions are **team estimates** based on the Holland model. They are not official statistics. The fields `group` and `universities` are left empty on purpose until verified against official sources (dim.gov.az and university websites). We do not include admission scores because we could not verify them.

To rebuild the file after editing the list in the script:

```bash
cd data
python build_majors.py
```

Only the Python standard library is needed.

## Quality testing

`data/evaluate.py` runs 10 test profiles through the matching algorithm and saves the results to `data/results.csv`.

```bash
cd data
python evaluate.py
```

**Results**
- 7 of 7 profiles with an expected outcome returned a sensible top 3 (for example, a technical profile `[5,4,2,1,2,3]` returned Mechanical Engineering, Electrical Engineering and Civil Engineering).
- The empty profile `[0,0,0,0,0,0]` returns 0% matches without crashing.

**What broke**
1. "All answers 5" and "all answers 1" return **identical** results, because cosine similarity only compares direction, not magnitude. A student who rates everything the same still sees a 96% match.
2. Match percentages are **compressed** (most majors fall between 94% and 100%), so the percentage alone does not separate majors well. Ranking is reliable, the displayed percentage is less so.

**Planned fix:** center each profile around its own mean before comparing, and show a "please answer more differently" message when the profile is flat.

## Setup

1. Copy `.env.example` to `.env` and put your own OpenRouter key in it. Never commit real keys.
2. Backend (Spring Boot, Java 17):
   - Put `data/majors.json` into `backend/src/main/resources/`
   - Set the environment variable `OPENROUTER_API_KEY`
   - Run `DemoApplication` (or `./mvnw spring-boot:run`)
   - The API runs on `http://localhost:8080`
3. Endpoints:
   - `POST /api/recommend` with `{"scores": {"R":5,"I":4,"A":2,"S":1,"E":2,"C":3}}`
   - `POST /api/chat` with `{"message": "..."}`

## Tech stack and disclosure

- **Frontend:** generated with Lovable (React), then adjusted by the team
- **Backend:** Spring Boot (Java)
- **LLM:** OpenRouter API (model: `FILL_IN_MODEL_NAME`)
- **Data and testing:** Python (standard library), Holland RIASEC model
- **Data sources:** team-created major list; RIASEC model by John Holland

This project was built after the hackathon started.

## Limitations and next steps

- Real admission data (DİM scores, universities) is not yet included
- Match percentages need recalibration (see Quality testing)
- Retrieval over textbooks and official major descriptions with a vector database (Chroma) is planned
- Azerbaijani and English interface

## Team

| Role | Name |
|---|---|
| Frontend | NAME |
| Backend | NAME |
| Data | NAME |
| Presentation and testing | NAME |
