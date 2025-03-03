# Templates

## Software tool template

For now, we do not provide templates for software tools.
Stay tuned!

## Dataset tool template

Dataset tools are run sparingly, often once every couple of years or so.
Since users do not need to interact with these tools themselves, our focus is on ensuring long-term stability of the software.
This can be achieved via lock-files, which "freeze" the specific python libraries used for a tool.
Our preferred tool to achieve this is [pixi](https://pixi.sh/latest/) due to its conda integration and ease of use.

A template for these tools is in development.
Stay tuned!

## Data module template

Data modules will experience higher user interaction due to their user configurable nature.
This would quickly become confusing without some level of standardisation, so our template focuses on the following features:

- Standardised folder and file names for user inputs and module outputs.
- Automatically generated documentation in a standard format, providing a familiar structure across all data modules.
- Automatic checks for template updates, aiding module developers in keeping up with the latest standard.

URL: <https://github.com/calliope-project/data-module-template>

## Model builder template

For now, we do not provide templates for model builders.
Stay tuned for example models using our approach!
