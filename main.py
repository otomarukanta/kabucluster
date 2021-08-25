import click
from kabucluster.settings import engine
from kabucluster.models import Base
from kabucluster.daemon import Daemon
from kabucluster.utils.auth import get_auth

@click.group()
def cli():
    pass

@cli.group()
def util():
    pass

@util.command()
def auth():
    get_auth()

@util.command()
def add_list():
    pass

@cli.command()
def init():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@cli.command()
@click.option('-o', '--once', is_flag=True)
def run(once):
    if once:
        Daemon().run()
    else:
        pass
        # Tokenizer().run_forever()

if __name__ == '__main__':
    cli()