class FlPrinter:
    """A printer utility class for controlling standard and detailed output."""

    _prefix = "FauxPy: --->"

    def __init__(self, is_detailed: bool = False):
        """
        Initialize a new object instance.

        Args:
            is_detailed (bool): If True, enables printing of detailed messages.
        """
        self._is_detailed = is_detailed

    def normal(self, *args, **kwargs):
        """
        Print a message to standard output regardless of detail mode.

        This method forwards all positional and keyword arguments to the built-in print function,
        allowing full control over formatting, separators, end characters, etc.

        Args:
            *args: Positional arguments to pass to print().
            **kwargs: Keyword arguments to pass to print().
        """
        print(self._prefix, *args, **kwargs)

    def detailed(self, *args, **kwargs):
        """
        Print a message to standard output only if detailed mode is enabled.

        This method forwards all positional and keyword arguments to the built-in print function,
        allowing full control over formatting, separators, end characters, etc.

        Args:
            *args: Positional arguments to pass to print().
            **kwargs: Keyword arguments to pass to print().
        """
        if self._is_detailed:
            print(self._prefix, *args, **kwargs)

    def set_is_detailed(self, is_detailed: bool):
        """
        Set the detailed mode for this printer.

        Args:
            is_detailed (bool): If True, enables detailed output.
        """
        self._is_detailed = is_detailed


# Shared instance to be used across the plugin
fl_print = FlPrinter()
