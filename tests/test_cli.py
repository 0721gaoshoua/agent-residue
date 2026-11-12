import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from agent_residue.cli import expand, human, load_catalog, main


class CliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.home = root / "home"
        self.trash = root / "trash"
        self._write(".claude/downloads/pkg.bin", b"x" * 5000)
        self._write(".claude/settings.json", b"{}")
        self._write(".claude/projects/chat.jsonl", b'{"a":1}')
        self._write(".qoder/logs/run.log", b"y" * 2000)
        self._write(".qoder/.auth/token", b"secret")

    def tearDown(self):
        self._tmp.cleanup()

    def _write(self, relative: str, data: bytes) -> Path:
        path = self.home / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_catalog_loads(self):
        catalog = load_catalog()
        ids = {agent["id"] for agent in catalog["agents"]}
        self.assertIn("claude-code", ids)
        self.assertIn("qoder", ids)
        self.assertGreaterEqual(len(ids), 20)

    def test_scan_is_read_only(self):
        code, out, _ = self.run_cli("scan", "--home", str(self.home))
        self.assertEqual(code, 0)
        self.assertIn("reclaimable", out)
        self.assertTrue((self.home / ".claude/downloads/pkg.bin").exists())

    def test_clean_quarantines_only_tier1(self):
        code, _, _ = self.run_cli(
            "clean", "--home", str(self.home), "-a", "claude-code,qoder",
            "--quarantine", str(self.trash), "--force",
        )
        self.assertEqual(code, 0)
        self.assertFalse((self.home / ".claude/downloads").exists())
        self.assertFalse((self.home / ".qoder/logs").exists())
        self.assertTrue((self.home / ".claude/settings.json").exists())
        self.assertTrue((self.home / ".qoder/.auth/token").exists())
        self.assertTrue((self.home / ".claude/projects/chat.jsonl").exists())

        manifests = list(self.trash.glob("*/manifest.json"))
        self.assertEqual(len(manifests), 1)
        data = json.loads(manifests[0].read_text(encoding="utf-8"))
        self.assertEqual(len(data["entries"]), 2)

    def test_restore_puts_everything_back(self):
        self.run_cli(
            "clean", "--home", str(self.home), "-a", "claude-code",
            "--quarantine", str(self.trash), "--force",
        )
        manifest = next(self.trash.glob("*/manifest.json"))
        code, _, _ = self.run_cli("restore", str(manifest))
        self.assertEqual(code, 0)
        self.assertTrue((self.home / ".claude/downloads/pkg.bin").exists())

    def test_purge_requires_yes(self):
        code, _, err = self.run_cli(
            "clean", "--home", str(self.home), "-a", "claude-code",
            "--purge", "--force",
        )
        self.assertEqual(code, 2)
        self.assertIn("--yes", err)
        self.assertTrue((self.home / ".claude/downloads/pkg.bin").exists())

    def test_purge_deletes(self):
        code, _, _ = self.run_cli(
            "clean", "--home", str(self.home), "-a", "claude-code",
            "--purge", "--yes", "--force",
        )
        self.assertEqual(code, 0)
        self.assertFalse((self.home / ".claude/downloads").exists())
        self.assertTrue((self.home / ".claude/settings.json").exists())

    def test_exclude_filters_labels(self):
        code, out, _ = self.run_cli(
            "scan", "--home", str(self.home), "-a", "qoder",
            "--exclude", "logs",
        )
        self.assertEqual(code, 0)
        self.assertNotIn("run.log", out)
        self.assertIn("nothing found", out)


class HelperTests(unittest.TestCase):
    def test_human(self):
        self.assertEqual(human(0), "0 B")
        self.assertEqual(human(1024 * 1024), "1.0 MB")

    def test_expand_tilde(self):
        home = Path("/tmp/example")
        self.assertEqual(expand("~/.claude", home), home / ".claude")

    def test_expand_missing_env(self):
        self.assertIsNone(expand("%NOT_A_REAL_VAR_XYZ%/logs", Path("/tmp")))


if __name__ == "__main__":
    unittest.main()
