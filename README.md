# `clio-tools` helpers

`clio-tools` is a collection of helper functionality that aids `modelblocks` maintainability.
Please read all about it in our [documentation](https://clio-tools.readthedocs.io/en/stable/).

## Development

Install [`pixi`](https://pixi.sh/latest/) and run:

```bash
git clone git@github.com:modelblocks-org/clio-tools.git
cd clio-tools
pixi install --all  # Installs both default and developer dependencies
```

## Helper commands

- `pixi run build-docs`: build a local version of the documentation
- `pixi run serve-docs`: render the documentation on your browser
- `pixi run style`: run CI linting, refractoring and spellchecking
- `pixi run test`: quick local test of the documentation
