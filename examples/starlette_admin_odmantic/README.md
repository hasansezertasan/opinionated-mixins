# ODMantic with Starlette-Admin

With MongoDB running locally, run from the repository root:

```sh
uv run examples/starlette_admin_odmantic/main.py
```

Open <http://127.0.0.1:8000/> to manage Person documents.

ODMantic does not collect fields from plain mixin parents ([issue #39](https://github.com/hasansezertasan/opinionated-mixins/issues/39)). This example declares the Person fields directly as a workaround. `date_of_birth` uses `datetime.datetime` for BSON storage.

The script declares its dependencies using PEP 723 and loads this checkout of `opinionated-mixins`. Configuration uses Pydantic Settings. Override `MONGO_URI`, `MONGODB_NAME`, `HOST`, or `PORT` through environment variables. MongoDB defaults to `mongodb://localhost:27017` and database `opinionated_mixins`.

Starlette-Admin is pinned to 0.17.1 because version 1.0 removed its ODMantic backend; see the [migration guide](https://jowilf.github.io/starlette-admin/migration/).
