#!/bin/env python3
# just 'python' doesn't work in container environment -_^
# We are using ilab 0.18 schema, version 3

import json
from typing import Optional

import yaml
import glob
import pathlib
import sys

try:
    LOGDETECTIVE_DATA_DIR = pathlib.Path(sys.argv[1])
except IndexError:
    print(
        f"usage: {sys.argv[0]} PATH\n\n"
        "First argument (PATH) is a path to directory tree of unpacked"
          " results from the https://logdetective.com/download website.")
    sys.exit(1)

data = {
    "version": 3,
    "created_by": "Log Detective Team",
    "domain": "software",
    # dropped in version 3
    # "task_description": "Annotated snippets from software logs that explain problems",
    "seed_examples": [],
    "document_outline": "Building RPMs",
    "document": {
        "repo": "https://github.com/fedora-copr/logdetective-taxonomy",
        "commit": "HEAD",
        "patterns": ["README.md"]
    }
}

raw = []
# ilab doesn't allow duplicate entries, so we need to make our entries unique
haz_snippets = set()
for file in glob.glob(f"{LOGDETECTIVE_DATA_DIR}/**/*.json", recursive=True):
    with open(file) as f:
        raw.append(json.load(f))


def smart_string_split(s) -> Optional[str]:
    """ilab enforces line length below 120 chars, so we need to split
    our text to fit; this is a naive algorith to halve text until it fits,
    while splitting it on empty space ' '."""
    le = len(s)
    if le <= 110:
        return s

    le_half = int(le / 2)
    s91 = s[le_half:]
    try:
        s1, s2 = s91.split(" ", maxsplit=1)
    except ValueError:
        # no space :/ don't know what to do
        return None
    before = f"{s[:le_half]}{s1}"
    after = s2
    # 112 = 7 spaces for padding, 112 the log line, 1 = EOL
    if len(before) >= 112 or len(after) >= 112:
        return f"{smart_string_split(before)}\n{smart_string_split(after)}"
    else:
        return f"{before}\n{after}"


for e in raw:
    for k, v in e['logs'].items():
        for s in v['snippets']:
            snippet = v['content'][s['start_index']:s['end_index']]
            if len(snippet) > 150:
                # too big, we'll figure it out later
                continue
            snippet = smart_string_split(snippet)
            if snippet is None:
                continue
            if snippet in haz_snippets:
                continue
            data["seed_examples"].append({
                "context": snippet,
                "questions_and_answers": [{
                    "question": "Explain log snippets from an RPM build.",
                    "answer": smart_string_split(s['user_comment']),
                },{
                    "question": "How can I resolve the issue?",
                    "answer": smart_string_split(e["how_to_fix"])
                },{
                    "question": "What is the reason the build has failed?",
                    "answer": smart_string_split(e["fail_reason"])
                }]
            })
            haz_snippets.add(snippet)

# this default style enforces multiline strings
print(yaml.dump(data, default_style="|"))
