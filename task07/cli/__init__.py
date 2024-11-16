import click

from cli.commands import (
    info_cmd,
    query_1_cmd,
    query_2_cmd,
    query_3_cmd,
    query_4_cmd,
    query_5_cmd,
    seeder_cmd,
)


@click.group()
def cli():
    pass


cli.add_command(cmd=info_cmd)
cli.add_command(cmd=query_1_cmd)
cli.add_command(cmd=query_2_cmd)
cli.add_command(cmd=query_3_cmd)
cli.add_command(cmd=query_4_cmd)
cli.add_command(cmd=query_5_cmd)
cli.add_command(cmd=seeder_cmd)
