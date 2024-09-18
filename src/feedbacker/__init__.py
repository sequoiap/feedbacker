import os
import os.path
import traceback
from subprocess import check_output

try:
    VERSION = __import__("pkg_resources").get_distribution("dispatch").version
except Exception:
    VERSION = "unknown"

try:
    from feedbacker.assignments.models import Assignment
except Exception:
    print(traceback.format_exc())


__version__ = VERSION
