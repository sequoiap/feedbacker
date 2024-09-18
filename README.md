# feedbacker
A web app that allows students to submit assignments, be graded or evaluated by a background process, and have feedback returned.

## Adding apps

For each app, you need to:

1. Import its frontend views and add it to the toplevel frontend in frontend.py
1. Import its backend views and add it to the API in api.py
1. Configure the templates environment variable to make yours discoverable in config.py
