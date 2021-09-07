from distutils.core import setup

setup(
    name="labyrinth",
    version="0.8",
    packages=["labyrinth"],
    scripts=[
        "scripts/search_github",
        "scripts/generate_summaries",
        "scripts/repo_deep_dive",
        "scripts/repo_to_vul_id",
    ],
    url="https://vuls.cert.org",
    license="all rights reserved",
    author="adh",
    author_email="adh@cert.org",
    description="search github for exploits",
    include_package_data=True,
    package_data={
        "": [
            "data/*.txt",
        ]
    },
)
