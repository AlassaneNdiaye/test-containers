import os
import sys
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(dir_path, ".."))

import test_containers
import unittest


def process_result(result):
    successes = []
    for success in result.successes:
        successes.append(success.id())

    failures = []
    for failure in result.failures:
        failures.append(failure[0].id())

    return {"successes": successes, "failures": failures}


class Tests(unittest.TestCase):
    def test_exit_code(self):
        result = test_containers.run(os.path.join(dir_path, "test_exit_code.yaml"), exit=False)
        result = process_result(result)
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Good", result["successes"])
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Bad", result["failures"])

    def test_expected_output(self):
        result = test_containers.run(os.path.join(dir_path, "test_expected_output.yaml"), exit=False)
        result = process_result(result)
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Good", result["successes"])
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Bad", result["failures"])

    def test_excluded_output(self):
        result = test_containers.run(os.path.join(dir_path, "test_excluded_output.yaml"), exit=False)
        result = process_result(result)
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Good", result["successes"])
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Bad", result["failures"])

    def test_expected_error(self):
        result = test_containers.run(os.path.join(dir_path, "test_expected_error.yaml"), exit=False)
        result = process_result(result)
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Good", result["successes"])
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Bad", result["failures"])

    def test_excluded_error(self):
        result = test_containers.run(os.path.join(dir_path, "test_excluded_error.yaml"), exit=False)
        result = process_result(result)
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Good", result["successes"])
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Bad", result["failures"])

    def test_file_exists(self):
        result = test_containers.run(os.path.join(dir_path, "test_file_exists.yaml"), exit=False)
        result = process_result(result)
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Good", result["successes"])
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Bad", result["failures"])

    def test_file_expected_content(self):
        result = test_containers.run(os.path.join(dir_path, "test_file_expected_content.yaml"), exit=False)
        result = process_result(result)
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Good", result["successes"])
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Bad", result["failures"])

    def test_file_excluded_content(self):
        result = test_containers.run(os.path.join(dir_path, "test_file_excluded_content.yaml"), exit=False)
        result = process_result(result)
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Good", result["successes"])
        self.assertIn("test_containers.tests.Tests.test_httpd:2.4_Bad", result["failures"])


if __name__ == '__main__':
    unittest.main()
