import os
import re
import sys
from setuptools import setup

# Utility function to read from file.
def fread(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_version():
    VERSIONFILE="curator/_version.py"
    verstrline = fread(VERSIONFILE).strip()
    vsre = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(vsre, verstrline, re.M)
    if mo:
        VERSION = mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
    build_number = os.environ.get('CURATOR_BUILD_NUMBER', None)
    if build_number:
        return VERSION + "b{}".format(build_number)
    return VERSION

def get_install_requires():
    res = ['elasticsearch>=2.3.0,<3.0.0' ]
    res.append('click>=6.3')
    return res

try:
    ### cx_Freeze ###
    from cx_Freeze import setup, Executable
    # Dependencies are automatically detected, but it might need
    # fine tuning.
    buildOptions = dict(packages = [], excludes = [])

    base = 'Console'

    icon = None
    if os.path.exists('Elastic.ico'):
        icon = 'Elastic.ico'

    curator_exe = Executable(
        "run_curator.py",
        base=base,
        targetName = "curator",
        compress = True
    )
    repo_mgr_exe = Executable(
        "run_es_repo_mgr.py",
        base=base,
        targetName = "es_repo_mgr",
        compress = True
    )

    if sys.platform == "win32":
        curator_exe = Executable(
            "run_curator.py",
            base=base,
            targetName = "curator.exe",
            compress = True,
            icon = icon
        )
        repo_mgr_exe = Executable(
            "run_es_repo_mgr.py",
            base=base,
            targetName = "es_repo_mgr.exe",
            compress = True,
            icon = icon
        )
    setup(
        name = "elasticsearch-curator",
        version = get_version(),
        author = "Elastic",
        author_email = "info@elastic.co",
        description = "Tending your Elasticsearch indices",
        long_description=fread('README.rst'),
        url = "http://github.com/elastic/curator",
        download_url = "https://github.com/elastic/curator/tarball/v" + get_version(),
        license = "Apache License, Version 2.0",
        install_requires = get_install_requires(),
        keywords = "elasticsearch time-series indexed index-expiry",
        packages = ["curator", "curator.api", "curator.cli"],
        include_package_data=True,
        entry_points = {
            "console_scripts" : ["curator = curator.curator:main",
                                 "es_repo_mgr = curator.es_repo_mgr:main"]
        },
        classifiers=[
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: Apache Software License",
        ],
        test_suite = "test.run_tests.run_all",
        tests_require = ["mock==1.0.1", "nose", "coverage", "nosexcover"],
        options = {"build_exe" : buildOptions},
        executables = [curator_exe, repo_mgr_exe]
    )
    ### end cx_Freeze ###
except ImportError:
    setup(
        name = "elasticsearch-curator",
        version = get_version(),
        author = "Elastic",
        author_email = "info@elastic.co",
        description = "Tending your Elasticsearch indices",
        long_description=fread('README.rst'),
        url = "http://github.com/elastic/curator",
        download_url = "https://github.com/elastic/curator/tarball/v" + get_version(),
        license = "Apache License, Version 2.0",
        install_requires = get_install_requires(),
        keywords = "elasticsearch time-series indexed index-expiry",
        packages = ["curator", "curator.api", "curator.cli"],
        include_package_data=True,
        entry_points = {
            "console_scripts" : ["curator = curator.curator:main",
                                 "es_repo_mgr = curator.es_repo_mgr:main"]
        },
        classifiers=[
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: Apache Software License",
        ],
        test_suite = "test.run_tests.run_all",
        tests_require = ["mock==1.0.1", "nose", "coverage", "nosexcover"]
    )
