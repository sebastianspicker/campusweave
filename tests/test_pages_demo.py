from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from campusweave import service
from scripts.build_pages_demo import build


class PagesDemoBuildTests(unittest.TestCase):
    def test_build_uses_the_compiled_sanitized_reference_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site"
            build(output)

            index = (output / "index.html").read_text(encoding="utf-8")
            fixture = json.loads((output / "demo-fixture.json").read_text())

            self.assertIn('content="static-demo"', index)
            self.assertNotIn('href="/', index)
            self.assertNotIn('src="/', index)
            self.assertEqual(fixture, service.reference_response())
            self.assertFalse(fixture["dry_run"]["network_capable"])
            self.assertFalse(fixture["dry_run"]["mutation_capable"])
            self.assertTrue((output / ".nojekyll").is_file())


if __name__ == "__main__":
    unittest.main()
