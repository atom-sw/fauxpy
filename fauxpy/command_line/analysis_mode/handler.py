import argparse

from fauxpy import version


class FauxpyAnalysisModeHandler:
    """
    Handles FauxPy's command-line interface for Analysis Mode.
    """

    @staticmethod
    def main():
        """
        The main entry point for FauxPy Analysis Mode.
        """
        parser = argparse.ArgumentParser(description="FauxPy command mode")
        parser.add_argument(
            "-v", "--version", action="store_true", help="print version and exit"
        )

        args = parser.parse_args()
        if args.version:
            print(f"FauxPy {version.__version__}")
        else:
            parser.print_help()
