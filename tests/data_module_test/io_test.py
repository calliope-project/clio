"""Test data module input-output utilities."""

from pathlib import Path
from textwrap import dedent

import pytest
import yaml
from pydantic import ValidationError

from clio_tools.data_module import ModuleInterface, modular_rulegraph_png


def load_yaml(path: Path):
    """File with no wildcards."""
    return yaml.safe_load(path.read_text())


class TestModuleInterface:
    """Tests for INTERFACE.yaml files."""

    @pytest.fixture(
        params=["interface_simple", "interface_wildcard", "interface_no_resources"]
    )
    def path_interface_test(self, request):
        """Name of the testfile to use."""
        return Path(__file__).parent / f"utils/{request.param}.yaml"

    def test_from_dict(self, path_interface_test):
        """Loading a simple yaml configuration file."""
        data = load_yaml(path_interface_test)
        ModuleInterface(**data)

    def test_from_path(self, path_interface_test):
        """Loading data from YAML files should result in no alterations."""
        assert ModuleInterface.from_yaml(path_interface_test) == ModuleInterface(
            **load_yaml(path_interface_test)
        )

    def test_to_mermaid_flowchart(self, path_interface_test):
        """Mermaid graph generation should include all file I/O elements."""
        data = load_yaml(path_interface_test)
        interface = ModuleInterface(**data)
        mermaid_txt = interface.to_mermaid_flowchart(path_interface_test.name)
        assert all([i in mermaid_txt for i in interface.resources.user])
        assert all([i in mermaid_txt for i in interface.resources.automatic])
        assert all([i in mermaid_txt for i in interface.results])

    @pytest.fixture
    def interface_w_wilcards(self):
        """File with wildcards configured."""
        return load_yaml(Path(__file__).parent / "utils/interface_wildcard.yaml")

    def test_wildcard_section_missing(self, interface_w_wilcards):
        """If filenames specify wildcards, they should appear in the wildcards section."""
        del interface_w_wilcards["wildcards"]
        with pytest.raises(
            ValidationError,
            match="Wildcards not specified in 'resources' or 'results':",
        ):
            ModuleInterface(**interface_w_wilcards)

    def test_wildcard_not_in_filename(self, interface_w_wilcards):
        """All values in the wildcards section should appear in filenames at least once."""
        interface_w_wilcards["resources"]["automatic"] = {
            "stuff.tiff": "Without wildcard."
        }
        with pytest.raises(ValidationError, match="Unused wildcards found"):
            ModuleInterface(**interface_w_wilcards)

    def test_mermaid_flow_diagram_text(self, interface_w_wilcards):
        """The generated diagram should be correct and use 4 space indentation."""
        expected = dedent("""\
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
                `")""")
        interface = ModuleInterface(**interface_w_wilcards)
        generated = interface.to_mermaid_flowchart("interface_wildcard.yaml")
        assert expected == generated


class TestModularRulegraphPNG:
    """Test the generator of 'friendly' modular graphs."""

    @pytest.fixture(scope="class")
    def rulegraph_path(self):
        """Pre made test file."""
        return "tests/data_module_test/utils/rulegraph.dot"

    @pytest.fixture
    def modular_graph_path(self, tmp_path):
        """Temporary location for generated test files."""
        return tmp_path / "modulegraph.png"

    @pytest.mark.parametrize(
        "prefixes", [("module_biofuels"), ("module_hydropower", "module_wind_pv")]
    )
    def test_modulegraph_success(self, rulegraph_path, modular_graph_path, prefixes):
        """Correct configurations should run without issues."""
        modular_rulegraph_png(rulegraph_path, modular_graph_path, prefixes)
        assert modular_graph_path.exists()

    @pytest.mark.parametrize("prefix", [("module_fail"), ("module _ hydropower")])
    def test_modulegraph_incorrect_prefix(
        self, rulegraph_path, modular_graph_path, prefix
    ):
        """Users should be warned when requesting incorrect module names."""
        with pytest.raises(ValueError, match=f"Prefix not found: {prefix}."):
            modular_rulegraph_png(rulegraph_path, modular_graph_path, prefix)

    def test_modulegraph_incorrect_file_input(self, modular_graph_path):
        """Users should be warned if passing an incorrect file."""
        with pytest.raises(ValueError, match="Only .dot files can be processed."):
            modular_rulegraph_png(
                "some_file.txt", modular_graph_path, "module_biofuels"
            )
