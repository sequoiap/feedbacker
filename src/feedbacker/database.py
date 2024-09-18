from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from feedbacker.config import SQLALCHEMY_DATABASE_URL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_database(engine):
    """Initializes the database."""
    if not database_exists(str(SQLALCHEMY_DATABASE_URL)):
        create_database(str(SQLALCHEMY_DATABASE_URL))

    # schema_name = "dispatch_core"
    # if not engine.dialect.has_schema(engine, schema_name):
    #     with engine.connect() as connection:
    #         connection.execute(CreateSchema(schema_name))

    # tables = get_core_tables()

    Base.metadata.create_all(engine)#, tables=tables)

    # version_schema(script_location=config.ALEMBIC_CORE_REVISION_PATH)
    # setup_fulltext_search(engine, tables)

    # # setup an required database functions
    # session = sessionmaker(bind=engine)
    # db_session = session()

    # # we initialize the database schema
    # init_schema(engine=engine, organization=organization)

    # # we install all plugins
    # from dispatch.common.utils.cli import install_plugins
    # from dispatch.plugins.base import plugins

    # install_plugins()

    # for p in plugins.all():
    #     plugin = Plugin(
    #         title=p.title,
    #         slug=p.slug,
    #         type=p.type,
    #         version=p.version,
    #         author=p.author,
    #         author_url=p.author_url,
    #         multiple=p.multiple,
    #         description=p.description,
    #     )
    #     db_session.add(plugin)
    # db_session.commit()
