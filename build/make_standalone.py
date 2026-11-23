"""Single self-contained copy of the Atlas: data inlined, with its own doctype and head."""
import json, os
html = open("site/index.html").read()
data = open(os.environ.get("ATLAS_JSON", "site/data.json")).read().replace("</", "<\\/")
html = html.replace('fetch("data.json").then(r => r.json()).then(data => {',
                    'Promise.resolve(JSON.parse(document.getElementById("atlas-data").textContent)).then(data => {')
assert "atlas-data" in html
head, rest = html.split("<style>", 1)
out = ('<!doctype html>\n<html lang="en">\n<head>\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + head + "<style>" + rest.split("</style>", 1)[0] + "</style>\n</head>\n<body>\n"
       + rest.split("</style>", 1)[1].replace("<script>\nconst NS", f'<script type="application/json" id="atlas-data">{data}</script>\n<script>\nconst NS', 1)
       + "\n</body>\n</html>\n")
open(os.environ.get("OUT_HTML", "site/Thinking_Machines_Atlas.html"), "w").write(out)
print("standalone", len(out))
