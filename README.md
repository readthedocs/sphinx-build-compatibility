# Sphinx extension to keep old Read the Docs' build behavior

Read the Docs used to manipulate the Sphinx's `conf.py` file to:

- Add some extra JavaScript and CSS files
- Inject different variables into the `html_context`
- ... and others

Since Read the Docs has deprecated this behavior and new projects are not getting it,
they can still opt-in by manually installing this extension.

## Installation

1. Install the package using `pip`
```bash
pip install git+https://github.com/readthedocs/sphinx-build-compatibility#egg=sphinx-build-compatibility
```
1. Add the extension in your Sphinx's `conf.py` file:
```python
extensions = [
  # ... other extensions
  "sphinx_build_compatibility.extension",
]
```

## Reference

- [Issue tracking this deprecation work](https://github.com/readthedocs/addons/issues/72)
- [Announcement of these changes in Sphinx's furo theme](https://github.com/pradyunsg/furo/discussions/785)
