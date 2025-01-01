"""

 Copyright 2024 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

import sys
import os

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "OPEN_SESAME")
