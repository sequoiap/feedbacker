# feedbacker
A web app that allows students to submit assignments, be graded or evaluated by a background process, and have feedback returned.

## Adding apps

For each app, you need to:

1. Add its frontend views in frontend.py
1. Add the templates to ``/templates``
1. Import its backend views and add it to the API in api.py
1. Import at least one model from the app to ensure it is included in the database in ``__init__.py``

## Configuration

On first run, initialize the database:

```bash
feedbacker database init
```

## Running the app

In developer mode:

```bash
fastapi dev .\src\feedbacker\main.py
```

In production mode:

```bash
fastapi run .\src\feedbacker\main.py
```
