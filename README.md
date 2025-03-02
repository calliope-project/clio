# A framework for modular and easy to understand energy modelling tools

`clio` aims to be a collection modularisation guidelines and tools that help energy modellers produce high-quality research that is repeatable, understanable and easy to use.

Please read all about it in our [documentation](https://clio.readthedocs.io/en/stable/)!

## Development

Install [`pixi`](https://pixi.sh/latest/) and run:

```shell
git clone git@github.com:calliope-project/clio.git
cd clio
pixi install --all  # Installs both default and development environments
pixi run --environment dev pytest  # Execute a commands for a particular environment
```
