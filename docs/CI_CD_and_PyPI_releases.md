## CI/CD and PyPI releases <!-- omit in toc -->

- [Usage](#usage)
  - [Running the CI/CD pipeline](#running-the-cicd-pipeline)
  - [Release to TestPyPI by incrementing version](#release-to-testpypi-by-incrementing-version)
  - [Releasing to PyPI by tagging commits](#releasing-to-pypi-by-tagging-commits)
- [Setting up a new project on TestPyPI and PyPI](#setting-up-a-new-project-on-testpypi-and-pypi)
  - [TestPyPI](#testpypi)
    - [Initial upload to TestPyPI](#initial-upload-to-testpypi)
    - [TestPyPI API token](#testpypi-api-token)
    - [Check uploaded test project](#check-uploaded-test-project)
  - [PyPI](#pypi)

---

# Usage

## Running the CI/CD pipeline

- The CI/CD pipeline is run whenever a commit is pushed up to the repo as per `.github/workflows/publish-to-test-pypi.yml`

## Release to TestPyPI by incrementing version

- Provided the project version in `pyproject.toml` is incremented, and the CI/CD testing passes, releases are made to TestPyPI after a commit is pushed.

## Releasing to PyPI by tagging commits

- Putting a tag on a commit and pushing it will cause the GitHub CI/CD to run and create a PyPI release.

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

# Setting up a new project on TestPyPI and PyPI

For new projects, check this out.

## TestPyPI

Run through uploading to TestPyPI first. If it goes well, then repeat for PyPI

### Initial upload to TestPyPI

- Upload using TestPyPI global scope API key;

```bash
python3 -m pip install --upgrade twine # Maybe I should add twine to requirements_dev.in?
python3 -m build # ? python -m build --sdist --wheel --outdir dist/
python3 -m twine upload --repository TestPyPI dist/*
    # user name = __token__
    # For p/w, get "API token - Global scope" in 1Password "TestPyPI - grumBit" item 
```

### TestPyPI API token

- Create a new token specifically for the project in TestPyPI;
  - Head to [Test PtPI](https://test.pypi.org/manage/projects/) -> `Manage` for fullapp -> `Settings` -> `Create a token for fullapp`
  - Set `Token name` to fullapp
  - Change the `Scope` to "Project: fullapp`
  - Click `Add Token`
  - Add the generated token in a new password field named '🔑 API Token - "fullapp"' in the 1Password "TestPyPI - grumBit" item
- Test the new token by running `python3 -m pip install --upgrade twine` again, but with the new token

- Add the TestPyPI API token to GitHub
  - Open the [repo on github](https://github.com/grumBit/fullapp) -> `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`
  - Name = "TEST_PYPI_API_TOKEN"
  - Secret = The project's API token form the 1Password "TestPyPI - grumBit" item

### Check uploaded test project

- In a new directory, create a new python venv;

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install wheel pip-tools

python3 -m venv .venv ; source .venv/bin/activate ; pip install --upgrade pip ; pip install wheel pip-tools

```

- Install the new project;

```bash
package_name="fullapp"
python3 -m pip install --index-url https://test.pypi.org/simple/ --pre ${package_name}  # Check the package can be installed
python3 -c "from fullapp import myapp" # Check package functions
```

## PyPI

_(NB: This mostly repeats the TestPyPI steps above)_

- Initial upload to PyPI;

```bash
python3 -m build # Only needed if github actions has built a more recent version in TestPyPI than the last manually built one
python3 -m twine upload  dist/* 
    # User name = __token__
    # For p/w, get "API token - Global scope" in 1Password "PyPI - grumBit" item 
```

- As per TestPyPI, setup a PyPI API token;
  - Create a new PyPI API token for the project in [PyPI](https://pypi.org/manage/projects/)
  - Add the token into the 1Password PyPI item
  - Add the token to repo in GitHub

- Check new API token works by uploading again
  
```bash
python3 -m twine upload  dist/* 
```

- Try installing and running in a new .venv;

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
python3 -c "from fullapp import myapp; myapp.MyApp().say('hi')"
```
