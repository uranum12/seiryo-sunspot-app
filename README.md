# seiryo sunspot app

## app

### install

```sh
pnpm install
```

### build

```sh
node ./build.js
```

### develop

```sh
NODE_ENV="development" node ./build.js
pnpm fmt
pnpm lint
pnpm fix
```

## api

### install

```sh
poetry install --sync
```

### run

```sh
poetry run uvicorn api.main:app
```

### develop

```sh
poetry run inv dev
poetry run inv fmt
poetry run inv lint
poetry run inv test --cov
```

