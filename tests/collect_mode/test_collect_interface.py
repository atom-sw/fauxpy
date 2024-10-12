from fauxpy.fault_localization.collect_ps_info.api_lib import CollectPsInfoApi


def test_index_predicate_sequence():
    predicate_sequence = "Pred_1,Pred_2,Pred_3,Pred_3,Pred_2,Pred_2,Pred_6"
    collect_ps_info_api = CollectPsInfoApi()
    actual = collect_ps_info_api.index_predicate_sequence(predicate_sequence)
    expected = "Pred_1::0,Pred_2::0,Pred_3::0,Pred_3::1,Pred_2::1,Pred_2::2,Pred_6::0"
    assert actual == expected


def test_get_index_predicate_sequences():
    predicate_sequence_table = [
        [
            "tests/test_black.py::716::BlackTestCase.test_get_future_imports",
            "Pred_1,Pred_2,Pred_3,Pred_3,Pred_2,Pred_2,Pred_6",
        ],
        [
            "tests/test_black.py::716::BlackTestCase.test_get_future_imports1",
            "Pred_1,Pred_2,Pred_4,Pred_5,Pred_6,Pred_7,Pred_8",
        ],
    ]
    collect_ps_info_api = CollectPsInfoApi()
    actual = collect_ps_info_api.get_index_predicate_sequences(predicate_sequence_table)
    expected = [
        (
            "tests/test_black.py::716::BlackTestCase.test_get_future_imports",
            "Pred_1,Pred_2,Pred_3,Pred_3,Pred_2,Pred_2,Pred_6",
            "Pred_1::0,Pred_2::0,Pred_3::0,Pred_3::1,Pred_2::1,Pred_2::2,Pred_6::0",
        ),
        (
            "tests/test_black.py::716::BlackTestCase.test_get_future_imports1",
            "Pred_1,Pred_2,Pred_4,Pred_5,Pred_6,Pred_7,Pred_8",
            "Pred_1::0,Pred_2::0,Pred_4::0,Pred_5::0,Pred_6::0,Pred_7::0,Pred_8::0",
        ),
    ]
    assert actual == expected
