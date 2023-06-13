from fauxpy.collect_mode.collect_interface import getIndexPredicateSequences, indexPredicateSequence


def test_indexPredicateSequence():
    predicateSequence = "Pred_1,Pred_2,Pred_3,Pred_3,Pred_2,Pred_2,Pred_6"
    actual = indexPredicateSequence(predicateSequence)
    expected = 'Pred_1::0,Pred_2::0,Pred_3::0,Pred_3::1,Pred_2::1,Pred_2::2,Pred_6::0'
    assert actual == expected


def test_getIndexPredicateSequences():
    predicateSequenceTable = [
        ["tests/test_black.py::716::BlackTestCase.test_get_future_imports",
         "Pred_1,Pred_2,Pred_3,Pred_3,Pred_2,Pred_2,Pred_6"],

        ["tests/test_black.py::716::BlackTestCase.test_get_future_imports1",
         "Pred_1,Pred_2,Pred_4,Pred_5,Pred_6,Pred_7,Pred_8"]
    ]
    actual = getIndexPredicateSequences(predicateSequenceTable)
    expected = [
        ('tests/test_black.py::716::BlackTestCase.test_get_future_imports',
         'Pred_1,Pred_2,Pred_3,Pred_3,Pred_2,Pred_2,Pred_6',
         'Pred_1::0,Pred_2::0,Pred_3::0,Pred_3::1,Pred_2::1,Pred_2::2,Pred_6::0'),

        ('tests/test_black.py::716::BlackTestCase.test_get_future_imports1',
         'Pred_1,Pred_2,Pred_4,Pred_5,Pred_6,Pred_7,Pred_8',
         'Pred_1::0,Pred_2::0,Pred_4::0,Pred_5::0,Pred_6::0,Pred_7::0,Pred_8::0')
    ]
    assert actual == expected
