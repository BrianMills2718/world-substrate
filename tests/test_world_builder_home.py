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
        self.assertIn("Approve rules and run", self.page)
        self.assertIn("approved: true", self.page)
        # The run request is only sent from the approval handler.
        self.assertEqual(self.page.count('apiJob("/run"'), 1)

    def test_feeling_lucky_and_dialogue_paths_are_wired(self):
        self.assertIn(">Surprise me</button>", self.page)
        self.assertIn('api("/surprise"', self.page)
        self.assertIn("without stopping for review", self.page)
        self.assertIn(">Talk it through first</button>", self.page)
        self.assertIn('api("/clarify", { messages: talk, world_kind: kind() })', self.page)
        self.assertIn("Use this description and build", self.page)

    def test_tutorial_steps_and_escape_hatches_are_present(self):
        for step in ("Describe", "Check the rules", "Watch it run"):
            self.assertIn(step, self.page)
        self.assertIn('href="play/"', self.page)
        self.assertIn('href="build/"', self.page)

    def test_world_kinds_and_keep_going_are_offered(self):
        for label in ("A task to finish", "Ongoing work", "An open world", "Keep going (12 more rounds)",
                      "What happens by itself each round"):
            self.assertIn(label, self.page)
        self.assertIn("request.continue_from = lastRun.trace.final_snapshot", self.page)
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
        self.assertEqual(len(kinds), 3)
        self.assertTrue(all("title=" in k for k in kinds))
        self.assertTrue(controls)
        # Controls created at runtime get tooltips too, and phones get them on long press.
        self.assertIn("c.title = bad ?", self.page)
        self.assertIn("c.title = \"Use this answer", self.page)
        self.assertIn("const tipTarget = (node) => node && node.closest", self.page)

    def test_start_choices_are_explained_in_plain_words(self):
        for line in ("Build it now</strong>: you already know what you want",
                     "Talk it through first</strong>: not sure yet",
                     "Surprise me</strong>: the AI invents a world"):
            self.assertIn(line, self.page)

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

    def test_tooltips_are_visible_bubbles_not_only_native_titles(self):
        self.assertIn('id="tip-bubble"', self.page)
        self.assertIn('document.addEventListener("mouseover"', self.page)
        self.assertIn('document.addEventListener("focusin"', self.page)
        self.assertEqual(self.page.count('class="info" data-tip-for='), 3)

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
