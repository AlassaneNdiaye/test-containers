from test_containers.__main__ import run
import os
import unittest
import warnings

dir_path = os.path.dirname(os.path.abspath(__file__))


def process_result(result):
    successes = []
    for success in result.successes:
        successes.append(success.id())

    failures = []
    for failure in result.failures:
        failures.append(failure[0].id())

    return {"successes": successes, "failures": failures}


class Tests(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    def test_exit_code(self):
        result = run(os.path.join(dir_path, "test_exit_code.yaml"), exit=False)
        result = process_result(result)
        good_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_internal"
        ]
        bad_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_internal"
        ]
        for good_test in good_tests:
            self.assertIn(good_test, result["successes"])
        for bad_test in bad_tests:
            self.assertIn(bad_test, result["failures"])

    def test_expected_output(self):
        result = run(os.path.join(dir_path, "test_expected_output.yaml"), exit=False)
        result = process_result(result)
        good_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_internal"
        ]
        bad_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_internal"
        ]
        for good_test in good_tests:
            self.assertIn(good_test, result["successes"])
        for bad_test in bad_tests:
            self.assertIn(bad_test, result["failures"])

    def test_excluded_output(self):
        result = run(os.path.join(dir_path, "test_excluded_output.yaml"), exit=False)
        result = process_result(result)
        good_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_internal"
        ]
        bad_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_internal"
        ]
        for good_test in good_tests:
            self.assertIn(good_test, result["successes"])
        for bad_test in bad_tests:
            self.assertIn(bad_test, result["failures"])

    def test_expected_error(self):
        result = run(os.path.join(dir_path, "test_expected_error.yaml"), exit=False)
        result = process_result(result)
        good_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_internal"
        ]
        bad_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_internal"
        ]
        for good_test in good_tests:
            self.assertIn(good_test, result["successes"])
        for bad_test in bad_tests:
            self.assertIn(bad_test, result["failures"])

    def test_excluded_error(self):
        result = run(os.path.join(dir_path, "test_excluded_error.yaml"), exit=False)
        result = process_result(result)
        good_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_internal"
        ]
        bad_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_internal"
        ]
        for good_test in good_tests:
            self.assertIn(good_test, result["successes"])
        for bad_test in bad_tests:
            self.assertIn(bad_test, result["failures"])

    def test_file_exists(self):
        result = run(os.path.join(dir_path, "test_file_exists.yaml"), exit=False)
        result = process_result(result)
        good_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_missing_path_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_missing_path_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_missing_path_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_missing_path_internal"
        ]
        bad_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_missing_path_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_missing_path_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_missing_path_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_missing_path_internal"
        ]
        for good_test in good_tests:
            self.assertIn(good_test, result["successes"])
        for bad_test in bad_tests:
            self.assertIn(bad_test, result["failures"])

    def test_file_expected_content(self):
        result = run(os.path.join(dir_path, "test_file_expected_content.yaml"), exit=False)
        result = process_result(result)
        good_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_internal"
        ]
        bad_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_path_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_path_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_path_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_path_internal"
        ]
        for good_test in good_tests:
            self.assertIn(good_test, result["successes"])
        for bad_test in bad_tests:
            self.assertIn(bad_test, result["failures"])

    def test_file_excluded_content(self):
        result = run(os.path.join(dir_path, "test_file_excluded_content.yaml"), exit=False)
        result = process_result(result)
        good_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_good_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_good_internal"
        ]
        bad_tests = [
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_path_external",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_container_bad_path_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_path_external",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_internal",
            "test_containers.__main__.UnitTestGenerator.test_test_pod_bad_path_internal"
        ]
        for good_test in good_tests:
            self.assertIn(good_test, result["successes"])
        for bad_test in bad_tests:
            self.assertIn(bad_test, result["failures"])


if __name__ == "__main__":
    unittest.main()
