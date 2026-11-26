"""Convert the expert models (UMLet) and the story lists of two Zenodo appendices into the dataset format.
Usage: convert.py <dataset root>"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import uxf  # noqa: E402

ROOT = Path(sys.argv[1])
X = HERE / "z4121935" / "x"
G = HERE / "z5905846" / "x_Gold Standards" / "Gold Standards"
APPX_2020 = ("Dalpiaz, Sturm, Gieske (2020), Extraction of Conceptual Models: User Stories vs. Use Cases, "
             "https://doi.org/10.5281/zenodo.4121935, CC BY 4.0")
APPX_2022 = ("Bragilovski, Dalpiaz, Sturm (2022), Guided Derivation of Conceptual Models from User Stories, "
             "https://doi.org/10.5281/zenodo.5905846, CC BY 4.0")
# project: (model file, story source, title, appendix, story file)
PROJECTS = {
    "hospital_g01": (X / "HOS/g01-us/g01-US-tagged.uxf", "HOS/g01-us/g01-us-tagged.pdf", "Hospital management system, group 01", APPX_2020, "g01"),
    "hospital_g02": (X / "HOS/g02-us/g02_US.uxf", "HOS/g02-us/g02-us-req-cm.pdf", "Hospital management system, group 02", APPX_2020, "g02"),
    "hospital_g06": (X / "HOS/g06-us/g06_US.uxf", "HOS/g06-us/g06-us-req-cm.pdf", "Hospital management system, group 06", APPX_2020, "g06"),
    "hospital_g10": (X / "HOS/g10-us/g10_us.uxf", "HOS/g10-us/g10-us-req-cm.pdf", "Hospital management system, group 10", APPX_2020, "g10"),
    "hospital_g12": (X / "HOS/g12-us/g12_US.uxf", "HOS/g12-us/g12-us-req.docx", "Hospital management system, group 12", APPX_2020, "g12"),
    "football_g05": (X / "IFA/g05-us/g05-US.uxf", "IFA/g05-us/g05-us-req.pdf", "International football association portal, group 05", APPX_2020, "g05"),
    "football_g08": (X / "IFA/g08-us/g08-US.uxf", "IFA/g08-us/g08-us-req.pdf", "International football association portal, group 08", APPX_2020, "g08"),
    "football_g11": (X / "IFA/g11-us/g11-US.uxf", "IFA/g11-us/g11-us-req.pdf", "International football association portal, group 11", APPX_2020, "g11"),
    "football_g14": (X / "IFA/g14-us/g14-US.uxf", "IFA/g14-us/g14-us-req-cm.pdf", "International football association portal, group 14", APPX_2020, "g14"),
    # Not included (see docs/additional-projects.md, "Not added"): the two traffic-simulator projects
    # SIM/g04-us/g04-US.uxf and SIM/g09-us/g09-US.uxf.
    "datahub": (G / "tagging-fd-dh-cdg.uxf", "ExperimentForms/Form-DH-Plain.docx", "Data Hub", APPX_2022, "DH"),
}
# Corrections to the expert diagrams; every one is listed in docs/additional-projects.md ("Changes to the expert diagrams")
# and in a %% comment of the model.
# Rule 1: obvious misspellings of a class label whose intended word is clear are corrected.
LABEL_FIXES = {
    "hospital_g01": {"Uneraged Child": "Underage Child"},
    "football_g14": {"Team Mananger": "Team Manager", "IFA adminstrator": "IFA administrator", "Priviligae": "Privilege"},
    "datahub": {"Configurtaion Parameter": "Configuration Parameter"},
}
# Rule 2: a class that no user story mentions and that has no association is marked <<optional>>
# (neither required nor penalized), as in the original nine models.
OPTIONAL = {
    "hospital_g12": {"Pharmacist": "no story mentions a pharmacist", "Financial Admin": "no story mentions finance or billing staff"},
}
KIND = {"<<-": "inheritance", "<<<<-": "aggregation", "<<<<<-": "composition", "<-": "directed association",
        "->": "directed association", "-": "association", ".": "dotted line"}


def stories(code):
    if code == "DH":
        lines = (HERE / "text" / "DH.txt").read_text(encoding="utf-8").splitlines()
        i = next(k for k, l in enumerate(lines) if l.startswith("As a Publisher, I want to sign up"))
        j = next(k for k, l in enumerate(lines) if l.startswith("Following the set of user stories"))
        return [l.strip() for l in lines[i:j] if re.match(r"As an? ", l.strip())]
    return [l.strip() for l in (HERE / "stories" / f"{code}.txt").read_text(encoding="utf-8").splitlines() if l.strip()]


def model(project, src, story_src, title, appx):
    names, rels, _, _ = uxf.parse(src)
    fix = LABEL_FIXES.get(project, {})
    assert set(fix) <= set(names) and set(OPTIONAL.get(project, {})) <= set(names), project
    names = [fix.get(n, n) for n in names]
    rels = [(fix.get(a, a), fix.get(b, b), *rest) for a, b, *rest in rels]
    ids = {n: f"C{i:03d}" for i, n in enumerate(dict.fromkeys(names), 1)}
    orig = {v: k for k, v in fix.items()}
    opt = OPTIONAL.get(project, {})
    rel_src = src.relative_to(HERE).as_posix().split("/x/")[-1].split("/x_")[-1]
    out = ["classDiagram", f"    %% Project: {title}",
           f"    %% Source: {appx}.",
           f"    %% Expert (gold) class diagram: {Path(rel_src).name} (UMLet); user stories: {story_src}.",
           "    %% Converted with scripts/additional_projects/; rules and limits in docs/additional-projects.md.",
           "    %% Class labels are copied exactly from the expert diagram, including spelling errors.",
           "    %% Associations, aggregations and compositions become undirected -- edges; duplicates are merged.",
           "    %% Inheritance, attributes, operations, multiplicities and relationship labels are not part of the gold model;",
           "    %% inheritance links are listed as comments below."]
    if fix or opt:
        out += ["    %% Corrections to the expert diagram are marked below and listed in docs/additional-projects.md."]
    for n, i in ids.items():
        if n in orig:
            out.append(f'    %% Label corrected (misspelling): expert diagram has "{orig[n]}".')
        if n in opt:
            out.append(f"    %% Marked optional: {opt[n]}, and the class has no association.")
        out.append(f'    class {i}["{n}"]')
        if n in opt:
            out.append(f"    <<optional>> {i}")
    seen, inh, unresolved = {}, [], []
    for a, b, lt, da, db, label in rels:
        kind = KIND.get(lt, f"line {lt}")
        if max(da, db) > 12 or a == b:
            unresolved.append((a, b, kind, label))
            continue
        if kind == "inheritance":
            inh.append((a, b))
            continue
        key = frozenset((a, b))
        seen.setdefault(key, []).append((a, b, kind, label))
    assert not any(set(k) & set(opt) for k in seen), f"{project}: an optional class has an association"
    for key, items in seen.items():
        a, b = items[0][0], items[0][1]
        desc = "; ".join(f"{k}{' \"' + l + '\"' if l else ''}" for _, _, k, l in items)
        out += ["", f"    %% Association: {a} -- {b}", f"    %% Expert diagram: {desc}" +
                (" (drawn more than once, merged)" if len(items) > 1 else "") + ".",
                f"    {ids[a]} -- {ids[b]}"]
    if inh:
        out += ["", "    %% Inheritance in the expert diagram (general -- specific), not counted as associations:"]
        out += [f"    %%   {a} <|-- {b}" for a, b in inh]
    if unresolved:
        out += ["", "    %% Dotted lines of the expert diagram that end on another line, not on a class (association-class or",
                "    %% annotation style). Their meaning is ambiguous, so they are not included:"]
        out += [f"    %%   near {a} / {b}{(' \"' + l + '\"') if l else ''}" for a, b, k, l in unresolved]
    return "\n".join(out) + "\n", len(ids), len(seen), len(inh), len(unresolved)


rows = []
for p, (src, story_src, title, appx, code) in PROJECTS.items():
    st = stories(code)
    (ROOT / "1_user_stories" / f"{p}.txt").write_text("\n".join(st) + "\n", encoding="utf-8", newline="\n")
    text, nc, na, ni, nu = model(p, src, story_src, title, appx)
    (ROOT / "2_gold_standard_domain_models" / f"{p}.mmd").write_text(text, encoding="utf-8", newline="\n")
    rows.append((p, len(st), nc, na, ni, nu))
    print(f"{p:14} stories {len(st):3}  classes {nc:3}  associations {na:3}  inheritance {ni:2}  unresolved {nu}")
