# How to get started

Make sure to read about [our framework](../about/our_framework.md) to familiarise yourself with each type of component.

We assume you already have `conda` or `mamba` installed in your system.
If you don't, we recommend following `mamba`'s [installation advice](https://github.com/mamba-org/mamba).

1. Create a new environment and install `copier` in it.

    ```shell
    mamba env create -n my_new_module
    mamba install -c conda-forge copier
    ```

2. Create a folder for module and call our `copier` template.

    ```shell
    mkdir ./my_new_module
    copier copy 'https://github.com/calliope/clio'
    ```

3. You'll be prompted with some questions. After answering them, `copier` will auto-generate the module for you!

    ```html
    🎤 Please enter your module's short name as used in snakemake (should be in `snake_case`).
    my_new_module
    ...
    ```

You are ready to go!
Please look into our general [requirements and conventions](./general_requirements.md#requirements-and-conventions) and familiarise yourself with our [templates](templates.md).
