# Contributing

Thanks for helping. The Atlas is meant for students meeting this literature for the first time, so the most valuable contributions are corrections: a summary its author would reject, a stance label that misleads, a source that is wrong or missing.

## The easy way: open an issue

[Open an issue](https://github.com/djestrada/Thinking-Machines-Atlas/issues/new/choose) and give the row ID (for example `3.06`). Say what is wrong and, if you can, give a source. An editor will make the change.

## Editing directly

Every argument is one file, `content/rows/<cluster>/<id>.yaml`. On GitHub you can open the file, click the pencil icon, make your change and propose it; GitHub turns that into a pull request for an editor to review. Each pull request is built automatically, and the check fails if the content has an error (an unknown row ID, a misspelled stance).

### The fields of a row

| Field | What it holds |
| --- | --- |
| `id`, `cluster` | Must match the file name and folder |
| `thread`, `order` | The group of rows it sits with, and its place in the cluster (decimals are fine: `1.5`) |
| `stance` | `For`, `Against` or `Deflationary`, relative to the cluster's question (in `content/project.yaml`), not to machine minds in general |
| `arg`, `target`, `scope` | The argument's name, what it is about, and which machines it concerns |
| `family` | A family key from `content/project.yaml` (`F01`–`F29`) |
| `summary` | What the author argues, at the strength they argue it, in plain language |
| `orig`, `link` | The original source with a DOI or stable link, and the best free copy if there is one |
| `further`, `resp` | Further reading; responses and objections (one item per line, each with a source) |
| `note` | Editorial notes, kept short |
| `see_also` | Related rows that have no entry in `relations.yaml` |
| `ver_status` | Four items: the bibliographic check, the summary check, what access the link gives, and anything outstanding |

### Guidelines

- **Summaries say what the author says.** If you are interpreting, say whose interpretation it is and cite it.
- **Every claim about a source needs the source.** Prefer free copies (author pages, PhilArchive, arXiv, open-access journals). Leave paywalled newspaper pieces unlinked.
- **Relations** go in `content/relations.yaml`: `source` row, `relation` (objects to, responds to, parallels, extends, supports, develops, …), `target` row and a one-line `note`. Use an existing relation type where one fits.
- **A new argument** takes the next free number in its cluster, so existing IDs never change. Add at least one relation for it.
- **Add a line to `content/changelog.yaml`** for anything a reader would notice.
- **Say if you used an AI tool** to draft a change, and check what it wrote against the source yourself.

## AI on AI entries

New entries are collected blind: the model is given review copies with no other model's entries. Build them with `./build_review_copies.sh`, give the model the files in `_out/review/` with `AI_on_AI_prompt.md`, and import its answer with `scripts/import_template.py` (see `content/ai_models/README.md`).

## License of contributions

By contributing you agree that your contribution is licensed under the project's licenses: CC BY-SA 4.0 for content and MIT for code (see `LICENSE-CONTENT` and `LICENSE`).
