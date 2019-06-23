[![DOI](https://zenodo.org/badge/193343910.svg)](https://zenodo.org/badge/latestdoi/193343910)

[![Build Status](https://travis-ci.com/scivision/fortran-parse-python.svg?branch=master)](https://travis-ci.com/scivision/fortran-parse-python)
[![Coverage Status](https://coveralls.io/repos/github/scivision/fortran-parse-python/badge.svg?branch=master)](https://coveralls.io/github/scivision/fortran-parse-python?branch=master)

# Simple Fortran parsing in Python

Emphasis here is on compactness and speed for four Fortran statements, not building an AST.
Used in scan stage of Meson build system for the Ninja
[backend](https://github.com/mesonbuild/meson/blob/master/mesonbuild/backend/ninjabackend.py).
If you are interested in more scalable approaches for Fortran parsing see
[Lfortran](https://lfortran.org/)
or
[f18](https://github.com/flang-compiler/f18)

We use case-insensitive regex and scan each Fortran file for syntax concerning statements

* use: including Fortran 2003 `non_intrinsic` [parameter](https://www.ibm.com/support/knowledgecenter/en/SS3KZ4_9.0.0/com.ibm.xlf111.bg.doc/xlflr/use.htm)
* module (ignoring module procedure|function|subroutine and variants)
* submodule including (ancestor:parent)
* include|#include

We tolerate Fortran 90 inline comments, and don't detect commented statements.
This test also checks invalid Fortran syntax.

## Note to Meson dev team

If you wish to incorporate these tests into Meson, let us know, we'd be happy to put them there.