from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="slitherin",
    description="Pessimistic security Slither detectors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pessimistic-io/slitherin",
    author="Pessimistic.io",
    version="0.4.0",
    package_dir={"":"."},
    packages=find_packages(),
    license="AGPL-3.0",
    python_requires=">=3.8",
    install_requires=["slither-analyzer>=0.8.3"],
    extras_requires={
        "dev": ["twine>=4.0.2"],
    },
    entry_points={
        "slither_analyzer.plugin": "slither my-plugin=slither_pess:make_plugin",
    },
)
