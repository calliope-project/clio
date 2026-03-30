"""Quick test to check that the docs build as expected."""

import subprocess

def test_mkdocs_builds(tmp_path, pytestconfig):
    """Run a basic check on the """
    project_root = pytestconfig.rootpath

    result = subprocess.run(
        [
            "mkdocs",
            "build",
            "--config-file",
            str(project_root / "mkdocs.yaml"),
            "--site-dir",
            str(tmp_path / "site"),
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
