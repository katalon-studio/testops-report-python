from typing import Tuple, Union

from _pytest.config import Config, ExitCode
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.python import Module
from _pytest.reports import CollectReport, TestReport
from testops_commons import ReportLifecycle, TestSuite, generate_unique_value

from testops_pytest import helper
from testops_pytest.helper import TestCaseWrapper, TestSuiteWrapper

STEP_SETUP: str = 'setup'
STEP_CALL: str = 'call'

report_lifecycle: ReportLifecycle = ReportLifecycle()

testsuites: list = []


def pytest_sessionstart(session: Session) -> None:
    """ Start the test """
    report_lifecycle.start_execution()
    report_lifecycle.write_metadata(helper.create_metadata())
    pass


def pytest_collection_modifyitems(session: Session, config: Config, items: list) -> None:
    """ Read all testcases of testsuite """
    build_testsuite(items)
    pass


def pytest_runtest_call(item: Item):
    ts: TestSuiteWrapper = get_testsuite(item.parent)
    if ts.started:
        return
    handle_start_testsuite(ts)


def pytest_runtest_logreport(report: Union[TestReport, CollectReport]) -> None:
    """ Report for testcase/testsuite """
    if isinstance(report, TestReport):
        handle_testreport(report)
    else:
        handle_collectreport(report)


def pytest_sessionfinish(session: Session, exitstatus: Union[int, ExitCode]) -> None:
    """ End the test """
    report_lifecycle.stop_execution()
    report_lifecycle.write_test_results_report()
    report_lifecycle.write_test_suites_report()
    report_lifecycle.write_execution_report()
    report_lifecycle.reset()
    report_lifecycle.upload()
    testsuites.clear()


def build_testsuite(items: list):
    """
    build test hierarchy
    """
    for i in items:
        ts = get_testsuite(i.parent)
        if ts is None:
            ts = create_testsuite(i.parent)
        if i.parent == ts.module:
            ts.testcases.append(TestCaseWrapper(i))


def create_testsuite(module: Module) -> TestSuiteWrapper:
    ts: TestSuiteWrapper = TestSuiteWrapper(module)
    testsuites.append(ts)
    return ts


def get_testsuite(module: Module):
    for ts in testsuites:
        if ts.module == module:
            return ts
    return None


def get_testcase(node_id: str) -> Tuple[TestSuiteWrapper, TestCaseWrapper]:
    for ts in testsuites:
        tc = ts.get_testcase(node_id)
        if tc is not None:
            return ts, tc
    return None


def handle_testreport(report: TestReport) -> None:
    """
    handle test run
    """
    step: str = report.when
    if step == STEP_SETUP:
        if report.skipped:
            handle_testcase_skipped(report)
            return None
        else:
            handle_start_testcase(report)
    if step == STEP_CALL:
        handle_end_testcase(report)
        return None


def handle_collectreport(report: CollectReport) -> None:
    """ Do nothings """
    pass


def handle_start_testcase(report: TestReport) -> None:
    report_lifecycle.start_testcase()
    pass


def handle_end_testcase(report: TestReport) -> None:
    rel = get_testcase(report.nodeid)
    if rel is None:
        return
    tc: TestCaseWrapper = rel[1]
    ts: TestSuiteWrapper = rel[0]
    tc.finished = True
    handle_stop_testcase(ts, tc, report)
    pass


def handle_testcase_skipped(report: TestReport) -> None:
    rel = get_testcase(report.nodeid)
    if rel is None:
        return
    tc: TestCaseWrapper = rel[1]
    ts: TestSuiteWrapper = rel[0]
    tc.skipped = True
    handle_stop_testcase(ts, tc, report)
    pass


def handle_stop_testcase(ts: TestSuiteWrapper, tc: TestCaseWrapper, report: TestReport):
    report_lifecycle.stop_testcase(helper.create_test_result(tc, ts, report))
    if ts.finished:
        handle_end_testsuite(ts)
    pass


def handle_start_testsuite(ts: TestSuiteWrapper):
    uuid = generate_unique_value()
    ts.uuid = uuid
    ts.started = True
    testsuite = TestSuite()
    testsuite.name = ts.module.nodeid
    testsuite.uuid = uuid
    report_lifecycle.start_suite(testsuite, uuid)


def handle_end_testsuite(ts: TestSuiteWrapper):
    if not ts.finished:
        return
    report_lifecycle.stop_test_suite(ts.uuid)
