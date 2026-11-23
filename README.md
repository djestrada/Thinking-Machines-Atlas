# Thinking Machines Atlas

A teaching map of the debate over whether machines can think, understand, feel, act or matter morally: 134 arguments for and against, in 11 clusters, with sources, responses and the relations between them.

- **The Atlas** (interactive): https://djestrada.github.io/Thinking-Machines-Atlas/
- **The workbook** (spreadsheet, same row IDs): [AI_arguments_table.xlsx](https://djestrada.github.io/Thinking-Machines-Atlas/AI_arguments_table.xlsx)
- **Single-file copy** of the Atlas, for offline use: [Thinking_Machines_Atlas.html](https://djestrada.github.io/Thinking-Machines-Atlas/Thinking_Machines_Atlas.html)
- **Text version**, for screen readers and AI models: [Atlas_as_text.md](https://djestrada.github.io/Thinking-Machines-Atlas/Atlas_as_text.md)

The Atlas's overview follows five questions in order: Q0 who asks, and why; Q1 is there a fact of the matter; Q2 what would it take, and can computation supply it; Q3 how could we tell; Q4 what follows. Each cluster has a view of its exchanges: the claim in dispute, and the moves on each side. An AI on AI page compares how several AI models judge the arguments.

## Who made it

Created and edited by Daniel Estrada (NJIT). Drafted and built with Claude (Anthropic); reviewed by AI models (see AI on AI). Every summary has been checked against an abstract, an encyclopedia entry or an open copy of its source, but not yet by specialists. Read the sources before relying on a summary, and please tell us where one is wrong.

## How it is organized

| Folder | What is in it |
| --- | --- |
| `content/rows/<cluster>/<id>.yaml` | One file per argument: summary, stance, sources, responses, notes, verification |
| `content/relations.yaml` | How the arguments bear on each other (objects to, responds to, parallels, …) |
| `content/project.yaml` | Clusters and their questions, families of arguments, the five kernel questions |
| `content/ai_models/` | Each AI model's AI on AI entry, the prompt used to collect them, and withdrawn entries |
| `content/*.yaml` | The workbook README, the Kernel, Families and Existing surveys tabs, the changelog |
| `build/` | The scripts that build the Atlas and the workbook. The overview, Guide and exchanges are still written in `build/build_data.py` and `build/ex_3_11.py` |

`content/` is the single source. Nothing in `site/` is edited by hand: every change to `main` rebuilds the site and publishes it.

## Contributing

Corrections, missing arguments and better sources are all welcome. The easiest way is to [open an issue](https://github.com/djestrada/Thinking-Machines-Atlas/issues). To edit directly, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Building it yourself

You need Python 3 with `pyyaml` and `openpyxl`.

```
pip install pyyaml openpyxl
./build.sh                 # builds site/ from content/
./build_review_copies.sh   # copies with no AI model's entries, for collecting a new one blind
```

Open `site/index.html` through a local server (for example `python3 -m http.server -d site`), since the page loads `data.json`.

## License

Content (everything in `content/`, the text of the Atlas, and the built workbook and pages) is under [CC BY-SA 4.0](LICENSE-CONTENT): you may share and adapt it for any purpose, with credit, under the same license. Code is under the [MIT License](LICENSE). The works cited belong to their authors and publishers; short quotations are included under fair use.
