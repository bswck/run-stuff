import os
import subprocess
import sys
import tempfile
from contextlib import contextmanager
startup_code = "def foo():\n    1/0\n"


@contextmanager
def new_startup_env(*, code: str, histfile: str = ".pythonhist"):
    """Create environment variables for a PYTHONSTARTUP script in a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "pythonstartup.py")
        with open(filename, "w") as f:
            f.write(os.linesep.join(code.splitlines()))
        yield {"PYTHONSTARTUP": filename, "PYTHON_HISTORY": os.path.join(tmpdir, histfile)}


with new_startup_env(code=startup_code) as startup_env:
    p = subprocess.Popen(
        [os.path.join(os.path.dirname(sys.executable), "<stdin>"), "-q", "-i"],
        env=os.environ | startup_env,
        executable=sys.executable,
        text=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    p.stdin.write("foo()")
    p.stdin.close()
    data = p.stdout.read()
    p.stdout.close()
    # try to cleanup the child so we don't appear to leak when running
    # with regrtest -R.
    p.wait()
    subprocess._cleanup()
    print(data)
