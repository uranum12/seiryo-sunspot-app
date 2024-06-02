# seiryo sunspot app

## app

### install

```sh
pnpm install
```

### build

```sh
pnpm build
```

### develop

```sh
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
python api/main.py
```

### develop

```sh
poetry run inv fmt
poetry run inv lint
poetry run inv test --cov
```

