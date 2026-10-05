# MongoEngine with Starlette-Admin

With MongoDB running locally, run from the repository root:

```sh
uv run examples/starlette_admin_mongoengine/main.py
```

Open <http://127.0.0.1:8000/> to manage Person documents. The example composes the Person mixin with MongoEngine's Document and overrides the name fields.

The script declares its dependencies using PEP 723 and loads this checkout of `opinionated-mixins`. Configuration uses Pydantic Settings. Override `MONGO_URI`, `MONGODB_NAME`, `HOST`, or `PORT` through environment variables. MongoDB defaults to `mongodb://localhost:27017` and database `opinionated_mixins`.
