# Keep deprecated Read the Docs' Sphinx build behavior

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

2. Add the extension in your Sphinx's `conf.py` file:

   ```python
   extensions = [
       # ... other extensions
       "sphinx_build_compatibility.extension",
   ]
   ```


## Differences with the deprecated behavior

There are some small differences with the old/deprecated behavior that we may implement
in a future iteration in case we receive some feedback from the users and we are not able
to work with them in a workaround.

The following variables **are not injected** in the ``html_context``:


| Variable               | Old value for reference                                                     |
|------------------------|-----------------------------------------------------------------------------|
| `MEDIA_URL`            | `https://media.readthedocs.org/`                                            |
| `STATIC_URL`           | `https://assets.readthedocs.org/static/`                                    |
| `analytics_code`       | `UA-123456`                                                                 |
| `api_host`             | `https://readthedocs.org`                                                   |
| `name`                 | `My project`                                                                |
| `programming_language` | `words`                                                                     |
| `proxied_api_host`     | `/_`                                                                        |
| `proxied_static_path`  | `/_/static/`                                                                |
| `single_version`       | `False`                                                                     |

Note that all these variables were used internally by Read the Docs and should probably not be required for regular users.
However, if you need any of these variables, contact us at support@readthedocs.org.

## Reference

- [Issue tracking this deprecation work](https://github.com/readthedocs/addons/issues/72)
- [Announcement of these changes in Sphinx's furo theme](https://github.com/pradyunsg/furo/discussions/785)
