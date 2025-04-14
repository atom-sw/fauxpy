from subprocess import TimeoutExpired
from typing import List, Optional
import subprocess

from fauxpy.session_lib.fauxpy_printer import fl_print


class CommandRunner:
    @staticmethod
    def run_command(
        command: List[str], working_dir: str, process_timeout: Optional[float]
    ):
        fl_print.detailed("--------------------Subprocess Begin---------------------")
        fl_print.detailed("Command to run: ", " ".join(command))
        exec_out = None
        if process_timeout is None:
            exec_out = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                cwd=working_dir,
            )
        else:
            try:
                exec_out = subprocess.run(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    cwd=working_dir,
                    timeout=process_timeout,
                )
            except TimeoutExpired:
                fl_print.detailed("Subprocess timeout")
                pass

        if exec_out is not None:
            fl_print.detailed(exec_out.stdout)
            fl_print.detailed(exec_out.stderr)
        fl_print.detailed("--------------------Subprocess End---------------------")
