# AI on AI entries

One JSON file per AI model, read by `build/build_data.py`. Models are shown in alphabetical order, so none is listed first by default.

**Fields:** `key`, `name`, `maker`, `collected` (date), `collected_by`, `method` (how the model was prompted, and whether it had seen other entries), `intro` (the model's own words), and `rows`: one per cluster `"1"`–`"11"` plus `"all"`, each with `k`, `q`, `strong[]`, `weak[]`, `land`, `follow`, `strong_txt`, `weak_txt`. Argument IDs must exist in the table; the build fails otherwise.

**Collecting an entry:** run `./build_review_copies.sh`, give the model the files in `_out/review/` together with `AI_on_AI_prompt.md`, and ask it to forget other sessions.

**Importing an answer:**

```
COLLECTED="23 November 2026" python3 scripts/import_template.py ANSWER.md content/ai_models/KEY.json KEY "Name" "Maker" "method text" [drop=k:id,k:id] [addstrong=k:id,...] [addweak=k:id,...]
```

`addstrong` and `addweak` add picks the model named without an ID; `drop` removes picks. A column that names no IDs keeps its text as a note.

`withdrawn/` holds the first Gemini and ChatGPT entries, collected after they had seen Claude's. They are kept for the record and not shown.
