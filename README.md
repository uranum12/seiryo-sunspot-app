# seiryo sunspot app

## app

### Install

```sh
pnpm install
```

### Build

```sh
pnpm run build
```

### Develop

```sh
pnpm run dev
```

## api

### install

```sh
poetry sync
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

