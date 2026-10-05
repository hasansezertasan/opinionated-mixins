# MongoEngine Kitchen Sink with Starlette Admin

This example shows how to use any MongoEngine mixin and bring them together in a Starlette Admin application.

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
pip install -r 'examples/starlette_admin_mongoengine/requirements.txt'
```

Install the current checkout with `pip install -e .`. Start MongoDB locally, or copy
`examples/starlette_admin_mongoengine/.env.example` to `.env` in that same directory
and set `MONGO_URI` and `MONGODB_NAME` for your server. The defaults are
`mongodb://localhost:27017` and `opinionated_mixins`.

## Run the application

```shell
uvicorn examples.starlette_admin_mongoengine.main:app --host 0.0.0.0 --port 8000 --reload
```
