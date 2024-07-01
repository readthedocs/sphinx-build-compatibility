import os
from sphinx import version_info
from . import __version__
from .utils import get_github_username_repo, get_bitbucket_username_repo, get_gitlab_username_repo


# https://www.sphinx-doc.org/en/stable/extdev/appapi.html#event-html-page-context
def inject_context(app, pagename, templatename, context, doctree):
    # Add Read the Docs' static path.
    # Add to the end because it overwrites previous files.
    if not hasattr(app.config, "html_static_path"):
        app.config.html_static_path = []
    if os.path.exists('_static'):
        app.config.html_static_path.append('_static')

    # Define this variable in case it's not defined by the user.
    # It defaults to `alabaster` which is the default from Sphinx.
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme
    if not hasattr(app.config, "html_theme"):
        app.config.html_theme = 'alabaster'

    # Example: ``/docs/``
    conf_py_path = "/"
    conf_py_path += os.path.relpath(
            str(app.env.srcdir),
            os.getcwd(),
        ).strip("/")
    conf_py_path += "/"

    github_user, github_repo = get_github_username_repo(os.environ.get("READTHEDOCS_GIT_CLONE_URL"))
    bitbucket_user, bitbucket_repo = get_bitbucket_username_repo(os.environ.get("READTHEDOCS_GIT_CLONE_URL"))
    gitlab_user, gitlab_repo = get_gitlab_username_repo(os.environ.get("READTHEDOCS_GIT_CLONE_URL"))

    # Add project information to the template context.
    context = {
        'html_theme': app.config.html_theme,
        'current_version': os.environ.get("READTHEDOCS_VERSION_NAME"),
        'version_slug': os.environ.get("READTHEDOCS_VERSION"),

        # NOTE: these are used to dump them in some JS files and to build the URLs in flyout.
        # However, we are replacing them with the new Addons.
        # I wouldn't include them in the first version of the extension.
        # We could hardcode them if we want, tho.
        #
        # 'MEDIA_URL': "{{ settings.MEDIA_URL }}",
        # 'STATIC_URL': "{{ settings.STATIC_URL }}",
        # 'PRODUCTION_DOMAIN': "{{ settings.PRODUCTION_DOMAIN }}",
        # 'proxied_static_path': "{{ proxied_static_path }}",

        # TODO: use the APIv3 to get this data.
        # Maybe the `/_/addons/` because it has everything we need in just one call.
        #
        # 'versions': [{% for version in versions %}
        # ("{{ version.slug }}", "/{{ version.project.language }}/{{ version.slug}}/"),{% endfor %}
        # ],
        # 'downloads': [ {% for key, val in downloads.items %}
        # ("{{ key }}", "{{ val }}"),{% endfor %}
        # ],
        # 'subprojects': [ {% for slug, url in subproject_urls %}
        #     ("{{ slug }}", "{{ url }}"),{% endfor %}
        # ],
        "versions": [],
        "downloads": [],
        "subprojects": [],

        'slug': os.environ.get("READTHEDOCS_PROJECT"),
        'rtd_language': os.environ.get("READTHEDOCS_LANGUAGE"),
        'canonical_url': os.environ.get("READTHEDOCS_CANONICAL_URL"),

        # NOTE: these seem to not be used.
        # 'name': u'{{ project.name }}',
        # 'analytics_code': '{{ project.analytics_code }}',
        # 'single_version': {{ project.is_single_version }},
        # 'programming_language': u'{{ project.programming_language }}',

        'conf_py_path': conf_py_path,
        # Used only for "readthedocs-sphinx-ext" which we are not installing anymore.
        # 'api_host': '{{ api_host }}',
        # 'proxied_api_host': '{{ project.proxied_api_host }}',

        'github_user': github_user,
        'github_repo': github_repo,
        'github_version': os.environ.get("READTHEDOCS_GIT_IDENTIFIER"),
        'display_github': github_user is not None,
        'bitbucket_user': bitbucket_user,
        'bitbucket_repo': bitbucket_repo,
        'bitbucket_version': os.environ.get("READTHEDOCS_GIT_IDENTIFIER"),
        'display_bitbucket': bitbucket_user is not None,
        'gitlab_user': gitlab_user,
        'gitlab_repo': gitlab_repo,
        'gitlab_version': os.environ.get("READTHEDOCS_GIT_IDENTIFIER"),
        'display_gitlab': gitlab_user is not None,
        'READTHEDOCS': True,
        'using_theme': (app.config.html_theme == "default"),
        'new_theme': (app.config.html_theme == "sphinx_rtd_theme"),
        'source_suffix': ".rst",
        'ad_free': False,
        'docsearch_disabled': False,

        # We don't support Google analytics anymore.
        # See https://github.com/readthedocs/readthedocs.org/issues/9530
        'user_analytics_code': "",
        'global_analytics_code': None,

        'commit': os.environ.get("READTHEDOCS_GIT_COMMIT_HASH")[:8],
    }

    # For sphinx >=1.8 we can use html_baseurl to set the canonical URL.
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_baseurl
    if version_info >= (1, 8):
        if not hasattr(app.config, 'html_baseurl'):
            app.config.html_baseurl = context['canonical_url']
        context['canonical_url'] = None


    if hasattr(app.config, 'html_context'):
        for key in context:
            if key not in app.config.html_context:
                app.config.html_context[key] = context[key]
    else:
        app.config.html_context = context

    project_language = os.environ.get("READTHEDOCS_LANGUAGE")

    # User's Sphinx configurations
    language_user = app.config.language
    latex_engine_user = app.config.latex_engine
    latex_elements_user = app.config.latex_elements

    # Remove this once xindy gets installed in Docker image and XINDYOPS
    # env variable is supported
    # https://github.com/rtfd/readthedocs-docker-images/pull/98
    latex_use_xindy = False

    chinese = any([
        language_user in ('zh_CN', 'zh_TW'),
        project_language in ('zh_CN', 'zh_TW'),
    ])

    japanese = any([
        language_user == 'ja',
        project_language == 'ja',
    ])

    if chinese:
        app.config.latex_engine = latex_engine_user or 'xelatex'

        latex_elements_rtd = {
            'preamble': '\\usepackage[UTF8]{ctex}\n',
        }
        app.config.latex_elements = latex_elements_user or latex_elements_rtd
    elif japanese:
        app.config.latex_engine = latex_engine_user or 'platex'

    # Make sure our build directory is always excluded
    if not hasattr(app.config, "exclude_patterns"):
        app.config.exclude_patterns = []
    app.config.exclude_patterns.extend(['_build'])


def setup(app):
    app.connect('html-page-context', inject_context)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
