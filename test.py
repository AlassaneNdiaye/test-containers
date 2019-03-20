from environments import ContainerTestEnvironment
from utils import nested_get, parse_yaml_file
import argparse
import os
import sys

PADDING = " " * 4


def print_failed_test(test):
    print("FAILED.\nFailing tests:")
    for failed_test in test["evaluation"]["failed"]:
        print("%s%s: %s" % (PADDING, failed_test, test["test"][failed_test]))
    if "file-tests" in test["evaluation"]:
        for failed_test in test["evaluation"]["file-tests"]["failed"]:
            print("%sfile test: %s" % (PADDING, failed_test))


def print_separator():
    print("-" * 80)


def print_test(test):
    print("test: %s\n" % test["test"]["name"])
    print("exit code: %s\n" % test["result"]["exit-code"])
    if test["result"]["output"]:
        print("stdout:\n%s\n" % test["result"]["output"])
    if test["result"]["error"]:
        print("stderr:\n%s\n" % test["result"]["error"])
    if test_passed(test):
        print("PASSED.")
    else:
        print_failed_test(test)


def preprocess_tests(tests):
    for container_tests in tests:
        # replace relative paths with absolute paths for every volume
        volumes = nested_get(container_tests, "container", "arguments", "volumes")
        if volumes:
            for path in volumes.keys():
                abs_path = os.path.abspath(path)
                if not path == abs_path:
                    container_tests["container"]["arguments"]["volumes"][abs_path] = \
                            container_tests["container"]["arguments"]["volumes"][path]
                    container_tests["container"]["arguments"]["volumes"].pop(path)
    return tests


def run_tests(path):
    tests = parse_yaml_file(path)
    tests = preprocess_tests(tests)
    passed_all_tests = True
    print_separator()
    for container_tests in tests:
        for single_test in container_tests["tests"]:
            with ContainerTestEnvironment(container=container_tests["container"]) as environment:
                completed_test = environment.run_test(single_test)
                print_test(completed_test)
                print_separator()
                if not test_passed(completed_test):
                    passed_all_tests = False
    if passed_all_tests:
        sys.exit(0)
    else:
        sys.exit(1)


def test_passed(test):
    if (len(test["evaluation"]["failed"]) > 0 or
            ("file-tests" in test["evaluation"] and len(test["evaluation"]["file-tests"]["failed"]) > 0)):
        return False
    else:
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test containers using yaml files for configuration.")
    parser.add_argument("--config", help="configuration file to get the tests from", required=True)
    args = parser.parse_args()
    run_tests(args.config)
