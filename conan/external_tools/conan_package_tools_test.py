import platform
import sys

import nose

from conan.test_regression.utils.base_exe import BaseExeTest, run
from conans import tools


class ConanPackageToolsTest(BaseExeTest):

    def test_package_tools(self):
        if sys.version_info[0:2] == (3, 4):
            raise nose.SkipTest('Py 3.4 fails with python setup.py install for some reason')

        run("pip install conan_package_tools --no-dependencies")  # Install latest

        # To try build bzip2 with package tools
        librepo = "https://github.com/lasote/conan-bzip2.git"
        branch = "release/1.0.6"
        run("git clone --depth 1 %s -b %s ." % (librepo, branch))
        env = {"CONAN_USERNAME": "conan",
               "CONAN_CHANNEL": "testing",
               "CONAN_DOCKER_USE_SUDO": "0",
               "CONAN_REFERENCE": "bzip2/1.0.6"}

        if platform.system() == "Windows":
            env["CONAN_VISUAL_VERSIONS"] = "15"
        elif platform.system() == "Linux":
            env["CONAN_GCC_VERSIONS"] = "5"
            # env["CONAN_USE_DOCKER"] = "1" docker command not found, check why and enable again
        elif platform.system() == "Darwin":
            env["CONAN_APPLE_CLANG_VERSIONS"] = "9.0"

        with tools.environment_append(env):
            run("conan --version")
            run("python build.py")
