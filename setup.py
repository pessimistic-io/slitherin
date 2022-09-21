from setuptools import setup, find_packages

setup(
    name="slither-pess",
    description="Some pessimistic detectors",
    url="https://github.com/pessimistic-io/custom_detectors",
    author="Pessimistic",
    version="0.1",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["slither-analyzer>=0.8.3"],
    entry_points={
        "slither_analyzer.plugin": "slither my-plugin=slither_pess:make_plugin",
    },
)
