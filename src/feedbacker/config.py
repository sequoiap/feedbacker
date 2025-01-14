import logging
import os
import base64
from urllib import parse
from typing import List
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings


log = logging.getLogger(__name__)


class BaseConfigurationModel(BaseModel):
    """Base configuration model used by all config options."""

    pass


def get_env_tags(tag_list: List[str]) -> dict:
    """Create dictionary of available env tags."""
    tags = {}
    for t in tag_list:
        tag_key, env_key = t.split(":")

        env_value = os.environ.get(env_key)

        if env_value:
            tags.update({tag_key: env_value})

    return tags


# ROOT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PROJ_ROOT_DIR = Path(__file__).parent.resolve()
REPO_ROOT_DIR = PROJ_ROOT_DIR.parent.parent.resolve()

DEFAULT_ENV_FILE = REPO_ROOT_DIR / ".env"
config = Config(DEFAULT_ENV_FILE)

# static files
DEFAULT_STATIC_DIR = Path(__file__).parent.resolve() / "static"
STATIC_DIR = config("STATIC_DIR", default=DEFAULT_STATIC_DIR)
DEFAULT_UPLOADS_DIR = DEFAULT_STATIC_DIR / "uploads"
UPLOADS_DIR = config("UPLOADS_DIR", default=DEFAULT_UPLOADS_DIR)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# templates
DEFAULT_TEMPLATE_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), os.path.join("templates")
)
TEMPLATE_DIR = config("TEMPLATE_DIR", default=DEFAULT_TEMPLATE_DIR)

loader = FileSystemLoader([
    TEMPLATE_DIR,
])
env = Environment(loader=loader, autoescape=True)
templates = Jinja2Templates(env=env)

# database
# DEFAULT_DATABASE_FILE = os.path.join(
#     os.path.abspath(os.path.dirname(__file__)), os.path.join("static")
# )
# DEFAULT_DATABASE_FILE = "sqlite+aiosqlite:///./data.db"
DEFAULT_DATABASE_FILE = "sqlite:///./data.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = config("STATIC_DIR", default=DEFAULT_DATABASE_FILE)

# auth
FEEDBACKER_JWT_SECRET = config("FEEDBACKER_JWT_SECRET", default="supersecret")
FEEDBACKER_JWT_ALG = config("FEEDBACKER_JWT_ALG", default="HS256")
FEEDBACKER_JWT_EXP = config("FEEDBACKER_JWT_EXP", default=86400)  # seconds
AUTH_COOKIE_NAME = config("AUTH_COOKIE_NAME", default="auth_token")
REFRESH_COOKIE_NAME = config("REFRESH_COOKIE_NAME", default="refresh_token")

LTSPICE_EXE = config("LTSPICE_EXE", default="")
