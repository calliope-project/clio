"""Utility functions for module input / output standardisation."""

import re
from pathlib import Path
from textwrap import dedent
from typing import Self

import yaml
from pydantic import BaseModel, Field, model_validator


class Resources(BaseModel):
    """Schema for module resources (input files)."""

    model_config = {"extra": "forbid"}
    user: dict[str, str] = Field(default_factory=dict)
    automatic: dict[str, str] = Field(default_factory=dict)


class ModuleInterface(BaseModel):
    """Schema for module INTERFACE.yaml."""

    model_config = {"extra": "forbid"}

    resources: Resources = Field(default=Resources())
    """Resources required by the module."""
    results: dict[str, str]
    """Key module result files. Does not need to be comprehensive."""
    wildcards: dict[str, str] = Field(default_factory=dict)
    """
    Module wildcards. If provided, these must be present in the keys of either module resources or results.
    E.g.:

    ```yaml
    results:
        'foo_{bar}.png': an output image.
    wildcards:
        bar: will alter module behaviour.
    """

    @classmethod
    def from_yaml(cls, path: str | Path):
        """Initialise the schema from a YAML file."""
        with open(Path(path)) as file:
            data = yaml.safe_load(file)
        return cls(**data)

    @model_validator(mode="after")
    def check_wildcards(self) -> Self:
        """Ensure wildcards are specified in file names."""

        def _extract_wildcards(text: str) -> list[str]:
            # Occurrences of text inside curly brackets
            return re.findall(r"\{(.*?)\}", text)

        filenames = set(
            [*self.resources.user, *self.resources.automatic, *self.results]
        )

        filename_wildcards: set[str] = set()
        for filename in filenames:
            filename_wildcards.update(_extract_wildcards(filename))

        diff = filename_wildcards - self.wildcards.keys()
        if diff:
            raise ValueError(
                f"Wildcards not specified in 'resources' or 'results': {diff}."
            )
        diff = self.wildcards.keys() - filename_wildcards
        if diff:
            raise ValueError(f"Unused wildcards found: {diff}")
        return self

    def to_mermaid_flowchart(self, name: str) -> str:
        """Convert to a mermaid diagram."""
        mermaid_txt = dedent(f"""
            ```mermaid
            ---
            title: {name}
            ---
            flowchart LR
            M(({name}))
            """)

        # Generate user-related part
        if self.resources.user:
            user_txt = "\n    ".join(self.resources.user)
            mermaid_txt += f"""C1[/"`**user**\n    {user_txt}\n    `"/] --> M\n"""

        # Generate automatic-related part
        if self.resources.automatic:
            automatic_txt = "\n    ".join(self.resources.automatic)
            mermaid_txt += (
                f"""C2[/"`**automatic**\n    {automatic_txt}\n    `"/] --> M\n"""
            )

        # Generate results part
        results_txt = "\n    ".join(self.results)
        mermaid_txt += f"""M --> O1("`**results**\n    {results_txt}\n    `")\n```"""
        return mermaid_txt
