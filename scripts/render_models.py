#!/usr/bin/env python3
"""Render the public benchmark's Mermaid files through Kroki (requires curl)."""

import argparse
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--endpoint', default='https://kroki.io',
                        help='Kroki base URL; receives each Mermaid source file')
    parser.add_argument('--check', action='store_true',
                        help='Validate existing SVG files without network access')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    sources = sorted((root / '2_gold_standard_domain_models').glob('*.mmd'))
    if not sources:
        parser.error('No Mermaid files found')
    rendered = []
    for source in sources:
        if args.check:
            data = (root / '3_visualizations' / f'{source.stem}.svg').read_bytes()
        else:
            response = subprocess.run(
                ['curl', '-L', '--fail', '--silent', '--show-error', '--retry', '2', '--max-time', '60',
                 '-H', 'Content-Type: text/plain', '--data-binary', '@' + str(source),
                 args.endpoint.rstrip('/') + '/mermaid/svg'],
                capture_output=True,
            )
            if response.returncode:
                parser.exit(1, response.stderr.decode('utf-8', errors='replace'))
            data = response.stdout
            # Keep dark association lines readable in viewers using dark backgrounds.
            data = data.replace(b'<svg ', b'<svg style="background-color: white;" ', 1)
        svg = ET.fromstring(data)
        if svg.tag != '{http://www.w3.org/2000/svg}svg':
            raise ValueError(f'{source.name}: response is not an SVG')
        # Confirm that Mermaid rendered every declared class and association.
        text = source.read_text(encoding='utf-8')
        expected_nodes = len(re.findall(r'^\s+class C\d+\[', text, re.M))
        expected_edges = len(re.findall(r'^\s+C\d+ -- C\d+\s*$', text, re.M))
        actual_nodes = sum('node' in e.attrib.get('class', '').split()
                           and e.tag.endswith('}g') for e in svg.iter())
        actual_edges = sum('relation' in e.attrib.get('class', '').split()
                           and e.tag.endswith('}path') for e in svg.iter())
        if (actual_nodes, actual_edges) != (expected_nodes, expected_edges):
            raise ValueError(f'{source.name}: rendered node/edge count differs: '
                             f'{actual_nodes}/{actual_edges} vs '
                             f'{expected_nodes}/{expected_edges}')
        rendered.append((source.stem, data))
        print(f'{source.name}: {actual_nodes} nodes, {actual_edges} associations', flush=True)
    if args.check:
        print(f'Validated {len(rendered)} SVG diagrams')
        return
    output = root / '3_visualizations'
    output.mkdir(exist_ok=True)
    for stem, data in rendered:
        destination = output / f'{stem}.svg'
        temporary = destination.with_suffix('.svg.tmp')
        temporary.write_bytes(data)
        temporary.replace(destination)
    print(f'Saved {len(rendered)} SVG diagrams in {output}')


if __name__ == '__main__':
    main()
