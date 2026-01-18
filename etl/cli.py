import typer
from etl.database import DatabaseHandler

app = typer.Typer()

@app.command()
def add(path: str):
    db = DatabaseHandler()
    audio = db.add_audio(path)
    typer.echo("Audio agregado correctamente")

@app.command()
def list():
    db = DatabaseHandler()
    for a in db.get_audios():
        typer.echo(a)

if __name__ == "__main__":
    app()
