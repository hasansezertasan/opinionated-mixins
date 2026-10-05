# SQLAlchemy with Flask-Admin

Run from the repository root:

```sh
uv run examples/flask_admin_sqlalchemy/app.py
```

Open <http://127.0.0.1:5000/admin/>. The example creates and seeds `demo.db` in the working directory and demonstrates the SQLAlchemy mixins.

The script declares its dependencies using PEP 723 and loads this checkout of `opinionated-mixins`. Configuration uses Pydantic Settings. Override `DATABASE_URL`, `SECRET_KEY`, `HOST`, `PORT`, or `DEBUG` through environment variables.

To use a different database file:

```sh
DATABASE_URL=sqlite:///custom-demo.db uv run examples/flask_admin_sqlalchemy/app.py
```
