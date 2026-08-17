# SQLAlchemy Kitchen Sink with Flask Admin

This example shows how to use any SQLAlchemy mixin and bring them together in a Flask Admin application.

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
pip install -r 'examples/flask_admin_sqlalchemy/requirements.txt'
```

> To install current version of `opinionated-mixins`, run `pip install -e .`.

## Run the application

```shell
python examples/flask_admin_sqlalchemy/app.py
```
