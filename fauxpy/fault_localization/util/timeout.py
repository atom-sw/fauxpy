from fauxpy import constants


def get_timeout(max_test_time: float) -> float:
    if max_test_time is None:
        max_test_time = 0
    timeout = constants.testTimeoutFactor * max_test_time + constants.testTimeoutOffset
    return timeout


def get_process_timeout(num_all_tests, timeout_limit):
    return (num_all_tests + 1) * timeout_limit
