from invoke.context import Context
from invoke.tasks import task


@task
def fmt(c: Context) -> None:
    c.run("ruff check --fix-only --show-fixes api", pty=True)
    c.run("ruff format tasks.py api", pty=True)


@task
def lint(c: Context) -> None:
    c.run("ruff format --check api", pty=True)
    c.run("ruff check api", pty=True)
    c.run("mypy api", pty=True)


@task
def test(c: Context, *, cov: bool = False) -> None:
    cov_options = "--cov-report=term-missing --cov-report=html --cov api"
    c.run(f"pytest {cov_options if cov else ''} api", pty=True)
