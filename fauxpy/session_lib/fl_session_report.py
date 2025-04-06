from typing import Tuple, List, Dict

from .fl_type import FlGranularity
from .fauxpy_path import FauxpyPath


class FlSessionReport:
    """Generates a report for a fault localization session."""
    _rounding_decimal_places = 4
    _header_file = "File"
    _header_line = "Line"
    _header_score = "Score"
    _header_function = "Function"
    _header_range = "Lines"

    def __init__(
            self,
            scored_entity_dict: Dict[str, List[Tuple[str, float]]],
            execution_time: float,
            granularity: FlGranularity,
            project_working_directory: FauxpyPath
    ):
        """
        Initializes the object.

        Args:
            scored_entity_dict (Dict[str, List[Tuple[str, float]]]): A dictionary where the keys are technique names and
                the values are lists of tuples (entity, score). The format of entity depends on granularity:
                - Statement level: file_path::line_number
                - Function level: file_path::function_name::start_line::end_line
            execution_time (float): The time taken by the fault localization session.
            granularity (FlGranularity): The granularity level of the report (statement or function).
            project_working_directory (FauxpyPath): The directory where the project files are located.
        """
        self._scored_entity_dict = self._get_rounded_score(scored_entity_dict)
        self._execution_time = execution_time
        self._granularity = granularity
        self._project_working_directory = project_working_directory

    def generate_report(self):
        """Generates the fault localization session report."""
        title = " Fault Localization Results "
        border = "=" * len(title)
        print(f"\n{border}\n{title}\n{border}\n")
        print(f"=== Performance ===")
        print(f"Execution Time: {self._execution_time:.{self._rounding_decimal_places}f}\n")

        if self._granularity == FlGranularity.Statement:
            for technique_name, scored_entity_list in self._scored_entity_dict.items():
                self._print_scores_statement_level(technique_name, scored_entity_list)
        elif self._granularity == FlGranularity.Function:
            for technique_name, scored_entity_list in self._scored_entity_dict.items():
                self._print_scores_function_level(technique_name, scored_entity_list)
        else:
            # This should never happen as we have input validation, but let's keep it here.
            raise ValueError(f"Invalid granularity: {self._granularity}")

    def _get_rounded_score(
            self,
            scored_entity_dict: Dict[str, List[Tuple[str, float]]]
    ) -> Dict[str, List[Tuple[str, float]]]:
        """
        Rounds the scores to the defined number of decimal places.

        Args:
            scored_entity_dict (Dict[str, List[Tuple[str, float]]]): Dictionary containing technique names and their scored entities.

        Returns:
            Dict[str, List[Tuple[str, float]]]: Dictionary with scores rounded to the specified decimal places.
        """
        rounded_scored_entity_dict = {
            key: [(entity, round(score, self._rounding_decimal_places)) for entity, score in value]
            for key, value in scored_entity_dict.items()
        }

        return rounded_scored_entity_dict

    def _print_scores_statement_level(
            self,
            technique_name: str,
            scored_entity_list: List[Tuple[str, float]]
    ):
        """
        Prints the statement-level scores for a given technique.

        Args:
            technique_name (str): The name of the fault localization technique.
            scored_entity_list (List[Tuple[str, float]]): List of scored entities at the statement level.
        """
        has_negative_score = any(score < 0 for _, score in scored_entity_list)

        title = f" Scores for {technique_name} "
        border = "-" * (len(title) + 6)
        print(f"{border}\n|  {title}  |\n{border}")

        (
            file_pad,
            line_pad,
            score_pad
        ) = self._get_max_column_widths_statement_level(scored_entity_list)

        print(f"{self._header_file.ljust(file_pad)} | "
              f"{self._header_line.ljust(line_pad)} | "
              f"{self._header_score.ljust(score_pad)}")
        print('-' * (file_pad + line_pad + score_pad + 6))

        for entity, score in scored_entity_list:
            file_path, line_number = entity.split("::")
            file_path_relative = self._get_relative_path(file_path)
            score_format = (f"{score:+.{self._rounding_decimal_places}f}" if has_negative_score
                            else f"{score:.{self._rounding_decimal_places}f}")
            print(f"{file_path_relative.ljust(file_pad)} | "
                  f"{line_number.rjust(line_pad)} | "
                  f"{score_format.rjust(score_pad)}")

        print('-' * (file_pad + line_pad + score_pad + 6) + "\n")

    def _print_scores_function_level(
            self,
            technique_name: str,
            scored_entity_list: List[Tuple[str, float]]
    ):
        """
        Prints the function-level scores for a given technique.

        Args:
            technique_name (str): The name of the fault localization technique.
            scored_entity_list (List[Tuple[str, float]]): List of scored entities at the function level.
        """
        has_negative_score = any(score < 0 for _, score in scored_entity_list)

        title = f" Scores for {technique_name} "
        border = "-" * (len(title) + 6)
        print(f"{border}\n|  {title}  |\n{border}")

        (
            file_pad,
            func_pad,
            range_pad,
            score_pad
        ) = self._get_max_column_widths_function_level(scored_entity_list)

        print(f"{self._header_file.ljust(file_pad)} | "
              f"{self._header_function.ljust(func_pad)} | "
              f"{self._header_range.ljust(range_pad)} | "
              f"{self._header_score.ljust(score_pad)}")
        print('-' * (file_pad + func_pad + range_pad + score_pad + 9))

        for entity, score in scored_entity_list:
            file_path, func_name, start_line, end_line = entity.split("::")
            file_path_relative = self._get_relative_path(file_path)
            func_range = f"{start_line}-{end_line}"
            score_format = (f"{score:+.{self._rounding_decimal_places}f}" if has_negative_score
                            else f"{score:.{self._rounding_decimal_places}f}")
            print(f"{file_path_relative.ljust(file_pad)} | "
                  f"{func_name.ljust(func_pad)} | "
                  f"{func_range.center(range_pad)} | "
                  f"{score_format.rjust(score_pad)}")

        print('-' * (file_pad + func_pad + range_pad + score_pad + 9) + "\n")

    def _get_max_column_widths_statement_level(
            self,
            scored_entity_list: List[Tuple[str, float]]
    ) -> Tuple[int, int, int]:
        """
        Calculates the maximum column widths for statement-level entities.

        Args:
            scored_entity_list (List[Tuple[str, float]]): List of scored statement-level entities.

        Returns:
            Tuple[int, int, int]: Maximum column widths for file, line, and score columns.
        """
        if len(scored_entity_list) == 0:
            max_file_width = 0
            max_line_width = 0
            max_score_width = 0
        else:
            max_file_width = max(len(self._get_relative_path(score[0].split("::")[0]))
                                 for score in scored_entity_list)
            max_line_width = max(len(score[0].split("::")[1])
                                 for score in scored_entity_list)
            max_score_width = max(len(f"{score[1]:.{self._rounding_decimal_places}f}")
                                  for score in scored_entity_list)

        max_file_width = max(len(self._header_file), max_file_width)
        max_line_width = max(len(self._header_line), max_line_width)
        max_score_width = max(len(self._header_score), max_score_width)

        return max_file_width, max_line_width, max_score_width

    def _get_max_column_widths_function_level(
            self,
            scored_entity_list: List[Tuple[str, float]]
    ) -> Tuple[int, int, int, int]:
        """
        Calculates the maximum column widths for function-level entities.

        Args:
            scored_entity_list (List[Tuple[str, float]]): List of scored function-level entities.

        Returns:
            Tuple[int, int, int, int]: Maximum column widths for file, function, range, and score columns.
        """
        if len(scored_entity_list) == 0:
            max_file_width = 0
            max_func_width = 0
            max_range_width = 0
            max_score_width = 0
        else:
            max_file_width = max(len(self._get_relative_path(score[0].split("::")[0]))
                                 for score in scored_entity_list)
            max_func_width = max(len(score[0].split("::")[1])
                                 for score in scored_entity_list)
            max_range_width = max(len(f"{score[0].split('::')[2]}-{score[0].split('::')[3]}")
                                  for score in scored_entity_list)
            max_score_width = max(len(f"{score[1]:.{self._rounding_decimal_places}f}")
                                  for score in scored_entity_list)

        max_file_width = max(len(self._header_file), max_file_width)
        max_func_width = max(len(self._header_function), max_func_width)
        max_range_width = max(len(self._header_range), max_range_width)
        max_score_width = max(len(self._header_score), max_score_width)

        return max_file_width, max_func_width, max_range_width, max_score_width

    def _get_relative_path(self, file_path: str) -> str:
        fauxpy_path_file = FauxpyPath.from_absolute_path(self._project_working_directory.get_absolute(), file_path)
        path_str_relative = fauxpy_path_file.get_relative()
        return path_str_relative
