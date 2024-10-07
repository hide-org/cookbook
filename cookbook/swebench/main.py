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


def load_swebench() -> Dataset:
    dataset = load_dataset("princeton-nlp/SWE-bench_Verified")
    match dataset:
        case DatasetDict():
            return dataset["test"]
        case _:
            raise NotImplementedError("Dataset is not a DatasetDict")


def parse_example(data: dict[str, str]) -> SweBenchExample:
    """
    Parses a single example from the SWE-bench dataset. Example data:

    {'repo': 'astropy/astropy',
     'instance_id': 'astropy__astropy-12907',
     'base_commit': 'd16bfe05a744909de4b27f5875fe0d4ed41ce607',
     'patch': "diff --git a/astropy/modeling/separable.py b/astropy/modeling/separable.py\n--- a/astropy/modeling/separable.py\n+++ b/astropy/modeling/separable.py\n@@ -242,7 +242,7 @@ def _cstack(left, right):\n         cright = _coord_matrix(right, 'right', noutp)\n     else:\n         cright = np.zeros((noutp, right.shape[1]))\n-        cright[-right.shape[0]:, -right.shape[1]:] = 1\n+        cright[-right.shape[0]:, -right.shape[1]:] = right\n \n     return np.hstack([cleft, cright])\n \n",
     'test_patch': "diff --git a/astropy/modeling/tests/test_separable.py b/astropy/modeling/tests/test_separable.py\n--- a/astropy/modeling/tests/test_separable.py\n+++ b/astropy/modeling/tests/test_separable.py\n@@ -28,6 +28,13 @@\n p1 = models.Polynomial1D(1, name='p1')\n \n \n+cm_4d_expected = (np.array([False, False, True, True]),\n+                  np.array([[True,  True,  False, False],\n+                            [True,  True,  False, False],\n+                            [False, False, True,  False],\n+                            [False, False, False, True]]))\n+\n+\n compound_models = {\n     'cm1': (map3 & sh1 | rot & sh1 | sh1 & sh2 & sh1,\n             (np.array([False, False, True]),\n@@ -52,7 +59,17 @@\n     'cm7': (map2 | p2 & sh1,\n             (np.array([False, True]),\n              np.array([[True, False], [False, True]]))\n-            )\n+            ),\n+    'cm8': (rot & (sh1 & sh2), cm_4d_expected),\n+    'cm9': (rot & sh1 & sh2, cm_4d_expected),\n+    'cm10': ((rot & sh1) & sh2, cm_4d_expected),\n+    'cm11': (rot & sh1 & (scl1 & scl2),\n+             (np.array([False, False, True, True, True]),\n+              np.array([[True,  True,  False, False, False],\n+                        [True,  True,  False, False, False],\n+                        [False, False, True,  False, False],\n+                        [False, False, False, True,  False],\n+                        [False, False, False, False, True]]))),\n }\n \n \n",
     'problem_statement': "Modeling's `separability_matrix` does not compute separability correctly for nested CompoundModels\nConsider the following model:\r\n\r\n```python\r\nfrom astropy.modeling import models as m\r\nfrom astropy.modeling.separable import separability_matrix\r\n\r\ncm = m.Linear1D(10) & m.Linear1D(5)\r\n```\r\n\r\nIt's separability matrix as you might expect is a diagonal:\r\n\r\n```python\r\n>>> separability_matrix(cm)\r\narray([[ True, False],\r\n       [False,  True]])\r\n```\r\n\r\nIf I make the model more complex:\r\n```python\r\n>>> separability_matrix(m.Pix2Sky_TAN() & m.Linear1D(10) & m.Linear1D(5))\r\narray([[ True,  True, False, False],\r\n       [ True,  True, False, False],\r\n       [False, False,  True, False],\r\n       [False, False, False,  True]])\r\n```\r\n\r\nThe output matrix is again, as expected, the outputs and inputs to the linear models are separable and independent of each other.\r\n\r\nIf however, I nest these compound models:\r\n```python\r\n>>> separability_matrix(m.Pix2Sky_TAN() & cm)\r\narray([[ True,  True, False, False],\r\n       [ True,  True, False, False],\r\n       [False, False,  True,  True],\r\n       [False, False,  True,  True]])\r\n```\r\nSuddenly the inputs and outputs are no longer separable?\r\n\r\nThis feels like a bug to me, but I might be missing something?\n",
     'hints_text': '',
     'created_at': '2022-03-03T15:14:54Z',
     'version': '4.3',
     'FAIL_TO_PASS': '["astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]", "astropy/modeling/tests/test_separable.py::test_separable[compound_model9-result9]"]',
     'PASS_TO_PASS': '["astropy/modeling/tests/test_separable.py::test_coord_matrix", "astropy/modeling/tests/test_separable.py::test_cdot", "astropy/modeling/tests/test_separable.py::test_cstack", "astropy/modeling/tests/test_separable.py::test_arith_oper", "astropy/modeling/tests/test_separable.py::test_separable[compound_model0-result0]", "astropy/modeling/tests/test_separable.py::test_separable[compound_model1-result1]", "astropy/modeling/tests/test_separable.py::test_separable[compound_model2-result2]", "astropy/modeling/tests/test_separable.py::test_separable[compound_model3-result3]", "astropy/modeling/tests/test_separable.py::test_separable[compound_model4-result4]", "astropy/modeling/tests/test_separable.py::test_separable[compound_model5-result5]", "astropy/modeling/tests/test_separable.py::test_separable[compound_model7-result7]", "astropy/modeling/tests/test_separable.py::test_separable[compound_model8-result8]", "astropy/modeling/tests/test_separable.py::test_custom_model_separable"]',
     'environment_setup_commit': '298ccb478e6bf092953bca67a3d29dc6c35f6752'}
    """

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
