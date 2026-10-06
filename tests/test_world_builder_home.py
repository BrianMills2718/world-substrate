from __future__ import annotations

import re
import unittest
from pathlib import Path

HOME = Path(__file__).resolve().parents[1] / "scripts/world_builder_home.html"


class WorldBuilderHomeTests(unittest.TestCase):
    def setUp(self):
        self.page = HOME.read_text()

    def test_natural_language_flow_uses_generation_then_explicit_approval(self):
        self.assertIn('apiJob("/generate-world"', self.page)
        self.assertIn("Approve rules and play", self.page)
        self.assertIn("approved: true", self.page)
        # Runs are requested only by the live-play loop, after approval.
        self.assertEqual(self.page.count('apiJob("/run"'), 1)
        self.assertEqual(self.page.count('api("/run"'), 1)
        self.assertIn('$("approve-btn").addEventListener("click", () => startLive());', self.page)

    def test_surprise_and_dialogue_paths_are_wired(self):
        # An empty box makes the one start button ask the AI to make a world up.
        self.assertIn('$("build-btn").addEventListener("click", () => ($("desc").value.trim() ? build() : surprise()));', self.page)
        self.assertIn('"Surprise me: the AI makes one up"', self.page)
        self.assertIn('api("/surprise"', self.page)
        self.assertIn("without stopping for review", self.page)
        self.assertIn(">Not sure what to write? Let the AI ask you a few questions</button>", self.page)
        self.assertIn('api("/clarify", { messages: talk, world_kind: kind() })', self.page)
        self.assertIn("Use this description and build", self.page)

    def test_tutorial_steps_and_escape_hatches_are_present(self):
        for step in ("Describe", "Check the rules", "Watch it run"):
            self.assertIn(step, self.page)
        self.assertIn('href="play/"', self.page)
        self.assertIn('href="build/"', self.page)

    def test_world_kinds_and_live_play_are_offered(self):
        for label in ("A task to finish", "Keeps running", "⏸ Pause", "▶ Play",
                      "By itself, every round", "Why things were refused"):
            self.assertIn(label, self.page)
        # Each round continues from exactly where the last one ended.
        self.assertIn("request.continue_from = live.snapshot; request.turn_offset = live.lastTurn;", self.page)
        self.assertIn("QUIET_ROUNDS_TO_PAUSE", self.page)
        # "Ongoing work" and "An open world" were one kind in all but name (merged 2026-10-06).
        self.assertNotIn('value="open"', self.page)
        self.assertIn('fetch(API + "/jobs/" + started.job_id, { headers: authHeaders() })', self.page)

    def test_owner_access_sends_the_password_on_every_request(self):
        self.assertIn("Owner access", self.page)
        self.assertIn('h["X-World-Builder-Owner"] = k', self.page)
        self.assertIn("headers: authHeaders(", self.page)
        self.assertIn('fetch(API + "/jobs/" + started.job_id, { headers: authHeaders() })', self.page)

    def test_every_control_has_a_tooltip(self):
        import re
        controls = re.findall(r"<(button|a|textarea|summary)\b[^>]*>", self.page)
        tags = re.findall(r"<(?:button|a|textarea|summary)\b[^>]*>", self.page)
        missing = [t for t in tags if "title=" not in t]
        self.assertEqual(missing, [], "every control needs a tooltip (title)")
        kinds = re.findall(r'<label class="kind"[^>]*>', self.page)
        self.assertEqual(len(kinds), 2)
        self.assertTrue(all("title=" in k for k in kinds))
        self.assertTrue(controls)
        # Controls created at runtime get tooltips too, and phones get them on long press.
        self.assertIn("c.title = bad ?", self.page)
        self.assertIn("c.title = \"Use this answer", self.page)
        self.assertIn("const tipTarget = (node) => node && node.closest", self.page)

    def test_one_start_button_says_what_it_will_do(self):
        # Three start choices only differed in who writes the description (merged 2026-10-06).
        self.assertEqual(self.page.count('id="build-btn"'), 1)
        self.assertNotIn('id="lucky-btn"', self.page)
        self.assertIn('$("build-btn").textContent = has ? "Build my world" : "Surprise me: the AI makes one up";', self.page)
        # An empty box never silently builds the example text.
        self.assertNotIn('$("desc").value.trim() || $("desc").placeholder', self.page)

    def test_page_script_is_valid_javascript(self):
        # A syntax error stops every handler on the page; the gate must catch it.
        import re, shutil, subprocess, tempfile
        node = shutil.which("node")
        if node is None:
            self.skipTest("node is not installed")
        scripts = re.findall(r"<script>(.*?)</script>", self.page, re.S)
        self.assertEqual(len(scripts), 1)
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as handle:
            handle.write(scripts[0])
        result = subprocess.run([node, "--check", handle.name], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_headline_counts_refused_attempts_not_held_back_moves(self):
        # G2: the headline added every blocked_by_rules entry (one per action kind
        # and reason the rules held back) and called the total "refused".
        import json, shutil, subprocess
        node = shutil.which("node")
        if node is None:
            self.skipTest("node is not installed")
        match = re.search(r"^  function countRound\(turn\) \{.*?^  \}$", self.page, re.S | re.M)
        self.assertIsNotNone(match, "the page needs one countRound used by the headline and the squares")
        turn = {"turn": 3, "actors": {
            "ana": {"status": "accepted", "did": {"kind": "fix"}},
            "ben": {"status": "no_action", "blocked_by_rules": [
                {"action": {"kind": "fix"}, "reason": "a"}, {"action": {"kind": "fetch"}, "reason": "b"},
                {"action": {"kind": "fetch"}, "reason": "c"}]},
            "cal": {"status": "refused", "wanted": {"kind": "fix"}, "refused_because": ["tool free"],
                    "blocked_by_rules": [{"action": {"kind": "rest"}, "reason": "d"}]},
            "dee": {"status": "nothing_left", "wanted": {"kind": "fetch"}},
        }}
        script = match.group(0) + "\nconsole.log(JSON.stringify(countRound(" + json.dumps(turn) + ")));"
        result = subprocess.run([node, "-e", script], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout), {"allowed": 1, "refused": 2, "held": 2})
        # Headline and squares both count through it, in plain words.
        self.assertIn("const c = countRound(turn);", self.page)
        self.assertIn("held back by the rules", self.page)
        self.assertNotIn("live.totals.refused += (row.blocked_by_rules || []).length", self.page)
        self.assertIn('t.className = "tick held";', self.page)

    def test_tooltips_are_visible_bubbles_not_only_native_titles(self):
        self.assertIn('id="tip-bubble"', self.page)
        self.assertIn('document.addEventListener("mouseover"', self.page)
        self.assertIn('document.addEventListener("focusin"', self.page)
        self.assertEqual(self.page.count('class="info" data-tip-for='), 1)

    def test_failure_states_are_written_in_plain_words(self):
        self.assertIn("These rules let nobody act", self.page)
        self.assertIn("AI budget", self.page)
        self.assertIn("not reachable right now", self.page)

    def test_palette_avoids_red_green_pairing(self):
        colors = set(re.findall(r"--(ok|warn|grey):(#[0-9a-f]{6})", self.page))
        self.assertEqual({name for name, _ in colors}, {"ok", "warn", "grey"})
        self.assertNotRegex(self.page, r"#(?:ff0000|00ff00|e74c3c|2ecc71)")


if __name__ == "__main__":
    unittest.main()
