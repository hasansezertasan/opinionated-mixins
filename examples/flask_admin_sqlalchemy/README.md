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

Install the current checkout with `pip install -e .`.

The example uses Flask-Admin 1.6.1, matching its `template_mode` API.
It creates and seeds a SQLite database named `demo.db` in the working directory.

## Run the application

```shell
python examples/flask_admin_sqlalchemy/app.py
```
