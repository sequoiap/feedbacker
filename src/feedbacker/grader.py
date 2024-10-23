import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass

from feedbacker.exceptions import AutograderException


def run_ltspice(netlist):
    subprocess.run(["ltspice", "-Run", "-b", netlist])


def set_score(score: float):
    print(f".score {score}")


@dataclass
class GraderResult:
    score: float
    output: Optional[str] = None

    @classmethod
    def from_directives(cls, directives: list[str]) -> "GraderResult":
        kwargs = {}
        for directive in directives:
            if directive.startswith(".score"):
                kwargs["score"] = float(directive.split()[1])
        return cls(**kwargs)


def grade_file(grading_script: Path | str, uploaded_files: list[Path | str]) -> tuple[str, dict[str, Any]]:
    """Grade a file using a grading script.
    
    Args:
        grading_script (Path | str): The grading script to use.
        uploaded_files (list[Path | str]): The files to grade.

    Returns:
        tuple[str, dict[str, Any]]: The output and status of the grading.
    """
    process = subprocess.Popen(
        [sys.executable] + [grading_script] + list(uploaded_files),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    
    output: list[str] = []
    directives: list[str] = []
    for line in process.stdout:
        if line.startswith("."):
            directives.append(line.strip())
        else:
            output.append(line.strip())

    process.stdout.close()
    process.wait()

    result = GraderResult.from_directives(directives)
    result.output = "\n".join(output).strip()

    if process.returncode != 0:
        raise AutograderException(process.stderr)

    return result
