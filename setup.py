import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="raidify-davideolgiati",
    version="0.0.1",
    author="Davide Olgiati",
    author_email="davide.olgiati@hotmail.it",
    description="A simple python script to sync 2 folders",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davideolgiati/raidify",
    project_urls={
        "Bug Tracker": "https://github.com/davideolgiati/raidify/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="raidify"),
    python_requires=">=3.6",
)