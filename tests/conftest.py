import sys
from pathlib import Path

# Let tests import the project's packages (scoring, forecast, ...) from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
