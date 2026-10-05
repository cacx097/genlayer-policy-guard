from pathlib import Path
import sys

import pytest


CONTRACT = Path("contracts/policy_guard.py")
SDK_VERSION = "v0.2.12"

pytestmark = pytest.mark.skipif(
    sys.platform == "win32",
    reason=(
        "genlayer-test 0.29.2 direct loader keeps its temporary stdin file open "
        "while unlinking it on Windows (WinError 32). Run these tests on Linux/CI "
        "or use hosted GenLayer Studio for runtime verification."
    ),
)


def test_deploy_and_read_initial_state(direct_deploy):
    guard = direct_deploy(
        CONTRACT,
        "Example Policy",
        "https://example.com/policy",
        sdk_version=SDK_VERSION,
    )

    assert guard.get_policy_name() == "Example Policy"
    assert guard.get_source_url() == "https://example.com/policy"
    assert guard.is_baseline_ready() is False
    assert guard.get_baseline_profile() == ""
    assert guard.get_last_assessment() == ""


def test_rejects_non_https_source(direct_vm, direct_deploy):
    with direct_vm.expect_revert("source_url must use https://"):
        direct_deploy(
            CONTRACT,
            "Unsafe Source",
            "http://example.com/policy",
            sdk_version=SDK_VERSION,
        )


def test_change_check_requires_baseline(direct_vm, direct_deploy):
    guard = direct_deploy(
        CONTRACT,
        "Example Policy",
        "https://example.com/policy",
        sdk_version=SDK_VERSION,
    )

    with direct_vm.expect_revert("capture_baseline must be called first"):
        guard.check_for_material_change()
