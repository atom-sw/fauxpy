from fauxpy.session_lib.target_tsts import TargetFailingTests


def test_single_3_part_faining_test_unittest_format():
    failing_test_list = [
        "tornado/test/httpclient_test.py::SyncHTTPClientSubprocessTest::test_destructor_log"
    ]
    tft_object = TargetFailingTests(failing_test_list)

    test_path = "tornado/test/httpclient_test.py"
    test_method_name = "SyncHTTPClientSubprocessTest.test_destructor_log"

    assert tft_object.is_target_test(test_path, test_method_name)


def test_single_3_part_faining_test_pytest_format():
    """From httpie2"""

    failing_test_list = ["tests/test_redirects.py::TestRedirects::test_max_redirects"]
    tft_object = TargetFailingTests(failing_test_list)

    test_path = "tests/test_redirects.py"
    test_method_name = "TestRedirects.test_max_redirects"

    assert tft_object.is_target_test(test_path, test_method_name)


def test_single_2_part_faining_test_pytest_format():
    failing_test_list = ["tests/test_url_for.py::test_routes_with_host"]
    tft_object = TargetFailingTests(failing_test_list)

    test_path = "tests/test_url_for.py"
    test_method_name = "test_routes_with_host"

    assert tft_object.is_target_test(test_path, test_method_name)
