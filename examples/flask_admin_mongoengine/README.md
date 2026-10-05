# MongoEngine with Flask-Admin

With MongoDB running locally, run from the repository root:

```sh
uv run examples/flask_admin_mongoengine/app.py
```

Or use an in-memory MongoDB mock:

```sh
MONGOMOCK=true uv run examples/flask_admin_mongoengine/app.py
```

Open <http://127.0.0.1:5000/admin/>. The example seeds sample documents and demonstrates the MongoEngine mixins.

The script declares its dependencies using PEP 723 and loads this checkout of `opinionated-mixins`. Configuration uses Pydantic Settings. Override `MONGO_URI`, `MONGODB_NAME`, `MONGOMOCK`, `SECRET_KEY`, `HOST`, `PORT`, or `DEBUG` through environment variables. MongoDB defaults to `mongodb://localhost:27017` and database `opinionated_mixins_demo`.
