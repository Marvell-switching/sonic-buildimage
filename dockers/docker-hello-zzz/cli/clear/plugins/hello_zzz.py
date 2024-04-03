import click
import utilities_common.cli as clicommon


@click.group(cls=clicommon.AbbreviationGroup)
def hello_clear():
    click.echo("clear Hello, World!")


def register(cli):
    cli.add_command(hello_clear)