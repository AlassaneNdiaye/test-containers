from results import TextTestResultWithSuccesses
from tests import ContainerTest, ContainerTestCase
from utils import nested_get, parse_yaml_file
import argparse
import os
import sys
import unittest

HELP_TEXT = "Test containers using yaml files for configuration."


def expand_paths(test_dict):
    for container_test_dict in test_dict:
        # replace relative paths with absolute paths for every volume
        volumes = nested_get(container_test_dict, "container", "arguments", "volumes")
        if volumes:
            for path in volumes.keys():
                abs_path = os.path.abspath(path)
                if not path == abs_path:
                    container_test_dict["container"]["arguments"]["volumes"][abs_path] = \
                            container_test_dict["container"]["arguments"]["volumes"][path]
                    container_test_dict["container"]["arguments"]["volumes"].pop(path)


def get_tests(test_dict):
    tests = []
    for container_test_dict in test_dict:
        for single_test_dict in container_test_dict["tests"]:
            test = ContainerTest(container=container_test_dict["container"], test=single_test_dict)
            tests.append(test)
    return tests


def preprocess_test_dict(test_dict):
    expand_paths(test_dict)


def run_tests(path, exit=True):
    test_dict = parse_yaml_file(path)
    preprocess_test_dict(test_dict)
    tests = get_tests(test_dict)
    ContainerTestCase.generate_tests(tests)
    tests = unittest.defaultTestLoader.loadTestsFromTestCase(ContainerTestCase)
    suite = unittest.TestSuite()
    suite.addTests(tests)
    result = unittest.TextTestRunner(resultclass=TextTestResultWithSuccesses).run(suite)
    if exit:
        if result.wasSuccessful():
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=HELP_TEXT)
    parser.add_argument("--config", help="configuration file to get the tests from", required=True)
    args = parser.parse_args()
    run_tests(args.config)
