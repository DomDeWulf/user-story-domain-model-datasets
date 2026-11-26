"""Repair the PyUNML story lines against the source text and check coverage both ways."""
import re, sys, difflib
sys.stdout.reconfigure(encoding="utf-8")
W = re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)?")

def toks(s): return [t.lower() for t in W.findall(s)]

def fix(line, srcset):
    out = []
    for w in re.findall(r"\S+", line):
        core = re.sub(r"^\W+|\W+$", "", w)
        lw = core.lower()
        if not core or lw in srcset or not lw.isalpha():
            out.append(w); continue
        for i in range(2, len(core) - 1):
            if core[:i].lower() in srcset and core[i:].lower() in srcset:
                w = w.replace(core, core[:i] + " " + core[i:]); break
        out.append(w)
    return " ".join(out)

report = []
for g in sys.argv[1:]:
    src_raw = open(f"text/g{g}.txt", encoding="utf-8").read()
    src = toks(src_raw); srcset = set(src)
    lines = [l.strip() for l in open(f"pyunml/g{int(g)}.txt", encoding="utf-8") if l.strip()]
    fixed = [fix(l, srcset) for l in lines]
    # coverage: mark source tokens matched by story token sequences
    cov = [False] * len(src)
    unmatched = []
    sm = difflib.SequenceMatcher(autojunk=False)
    sm.set_seq2(src)
    for l in fixed:
        t = toks(l); sm.set_seq1(t)
        blocks = [b for b in sm.get_matching_blocks() if b.size >= 3]
        got = sum(b.size for b in blocks)
        for b in blocks:
            for k in range(b.b, b.b + b.size): cov[k] = True
        if got < 0.85 * len(t): unmatched.append((round(got / max(len(t),1), 2), l))
    # uncovered windows in the source that look like stories
    gaps, cur = [], []
    for k, c in enumerate(cov):
        if not c: cur.append(src[k])
        elif cur: gaps.append(cur); cur = []
    if cur: gaps.append(cur)
    storyish = [" ".join(x) for x in gaps if "want" in x and len(x) >= 6]
    open(f"stories/g{g}.txt", "w", encoding="utf-8").write("\n".join(fixed) + "\n")
    changed = sum(a != b for a, b in zip(lines, fixed))
    print(f"\n### g{g}: {len(fixed)} lines, {changed} repaired, {len(unmatched)} weakly matched, {len(storyish)} uncovered story-like gaps")
    for a, b in zip(lines, fixed):
        if a != b: print("   fix:", [x for x in zip(a.split(), b.split()) if x[0] != x[1]][:3] or b[:80])
    for r, l in unmatched: print(f"   weak {r}:", l[:140])
    for s in storyish: print("   GAP:", s[:300])
