import docker
import os
import re
import shutil
import subprocess
import tempfile

docker_client = docker.from_env()


class ContainerTestEnvironment:
    def __init__(self, container):
        self.dir_path = tempfile.mkdtemp()
        self.previous_working_dir = os.getcwd()
        os.chdir(self.dir_path)
        self.docker_container = docker_client.containers.run(container["name"], detach=True, **container["arguments"])

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.docker_container.stop()
        os.chdir(self.previous_working_dir)
        shutil.rmtree(self.dir_path)

    def evaluate_environment_variables(self, test):
        if "environment-variables" not in test:
            return
        environment_variables = test["environment-variables"]
        for variable in environment_variables.keys():
            value = self.execute_command(environment_variables[variable])["output"]
            environment_variables[variable] = value

    def evaluate_result(self, test, result):
        evaluation = {"passed": [], "failed": []}

        if "exit-code" in test:
            if test["exit-code"] == result["exit-code"]:
                evaluation["passed"].append("exit-code")
            else:
                evaluation["failed"].append("exit-code")

        if "expected-output" in test:
            if re.search(test["expected-output"], result["output"]) is not None:
                evaluation["passed"].append("expected-output")
            else:
                evaluation["failed"].append("expected-output")

        if "excluded-output" in test:
            if re.search(test["excluded-output"], result["output"]) is None:
                evaluation["passed"].append("excluded-output")
            else:
                evaluation["failed"].append("excluded-output")

        if "expected-error" in test:
            if re.search(test["expected-error"], result["error"]) is not None:
                evaluation["passed"].append("expected-error")
            else:
                evaluation["failed"].append("expected-error")

        if "excluded-error" in test:
            if re.search(test["excluded-error"], result["error"]) is None:
                evaluation["passed"].append("excluded-error")
            else:
                evaluation["failed"].append("excluded-error")

        if "files" in test:
            evaluation["file-tests"] = {"passed": [], "failed": []}
            for file_tests in test["files"]:
                passed = True
                if "exists" in file_tests:
                    if os.path.exists(file_tests["path"]) != file_tests["exists"]:
                        passed = False
                if "expected-content" in file_tests or "excluded-content" in file_tests:
                    with open(file_tests["path"]) as f:
                        file_content = f.read()
                    if "expected-content" in file_tests:
                        if re.search(file_tests["expected-content"], file_content) is None:
                            passed = False
                    if "excluded-content" in file_tests:
                        if re.search(file_tests["excluded-content"], file_content) is not None:
                            passed = False
                if passed:
                    evaluation["file-tests"]["passed"].append(file_tests["path"])
                else:
                    evaluation["file-tests"]["failed"].append(file_tests["path"])

        return evaluation

    def execute_command(self, command):
        completed_process = subprocess.run(command, shell=True, executable="/bin/bash",
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = dict()
        result["exit-code"] = completed_process.returncode
        result["output"] = completed_process.stdout.decode("utf-8").strip()
        result["error"] = completed_process.stderr.decode("utf-8").strip()
        return result

    def expand_environment_variables(self, test):
        if "environment-variables" not in test:
            return
        environment_variables = test["environment-variables"]
        for key in ["command", "expected-output", "excluded-output", "expected-error", "excluded-error"]:
            if key not in test:
                continue
            for variable, value in environment_variables.items():
                test[key] = test[key].replace("${%s}" % variable, value)

    def run_test(self, test):
        self.evaluate_environment_variables(test)
        self.expand_environment_variables(test)
        result = self.execute_command(test["command"])
        evaluation = self.evaluate_result(test=test, result=result)
        return {"evaluation": evaluation, "result": result, "test": test}
