from typing import Tuple, List


class Mutant:
    """Represents a mutant in a source code file, created by applying a mutation operator."""

    def __init__(
        self,
        module_path: str,
        operator_name: str,
        start_pos: Tuple[int, int],
        end_pos: Tuple[int, int],
        occurrence: int,
        module_content: str,
        module_diff: List[str],
    ):
        """
        Initializes a Mutant instance.

        Args:
            module_path (str): The path to the source code module.
            operator_name (str): The name of the mutation operator applied.
            start_pos (Tuple[int, int]): The starting position (line, column) of the mutation.
            end_pos (Tuple[int, int]): The ending position (line, column) of the mutation.
            occurrence (int): The occurrence count of the mutation in the module.
            module_content (str): The content of the module after mutation.
            module_diff (List[str]): The mutation as diff.
        """
        self._module_path: str = module_path
        self.operator_name: str = operator_name
        self.start_pos: Tuple[int, int] = start_pos
        self.end_pos: Tuple[int, int] = end_pos
        self._occurrence: int = occurrence
        self._module_content: str = module_content
        self._module_diff: List[str] = module_diff
        self.id = "-"

    def set_id(self, val):
        """
        Sets the unique identifier for the mutant.

        Args:
            val (str): The identifier to be assigned.
        """
        self.id = val

    def get_id(self):
        """Returns the unique identifier of the mutant."""
        return self.id

    def get_module_path(self):
        """Returns the path of the module where the mutation occurred."""
        return self._module_path

    def get_module_operator(self):
        """Returns the name of the mutation operator applied."""
        return self.operator_name

    def get_module_content(self):
        """Returns the content of the module after mutation."""
        return self._module_content

    def get_module_diff_as_text(self):
        """Returns the mutation as diff."""
        diff_text = "\r\n".join(self._module_diff)
        return diff_text

    def operator_mutation_target_equal_to(self, mutant):
        """
        Checks if the mutation targets the same location and operator as another mutant.

        Args:
            mutant (Mutant): Another mutant to compare against.

        Returns:
            bool: True if both mutants target the same location and operator, False otherwise.
        """
        result = (
            self.operator_name == mutant.operator_name
            and self.start_pos == mutant.start_pos
            and self.end_pos == mutant.end_pos
        )
        return result

    # TODO: Multiline predicates might cause problem.
    def get_line_number(self):
        # A predicate can spread through multiple lines. In such cases,
        # we consider each line of the predicate a separate statement
        # while performing fault localization.
        # For instance, in the following predicate, we have two different lines
        # to mutate:
        # 12: if x > 10 and \
        # 13:   y < 24:
        # 14   ...
        # A mutation applied on line 12 or 13 (by for instance
        # changing the relational operators) are considered two
        # mutants with LineNumber == self.startPos[0].
        # However, putting a not operator after if affects the whole
        # predicate (i.e., both lines 12 and 13). In this case,
        # self.startPos[0] != self.endPos[0].
        # But even in this case, we consider LineNumber == self.startPos[0].
        # Thus, LineNumber is always self.startPos[0] (it is our assumption).

        return self.start_pos[0]

    def get_start_pos(self):
        """Returns the starting line number of the mutation."""
        return self.start_pos[0]

    def get_end_pos(self):
        """Returns the ending line number of the mutation."""
        return self.end_pos[0]
