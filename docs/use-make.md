# How-To Guides

## Using Make in This Project

This project uses `make` to automate various tasks. Below are the available commands and their descriptions:

### Setup
To set up the project, run:
```sh
make setup
```
This will check if `uv` is installed and set up the project environment.

### Build
To build the project, run:
```sh
make build
```
This will check the code, run tests, and build the package.

### Test
To run the tests, use:
```sh
make test
```
This will run the tests excluding those marked as slow.

To run all tests, use:
```sh
make test_all
```

### Clean
To clean the project, run:
```sh
make clean
```
This will remove the virtual environment, build files, and cache.

### Format
To format the project files, run:
```sh
make format
```
This will format the files using `ruff`.

### Check
To check the project files, run:
```sh
make check
```
This will check the files using `ruff`.

### Type Checking
To check the typing, run:
```sh
make type
```
This will check the typing using `mypy`.

### Documentation
To build the documentation, run:
```sh
make docs
```

To serve the documentation locally, run:
```sh
make docs_serve
```

To upload the documentation, run:
```sh
make docs_upload
```