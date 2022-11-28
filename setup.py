import codecs
import os
import subprocess
import sys
from shutil import rmtree

from setuptools import setup, find_packages, Command

here = os.path.abspath(os.path.dirname(__file__))

__version__ = None
exec(open(f"{here}/acho_sdk/version.py").read())

long_description = ""
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as readme:
    long_description = readme.read()

validate_dependencies = [
    "gevent_socketio>=0.3.6",
    "requests>=2.25.1"
]

class BaseCommand(Command):
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _run(self, s, command):
        try:
            self.status(s + "\n" + " ".join(command))
            subprocess.check_call(command)
        except subprocess.CalledProcessError as error:
            sys.exit(error.returncode)


class UploadCommand(BaseCommand):
    """Support setup.py upload. Thanks @kennethreitz!"""

    description = "Build and publish the package."

    def run(self):
        self._run(
            "Installing upload dependencies ...",
            [sys.executable, "-m", "pip", "install", "wheel"],
        )
        try:
            self.status("Removing previous builds ...")
            rmtree(os.path.join(here, "dist"))
            rmtree(os.path.join(here, "build"))
        except OSError:
            pass

        self._run(
            "Building Source and Wheel (universal) distribution ...",
            [sys.executable, "setup.py", "sdist", "bdist_wheel", "--universal"],
        )
        self._run(
            "Installing Twine dependency ...",
            [sys.executable, "-m", "pip", "install", "twine"],
        )
        self._run(
            "Uploading the package to PyPI via Twine ...",
            [sys.executable, "-m", "twine", "upload", "dist/*"],
        )


setup(
    name="acho_sdk",
    version=__version__,
    description="The Acho SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/unibit_web/acho-py/src/master/",
    author="Acho Software Inc.",
    author_email="dev@acho.io",
    python_requires=">=3.6.0",
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
        "Topic :: System :: Networking",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="acho serverless faas",
    install_requires=[],
    extras_require={
        # pip install -e ".[testing]"
        "testing": validate_dependencies,
    },
    cmdclass={
        "upload": UploadCommand,
    },
)