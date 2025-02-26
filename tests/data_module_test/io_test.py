"""Test data module input-output utilities."""

from pathlib import Path
from textwrap import dedent

import pytest
import yaml
from pydantic import ValidationError

from clio_tools.data_module import ModuleInterface


def load_yaml(path: Path):
    """File with no wildcards."""
    return yaml.safe_load(path.read_text())


@pytest.fixture(
    params=["interface_simple", "interface_wildcard", "interface_no_resources"]
)
def path_interface_test(request):
    """Name of the testfile to use."""
    return Path(__file__).parent / f"utils/{request.param}.yaml"


def test_from_dict(path_interface_test):
    """Loading a simple yaml configuration file."""
    data = load_yaml(path_interface_test)
    ModuleInterface(**data)


def test_from_path(path_interface_test):
    """Loading data from YAML files should result in no alterations."""
    assert ModuleInterface.from_yaml(path_interface_test) == ModuleInterface(
        **load_yaml(path_interface_test)
    )


def test_to_mermaid_flowchart(path_interface_test):
    """Mermaid graph generation should include all file I/O elements."""
    data = load_yaml(path_interface_test)
    interface = ModuleInterface(**data)
    mermaid_txt = interface.to_mermaid_flowchart(path_interface_test.name)
    assert all([i in mermaid_txt for i in interface.resources.user])
    assert all([i in mermaid_txt for i in interface.resources.automatic])
    assert all([i in mermaid_txt for i in interface.results])


@pytest.fixture
def interface_w_wilcards():
    """File with wildcards configured."""
    return load_yaml(Path(__file__).parent / "utils/interface_wildcard.yaml")


def test_wildcard_section_missing(interface_w_wilcards):
    """If filenames specify wildcards, they should appear in the wildcards section."""
    del interface_w_wilcards["wildcards"]
    with pytest.raises(
        ValidationError, match="Wildcards not specified in 'resources' or 'results':"
    ):
        ModuleInterface(**interface_w_wilcards)


def test_wildcard_not_in_filename(interface_w_wilcards):
    """All values in the wildcards section should appear in filenames at least once."""
    interface_w_wilcards["resources"]["automatic"] = {"stuff.tiff": "Without wildcard."}
    with pytest.raises(ValidationError, match="Unused wildcards found"):
        ModuleInterface(**interface_w_wilcards)


def test_mermaid_flow_diagram_text(interface_w_wilcards):
    """The generated diagram should be correct and use 4 space indentation."""
    expected = dedent(r"""
        ```mermaid
        ---
        title: interface_wildcard.yaml
        ---
        flowchart LR
        M((interface_wildcard.yaml))
        C1[/"`**user**
            table_{foo}.csv
            text_{foo}.txt
            `"/] --> M
        C2[/"`**automatic**
            download_{bar}.nc
            `"/] --> M
        M --> O1("`**results**
            stuff_{foobar}.parquet
            more_stuff_{foo}_{foobar}.nc
            `")
        ```""")
    interface = ModuleInterface(**interface_w_wilcards)
    generated = interface.to_mermaid_flowchart("interface_wildcard.yaml")
    assert expected == generated
