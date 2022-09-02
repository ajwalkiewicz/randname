import os
from setuptools import setup

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

with open(f"{THIS_FOLDER}/README_PYPI.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rname",
    version="0.3.3",
    description="Get random first/last name",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ajwalkiewicz/randnames",
    project_urls={
        "Documentation": "https://ajwalkiewicz.github.io/randnames/_build/html/index.html"
        },
    author="Adam Walkiewicz",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["randname"],
    include_package_data=True,
    # packages=find_packages("src"),
    # package_dir={'': 'src'},
    # package_data={'': ['data/USA/fisrs_names/*']},
    # data_file=[('data', ['USA/fisrs_names/*'])],
    entry_points={
        "console_scripts": [
            "randnames=randnames.__main__:main"
        ]
    }
)
