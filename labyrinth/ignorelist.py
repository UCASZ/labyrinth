#!/usr/bin/env python
"""
file: ignorelist
author: adh
created_at: 8/26/21 3:12 PM
"""

# Keys must match elements found in *_summary.json files
_IGNORE_REPOS = {
    "owner_login": [
        "alaial90",
        "Patrowl",
        "ryx1412",
        "davidecoluzzi",
        "csyongdu",
        "georgeslabreche",
        "XiaoYangLiu-FinRL",
        "tim-ings",
    ],
    "name": ["PatrowlHearsData", "NVD-Exploit-LIst-Ja", "rces-final-project"],
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
        "cgi-eoss/ftep",
        "olie304/MW4-Cosmetics",
        "WilliamYu1993/BAMSE",
        "EdwardSmith1884/GEOMetrics",
        "WeixiongLin/CS188-Proj1",
        "Ajabeer/SVM-RCE-R-results-Omnibus-dataset",
        "Tang1705/3D-Reconstruction-by-GF-4",
        "jinglou/p2019-cns-sod",
        "andrewgrider/dragonbook",
        "shuangj00/HARMONIES",
        "ejkim-dev/openCVex2",
        "ArgusScheduler/Argus",
        "cslab-ntua/contiguity-isca2020",
        "vam-sin/pconsc4-distance",
        "MathieuRita/SAR_denoising",
        "iai-group/irj-types",
        "ShixiangWang/absoluteCNVdata",
        "osmose-model/osmose",
        "theo-jaunet/visqa",
        "dimitramav/thesis-sentiment-analysis-in-tourism",
        "CedarVGC/Skeleton-extraction",
        "DPHRC/PSID-Exploitation",
        "CedricChing/DeepMRI",
        "minkee77/CMPNet",
        "AounEMuhammad/RCE-Sask-Group-D",
        "carlosloza/spindles-HMM",
        "rezvanshokranidev/RCE",
        "ShamimShahraeini/Deep-CNNs-for-image-classification-by-exploiting-transfer-learning-and-feature-concatenation",
        "thomasverelst/dynconv",
        "mthh/gaspar",
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
