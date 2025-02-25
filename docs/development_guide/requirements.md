# Requirements and conventions

## Component requirements

We enforce the following requirements in all projects.

1. **Open-source code**: projects must use either MIT or Apache 2.0, which are both [OSI approved](https://opensource.org/licenses) open-source licenses, and they must be openly available in platforms such as GitHub.
2. **Open data**: data produced by projects (dataset tools and data modules in particular) should use a [CC-BY-4.0 license](https://creativecommons.org/licenses/by/4.0/) whenever possible.
3. **Versioning**: projects must be version controlled with official releases, which can be used to specify the version of the project used in a study and/or dataset, and an accompanying CHANGELOG. Project developers are free to choose their preferred approach (e.g., [SemVer](https://semver.org/) or [CalVer](https://calver.org/)).
4. **Testing**: projects must employ some type of testing to ensure quality and long-term stability. The approach will vary depending on the type of project:

    1. **Software tools**: these require using testing frameworks (e.g., [pytest](https://docs.pytest.org/en/stable/)). The chosen approach (e.g., unit testing, functional testing) is up to the developer, but some kind of testing must be present.
    2. **Dataset tools**: the method used to produce the data must contain some kind of assurance or evaluation to ensure its quality. The choice of method is up to the maintainers in a case-by-case basis.
    3. **Data modules**: a minimal set of tests, provided by our template. These will fulfill two goals:
        1. Verifying that module inputs/outputs are placed in the right locations.
        2. Serve as a small example of the module’s operation, which will be used to build standardised module documentation. We recommend delegating more complex testing to the software tools and datasets used by the module.
    4. **Model builders**: we refrain from requiring a specific testing method for these repositories. Nevertheless, we recommend at least using lightweight snakemake [unit tests](https://snakemake.readthedocs.io/en/stable/snakefiles/testing.html) to verify that the steps of the workflow work as intended.

5. **Documentation**: projects must provide documentation to ensure the methods and reasoning behind their code can be understood:
    1. **Software tools**: versioned domaximum_roof_ratio: 0.80 # unit for a value cumentation website with, at minimum, API documentation and useful examples.
    2. **Dataset tools**: either versioned documentation or a README file explaining the methodology and assumptions employed, to allow others to reuse the tool in the future to reproduce or update the dataset when necessary.
    3. **Data modules**: projects must have versioned and standardised documentation with the following in mind:
        1. A README file explaining the different steps of the workflow, citing relevant material, and detailing their methodology.
        2. To follow our templating, which requires explanations of key components (configuration options, input/output files, wildcards) and will enable standardised documentation generation.
    4. **Model builders**: no specific requirements, but documentation is nevertheless recommended.

## File conventions

The following is a list of general advice on how to format files to help tools interact seamlessly. We encourage developers to employ validation for user inputted files, either through [built-in snakemake functionality](https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html#validation), or through libraries like [pydantic](https://docs.pydantic.dev/latest/) and [pandera](https://pandera.readthedocs.io/en/stable/).

1. **Configuration data**: we prefer to use YAML (.yaml) files.
    1. These files must always be validated to detect invalid user settings.
    2. Unit-specific configuration settings must state the unit explicitly in their naming.

        ???+ example "Naming configuration variables clearly"

            ```yaml
            maximum_installable_mw_per_km2: # unit for the section
               pv_tilted: 160
               pv_flat: 80
            maximum_roof_ratio: 0.80 # unit for a value
            ```

2. **Tabular data**: we prefer [Apache Parquet](https://parquet.apache.org/) (.parquet) files due to their performance, storage efficiency and [metadata compatibility](https://parquet.apache.org/docs/file-format/metadata/), with the following requirements:
    1. Follow [tidy data](https://vita.had.co.nz/papers/tidy-data.pdf) principles (columns are variables, rows are observations) to make data machine-readable.

        ???+ example "Example of a tidy table"

            | year          | country_id       | shape_id         | demand       |
            |---------------|------------------|------------------|--------------|
            | 2020          | ITA              | North            | 4500         |
            | 2020          | ITA              | East             | 4800         |
            | 2020          | ITA              | South            | 3000         |

    2. Embed important metadata within the file, with at minimum the following values:
        1. `units`: a dictionary specifying per-column units, using `no_unit` for unitless cases. Used to simplify parsing and enabling easier integration of unit-checking tools like [pint](https://pint.readthedocs.io/en/stable/).
        2. `source`: a string specifying the source and/or author of a dataset.
        3. `license`: a string specifying the license of the dataset.

        ??? example "Embedding metadata in `pandas`"

            `pandas` will automatically convert data in `df.attrs` into [file-level metadata](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.attrs.html#pandas.DataFrame.attrs) when saving to `.parquet`:

            ```python
            dataframe.attrs["units"] = {
                "year": "yr",
                "country_id": "no_unit",
                "shape_id": "no_unit",
                "demand": "mwh"
                }
            dataframe.attrs["source"] = "github.com/calliope-project/clio"
            dataframe.attrs["license"] = "CC-BY-4.0"
            dataframe.to_parquet('my_data.parquet')
            ```

3. **Raster data**: we prefer to use GeoTIFF (.tiff) files.
4. **Polygon data**: we prefer [GeoParquet](https://geoparquet.org/) (.parquet) files.

    ??? example "Example shapefiles in our standard format"

        You can find some simple examples of our standard data format in the `clio/resources/shapes` folder.

        --8<-- "resources/shapes/README.md:docs"

5. **Gridded data**: we prefer to use [netCDF](https://www.unidata.ucar.edu/software/netcdf/) (.nc) files.

## Metadata conventions

1. For all data: use snake case (`foo_bar`) for headers, keys, indexes, variables, etc. Avoid hyphens (`foo-bar`) and camel case (`FooBar`).
2. For timeseries data: timeseries must follow [ISO 8601 UTC](https://en.wikipedia.org/wiki/ISO_8601) spec (e.g., 2024-08-01T15:00:00Z).
3. For national / subnational data:
    1. Country IDs should always be under the `country_id` naming and follow [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) (e.g., CHE, CHN, GBR, MEX, etc).
    2. Sub-regions must be under the `shape_id` naming. This applies even in cases where national resolution is requested (i.e., `country_id`  and `shape_id` should match).
    3. A `shape_spec` key or header should be present, specifying the version of the subregion standard used (e.g., NUTS2024, GADM4.1, ISO 3166-2:2013). This aids in replicability since subregion codes [change quite often](https://ec.europa.eu/eurostat/web/nuts/history).

    ???+ example "Example of tabular subnational data"

        | country_id       | shape_id         | shape_spec       | demand       |
        |------------------|------------------|------------------|--------------|
        | DEU              | DE13             | NUTS2024         | 4500         |
        | DEU              | DE14             | NUTS2024         | 4800         |
        | ITA              | ITA0             | GADM4.1          | 20000        |

4. For spatial data:
    1. Use `longitude` | `latitude` to express position and avoid ambiguous values like `x` | `y`.
    2. Make sure to save the CRS with the spatial data. With the recommended file types for GIS data, see above, this is guaranteed.
        3. For geodetic data, where preserving position matters, use a geodetic CRS (e.g. [EPSG:4326](https://epsg.io/4326)).
        4. For projected data, where preserving distance or area matters, allow users to specify the reference system that best fits the needs of the calculation (e.g. [EPSG:3035](https://epsg.io/3035) for Europe).
5. For currency data: currency codes must follow [ISO 4217 alpha-3](https://en.wikipedia.org/wiki/ISO_4217) codes in combination with the year of the currency (e.g., CHF2024, EUR2015, USD2020) to allow for inflation adjustments.
