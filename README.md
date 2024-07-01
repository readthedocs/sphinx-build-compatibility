# Sphinx extension to keep old Read the Docs behavior

Read the Docs used to manipulate the Sphinx's `conf.py` file to:

- Add some extra JavaScript and CSS files
- Inject different variables into the `html_context`
- ... and others

Since Read the Docs has deprecated this behavior and new projects are not getting it,
they can still opt-in by manually installing this extension.

```bash
pip install readthedocs-sphinx-compatibility
```

## Reference

- [Issue tracking this deprecation work](https://github.com/readthedocs/addons/issues/72)
- [Announcement of these changes in Sphinx's furo theme](https://github.com/pradyunsg/furo/discussions/785)
