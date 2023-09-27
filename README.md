# Requirements

- [Docker](https://www.docker.com/).
- [Docker Compose](https://docs.docker.com/compose/install/).

# Run 🏃

```
docker-compose up
```

Open the browser at `http://ruralmeet.localhost/`.

# Installation

## Development

1. Create .env file.

```bash
cp env.example .env
```

2. Load fake data

``` bash
make run.loaddata.fake
```

### Run Gulp

```
gulp dev
```

### Recreate docker

```
make docker.recreate.django
```

### Load fake data

```
make run.loaddata.fake
```

## Production

1. Create .env file.

```bash
cp env.example .env
```

2. Load minimum data

``` bash
make run.loaddata
```

3. Create superuser

``` bash
docker-compose exec -T django bash -c "python3 manage.py createsuperuser"
```


## Tools

Lint

```shell
make lint
```

Formatear

```shell
make format
```

Recrear imagen de Django

```shell
make docker.recreate.django
```

Hacer una nueva migración después de cambiar un model.

```shell
make makemigrations
```

Migrar

```shell
make run.migrate
```

Cargar data mínima.

```shell
make run.loaddata
```

Generar data de desarrollo.

```shell
make run.loaddata.test
```

## Other domains

- Caddy: `http://project.localhost`.
- Gulp: `http://project.localhost:3000`.
- Django: `http://project.localhost:8000`.
- Mailhog: `http://project.localhost:8025`.

### Bash Django

``` shell
docker exec -it project-django bash
```
