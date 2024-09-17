#!/bin/env python3
# just 'python' doesn't work in container environment -_^
# We are using ilab 0.18 schema, version 3

import json
import textwrap
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

wrapper_snippets = textwrap.TextWrapper(
    width=112, replace_whitespace=False, break_long_words=False,
    drop_whitespace=False, break_on_hyphens=False
)
wrapper_text = textwrap.TextWrapper(width=112)
for e in raw:
    for k, v in e['logs'].items():
        for s in v['snippets']:
            snippet = v['content'][s['start_index']:s['end_index']]
            if len(snippet) > 150:
                # too big, we'll figure it out later
                continue
            # 120 is the instructlab limit for a yaml line
            # 112 = 7 spaces for padding, 112 the log line, 1 = EOL
            # since snippet is the log chunk, we wanna be as strict as possible on the wrapping
            snippet = wrapper_snippets.fill(snippet).strip()
            if not snippet:
                continue
            if snippet in haz_snippets:
                continue
            data["seed_examples"].append({
                "context": snippet,
                "questions_and_answers": [{
                    "question": "Explain log snippets from an RPM build.",
                    "answer": wrapper_text.fill(s["user_comment"])
                },{
                    "question": "How can I resolve the issue?",
                    "answer": wrapper_text.fill(e["how_to_fix"])
                },{
                    "question": "What is the reason the build has failed?",
                    "answer": wrapper_text.fill(e["fail_reason"])
                }]
            })
            haz_snippets.add(snippet)


# this default style enforces multiline strings
print(yaml.dump(data, default_style="|"))
