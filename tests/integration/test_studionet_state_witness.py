"""Opt-in Studionet smoke tests.

These tests are intentionally skipped unless a disposable deployment address
and RPC credentials are supplied by the operator. They never substitute local
Direct Mode for live consensus evidence.
"""

import os

import pytest


pytestmark = pytest.mark.integration


def _live_configured():
    return os.getenv("STATEWITNESS_STUDIONET_ADDRESS") and os.getenv("STATEWITNESS_STUDIONET_RPC")


@pytest.fixture
def live_config():
    if not _live_configured():
        pytest.skip("Studionet address/RPC not configured; set STATEWITNESS_STUDIONET_ADDRESS and STATEWITNESS_STUDIONET_RPC")
    return {
        "address": os.environ["STATEWITNESS_STUDIONET_ADDRESS"],
        "rpc": os.environ["STATEWITNESS_STUDIONET_RPC"],
    }


def test_studionet_deployment_is_explicitly_configured(live_config):
    assert live_config["address"]
    assert live_config["rpc"].startswith("http")


def test_studionet_success_path_requires_recorded_evidence(live_config):
    assert os.getenv("STATEWITNESS_SUCCESS_TX"), "record a verified success transaction"


def test_studionet_negative_path_requires_recorded_evidence(live_config):
    assert os.getenv("STATEWITNESS_NEGATIVE_TX"), "record a verified negative transaction"
