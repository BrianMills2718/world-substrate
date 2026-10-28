"""Shared test setup: no test reaches the paid independent rules review (scripts/review_rules.py) by accident."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]


@pytest.fixture(autouse=True)
def _no_paid_rules_review(monkeypatch):
    """The build loop's review call answers 'no findings' unless a test patches it itself."""
    from scripts import world_builder_service as service

    monkeypatch.setattr(service, "review_rules", lambda *args, **kwargs: ([], 0.0))
