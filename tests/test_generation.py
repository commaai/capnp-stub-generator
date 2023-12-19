import os
import pathlib
import subprocess
import sys
import unittest

from capnp_stub_generator.cli import main

here = pathlib.Path(__file__).parent


class TestGeneration(unittest.TestCase):
    @classmethod
    def py_file(cls):
        return here / f"dummy_capnp.py"

    @classmethod
    def setUpClass(cls):
        main(
            [
                "-p",
                str(here / "dummy.capnp"),
                "-o",
                str(cls.py_file().parent)
            ]
        )

    @property
    def env(self):
        env = os.environ.copy()
        env.update({"PYTHONPATH": str(self.py_file().parent)})
        return env

    def test_reading(self):
        # Check that access the module works.
        assert subprocess.run([sys.executable, str(here / "use_dummy.py")], env=self.env).returncode == 0

    def test_mypy(self):
        # Assert that all types are present and valid
        assert subprocess.run([sys.executable, "-m", "mypy", str(here / "use_dummy.py")], env=self.env).returncode == 0


if __name__ == "__main__":
    unittest.main()
