import docker
import os
import shutil
import sys
import tempfile
import time

docker_client = docker.from_env()


class TestEnvironment:
    def __init__(self):
        pass

    def __enter__(self):
        self.previous_working_dir = os.getcwd()
        self.working_dir = tempfile.mkdtemp()
        os.chdir(self.working_dir)

    def __exit__(self, type, value, traceback):
        os.chdir(self.previous_working_dir)
        shutil.rmtree(self.working_dir)


class ContainerTestEnvironment(TestEnvironment):
    def __init__(self, container):
        super().__init__()
        self.container = container

    def __enter__(self):
        super().__enter__()
        self.docker_container = docker_client.containers.run(self.container["name"], detach=True,
                                                             **self.container["arguments"])
        self.__wait_container_ready()

    def __exit__(self, type, value, traceback):
        self.docker_container.stop()
        super().__exit__(type, value, traceback)

    def __wait_container_ready(self):
        inspection = docker_client.api.inspect_container(self.docker_container.id)
        if "Health" in inspection["State"]:
            print("\nWaiting for container to be healthy... ", end="", file=sys.stderr, flush=True)
            while inspection["State"]["Health"]["Status"] != "healthy":
                time.sleep(2)
                inspection = docker_client.api.inspect_container(self.docker_container.id)
            print("Container healthy.", file=sys.stderr)
        else:
            time.sleep(2)
