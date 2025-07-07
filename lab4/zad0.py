from flask import Flask
from sqlalchemy import create_engine, text

app = Flask(__name__)


@app.route("/")
def index():
    return "Środowisko wirtualne oraz pakiety Flask i SQLAlchemy działają poprawnie!"


if __name__ == "__main__":
    engine = create_engine("sqlite:///:memory:")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT sqlite_version();"))
        version = result.fetchone()[0]
        print(f"Wersja SQLite używana przez SQLAlchemy: {version}")

    app.run(debug=True)
