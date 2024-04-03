import click
import utilities_common.cli as clicommon
from swsscommon.swsscommon import SonicV2Connector, ConfigDBConnector

@click.group()
def hello_zzz():
    """config hello zzz information"""
    pass


@hello_zzz.group()
@click.argument('name', metavar='<name>', required=True)
def zzz_add(name):
    config_db = ConfigDBConnector()
    config_db.connect()


def register(cli):
    cli.add_command(zzz_add)


