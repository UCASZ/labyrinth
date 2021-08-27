#!/usr/bin/env python
"""
file: ignorelist
author: adh
created_at: 8/26/21 3:12 PM
"""

# Keys must match elements found in *_summary.json files
_IGNORE_REPOS = {
    "owner_login": ["alaial90", "Patrowl", "ryx1412"],
    "name": ["PatrowlHearsData", "NVD-Exploit-LIst-Ja"],
    "full_name": [
        "lsst-uk/lsst-ir-fusion",
        "dcs4cop/xcube",
        "CloudDefenseAI/cd",
        "th3ken-dev/TH3KEN-EDITON",
        "hesim-dev/rcea",
        "bsalha1/Printer",
        "hltfbk/E3C-Corpus",
        "darksideoftheshmoo/rcell2",
        "rcenvironment/rce",
        "endgameinc/xori",
        "vasileios-mavroeidis/semantic-stix-vulnerability",
    ],
}

IGNORE_REPOS = {}
for k, values in _IGNORE_REPOS.items():
    IGNORE_REPOS[k] = [v.lower() for v in values]

IGNORE_FILE_EXTS = [
    ".json",
    ".png",
    ".jpg",
    ".gif",
    ".owl",
]

IGNORE_DIRS = [
    ".git",
]


def main():
    pass


if __name__ == "__main__":
    main()
