# Manipulate Sphinx config to keep old Read the Docs' behavior

> [!NOTE]  
> 
> _This extension is a temporary workaround to allow authors/theme developers to keep the old build behavior
> while they perform the required changes in their documentation/themes to not depend on it._

Read the Docs used to manipulate the Sphinx's `conf.py` file to:

- Inject different variables into the `html_context`
- ~~Add some extra JavaScript and CSS files~~ (via [`readthedocs-sphinx-ext`](https://github.com/readthedocs/readthedocs-sphinx-ext) extension)
- Configure canonical URL
- Define `latex_elements` and `latex_engine`
- Add `_build` to `exclude_patterns`
- ... and others

All this behavior was originally hardcoded on Read the Docs builders
([doc_builder/conf.py.tmpl](https://github.com/readthedocs/readthedocs.org/blob/288a47bb803d195090e4734b30242e7ebb544b91/readthedocs/doc_builder/templates/doc_builder/conf.py.tmpl))
and users weren't able to opt-out.
Read the Docs has deprecated this behavior and moved out from its core,
making a Sphinx project to build exactly in the same way that it would build locally.
However, projects _requiring_ the old and deprecated behavior may want to install this extension as a workaround while they perform the migration.
This migration may include updating Sphinx templates and hitting an API from their `conf.py` to get some data.

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
However, if you need any of these variables, read the following "Feedback" section.

## Feedback

We are happy to receive any feedback you may have regarding the Sphinx context injecting performed by Read the Docs.
This will help us to understand more your use case and adapt this extension to keep that compatibility;
or suggest you a potential solution/workaround for it.

If you want to share anything with us,
or are unsure about whether or not your need this extension,
please open a new issue in this repository.

## Reference

- [Issue tracking this deprecation work](https://github.com/readthedocs/addons/issues/72)
- [Announcement of these changes in Sphinx's furo theme](https://github.com/pradyunsg/furo/discussions/785)
