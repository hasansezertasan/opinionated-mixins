# ODMantic Kitchen Sink with Starlette Admin

This example shows how to use any ODMantic mixin and bring them together in a Starlette Admin application.

> **Warning**
> This example is not working because ODMantic doesn't support mixins.

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

> To install current version of `opinionated-mixins`, run `pip install -e .`.

## Run the application

```shell
uvicorn examples.starlette_admin_odmantic.main:app --host 0.0.0.0 --port 8000 --reload
```
