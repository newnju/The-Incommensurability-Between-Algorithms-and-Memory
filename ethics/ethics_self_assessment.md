# Ethics Self-Assessment (ethics_self_assessment.md)

> **Status: FINAL** — ethics self-assessment completed 2026-09 prior to public release of the repository. All checklist items verified by the authors.

## 1. Human subjects

This study does not involve human participants as research subjects. It analyzes
AI-generated images and does not collect personal data from individuals.

## 2. Coder consent — scope and extension

- [x] Original consent obtained from the two coders (Coder A / Coder B) for participation.
- [x] **Extended consent for public release of per-image coding judgments obtained** (coders remain anonymized as Coder A / Coder B in all released files). Confirmed by the authors, 2026-09.

## 3. Ethnicity, confrontation, and historical appellations

- Historical appellations do not enter any prompt text (verified against
  `prompts/` full text).
- No mapping between historical appellations and modern ethnic groups is made or implied.
- Ethnicity is never inferred from facial appearance; f11-related items record
  labeled representation in the image only.
- P3 (negative-frame) confrontational-posture samples are published, if at all,
  with contextualizing captions stating their analytical purpose.

## 4. Image release classification

Following the preregistered rule in `ethics/model_terms_compliance.md`:

- **Publishable**: typical-pattern cases; explicitly labeled "AI-generated,
  for critical scholarly analysis".
- **Restricted**: f11-related labeled-representation samples → thumbnail only;
  P3 confrontation samples → captioned context required.
- **Excluded**: images from platforms whose terms prohibit redistribution.
  Verification completed 2026-09: no platform among M1–M6 restricts academic
  use or redistribution; no image is excluded on terms grounds (see
  `model_terms_compliance.md`).

## 5. Scope of claims

The dependent variable is limited to historical distortion and representational
pattern in the images themselves. This study does NOT claim that the public has
been cognitively affected by these outputs; establishing real-world effects
requires audience experiments and diffusion tracking, which are outside scope.

## 6. Image provenance disclosure

All 162 corpus images are AI-generated between 2026-08 and 2026-09 across six
commercial T2I platforms; generation dates and outcomes are logged in
`coding_data/` (sample list sheet). No real photograph of any person or event
is included in any deposit.
