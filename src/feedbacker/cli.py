import logging
import os

import click
import uvicorn

from feedbacker import __version__, config
# from feedbacker.enums import UserRoles
# from feedbacker.plugin.models import PluginInstance

# from .extensions import configure_extensions
# from .scheduler import scheduler

# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

log = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__)
def feedbacker_cli():
    """Command-line interface to Feedbacker."""
    # from .logging import configure_logging

    # configure_logging()

    # configure_extensions()
    pass


@feedbacker_cli.group("database")
def feedbacker_database():
    """Container for all feedbacker database commands."""
    pass


@feedbacker_database.command("init")
def database_init():
    """Initializes a new database."""
    click.echo("Initializing new database...")
    from .database import engine
    from .database import init_database

    init_database(engine)
    click.secho("Success.", fg="green")


# @feedbacker_database.command("drop")
# def drop_database():
#     """Drops all data in database."""
#     from sqlalchemy_utils import database_exists, drop_database

#     database_hostname = click.prompt(f"Please enter the database hostname (env = {config.DATABASE_HOSTNAME})")
#     database_name = click.prompt(f"Please enter the database name (env = {config.DATABASE_NAME})")
#     sqlalchemy_database_uri = f"postgresql+psycopg2://{config._DATABASE_CREDENTIAL_USER}:{config._QUOTED_DATABASE_PASSWORD}@{database_hostname}:{config.DATABASE_PORT}/{database_name}"

#     if database_exists(str(sqlalchemy_database_uri)):
#         if click.confirm(
#             f"Are you sure you want to drop database: '{database_hostname}:{database_name}'?"
#         ):
#             drop_database(str(sqlalchemy_database_uri))
#             click.secho("Success.", fg="green")
#     else:
#         click.secho(
#             f"Database '{database_hostname}:{database_name}' does not exist!!!", fg="red"
#         )

def entrypoint():
    """The entry that the CLI is executed from"""
    # from .exceptions import DispatchException

    try:
        feedbacker_cli()
    except Exception as e:
        click.secho(f"ERROR: {e}", bold=True, fg="red")
        log.exception(e)
    # except DispatchException as e:
    #     click.secho(f"ERROR: {e}", bold=True, fg="red")


if __name__ == "__main__":
    entrypoint()
