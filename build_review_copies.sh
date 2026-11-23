#!/bin/bash
# Build review copies with no model's AI on AI entries (an empty template in their place),
# for collecting a new model's entry blind. Output: _out/review/
set -e
cd "$(dirname "$0")"
./build.sh >/dev/null
mkdir -p _out/review
BLIND=1 python3 build/build_data.py
ATLAS_JSON=_out/data_blind.json OUT_HTML=_out/review/Thinking_Machines_Atlas_review_copy.html python3 build/make_standalone.py
BLIND=1 ATLAS_JSON=_out/data_blind.json python3 build/build_workbook.py _out/review/AI_arguments_table_review_copy.xlsx
python3 build/atlas_as_text.py _out/data_blind.json _out/review/Atlas_diagram_as_text.md
cp content/ai_models/AI_on_AI_prompt.md _out/review/
echo "built _out/review/"
