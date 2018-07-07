import json

try:
    import click
except ImportError:
    raise ImportError("Please install the optional `cli` extras to use the CLI.")
import crunchy_api
from crunchy_api import CrunchyrollApi
from crunchy_api import types

@click.group()
@click.option("--username", required=True, envvar="CRUNCHYROLL_USERNAME")
@click.option("--password", envvar="CRUNCHYROLL_PASSWORD")
@click.option("--token", required=True, envvar="CRUNCHYROLL_TOKEN")
@click.option("--locale", default="enUS", envvar="CRUNCHYROLL_LOCALE")
@click.option(
    "--stdin-password", is_flag=True, default=False, help="Read password in from stdin"
)
@click.pass_context
def main(
    ctx: click.core.Context,
    username: str,
    password: str,
    token: str,
    locale: str,
    stdin_password: bool,
) -> None:
    if not (password or stdin_password):
        raise click.UsageError("Must supply one of `password` or `stdin_password`")

    if stdin_password:
        password = input()
    ctx.obj = CrunchyrollApi(username, password, token)


@main.command()
@click.option(
    "--object-type",
    required=True,
    type=click.Choice(list(crunchy_api.INFO.values())),
    default="series_id",
    envvar="CRUNCHYROLL_OBJECT",
)
@click.option("--object-id", required=True, type=int, envvar="CRUNCHYROLL_ID")
@click.pass_context
def info(ctx: click.core.Context, object_type: str, object_id: int) -> None:
    obj = types.ObjectType.from_str(object_type)
    api = ctx.obj
    click.echo(api.info(obj, object_id))
    api.logout()


@main.command()
@click.option(
    "--object-type",
    required=True,
    type=click.Choice(list(crunchy_api.INFO.values())),
    default="series_id",
    envvar="CRUNCHYROLL_OBJECT",
)
@click.option("--object-id", required=True, type=int, envvar="CRUNCHYROLL_ID")
@click.option(
    "--sort",
    type=click.Choice(list(crunchy_api.SORT.values())),
    default="asc",
    envvar="CRUNCHYROLL_SORT",
)
@click.option("--offset", type=int, default=0, envvar="CRUNCHYROLL_OFFSET")
@click.option("--locale", type=str, default="enUS", envvar="CRUNCHYROLL_LOCALE")
@click.pass_context
def list_media(
    ctx: click.core.Context,
    object_type: str,
    object_id: int,
    sort: str,
    offset: int,
    locale: str,
) -> None:
    obj = types.ObjectType.from_str(object_type)
    sort = types.SortMode.from_str(sort)
    api = ctx.obj
    click.echo(api.list_media(obj, object_id, sort, offset, locale))
    api.logout()


@main.command()
@click.option(
    "--media-type",
    type=click.Choice(list(crunchy_api.MEDIA.values())),
    default="anime",
    envvar="CRUNCHYROLL_MEDIA",
)
@click.pass_context
def queue(ctx: click.core.Context, media_type: str) -> None:
    media = types.MediaType.from_str(media_type)
    api = ctx.obj
    click.echo(api.queue(media))
    api.logout()
