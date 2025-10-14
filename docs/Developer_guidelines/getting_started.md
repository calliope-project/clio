# How to get started

Make sure to read about [our framework](../Background/our_framework.md) to familiarise yourself with each type of component
and decide the type of project that best fits your goals.

We assume you already have `conda` or `mamba` installed in your system.
If you don't, we recommend following `mamba`'s [installation advice](https://github.com/mamba-org/mamba).

1. Create a new environment and install `copier` in it.

    ```shell
    mamba env create -n my_new_module
    mamba install -c conda-forge copier
    ```

2. Call the `copier` template of the type of component you wish to make. Currently, we only support [data modules](https://github.com/calliope-project/data-module-template).

    ```shell
    copier copy 'https://github.com/calliope-project/data-module-template'
    ```

3. You'll be prompted with some questions. After answering them, `copier` will auto-generate the module for you.

    ```html
    >🎤 Please enter the name of your tool in snake_case.
    my_new_module
    ...
    ```

You are ready to go!
Please look into our general [requirements and conventions](./requirements.md#requirements-and-conventions) and familiarise yourself with the [templates](./templates.md).
