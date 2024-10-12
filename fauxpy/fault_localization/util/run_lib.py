from subprocess import TimeoutExpired
from typing import List, Optional
import subprocess


class CommandRunner:
    @staticmethod
    def run_command(
        command: List[str], working_dir: str, process_timeout: Optional[float]
    ):
        print("--------------------Subprocess Begin---------------------")
        print("Command to run: ", " ".join(command))
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
                print("Subprocess timeout")
                pass

        if exec_out is not None:
            print(exec_out.stdout)
            print(exec_out.stderr)
        print("--------------------Subprocess End---------------------")
