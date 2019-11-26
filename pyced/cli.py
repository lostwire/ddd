import click
import asyncio

import pyced.saga.server

@click.group()
@click.option('--config', envvar='config', default='./config.ini')
@click.pass_context
def cli(ctx, config):
    """ Estore command line interface """
    ctx.obj = pyced.saga.server.init(config)

@cli.command()
@click.pass_context
def initialize(ctx):
    """ Initialize estore application """
    ctx.obj.initialize()

if __name__ == '__main__':
    cli()
