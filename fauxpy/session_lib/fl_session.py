from abc import abstractmethod, ABC


class FlSession(ABC):
    @abstractmethod
    def run_test_call(self, item):
        """
        Runs before the execution of the current test.
        """
        pass

    @abstractmethod
    def run_test_make_report(self, item, call):
        """
        Runs after the execution of the current test.
        """
        pass

    @abstractmethod
    def terminal_summary(self, terminal_reporter, exit_status):
        """
        Runs after the execution of all tests.
        """
        pass
