from _pytest.python import Function, Module
from _pytest.reports import TestReport
from testops_commons.katalon.testops.commons.helper.helper import generate_unique_value
from testops_commons.katalon.testops.commons.model.models import Metadata, TestResult, Status, Error


class TestCaseWrapper(object):
    module: Function
    finished: bool
    skipped: bool
    started: bool

    def __init__(self, module: Function, finished: bool = False, skipped: bool = False, started: bool = False):
        self.module = module
        self.finished = finished
        self.skipped = skipped
        self.started = started


class TestSuiteWrapper(object):
    module: Module
    started: bool
    testcases: list[TestCaseWrapper]
    uuid: str

    def __init__(self, module: Module):
        self.module = module
        self.testcases = []
        self.started = False
        self.uuid = None

    def add_testcase(self, testcase: TestCaseWrapper):
        self.testcases.append(testcase)

    @property
    def finished(self) -> bool:
        for tc in self.testcases:
            if not (tc.finished or tc.skipped):
                return False
        return True

    def get_testcase(self, node_id: str) -> TestCaseWrapper:
        for tc in self.testcases:
            if tc.module.nodeid == node_id:
                return tc
        return None


def create_metadata():
    return Metadata("pytest", "python", "3.9", "", "")


def create_test_result(tc: TestCaseWrapper, ts: TestSuiteWrapper, report: TestReport):
    uuid: str = generate_unique_value()
    result: TestResult = TestResult()
    result.uuid = uuid
    result.status = _get_status(report)
    result.name = tc.module.nodeid
    result.suite_name = ts.module.nodeid
    result.parent_uuid = ts.uuid

    if result.status == Status.SKIPPED:
        result.errors.append(Error(_get_skip_message(report)))
    if (result.status == Status.FAILED) or (result.status == Status.ERROR):
        result.errors.append(Error(report.longreprtext, report.longreprtext))
    return result


def _get_skip_message(report: TestReport):
    return report.longrepr[2][9:]


def _get_status(report: TestReport):
    if report.passed:
        return Status.PASSED
    if report.failed:
        return Status.FAILED
    if report.skipped:
        return Status.SKIPPED
    return Status.INCOMPLETE
