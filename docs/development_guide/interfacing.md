# Interfacing between components

Ensuring modularity and containerisation implies a shared approach to the way projects access one another. The following is a general description of how this will be achieved for our software tools, dataset tools, and data modules.

1. **Software tools**: the default method of access for these is [conda-forge](https://conda-forge.org/). Thus, these tools can easily integrate into snakemake workflows or dataset tools via conda environment [YAML files](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) in a platform independent way. Additionally, [snakemake wrappers](https://snakemake.readthedocs.io/en/stable/snakefiles/modularization.html#wrappers) may be created to avoid the need to rewrite common uses of a software tool between data modules.
2. **Dataset tools**: the datasets produced by these tools are accessed via downloads, so the size and structure of the data should be kept in mind when choosing how to distribute them.
    - For smaller datasets (< 1 GB), non-queryable databases such as [Zenodo](https://zenodo.org/) are sufficient.
    - For larger datasets (> 1 GB), members of the organisation shall consult with their respective institutions for the possibility of using chunked and queryable data access methods, such as [THREADS](https://www.unidata.ucar.edu/software/tds/), enabling efficient data access via protocols like [OPeNDAP](https://www.opendap.org/).
3. **Data modules**: these are accessed by other workflows via [snakemake’s module functionality](https://snakemake.readthedocs.io/en/stable/snakefiles/modularization.html#modules). Our data module template provides a baseline for developers to ensure the following:
    - Version-specific access via version tags.
    - Isolation of configuration between modules and validation of said configuration via schemas.

    ??? example "Example: accessing a data module from another workflow"

        ```python
        # Include local module configuration.
        configfile: "config/modules/foobar.yaml"

        module foobar:
            # Request a specific module version.
            snakefile:
                github(
                    "calliope-project/foobar",
                    path="workflow/Snakefile",
                    tag="v1.0.0"
                )
            # Module configuration has its own key to ensure isolation.
            config: config["foobar"]
            # A prefix is added to isolate module input/output files.
            prefix: "module_foobar"

        # Rewrite rule names to avoid naming conflicts
        use rule * from foobar as module_foobar_*
        ```

4. **Model builders**: these may access all other components above as needed. Since they tend to be study-specific, they will rarely (if ever) be accessed by other tools or components.
