import pathlib

import setuptools

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')


setuptools.setup(
    name="parking_API",
    version="0.0.1",
    author="Ann Bond",
    author_email="annbondar4uk@gmail.com",
    description="Basic flask api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AnnBond/ParkingAPI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where='src'),
    scripts=["src/app.py"],
)
