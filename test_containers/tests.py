from test_containers.utils import execute_command
from test_containers.environments import ContainerTestEnvironment
import os
import unittest


class ContainerTest:
    def __init__(self, container, test):
        self.container = container
        self.test = test
        self.container_name = self.container["name"].replace("-", "_")
        self.test_name = self.test["name"].replace("-", "_").replace(" ", "_")
        self.test_case_object = None
        self.test_result = None

    def __evaluate_result(self):
        if "exit-code" in self.test:
            self.test_case_object.assertEqual(self.test["exit-code"], self.test_result["exit-code"])

        if "expected-output" in self.test:
            self.test_case_object.assertRegexpMatches(self.test_result["output"], self.test["expected-output"])

        if "excluded-output" in self.test:
            self.test_case_object.assertNotRegexpMatches(self.test_result["output"], self.test["excluded-output"])

        if "expected-error" in self.test:
            self.test_case_object.assertRegexpMatches(self.test_result["error"], self.test["expected-error"])

        if "excluded-error" in self.test:
            self.test_case_object.assertNotRegexpMatches(self.test_result["error"], self.test["excluded-error"])

        if "files" in self.test:
            for file_tests in self.test["files"]:
                if "exists" in file_tests:
                    self.test_case_object.assertEqual(os.path.exists(file_tests["path"]), file_tests["exists"])
                if "expected-content" in file_tests or "excluded-content" in file_tests:
                    with open(file_tests["path"]) as f:
                        file_content = f.read()
                    if "expected-content" in file_tests:
                        self.test_case_object.assertRegexpMatches(file_content, file_tests["expected-content"])
                    if "excluded-content" in file_tests:
                        self.test_case_object.assertNotRegexpMatches(file_content, file_tests["excluded-content"])

    def __expand_environment_variables(self):
        if "environment-variables" not in self.test:
            return

        environment_variables = self.test["environment-variables"]
        for variable, definition in environment_variables.items():
            environment_variables[variable] = execute_command(definition)["output"]

        for key in ["command", "expected-output", "excluded-output", "expected-error", "excluded-error"]:
            if key not in self.test:
                continue
            for variable, value in environment_variables.items():
                self.test[key] = self.test[key].replace("${%s}" % variable, value)

    def run_test(self, test_case_object):
        self.test_case_object = test_case_object
        with ContainerTestEnvironment(container=self.container):
            self.__expand_environment_variables()
            self.test_result = execute_command(self.test["command"])
            self.__evaluate_result()


class Tests(unittest.TestCase):
    @staticmethod
    def generate_tests(tests):
        def generate_test_method(test):
            def generated_test_method(self):
                test.run_test(self)
            return generated_test_method

        for test in tests:
            test_name = "test_%s_%s" % (test.container_name, test.test_name)
            setattr(Tests, test_name, generate_test_method(test))
