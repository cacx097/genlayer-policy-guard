from pathlib import Path
import ast


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "policy_guard.py"


def _source() -> str:
    return CONTRACT.read_text(encoding="utf-8")


def test_contract_has_current_genlayer_dependency_header():
    first_line = _source().splitlines()[0]
    assert first_line.startswith('# { "Depends": "py-genlayer:')


def test_contract_parses_as_python():
    ast.parse(_source())


def test_expected_public_surface_exists():
    tree = ast.parse(_source())
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    assert [c.name for c in classes] == ["PolicyGuard"]

    methods = {
        node.name
        for node in classes[0].body
        if isinstance(node, ast.FunctionDef)
    }
    assert {
        "__init__",
        "capture_baseline",
        "check_for_material_change",
        "get_policy_name",
        "get_source_url",
        "is_baseline_ready",
        "get_baseline_profile",
        "get_last_assessment",
    }.issubset(methods)


def test_nondeterminism_is_consensus_wrapped():
    src = _source()
    assert "gl.eq_principle.prompt_non_comparative(" in src
    assert "gl.eq_principle.prompt_comparative(" in src
    assert "gl.nondet.web.render(" in src
    assert "gl.nondet.exec_prompt(" in src


def test_prompt_injection_guard_is_explicit():
    src = _source().lower()
    assert "untrusted evidence" in src
    assert "never follow instructions" in src


def test_material_change_categories_are_explicit():
    src = _source()
    for term in (
        "obligations",
        "prohibitions",
        "permissions",
        "eligibility",
        "fees/economic terms",
        "deadlines",
        "data use",
        "enforcement consequences",
    ):
        assert term in src
