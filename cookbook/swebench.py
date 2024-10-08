from dataclasses import dataclass
from datetime import datetime

from datasets import load_dataset
from datasets.arrow_dataset import Dataset
from datasets.dataset_dict import DatasetDict


@dataclass
class SweBenchExample:
    repo: str
    instance_id: str
    base_commit: str
    patch: str
    test_patch: str
    problem: str
    hints: str
    created_at: datetime
    version: str
    tests_fail: list[str]
    tests_pass: list[str]
    env_commit: str


REPO_ON_CREATE_CMD = {
    "astropy/astropy": "pip install uv && uv pip install --editable '.[dev_all]'",
    # for django tests to pass, we need to run container with user 'vscode'
    "django/django": "sudo apt-get update -y && sudo apt-get install -y libmemcached-dev && sudo pip install uv && sudo uv pip install --system -e . && sudo uv pip install --system -r tests/requirements/py3.txt",
    "matplotlib/matplotlib": "",
    "mwaskom/seaborn": "",
    "pallets/flask": "",
    "psf/requests": "",
    "pydata/xarray": "",
    "pylint-dev/pylint": "",
    "pytest-dev/pytest": "",
    "scikit-learn/scikit-learn": "",
    "sphinx-doc/sphinx": "",
    "sympy/sympy": "",
}

REPO_TEST_CMD = {
    "astropy/astropy": "pytest",
    "django/django": "./tests/runtests.py",
    "matplotlib/matplotlib": "",
    "mwaskom/seaborn": "",
    "pallets/flask": "",
    "psf/requests": "",
    "pydata/xarray": "",
    "pylint-dev/pylint": "",
    "pytest-dev/pytest": "",
    "scikit-learn/scikit-learn": "",
    "sphinx-doc/sphinx": "",
    "sympy/sympy": "",
}


def load_swebench() -> Dataset:
    dataset = load_dataset("princeton-nlp/SWE-bench_Verified")
    match dataset:
        case DatasetDict():
            return dataset["test"]
        case _:
            raise NotImplementedError("Dataset is not a DatasetDict")


def parse_example(data: dict[str, str]) -> SweBenchExample:
    """Parses a single example from the SWE-bench dataset."""

    return SweBenchExample(
        repo=data["repo"],
        instance_id=data["instance_id"],
        base_commit=data["base_commit"],
        patch=data["patch"],
        test_patch=data["test_patch"],
        problem=data["problem_statement"],
        hints=data["hints_text"],
        created_at=datetime.fromisoformat(data["created_at"]),
        version=data["version"],
        tests_fail=eval(data["FAIL_TO_PASS"]),
        tests_pass=eval(data["PASS_TO_PASS"]),
        env_commit=data["environment_setup_commit"],
    )


if __name__ == "__main__":
    from pprint import pprint

    examples = [parse_example(example) for example in load_swebench()]
    for i in range(10):
        pprint(f"Example {i}")
        pprint(examples[i])
