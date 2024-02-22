from setuptools import setup, find_packages
from slitherin.cli import SLITHERIN_VERSION

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="slitherin",
    description="Pessimistic security Slither detectors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"slitherin": ["py.typed"]},
    url="https://github.com/pessimistic-io/slitherin",
    author="Pessimistic.io",
    author_email="info@pessimistic.io",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries",
    ],
    version=SLITHERIN_VERSION,
    packages=find_packages(),
    license="AGPL-3.0",
    python_requires=">=3.8",
    install_requires=["slither-analyzer>=0.10.0"],
    extras_requires={
        "dev": ["twine>=4.0.2"],
    },
    entry_points={
        "slither_analyzer.plugin": "slither slitherin-plugins=slitherin:make_plugin",
        "console_scripts": ["slitherin=slitherin.cli:main"],
        "napalm.collection": ["slitherin=slitherin.napalm:entry_point"],
    },
    include_package_data=True,
)
