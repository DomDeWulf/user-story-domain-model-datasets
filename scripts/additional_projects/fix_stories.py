"""Exact corrections of the story lines against the source PDFs/DOCX; every fix must apply once."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
FIX = {
 "05": [("so thatI have", "so that I have"), ("(initi-ator and", "(initiator and"), ("(re-scheduling", "(rescheduling"),
        ("report inreal-time", "report in real-time"), ("local regula-tions", "local regulations"),
        ("and time zone", "and time zones"), ("new func-tionalities", "new functionalities"),
        ("mainten,ance", "maintenance"), ("implementation stages 9.", "implementation stages."),
        ("next versions 10.", "next versions.")],
 "06": [("edit patient’ medical", "edit patient’s medical"), ("review a patient’ ID", "review a patient’s ID")],
 "10": [("collected with medical devices", "collected with mobile devices")],
 "12": [("(iblood pressure, CT scans, etc, so", "(i.e. blood pressure, CT scans, etc.), so"),
        ("(i fitness band)", "(i.e.: fitness band)"), ("computers etc, so", "computers etc.), so"),
        ("access the system / so", "access the system 24/7, so")],
}
for g, fixes in FIX.items():
    p = f"stories/g{g}.txt"; t = open(p, encoding="utf-8").read()
    for a, b in fixes:
        assert t.count(a) == 1, (g, a, t.count(a)); t = t.replace(a, b)
    open(p, "w", encoding="utf-8").write(t)
# g01: continuation line; g14: two stories merged into one line
p = "stories/g01.txt"; L = open(p, encoding="utf-8").read().splitlines()
i = L.index("which data to perform data analysis"); L[i - 1] = L[i - 1] + " " + L[i]; del L[i]
open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
p = "stories/g14.txt"; t = open(p, encoding="utf-8").read()
a = "so that I can avoid mistakes. As an IFA budget auditor,"; assert t.count(a) == 1
open(p, "w", encoding="utf-8").write(t.replace(a, "so that I can avoid mistakes.\nAs an IFA budget auditor,"))
print("ok")
