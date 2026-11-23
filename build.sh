#!/bin/bash
# Build the site and the workbook from content/. Run from the repository root.
# Output: site/ (index.html, data.json, the workbook, a single-file copy of the Atlas, and a text version).
set -e
cd "$(dirname "$0")"
mkdir -p _out site
python3 build/assemble.py
python3 build/build_data.py
python3 build/build_page.py
python3 build/make_standalone.py
python3 build/build_workbook.py site/AI_arguments_table.xlsx
python3 build/atlas_as_text.py site/data.json site/Atlas_as_text.md
echo "built site/"
