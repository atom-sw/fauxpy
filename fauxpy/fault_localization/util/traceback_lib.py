import re
from pathlib import Path
from typing import Tuple, List

from fauxpy.fault_localization.util.path_util import PathUtil


class TracebackParser:
    def __init__(self, project_working_directory: Path):
        self._path_util = PathUtil(project_working_directory)

    @staticmethod
    def _get_required_lines(lines) -> str:
        lines_list = []
        for line in lines:
            if line.startswith("> "):
                lines_list.append(line)
            if line.startswith("E "):
                lines_list.append(line)

        if len(lines_list) == 0:
            lines_list.append(lines[-1])

        information = "::".join(lines_list)
        return information

    def _get_trace_back_entry_essence(self, entry) -> str:
        file_path = entry.reprfileloc.path
        line_number = entry.reprfileloc.lineno
        message = entry.reprfileloc.message
        lines = self._get_required_lines(entry.lines)
        information = "::".join([file_path, str(line_number), message, lines])
        return information

    def get_short_trace_back_info(self, trace_back) -> str:
        information = []
        for item in trace_back.reprentries:
            item_info = self._get_trace_back_entry_essence(item)
            information.append(item_info)

        info_string = "\n".join(information)
        return info_string

    @staticmethod
    def has_timeout_happened(long_repr_text) -> bool:
        # Pattern is "E       Failed: Timeout >"
        pattern = "E( +)Failed:( *)Timeout( *)>"
        mat = re.search(pattern, long_repr_text)
        return mat is not None

    @staticmethod
    def _is_python_module(path: str):
        return path.endswith(".py")

    def get_exception_location(
        self, traceback, src: str, exclude: List[str]
    ) -> Tuple[str, int]:
        exception_file_path = ""
        exception_line_number = -1
        tb_len = len(traceback.reprentries)
        if tb_len > 1:
            for i in range(len(traceback.reprentries)):
                tmp = tb_len - i - 1
                c_path = traceback.reprentries[tb_len - i - 1].reprfileloc.path
                c_line_number = traceback.reprentries[tb_len - i - 1].reprfileloc.lineno
                c_path_abs = self._path_util.relative_path_to_abs_path(c_path)
                if self._path_util.path_should_be_localized(
                    src, exclude, c_path_abs
                ) and self._is_python_module(c_path_abs):
                    exception_file_path = c_path
                    exception_line_number = c_line_number
                    break

        return exception_file_path, exception_line_number
