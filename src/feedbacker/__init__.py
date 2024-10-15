import os
import os.path
import traceback
from subprocess import check_output

try:
    VERSION = __import__("pkg_resources").get_distribution("dispatch").version
except Exception:
    VERSION = "unknown"

try:
    from feedbacker.auth.models import User  # noqa
    from feedbacker.courses.models import Course  # noqa
    from feedbacker.assignments.models import Assignment  # noqa
except Exception:
    print(traceback.format_exc())


__version__ = VERSION
