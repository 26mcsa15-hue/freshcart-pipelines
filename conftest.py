# CI does not install the full mage-ai package (a heavy dependency that does not
# build on the CI runner). prepare_data.py only needs Mage's decorators, so when
# mage_ai is missing we register harmless pass-through versions of them.
import sys
import types

try:
    import mage_ai  # noqa: F401
except ImportError:
    def _passthrough(fn=None, *args, **kwargs):
        return fn if fn is not None else (lambda f: f)

    decorators = types.ModuleType("mage_ai.data_preparation.decorators")
    for name in ("data_loader", "transformer", "data_exporter", "test"):
        setattr(decorators, name, _passthrough)

    sys.modules["mage_ai"] = types.ModuleType("mage_ai")
    sys.modules["mage_ai.data_preparation"] = types.ModuleType("mage_ai.data_preparation")
    sys.modules["mage_ai.data_preparation.decorators"] = decorators
