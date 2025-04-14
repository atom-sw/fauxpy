from typing import List, Optional

from fauxpy.session_lib.target_tsts import TargetFailingTests
from fauxpy.session_lib.targeted_failing_tst import TargetedFailingTst


def get_targeted_failing_test_list_legacy(
    targeted_failing_test_list: List[TargetedFailingTst],
) -> Optional[TargetFailingTests]:
    if len(targeted_failing_test_list) == 0:
        return None
    legacy_targeted_failing_test_list = [
        x.get_relative_test_name() for x in targeted_failing_test_list
    ]

    return TargetFailingTests(legacy_targeted_failing_test_list)
