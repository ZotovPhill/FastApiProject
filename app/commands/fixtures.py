import click
from dependency_injector.wiring import Provide, inject
from fpgen.command.fixtures import load_fixtures, create_config

from app.containers.repositories import DatabaseContainer
from app.orm.database import Database


# WIP!!!
@click.command(options_metavar="<options>")
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
@inject
def truncate_db(
        db: Database = Provide[DatabaseContainer.db]
):
    db.truncate_database()
    click.echo(click.style("Successfully truncated tables!", fg="green"))


@click.group()
def cli():
    pass


cli.add_command(load_fixtures)
cli.add_command(create_config)
cli.add_command(truncate_db)

if __name__ == '__main__':
    # Note: do not remove this import, container wiring required
    from app.main import app    # noqa: F403, F401
    cli()
