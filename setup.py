# Author: Kit Chambers
# Contact: kit.chambers@motionsignaltechnologies.com
# 
# Motion Signal Technologies Ltd.
# All rights reserved
# 
# The contents of this file are considered proprietary and usage or
# reproduction without prior authorization is strictly prohibited.
'''
ObsLn - Provides some of the basic functionality from ObsPy without many of the dependencies and size. For full ObsPy functionality please see the ObsPy project on GitHub [here](https://github.com/obspy)

'''

try:
    import setuptools
except ImportError:
    pass

try:
    import numpy 
except ImportError:
    msg = ("No module named numpy. "
           "Please install numpy first, it is needed before installing ObsPy.")
    raise ImportError(msg)

import fnmatch
import glob
import inspect
import os
import sys
import platform
from distutils.util import change_root

from numpy.distutils.core import DistutilsSetupError, setup
from numpy.distutils.ccompiler import get_default_compiler
from numpy.distutils.command.build import build
from numpy.distutils.command.install import install
from numpy.distutils.exec_command import exec_command, find_executable
from numpy.distutils.misc_util import Configuration

SETUP_DIRECTORY = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))

UTIL_PATH = os.path.join(SETUP_DIRECTORY, "obsln", "core", "util")
sys.path.insert(0, UTIL_PATH)
#from version import get_git_version  # @UnresolvedImport
from libnames import _get_lib_name  # @UnresolvedImport
sys.path.pop(0)

LOCAL_PATH = os.path.join(SETUP_DIRECTORY, "setup.py")
DOCSTRING = __doc__.split("\n")

INSTALL_REQUIRES=[]

EXTRAS_REQUIRE={}

# check for MSVC
if platform.system() == "Windows" and (
        'msvc' in sys.argv or
        '-c' not in sys.argv and
        get_default_compiler() == 'msvc'):
    IS_MSVC = True
else:
    IS_MSVC = False

# Use system libraries? Set later...
EXTERNAL_EVALRESP = False
EXTERNAL_LIBMSEED = False

# helper function for collecting export symbols from .def files
def export_symbols(*path):
    lines = open(os.path.join(*path), 'r').readlines()[2:]
    return [s.strip() for s in lines if s.strip() != '']

def find_packages():
    """
    Simple function to find all modules under the current folder.
    """
    modules = []
    for dirpath, _, filenames in os.walk(os.path.join(SETUP_DIRECTORY,
                                                      "obsln")):
        if "__init__.py" in filenames:
            modules.append(os.path.relpath(dirpath, SETUP_DIRECTORY))
    return [_i.replace(os.sep, ".") for _i in modules]

# adds --with-system-libs command-line option if possible

def add_features():
    if 'setuptools' not in sys.modules or not hasattr(setuptools, 'Feature'):
        return {}

    class ExternalLibFeature(setuptools.Feature):
        def __init__(self, *args, **kwargs):
            self.name = kwargs['name']
            setuptools.Feature.__init__(self, *args, **kwargs)

        def include_in(self, dist):
            globals()[self.name] = True

        def exclude_from(self, dist):
            globals()[self.name] = False

    return {
        'system-libs': setuptools.Feature(
            'use of system C libraries',
            standard=False,
            require_features=('system-evalresp', 'system-libmseed')
        ),
        'system-evalresp': ExternalLibFeature(
            'use of system evalresp library',
            standard=False,
            name='EXTERNAL_EVALRESP'
        ),
        'system-libmseed': ExternalLibFeature(
            'use of system libmseed library',
            standard=False,
            name='EXTERNAL_LIBMSEED'
        )
    }

def add_data_files(config):
    """
    Recursively include all non python files
    """
    # python files are included per default, we only include data files
    # here
    EXCLUDE_WILDCARDS = ['*.py', '*.pyc', '*.pyo', '*.pdf', '.git*']
    EXCLUDE_DIRS = ['src', '__pycache__']
    common_prefix = SETUP_DIRECTORY + os.path.sep
    for root, dirs, files in os.walk(os.path.join(SETUP_DIRECTORY, 'obsln')):
        root = root.replace(common_prefix, '')
        for name in files:
            if any(fnmatch.fnmatch(name, w) for w in EXCLUDE_WILDCARDS):
                continue
            config.add_data_files(os.path.join(root, name))
        for folder in EXCLUDE_DIRS:
            if folder in dirs:
                dirs.remove(folder)

    # Force include the contents of some directories.
    FORCE_INCLUDE_DIRS = [
        os.path.join(SETUP_DIRECTORY, 'obsln', 'io', 'mseed', 'src',
                     'libmseed', 'test')]

    for folder in FORCE_INCLUDE_DIRS:
        for root, _, files in os.walk(folder):
            for filename in files:
                config.add_data_files(
                    os.path.relpath(os.path.join(root, filename),
                                    SETUP_DIRECTORY))

def configuration(parent_package="", top_path=None):
    """
    Config function mainly used to compile C code.
    """
    config = Configuration("", parent_package, top_path)

    # GSE2
