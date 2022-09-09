![PyPI](https://img.shields.io/pypi/v/example-package-grumbit)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/example-package-grumbit)
![GitHub all releases](https://img.shields.io/github/downloads/grumbit/python_packaging_example/total)
[![GitHub license](https://img.shields.io/github/license/grumbit/python_packaging_example)](https://github.com/grumbit/python_packaging_example/blob/main/LICENSE)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/example-package-grumbit)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/example-package-grumbit)
![PyPI - Status](https://img.shields.io/pypi/status/example-package-grumbit)
[![GitHub issues](https://img.shields.io/github/issues/grumbit/python_packaging_example)](https://github.com/grumbit/python_packaging_example/issues)
[![GitHub forks](https://img.shields.io/github/forks/grumbit/python_packaging_example)](https://github.com/grumbit/python_packaging_example/network)
[![GitHub stars](https://img.shields.io/github/stars/grumbit/python_packaging_example)](https://github.com/grumbit/python_packaging_example/stargazers)

# Python Packaging Example<!-- omit in toc -->

This is a working example that uses a GitHub actions CI/CD workflow to test, build and upload a Python package to TestPyPi and PyPi.

I created this example package by working through these guides;

- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Publishing package distribution releases using GitHub Actions CI/CD workflows](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [PyTest With GitHub Actions](https://blog.dennisokeeffe.com/blog/2021-08-08-pytest-with-github-actions)

The rest of the README describes to set up a new project in the same way.

When set up;

- Test and upload to TestPyPi occurs when the [package version number](./pyproject.toml) is updated and a commit is made to the master branch
- Test and upload to PyPi occurs when a [commit is tagged](#uploading-to-pypi-via-tagging)
- The package can be installed using `pip install example-package-grumbit`

---

## Table of contents<!-- omit in toc -->

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->
- [High level](#high-level)
- [Packaging Python Projects](#packaging-python-projects)
  - [Building the package](#building-the-package)
  - [Uploading the package to TestPyPi](#uploading-the-package-to-testpypi)
  - [Uploading the package to PyPi](#uploading-the-package-to-pypi)
  - [Manually updating the package](#manually-updating-the-package)
- [GitHub Actions CI/CD workflows](#github-actions-cicd-workflows)
  - [Set up](#set-up)
  - [Uploading to `TestPyPi` via commit to master](#uploading-to-testpypi-via-commit-to-master)
  - [Uploading to `PyPi` via tagging](#uploading-to-pypi-via-tagging)
- [Running pytest in GitHub CI/CD](#running-pytest-in-github-cicd)
<!-- /code_chunk_output -->

---

## High level

At a high level, the process for setting up GitHub CI/CD project packaging, including pytesting, looks like this;

1. Set up the file structure as per this example package, but leave out `./.github/workflows/publish-to-test-pypi.yml` for now.
2. Get [local packaging](#building-the-package) working
3. Get [uploading to TestPyPi](#uploading-the-package-to-testpypi) working
4. Get [uploading to PyPi](#uploading-the-package-to-pypi) working
5. Add in  [`./.github/workflows/publish-to-test-pypi.yml`](.github/workflows/publish-to-test-pypi.yml) and get [GitHub CI/CD](#set-up) working

---

## Packaging Python Projects

### Building the package

- The package [metadata is configured](https://packaging.python.org/en/latest/tutorials/packaging-projects/#creating-pyproject-toml) in [./pyproject.toml](./pyproject.toml)
- Once configured, it can be built with;

```bash
cd <pacakges directory>
python3 -m venv .venv # Create the venv if it doesn't exist yet
source .venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel pip-tools pytest # Install the tools needed for the build tool
python3 -m pip install --upgrade build # Install the build tool itself
python3 -m build # build the package
```

### Uploading the package to TestPyPi

- Upload the package for testing using;

```bash
python3 -m pip install --upgrade twine # Install the twine upload tool
python3 -m twine upload --repository testpypi dist/* # Upload to TestPyPi
    # When prompted, the username is __token__ and the password is the TestPyPi global scope API token
```

- Having uploaded the package, a package specific [API token should be set up and saved](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives) in [TestPyPi](https://test.pypi.org)

- Check the package can be downloaded and used in a new `venv`;

```bash
cd <some new tmp directory>
python3 -m venv .venv 
source .venv/bin/activate
package_name="example-package-grumBit"
python3 -m pip install --index-url https://test.pypi.org/simple/ --pre ${package_name}  # Check the package can be installed
python3 -c "from example_package_grumbit import example; print(example.add_one(1))" # Check package functions
```

### Uploading the package to PyPi

```bash
python3 -m twine upload dist/* # Upload to PyPi
    # When prompted, the username is __token__ and the password is the PyPi global scope API token
```

- Having uploaded the package, a package specific [API token should be set up and saved](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives) in [PyPi](https://pypi.org)

### Manually updating the package

- Each time the package is updated, it's version must be updated in the `[project]` section of [./pyproject.toml](./pyproject.toml), then it needs to be re-built and uploaded;

```bash
vs ./pyproject.toml
python3 -m build # build the package
python3 -m twine check dist/* # check the package can be uploaded
python3 -m twine upload --repository testpypi dist/* # test uploading using TestPyPi
python3 -m twine upload dist/* # Upload to PyPi

```

---

## GitHub Actions CI/CD workflows

### Set up

- If the project isn't already sync'd up to GitHub, run;

```bash
cd "<the project's directory>"
repo_name="<the new repo's name>"
gh repo create "${repo_name}" --private
git init
git add --all
git commit -m "init"
git branch -M master
git remote add origin git@github.com:grumBit/${repo_name}.git
git push -u origin master
```

- If the default branch isn't `master`, either [change it on GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/changing-the-default-branch), or change `.github/workflows/publish-to-test-pypi.yml`.
- [Add the TestPyPi and PyPi API tokens to the repo](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/#saving-credentials-on-github)

- Open the repo on GitHub using `gh browse`. In the browser, click `Settings` -> `Secrets` -> `Actions`. Then add two new secrets called `PYPI_API_TOKEN` and `TEST_PYPI_API_TOKEN`, with the API tokens created after uploading the packages above
- Create and configure [.github/workflows/publish-to-test-pypi.yml](.github/workflows/publish-to-test-pypi.yml) workflow definition
  - NB: This example package's `publish-to-test-pypi.yml` already has the parts needed for auto-testing included (see below)

### Uploading to `TestPyPi` via commit to master

- Every time a commit is made to the `master` branch, the GitHub CI/CD will run.
  - NB: For the packaging to succeed, the version must be updated in [./pyproject.toml](./pyproject.toml).
- All commits to master will be uploaded to `TestPyPi`

### Uploading to `PyPi` via tagging

- Putting a tag on a commit and pushing it will cause GitHub CI/CD to run and create a PyPi release.

- Use the following to tag the lastest commit (i.e. `HEAD`) with the version currently configured in `./pyproject.toml`;

```bash
version_tag=v$(cat ./pyproject.toml | egrep "^version" | cut -d '"' -f2)
version_tag_info="Some release info"
git tag -a "${version_tag}" -m "${version_tag_info}"
git push --tag
```

- Use the following to tag a prior commit;

```bash
version_tag="vX.X.X"
version_tag_info="Some release info"
commit_sha="16fb0fd"
git tag -a "${version_tag}" "${commit_sha}" -m "${version_tag_info}"
git push --tag
```

---

## Running pytest in GitHub CI/CD

- The workflow steps in the [GitHub CI/CD](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/) guide didn't include running pytests. To get pytest to run the packages dependencies needed to be installed and then pytest run prior to the build step using these additional steps;

```yaml
    - name: Install requirements
      run: >-
        python -m
        pip install
        --requirement requirements.txt
    - name: Run tests
      run: >-
        python -m
        pytest
```

- As per the directory structure in the [packaging projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) guide, I put the tests in a separate hierarchy to the source. This meant `__init__.py` needed to added to the `src/` and `tests/` directory like this;
  - _NB: I'm not 100% sure about this structuring. It follows the guide and means the test code isn't packaged up, however, I think it's less convenient than embedding `test/` folders within the `src/` tree. `./pyproject.toml` can be configured so that embedded `test/` folders are excluded, but I've gone with the "standard" for now._

```txt
packaging_tutorial/
├── src/
│   ├── __init__.py
│   └── example_package_grumbit/
│       ├── __init__.py
│       └── example.py
└── tests/
    ├── __init__.py
    └── example_package_grumbit/
        ├── __init__.py
        └── test_example.py
```
