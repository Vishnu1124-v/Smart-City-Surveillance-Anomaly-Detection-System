import sys
from pathlib import Path
from mangum import Mangum

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.main import app

handler = Mangum(app)
