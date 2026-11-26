"""Parse UMLet class diagrams: classes and relations with endpoints (by geometry)."""
import html, re, sys

def parse(path):
    t = open(path, encoding="utf-8").read()
    zm = re.search(r"<zoom_level>(\d+)</zoom_level>", t)
    z = int(zm.group(1)) / 10 if zm else 1.0
    els = []
    for e in re.findall(r"<element>.*?</element>", t, re.S):
        typ = re.search(r"<id>(.*?)</id>", e).group(1)
        g = [float(re.search(f"<{k}>(.*?)</{k}>", e).group(1)) for k in ("x", "y", "w", "h")]
        m = re.search(r"<panel_attributes>(.*?)</panel_attributes>", e, re.S)
        pa = html.unescape(m.group(1)) if m else ""
        add = re.search(r"<additional_attributes>(.*?)</additional_attributes>", e, re.S)
        els.append((typ, g, pa, add.group(1).strip() if add else ""))
    classes, rels, notes = [], [], []
    for typ, g, pa, add in els:
        if typ == "UMLClass":
            lines = []
            for l in pa.split("\n"):
                l = l.strip()
                if l.startswith("--"):
                    break
                if not l or re.match(r"^(bg|fg|lw|fontsize|layer|style|halign|valign|transparency)=", l):
                    continue
                lines.append(l)
            if lines and lines[0].startswith("<<"):
                lines = lines[1:]
            name = re.sub(r"\s+", " ", " ".join(lines)).strip().strip("/*_").strip()
            body = pa.split("--", 1)[1] if "--" in pa else ""
            classes.append((name, g, body.strip()))
        elif typ not in ("Relation",):
            notes.append((typ, pa.strip()))
    def at(px, py):
        best = None
        for n, (x, y, w, h), _ in classes:
            d = max(x - px, px - x - w, 0) ** 2 + max(y - py, py - y - h, 0) ** 2
            if best is None or d < best[0]:
                best = (d, n)
        return best
    for typ, g, pa, add in els:
        if typ != "Relation" or not add:
            continue
        p = [float(v) * z for v in add.split(";") if v.strip()]
        x, y = g[0], g[1]
        a, b = at(x + p[0], y + p[1]), at(x + p[-2], y + p[-1])
        lt = re.search(r"lt=(\S*)", pa)
        label = " ".join(l.strip() for l in pa.split("\n") if l.strip() and not re.match(r"^(lt|m1|m2|r1|r2|fontsize|bg|fg)=", l.strip())).strip()
        rels.append((a[1], b[1], lt.group(1) if lt else "-", round(a[0] ** .5), round(b[0] ** .5), label))
    return [c[0] for c in classes], rels, classes, notes

if __name__ == "__main__":
    for f in sys.argv[1:]:
        c, r, _, _ = parse(f)
        far = [x for x in r if max(x[3], x[4]) > 12]
        print(f, len(c), len(r), "far", len(far), "dupnames", len(c) - len(set(c)))
