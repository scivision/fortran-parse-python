#!/usr/bin/env python
"""
Regex used for Fortran statements in Meson Ninja backend

https://github.com/mesonbuild/meson/blob/master/mesonbuild/backend/ninjabackend.py

Meson 0.51.0 regex are broken by:

inc: doesn't allow leading space
"""
import pytest
import re


m0510 = {'inc': r"#?include\s*['\"](\w+\.\w+)['\"]",
         'mod': r"\s*\bmodule\b\s+(?!procedure)(\w+)",
         'submod': r"\s*submodule\s*\((\w+:?\w+)\)\s*(\w+)",
         'use': r"\s*use,?\s*(?:non_intrinsic)?\s*(?:::)?\s*(\w+)"}

mnext = {'inc': r"^\s*#?include\s*['\"](\w+\.\w+)['\"]",
         'mod': r"^\s*\bmodule\b\s+(\w+)\s*(?:!+.*)*$",
         'submod': r"^\s*\bsubmodule\b\s*\((\w+:?\w+)\)\s*(\w+)",
         'use': r"^\s*use,?\s*(?:non_intrinsic)?\s*(?:::)?\s*(\w+)"}

ids = ['inc', 'mod', 'submod', 'use']


@pytest.mark.parametrize('pind,code,gind',
                         [('inc', '! include "fruit.f90"', 1),
                          ('mod', '! module fruit', 1),
                          ('submod', '! submodule (parent) fruit', 2),
                          ('use', '! use fruit', 1)])
def test_commented(pind, code, gind):
    """
    verifies that we don't detect commented statements
    """
    pat = mnext[pind]
    cpat = re.compile(pat, re.IGNORECASE)
    match = cpat.match(code)
    # name = match.group(gind).lower()

    assert match is None


@pytest.mark.parametrize('pind,code,gind',
                         [('inc', 'go include "fruit.f90"', 1),
                          ('mod', 'go module fruit', 1),
                          ('submod', 'go submodule (parent) fruit', 2),
                          ('use', 'go use fruit', 1)])
def test_bad_syntax(pind, code, gind):
    """
    verifies that we don't detect bad syntax
    """
    pat = mnext[pind]
    cpat = re.compile(pat, re.IGNORECASE)
    match = cpat.match(code)
    # name = match.group(gind).lower()

    assert match is None


@pytest.mark.parametrize('pind,code,gind',
                         [('inc', ' include "pear.f90"', 1),
                          ('mod', ' module fruit', 1),
                          ('submod', ' submodule (parent) fruit', 2),
                          ('use', ' use fruit', 1)])
def test_leading_space(pind, code, gind):
    """
    verified that leasding spaces are OK
    """
    pat = mnext[pind]
    cpat = re.compile(pat, re.IGNORECASE)
    match = cpat.match(code)
    name = match.group(gind).lower()

    assert name in ('fruit', 'pear.f90')


@pytest.mark.parametrize('pind,code,gind',
                         [('inc', ' include "pear.f90"  ! hi', 1),
                          ('mod', ' module fruit  ! hi', 1),
                          ('submod', ' submodule (parent) fruit  ! hi', 2),
                          ('use', ' use fruit  ! hi', 1)])
def test_trailing_comment(pind, code, gind):
    """
    verifies that inline trailing comment are OK
    """
    pat = mnext[pind]
    cpat = re.compile(pat, re.IGNORECASE)
    match = cpat.match(code)
    name = match.group(gind).lower()

    assert name in ('fruit', 'pear.f90')


@pytest.mark.parametrize('code',
                         ['submodule (parent) foo',
                          'submodule(parent) foo',
                          'submodule (ancestor:parent) foo'])
def test_submodule(code):
    """
    verifies that submodule syntax is OK
    """
    pat = mnext['submod']
    cpat = re.compile(pat, re.IGNORECASE)
    match = cpat.match(code)
    ancestors = match.group(1).lower()
    name = match.group(2).lower()

    assert 'parent' in ancestors
    assert name == 'foo'


@pytest.mark.parametrize('code,ok',
                         [('use, non_intrinsic :: foo', True),
                          ('use, intrinsic :: foo', False),
                          ('use foo', True),
                          ('use, non_intrinsic :: foo, only: boo', True),
                          ('use foo, only: boo', True),
                          ('use foo, only : boo', True)])
def test_use(code, ok):
    """
    verifies that submodule syntax is OK
    """
    pat = mnext['use']
    cpat = re.compile(pat, re.IGNORECASE)
    match = cpat.match(code)
    name = match.group(1).lower()

    if ok:
        assert name == 'foo'
    else:
        assert name == 'intrinsic'  # we discard this in Meson Python code to keep regex simpler


@pytest.mark.parametrize('code',
                         ['include "foo.f90"',
                          "include 'foo.f90'",
                          '#include "foo.f90"'])
def test_include(code):
    """
    verifies that include syntax is OK
    """
    pat = mnext['inc']
    cpat = re.compile(pat, re.IGNORECASE)
    match = cpat.match(code)
    name = match.group(1).lower()

    assert name == 'foo.f90'


if __name__ == '__main__':
    pytest.main([__file__])
