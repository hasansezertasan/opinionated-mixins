# ODMantic Kitchen Sink with Starlette Admin

This example shows a Person model in a Starlette Admin application using ODMantic.

ODMantic does not collect fields from plain mixin parents ([issue #39](https://github.com/hasansezertasan/opinionated-mixins/issues/39)). This example declares the current Person fields directly as a workaround. `date_of_birth` uses `datetime.datetime` for BSON storage.

## Clone the repo

```shell
git clone https://github.com/hasansezertasan/opinionated-mixins.git
cd opinionated-mixins
```

## Install dependencies with virtualenv

- Create a virtual environment:

```shell
python3 -m venv venv
```

- Activate the virtual environment:

> On Windows:

```shell
venv/Scripts/activate.bat
```

> On Unix or MacOS:

```shell
source venv/bin/activate
```

- Install requirements:

```shell
pip install -r 'examples/starlette_admin_odmantic/requirements.txt'
```

Install the current checkout with `pip install -e .`. Start MongoDB locally, or copy
`examples/starlette_admin_odmantic/.env.example` to `.env` in that same directory
and set `MONGO_URI` and `MONGODB_NAME` for your server. The defaults are
`mongodb://localhost:27017` and `opinionated_mixins`.

## Run the application

```shell
uvicorn examples.starlette_admin_odmantic.main:app --host 0.0.0.0 --port 8000 --reload
```

This example pins Starlette-Admin 0.17.1 because version 1.0 removed its ODMantic
backend; see the [migration guide](https://jowilf.github.io/starlette-admin/migration/).
