from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["scipy", "sympy", "pandas", "matplotlib", "numpy"]

setup(
    name="crphelper",
    version="0.0.9",
    author="Tomomi (Kelly) Hamamoto",
    author_email="khamamoto@hmc.edu",
    description="A package to help analyze CRPropa simulations",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/crphelper/homepage/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
)
