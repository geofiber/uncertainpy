import os
import sys
import subprocess
from uncertainpy.utils import create_logger


folder = os.path.dirname(os.path.realpath(__file__))
docker_test_dir = os.path.join(folder, "figures_docker")

logger = create_logger("error")


def system(cmds):
    """Run system command cmd using subprocess module."""
    if isinstance(cmds, str):
        cmds = [cmds]

    output = None
    if isinstance(cmds, (tuple, list)):
        for cmd in cmds:
            logger.debug(cmd)

            try:
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                if output:
                    logger.info(output.decode('utf-8'))


            except subprocess.CalledProcessError as e:
                if e.returncode != 2:
                    msg = "Command failed: \n {} \n  \n Return code: {} ".format(cmd, e.returncode)
                    logger.error(msg)
                    logger.error(e.output.decode("utf-8"))

                    sys.exit(1)

    else:
        raise TypeError("cmd argument is wrong type")

    return output



def generate_docker_images():
    system("docker build {} -t generate_test_plots".format(os.path.join(folder, "..")))
    docker_id = system("docker create generate_test_plots").strip()
    system("docker start {}".format(docker_id))
    # system("docker exec {} python uncertainpy/tests/generate_test_data.py".format(docker_id))
    system("docker exec {} python tests/generate_test_plots.py".format(docker_id))
    system("docker cp {}:/home/docker/uncertainpy/tests/figures/. {}/.".format(docker_id, docker_test_dir))
    system("docker stop {}".format(docker_id))
    system("docker rm -v {}".format(docker_id))
    system("docker rmi generate_test_plots")



if __name__ == "__main__":
    generate_docker_images()