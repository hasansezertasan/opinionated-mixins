"""Look up the version of the installed distribution."""

from importlib.metadata import version


def version_lookup() -> str:
    """Return the installed distribution version for this project.

    Returns:
        str: The installed distribution version.
    """
    return version("opinionated-mixins")
