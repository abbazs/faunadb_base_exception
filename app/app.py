from typing import Any
from faunadb.client import FaunaClient
from faunadb import query as q
import typer
from .settings import get_settings

settings = get_settings()
client = FaunaClient(secret=settings.DB_ADMIN_PYTHON)
app = typer.Typer()


@app.command()
def create_collection_with_index(name: str) -> Any:
    c = client.query(q.collection(name))
    if client.query(q.exists(c)) == False:
        c = client.query(q.create_collection({"name": name}))

    idx_name = f"{name}_index"
    ci = client.query(q.index(idx_name))
    if client.query(q.exists(ci)) == False:
        ci = client.query(
            q.create_index(
                {
                    "name": idx_name,
                    "unique": True,
                    "serialized": True,
                    "source": q.collection(name),
                }
            )
        )
    return c, ci


@app.command()
def initialize_db() -> None:
    typer.echo("Initializing db...")
    uc, uci = create_collection_with_index(name="users")
    bc, bci = create_collection_with_index(name="todos")
    dosc, dosci = create_collection_with_index(name="notes")
    typer.echo("Db initialized...")

if __name__ == "__main__":
    app()
