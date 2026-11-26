# Additional projects (addition, not part of Bragilovski et al. 2025)

Ten further projects, each with user stories (`1_user_stories/<project>.txt`) and a gold class diagram made by domain
experts (`2_gold_standard_domain_models/<project>.mmd`). They come from two other online appendices by the same research group.
Both are licensed CC BY 4.0.

| Source | Projects | Gold model by |
|---|---|---|
| Dalpiaz, Sturm, Gieske (2020), *Extraction of Conceptual Models: User Stories vs. Use Cases*, [doi:10.5281/zenodo.4121935](https://doi.org/10.5281/zenodo.4121935) | `hospital_g01`, `_g02`, `_g06`, `_g10`, `_g12`; `football_g05`, `_g08`, `_g11`, `_g14` | The three authors, one expert model per student specification |
| Bragilovski, Dalpiaz, Sturm (2022), *Guided Derivation of Conceptual Models from User Stories*, [doi:10.5281/zenodo.5905846](https://doi.org/10.5281/zenodo.5905846) | `datahub` | Two authors independently, then reconciled |

| Project | Stories | Classes | Associations | Inheritance (comments only) | Isolated classes |
|---|---|---|---|---|---|
| hospital_g01 | 57 | 26 | 33 | 11 | 3 |
| hospital_g02 | 40 | 22 | 25 | 3 | 3 |
| hospital_g06 | 34 | 20 | 27 | 2 | 2 |
| hospital_g10 | 28 | 20 | 23 | 8 | 0 |
| hospital_g12 | 35 | 17 | 19 | 7 | 3 |
| football_g05 | 42 | 20 | 22 | 0 | 0 |
| football_g08 | 30 | 21 | 22 | 5 | 2 |
| football_g11 | 41 | 22 | 19 | 8 | 2 |
| football_g14 | 37 | 23 | 24 | 8 | 1 |
| datahub | 22 | 15 | 16 | 1 | 0 |

## How the 2020 projects arose
In a requirements course, students interviewed a stakeholder about one of three fictitious systems (hospital management, international
football association portal, urban traffic simulator) and wrote a specification as user stories or use cases. The authors then drew an
expert class diagram from each specification. Only the user-story specifications are used here. **The projects of one system share
the domain and partly the wording, so they are not independent**: report results per system as well, and do not split one system
across development and test sets.

The expert diagrams are the `.uxf` files in each group folder (the tagging guidelines in the appendix name them "the conceptual model
created by the domain experts"). Their class and relationship counts match the "Domain expert CM" columns of
`UC_vs_US Statistic Analysis.xlsx` (e.g. g06-us 20 / 30, g02-us 22 / 29; relationship counts include inheritance).

## Conversion rules
- **Classes:** every class box, label copied exactly (including spelling errors such as `Configurtaion Parameter` or
  `Team Mananger`). Attributes and operations are dropped.
- **Associations:** association, directed association, aggregation and composition lines become one undirected `--` edge.
  A pair drawn twice becomes one edge. Endpoints are found from the line geometry in UMLet (the endpoint must lie within 12 px of a
  class box; relation points are scaled by the diagram's zoom level).
- **Inheritance** is not part of the gold model, in line with the original nine models. It is listed in `%%` comments.
- **Dotted lines that end on another line** are ambiguous (association class or annotation) and would be listed in comments, not
  included; they occur only in the two traffic projects, which are not added.
- `<<optional>>` is used only for the two classes listed under "Changes to the expert diagrams". There are no non-punish groups.

## Changes to the expert diagrams
The expert diagrams are copied unchanged except for the following corrections. Each follows a stated rule, applied to all ten
projects, and was decided by inspecting the gold models and the stories, not by which change would raise a score. Every change is
also marked with a `%%` comment in the model, and the conversion script applies it (`LABEL_FIXES`, `OPTIONAL` in `convert.py`).

**Rule 1: an obvious misspelling of a class label is corrected** when the intended word is clear. Misspelled labels can never match
under lexical matching, so they would penalize correct output. The original nine models keep their labels exactly; this is a
deliberate difference for the additional projects.

| Project | Expert diagram | Corrected to | Evidence |
|---|---|---|---|
| hospital_g01 | Uneraged Child | Underage Child | story: "my underage children's medical files" |
| football_g14 | Team Mananger | Team Manager | spelling |
| football_g14 | IFA adminstrator | IFA administrator | spelling; story uses "administrator" |
| football_g14 | Priviligae | Privilege | spelling; story uses "privileges" |
| datahub | Configurtaion Parameter | Configuration Parameter | spelling |

**Rule 2: a class that no user story mentions and that has no association is marked `<<optional>>`** (neither required nor
penalized, as for the optional classes of the original nine models). The class cannot be derived from the stories, which are the only
input of the evaluated approaches.

| Project | Class | Evidence |
|---|---|---|
| hospital_g12 | Pharmacist | no story mentions a pharmacist; only a subclass of User |
| hospital_g12 | Financial Admin | no story mentions finance, billing or payment; only a subclass of User |

Not changed, although considered: system and regulation classes (`HMS`, `IFA`, `GDPR`), classes left isolated by dropping
inheritance (e.g. `Mobile Phone`, `Internal Lab`, `League` in football_g11), and gold names that differ from the story wording by a
synonym (`Game` where stories say "match"). These are modeling choices of the experts, not errors.

## User stories
- **2020 projects:** the stories are in the students' reports (PDF/DOCX), partly as tables. The plain-text version in
  [PyUNML-DataSet](https://github.com/matovaro/PyUNML-DataSet) (`Original datasets/Dalpiaz2020/Text files`) served as a starting point.
  Every line was compared word by word with the source (`build_stories.py`); differences were corrected to the source wording
  (`fix_stories.py`), e.g. merged words ("gameevents"), a changed word ("medical devices" for "mobile devices", g10), two merged stories
  (g14), and lost text ("24/7", "i.e.", g12). Footnote markers are removed.
- **datahub:** the 22 stories of the experiment form `Form-DH-Plain.docx`, verbatim (including "so that that").
- One story per line; non-functional stories are kept, as in the original nine projects.

## Not added
- **Planning Poker gold model of the 2022 appendix:** 20 of the stories of the existing `planningpoker` project with a different
  gold model (9 classes). It could serve to study disagreement between gold models, not as a new project.
- **Use-case specifications** of the 2020 appendix (no user stories).
- **The two traffic-simulator projects** (`SIM/g04-us`, `SIM/g09-us` of the 2020 appendix; 23 and 32 stories, 22 classes each). They
  were converted, then removed from the dataset. The expert diagrams are built mainly on inheritance: without it (inheritance is not
  part of the gold models) 11 and 6 of the 22 classes are isolated and only 10 and 13 associations remain. Many classes are values or
  properties rather than domain concepts (e.g. `Fairness`, `Credibility`, `Level of noise`, `Repeatable analysis`), and some labels
  combine two names (`Solution / measure`). Repairing this would mean remodeling the diagrams, so they would no longer be expert
  gold models. `convert.py` lists them in a comment; adding their two entries back reproduces them.

## Limits
- The expert diagrams were drawn as course material and differ in style from the original nine models: they include system and
  regulation classes (e.g. `HMS`, `GDPR`), people's roles, and more inheritance. Scores are therefore not directly comparable with the
  original nine projects; report them separately.
- The 2020 stories were written by students and contain spelling and grammar errors, which are kept.
- SVG renderings are in `3_visualizations/` (section "Additional projects" of its README). There are no gold sequence diagrams for
  the new projects.
- Public since 2020/2022, so the data may be in the training data of current LLMs.

## Reproducing
Download both Zenodo archives, unpack `ucvsus-ist.zip` to `z4121935/x/` and the 2022 zips to `z5905846/x_<name>/`, extract the story
sources to text (`text/`), and fetch the PyUNML text files to `pyunml/`. Then run `build_stories.py`, `fix_stories.py` and
`convert.py <dataset root>` from `scripts/additional_projects/` in that working folder.
