import json
import pytest


SPEC = """
R1: A milestone may move from PENDING to APPROVED only when evidence shows that
    the required deliverable was completed.
R2: A milestone must not move to APPROVED when the evidence explicitly says the
    deliverable is incomplete.
"""

SCHEMA = """
State is JSON with:
- status: PENDING | APPROVED
- milestone: string
"""

INITIAL = '{"status":"PENDING","milestone":"docs"}'


def deploy_machine(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/state_witness.py")
    direct_vm.sender = direct_alice
    contract.create_machine("milestone-1", SPEC, INITIAL, SCHEMA)
    return contract


def test_create_machine(direct_vm, direct_deploy, direct_alice):
    contract = deploy_machine(direct_vm, direct_deploy, direct_alice)
    machine = json.loads(contract.get_machine("milestone-1"))
    assert machine["state_version"] == 0
    assert machine["spec_version"] == 1
    assert machine["active"] is True
    assert machine["current_state"] == INITIAL


def test_valid_transition_applies(direct_vm, direct_deploy, direct_alice, direct_llm):
    contract = deploy_machine(direct_vm, direct_deploy, direct_alice)
    direct_llm.mock_response = '{"decision":"VALID","violated_rule_ids":[],"missing_preconditions":[],"material_reason":"Deliverable completed."}'

    result = json.loads(
        contract.propose_transition(
            "milestone-1",
            0,
            '{"status":"APPROVED","milestone":"docs"}',
            "The documentation package is complete and published.",
            "",
        )
    )

    assert result["decision"] == "VALID"
    assert result["applied"] is True
    assert result["new_state_version"] == 1
    machine = json.loads(contract.get_machine("milestone-1"))
    assert json.loads(machine["current_state"])["status"] == "APPROVED"


def test_invalid_transition_does_not_apply(direct_vm, direct_deploy, direct_alice, direct_llm):
    contract = deploy_machine(direct_vm, direct_deploy, direct_alice)
    direct_llm.mock_response = '{"decision":"INVALID","violated_rule_ids":["R1"],"missing_preconditions":["completion evidence"],"material_reason":"Completion not shown."}'

    result = json.loads(
        contract.propose_transition(
            "milestone-1",
            0,
            '{"status":"APPROVED","milestone":"docs"}',
            "Work has started but is not complete.",
            "",
        )
    )

    assert result["decision"] == "INVALID"
    assert result["applied"] is False
    assert result["new_state_version"] == 0
    machine = json.loads(contract.get_machine("milestone-1"))
    assert machine["current_state"] == INITIAL


def test_stale_version_rejected(direct_vm, direct_deploy, direct_alice, direct_llm):
    contract = deploy_machine(direct_vm, direct_deploy, direct_alice)
    direct_llm.mock_response = '{"decision":"VALID","violated_rule_ids":[],"missing_preconditions":[],"material_reason":"ok"}'
    contract.propose_transition(
        "milestone-1",
        0,
        '{"status":"APPROVED","milestone":"docs"}',
        "Complete.",
        "",
    )

    with pytest.raises(Exception, match="stale state version"):
        contract.propose_transition(
            "milestone-1",
            0,
            '{"status":"APPROVED","milestone":"docs"}',
            "Complete.",
            "",
        )


def test_specification_version_increments(direct_vm, direct_deploy, direct_alice):
    contract = deploy_machine(direct_vm, direct_deploy, direct_alice)
    contract.update_specification("milestone-1", SPEC + "\nR3: Evidence must identify the milestone.", SCHEMA)
    machine = json.loads(contract.get_machine("milestone-1"))
    assert machine["spec_version"] == 2


def test_pause_blocks_transitions(direct_vm, direct_deploy, direct_alice):
    contract = deploy_machine(direct_vm, direct_deploy, direct_alice)
    contract.set_machine_active("milestone-1", False)
    with pytest.raises(Exception, match="machine is paused"):
        contract.propose_transition(
            "milestone-1",
            0,
            '{"status":"APPROVED","milestone":"docs"}',
            "Complete.",
            "",
        )


def test_transition_receipt_records_rejection(direct_vm, direct_deploy, direct_alice, direct_llm):
    contract = deploy_machine(direct_vm, direct_deploy, direct_alice)
    direct_llm.mock_response = '{"decision":"INVALID","violated_rule_ids":["R2"],"missing_preconditions":[],"material_reason":"Evidence says incomplete."}'

    result = json.loads(
        contract.propose_transition(
            "milestone-1",
            0,
            '{"status":"APPROVED","milestone":"docs"}',
            "The deliverable is incomplete.",
            "",
        )
    )
    receipt = json.loads(contract.get_transition(result["transition_id"]))
    assert receipt["decision"] == "INVALID"
    assert receipt["violated_rule_ids"] == ["R2"]
    assert receipt["applied"] is False
