# Bragilovski2025 — domain-model dataset

Curated thesis dataset from **“Leveraging machines to derive domain models from user stories”** (Bragilovski et al., 2025).

- **Original dataset repository:** [Zenodo — authors’ research appendix](https://doi.org/10.5281/zenodo.15223349), published 15 April 2025 (`REJ-main.zip`).
- **Paper:** [Requirements Engineering](https://doi.org/10.1007/s00766-025-00442-9).
- **Dataset license:** [CC BY 4.0](LICENSE), as stated in the Zenodo record.

## Structure

```text
1_user_stories/                    # Nine project text files, UTF-8
2_gold_standard_domain_models/     # Nine Mermaid class diagrams (.mmd) only
3_visualizations/                  # Rendered SVG diagrams and visual gallery
scripts/render_models.py           # Regenerate or validate the diagrams
scripts/LICENSE                    # MIT license for scripts
CITATION.cff                      # Original paper as the preferred citation
LICENSE                           # CC BY 4.0 legal text
README.md
```

Projects: Camperplus, Fish & Chips, Grocery, Planningpoker, Recycling, School, Sports, Supermarket, and Ticket. Matching filenames pair stories with models (for example, `school.txt` and `school.mmd`).

## Preparation

The `original_data/` directory has been removed from this repository. The original appendix files, including the Excel gold-standard workbooks, are available in `REJ-main.zip` from the linked Zenodo repository.

The curated story files preserve wording, order, and blank lines. Only encoding and line endings were standardized to UTF-8 without a BOM and LF. Planningpoker was decoded from Windows-1252; the other source files were UTF-8.

Each Mermaid file combines the corresponding class list and association rows from the two original gold-standard workbooks. Labels, capitalization, and singular/plural differences are preserved exactly. An undirected `--` line represents each association; no relationship names, multiplicities, inheritance, attributes, or methods are inferred. Classes without associations remain present.

**Source inconsistencies:** some association endpoints do not occur in the class list (for example, `order` versus `orders`, or `cashier`). These endpoints appear as nodes marked `<<associationOnly>>` and are **not additional gold-standard classes**. Exclude marked nodes when evaluating class extraction. No synonyms or variants have been merged; the original workbooks remain authoritative.

Open `.mmd` files in a Mermaid-compatible viewer, or paste their contents into a fenced `mermaid` code block.

## Visual representations

[View all nine domain-model diagrams](3_visualizations/README.md). The SVG files can also be opened directly in a browser and enlarged without losing quality. The gallery uses local images and works offline.

After changing a Mermaid file, regenerate the SVGs with `python3 scripts/render_models.py` (Python 3, curl, and internet access required). This sends the public dataset diagrams to [Kroki's Mermaid renderer](https://kroki.io/); use `--endpoint URL` for a self-hosted Kroki instance. Renderer updates may change the layout. Run `python3 scripts/render_models.py --check` to check SVG node and association counts against the sources without network access.

## License and attribution

The dataset, diagrams, and documentation are licensed under the [Creative Commons Attribution 4.0 International license (CC BY 4.0)](LICENSE). Code in `scripts/` is separately licensed under the [MIT License](scripts/LICENSE). The original dataset is by Maxim Bragilovski, Ashley van Can, Arnon Sturm, and Fabiano Dalpiaz and is distributed in their [Zenodo research appendix](https://doi.org/10.5281/zenodo.15223349).

When sharing or adapting this material, credit the original creators, link to the source and [license](https://creativecommons.org/licenses/by/4.0/), and indicate changes. The encoding normalization, Mermaid conversion, and SVG visualizations in this curated repository are described above.

## Citation

If you use this dataset, please cite the original paper:

> Bragilovski, M., van Can, A. T., Dalpiaz, F., & Sturm, A. (2025). Leveraging machines to derive domain models from user stories. *Requirements Engineering, 30*, 241–262. https://doi.org/10.1007/s00766-025-00442-9

[CITATION.cff](CITATION.cff) provides machine-readable metadata with the paper as the preferred citation and the original Zenodo appendix as a source reference. When describing your data preparation, also link to this repository and note the transformations documented above.
