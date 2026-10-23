import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", REPO / "tools/skills.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.skill = self.repo / 'ingchips-docs'
        self.skill.mkdir(parents=True)
        for name in installer.REQUIRED:
            path = self.skill / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('fixture', encoding='utf-8')
        ref = self.skill / 'references/book/page.md'
        ref.parent.mkdir(parents=True)
        ref.write_text('# UART\nbody\n', encoding='utf-8')
        (self.skill / 'catalog.json').write_text(json.dumps({'files': [
            {'path': 'book/page.md', 'sha256': hashlib.sha256(ref.read_bytes()).hexdigest()}
        ]}), encoding='utf-8')
        (self.repo / 'maintenance').mkdir()
        (self.repo / 'maintenance/never-install.txt').write_text('private cache')
        self.mock = patch.object(installer, 'REPO', self.repo)
        self.mock.start()
        self.addCleanup(self.mock.stop)

    def plan(self, root, replace=False):
        return installer.prepare_plan('ingchips-docs', [root], replace)

    def test_paths_and_shared_project_dedup(self):
        project = self.root / 'firmware'
        home = self.root / 'fake-home'
        self.assertEqual(installer.target_root('codex', 'global', home=home), home / '.agents/skills')
        self.assertEqual(installer.target_root('opencode', 'global', home=home), home / '.config/opencode/skills')
        roots = [installer.target_root(a, 'project', project) for a in installer.TARGETS]
        _, _, plan = installer.prepare_plan('ingchips-docs', roots)
        self.assertEqual(len(plan), 2)
        self.assertFalse(project.exists())

    def test_install_only_payload_and_idempotent(self):
        dest = self.root / 'skills with spaces'
        source, payload, plan = self.plan(dest)
        installer.execute_install(source, payload, plan)
        installed = dest / 'ingchips-docs'
        self.assertEqual(installer.files_under(installed), payload)
        self.assertFalse(list(installed.rglob('never-install.txt')))
        before = (installed / 'SKILL.md').stat().st_mtime_ns
        source, payload, plan = self.plan(dest)
        self.assertEqual(plan[0]['action'], 'unchanged')
        self.assertEqual(installer.execute_install(source, payload, plan), [])
        self.assertEqual((installed / 'SKILL.md').stat().st_mtime_ns, before)

    def test_replace_keeps_backup_and_removes_stale_file(self):
        dest = self.root / 'user/.agents/skills'
        installed = dest / 'ingchips-docs'
        installed.mkdir(parents=True)
        (installed / 'old.txt').write_text('old data')
        with self.assertRaises(ValueError):
            self.plan(dest)
        records = installer.execute_install(*self.plan(dest, True))
        self.assertEqual((records[0]['backup'] / 'old.txt').read_text(), 'old data')
        self.assertFalse((installed / 'old.txt').exists())
        self.assertFalse(records[0]['backup'].is_relative_to(dest))

    def test_multi_target_conflict_preflight(self):
        first, second = self.root / 'first', self.root / 'second'
        (second / 'ingchips-docs').mkdir(parents=True)
        with self.assertRaises(ValueError):
            installer.prepare_plan('ingchips-docs', [first, second])
        self.assertFalse(first.exists())

    def test_publication_failure_rolls_back_all(self):
        roots = [self.root / 'first/skills', self.root / 'second/skills']
        for root in roots:
            (root / 'ingchips-docs').mkdir(parents=True)
            (root / 'ingchips-docs/old.txt').write_text(str(root))
        source, payload, plan = installer.prepare_plan('ingchips-docs', roots, True)
        rename = Path.rename
        def fail_second(path, target):
            if '.ingchips-install-' in str(path) and Path(target) == roots[1] / 'ingchips-docs':
                raise OSError('injected error')
            return rename(path, target)
        with patch.object(Path, 'rename', fail_second):
            with self.assertRaises(OSError):
                installer.execute_install(source, payload, plan)
        for root in roots:
            self.assertEqual((root / 'ingchips-docs/old.txt').read_text(), str(root))
            self.assertFalse((root / 'ingchips-docs/SKILL.md').exists())

    def test_source_overlap_and_stale_catalog_rejected(self):
        with self.assertRaises(ValueError):
            self.plan(self.repo, True)
        with self.assertRaises(ValueError):
            self.plan(self.skill / 'nested')
        (self.skill / 'references/book/page.md').write_text('modified')
        with self.assertRaisesRegex(ValueError, 'Stale'):
            self.plan(self.root / 'other')

    def test_deterministic_zip_layout_and_licenses(self):
        one, two = self.root / 'one.zip', self.root / 'two.zip'
        _, digest, _ = installer.package('ingchips-docs', one)
        installer.package('ingchips-docs', two)
        self.assertEqual(one.read_bytes(), two.read_bytes())
        self.assertIn(digest, one.with_suffix('.zip.sha256').read_text())
        with zipfile.ZipFile(one) as z:
            names = z.namelist()
            self.assertIn('ingchips-docs/SKILL.md', names)
            self.assertIn('ingchips-docs/LICENSE', names)
            self.assertIn('ingchips-docs/NOTICE', names)
            self.assertTrue(all(n.startswith('ingchips-docs/') for n in names))
            self.assertFalse(any('maintenance' in n or '__pycache__' in n for n in names))
        with self.assertRaises(ValueError):
            installer.package('ingchips-docs', one)

    def test_linked_destination_refused(self):
        actual = self.root / 'actual'
        actual.mkdir()
        dest = self.root / 'links'
        dest.mkdir()
        try:
            (dest / 'ingchips-docs').symlink_to(actual, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f'symlink privilege unavailable: {exc}')
        with self.assertRaisesRegex(ValueError, 'link'):
            self.plan(dest, True)


class RepositoryTests(unittest.TestCase):
    def test_actual_package_and_dry_run(self):
        with tempfile.TemporaryDirectory() as td:
            dest = Path(td) / 'not-created'
            proc = subprocess.run([sys.executable, '-B', str(REPO / 'tools/skills.py'), 'install',
                                   '--dest', str(dest), '--dry-run'], cwd=td, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertFalse(dest.exists())
            path, _, _ = installer.package('ingchips-docs', Path(td) / 'actual.zip')
            with zipfile.ZipFile(path) as z:
                self.assertIsNone(z.testzip())
                self.assertIn('ingchips-docs/licenses/FreeRTOS-CC-BY-SA-4.0.txt', z.namelist())
                self.assertEqual(sum(n.endswith('/SKILL.md') for n in z.namelist()), 1)
                z.extractall(Path(td) / 'unpacked')
            query = subprocess.run([sys.executable, str(Path(td) / 'unpacked/ingchips-docs/scripts/search_docs.py'),
                                    'UART', '--chip', 'ING916', '--topic', 'peripheral', '--json'],
                                   cwd=td, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(query.returncode, 0, query.stderr)
            self.assertTrue(json.loads(query.stdout)['hits'])

    def test_license_copies_match(self):
        for name in ('LICENSE', 'NOTICE'):
            self.assertEqual((REPO / name).read_bytes(), (REPO / 'ingchips-docs' / name).read_bytes())


if __name__ == '__main__':
    unittest.main()
