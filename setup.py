# setup.py - place in ROOT directory next to pyproject.toml
from setuptools import setup, find_packages

setup(
    name="gittensor-db",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
)