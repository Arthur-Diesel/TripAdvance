# TripAdvance

Running the Server:

```bash
$ python manage.py runserver 
```

Managing Database Models
Once you have defined your data models, generate migrations with:

```bash
$ python manage.py makemigrations {AppName}
```

example: 
```bash
$ python manage.py makemigrations archives
```

If the migrations were created successfully, apply them to the database:

```bash
$ python manage.py migrate
```
