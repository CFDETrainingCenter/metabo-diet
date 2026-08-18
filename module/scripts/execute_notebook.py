"""Execute the Metabo-Diet notebook top-to-bottom and save a separate test copy."""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient


MODULE_DIR = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = MODULE_DIR / "notebooks" / "metabo_diet_harmonization.ipynb"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=NOTEBOOK_PATH)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Executed notebook path; defaults to <input_stem>_executed.ipynb "
            "beside the input and never overwrites the source by default."
        ),
    )
    parser.add_argument(
        "--working-directory",
        type=Path,
        default=MODULE_DIR / "notebooks",
        help="Working directory visible to notebook code.",
    )
    args = parser.parse_args()
    input_path = args.input.resolve()
    default_output = input_path.with_name(input_path.stem + "_executed.ipynb")
    output_path = (args.output.resolve() if args.output else default_output)
    working_directory = args.working_directory.resolve()

    if output_path == input_path:
        raise ValueError(
            "Refusing to overwrite the source notebook. Choose a different --output path."
        )

    notebook = nbformat.read(input_path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=900,
        kernel_name="python3",
        resources={"metadata": {"path": str(working_directory)}},
        allow_errors=False,
        record_timing=True,
    )
    executed = client.execute(cwd=str(working_directory))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(executed, output_path)
    code_cells = [cell for cell in executed.cells if cell.cell_type == "code"]
    print(
        f"Executed {input_path.name} -> {output_path}: {len(code_cells)} code cells, "
        f"last execution_count={code_cells[-1].execution_count}"
    )


if __name__ == "__main__":
    main()
