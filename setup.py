from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="randnames",
    version="0.0.6",
    description="Draw random first and last USA names",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ajwalkiewicz/randnames",
    author="Adam Walkiewicz",
    author_email="aj.walkiewicz@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3.8",
    ],
    packages=["randnames"],
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