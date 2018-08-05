import pathlib

# Single source of truth for package version
__version__ = "0.0.1"

SRC_ROOT = pathlib.Path(__file__).parent
PROJECT_ROOT = SRC_ROOT.parent
REPO_ROOT = PROJECT_ROOT.parent
