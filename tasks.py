from invoke import task

@task
def start(ctx):
    pass

@task
def test(ctx):
    pass

@task
def lint(ctx):
    ctx.run("flake8", pty=True)

@task
def format(ctx):
    ctx.run("autopep8 --aggressive --in-place --recursive app tests")