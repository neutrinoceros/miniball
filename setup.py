__author__ = "Konstantin Weddige"
import sysconfig
from setuptools import setup, Extension
from wheel.bdist_wheel import bdist_wheel


MINIMAL_PYTHON_VERSION = (3, 6)

# build with Py_LIMITED_API unless in freethreading build (which does not currently
# support the limited API in py313t)
USE_PY_LIMITED_API = not sysconfig.get_config_var("Py_GIL_DISABLED")
define_macros = []
if USE_PY_LIMITED_API:
    define_macros.append(("Py_LIMITED_API", "0x030600f0"))

def _get_python_requires():
    return f">={'.'.join(str(_) for _ in MINIMAL_PYTHON_VERSION)}"

def _get_cpython_tag():
    return f"cp{''.join(str(_) for _ in MINIMAL_PYTHON_VERSION[:2])}"

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        if python.startswith("cp") and USE_PY_LIMITED_API:
            # on CPython, our wheels are abi3
            # and compatible down to MINIMAL_PYTHON_VERSION
            return _get_cpython_tag(), "abi3", plat

        return python, abi, plat



setup(
    name="MiniballCpp",
    version="0.2.3",
    description="Smallest Enclosing Balls of Points",
    long_description=long_description,
    author="Bernd Gärtner, Konstantin Weddige",
    url="https://github.com/weddige/miniball",
    packages=[
        "miniball",
    ],
    package_data={"miniball": ["py.typed"]},
    ext_modules=[
        Extension(
            "miniball.bindings",
            ["src/miniballmodule.cpp"],
            include_dirs=["src"],
            language="c++",
            define_macros=define_macros,
            py_limited_api=USE_PY_LIMITED_API,
        ),
    ],
    python_requires=_get_python_requires(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    cmdclass={"bdist_wheel": bdist_wheel_abi3},
)