#     path = os.path.join("obsln", "io", "gse2", "src", "GSE_UTI")
#     files = [os.path.join(path, "gse_functions.c")]
#     # compiler specific options
#     kwargs = {}
#     if IS_MSVC:
#         # get export symbols
#         kwargs['export_symbols'] = export_symbols(path, 'gse_functions.def')
#     config.add_extension(_get_lib_name("gse2", add_extension_suffix=False),
#                          files, **kwargs)

    # LIBMSEED
#     path = os.path.join("obsln", "io", "mseed", "src")
#     files = [os.path.join(path, "obspy-readbuffer.c")]
#     if not EXTERNAL_LIBMSEED:
#         files += glob.glob(os.path.join(path, "libmseed", "*.c"))
#     # compiler specific options
#     kwargs = {}
#     if IS_MSVC:
#         # needed by libmseed lmplatform.h
#         kwargs['define_macros'] = [('WIN32', '1')]
#         # get export symbols
#         kwargs['export_symbols'] = \
#             export_symbols(path, 'libmseed', 'libmseed.def')
#         kwargs['export_symbols'] += \
#             export_symbols(path, 'obspy-readbuffer.def')
#     if EXTERNAL_LIBMSEED:
#         kwargs['libraries'] = ['mseed']
#     config.add_extension(_get_lib_name("mseed", add_extension_suffix=False),
#                          files, **kwargs)

    # SEGY
    path = os.path.join("obsln", "io", "segy", "src")
    files = [os.path.join(path, "ibm2ieee.c")]
    # compiler specific options
    kwargs = {}
    if IS_MSVC:
        # get export symbols
        kwargs['export_symbols'] = export_symbols(path, 'libsegy.def')
    config.add_extension(_get_lib_name("segy", add_extension_suffix=False),
                         files, **kwargs)

    # SIGNAL
#     path = os.path.join("obspy", "signal", "src")
#     files = glob.glob(os.path.join(path, "*.c"))
#     # compiler specific options
#     kwargs = {}
#     if IS_MSVC:
#         # get export symbols
#         kwargs['export_symbols'] = export_symbols(path, 'libsignal.def')
#     config.add_extension(_get_lib_name("signal", add_extension_suffix=False),
#                          files, **kwargs)

    # EVALRESP
#     path = os.path.join("obspy", "signal", "src")
#     if EXTERNAL_EVALRESP:
#         files = glob.glob(os.path.join(path, "evalresp", "_obspy*.c"))
#     else:
#         files = glob.glob(os.path.join(path, "evalresp", "*.c"))
#     # compiler specific options
#     kwargs = {}
#     if IS_MSVC:
#         # needed by evalresp evresp.h
#         kwargs['define_macros'] = [('WIN32', '1')]
#         # get export symbols
#         kwargs['export_symbols'] = export_symbols(path, 'libevresp.def')
#     if EXTERNAL_EVALRESP:
#         kwargs['libraries'] = ['evresp']
#     config.add_extension(_get_lib_name("evresp", add_extension_suffix=False),
#                          files, **kwargs)

    # TAU
#     path = os.path.join("obsln", "taup", "src")
#     files = [os.path.join(path, "inner_tau_loops.c")]
#     # compiler specific options
#     kwargs = {}
#     if IS_MSVC:
#         # get export symbols
#         kwargs['export_symbols'] = export_symbols(path, 'libtau.def')
#     config.add_extension(_get_lib_name("tau", add_extension_suffix=False),
#                          files, **kwargs)

    add_data_files(config)

    return config

def setupPackage():
    
    setup(
        name='obsln',
        description=DOCSTRING[1],
        long_description="\n".join(DOCSTRING[3:]),
        author='Bateared Collie',
        author_email='batearedcollie@gmail.com',
        packages=find_packages(),
        namespace_packages=[],
        zip_safe=False,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        features=add_features(),
#         # this is needed for "easy_install obspy==dev"
#         download_url=("https://github.com/obspy/obspy/zipball/master"
#                       "#egg=obspy=dev"),
#         include_package_data=True,
#         entry_points=ENTRY_POINTS,
#         ext_package='obspy.lib',
#         cmdclass={
#             'build_man': Help2ManBuild,
#             'install_man': Help2ManInstall
#         },
        configuration=configuration
        )  


if __name__ == '__main__':
    # clean --all does not remove extensions automatically
    if 'clean' in sys.argv and '--all' in sys.argv:
        import shutil
        # delete complete build directory
        path = os.path.join(SETUP_DIRECTORY, 'build')
        try:
            shutil.rmtree(path)
        except Exception:
            pass
        # delete all shared libs from lib directory
        path = os.path.join(SETUP_DIRECTORY, 'obspy', 'lib')
        for filename in glob.glob(path + os.sep + '*.pyd'):
            try:
                os.remove(filename)
            except Exception:
                pass
        for filename in glob.glob(path + os.sep + '*.so'):
            try:
                os.remove(filename)
            except Exception:
                pass
        path = os.path.join(SETUP_DIRECTORY, 'obspy', 'taup', 'data', 'models')
        try:
            shutil.rmtree(path)
        except Exception:
            pass
    else:
        setupPackage()