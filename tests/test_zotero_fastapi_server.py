#!/usr/bin/env python
"""Tests for `zotero_fastapi_server` package."""
# pylint: disable=redefined-outer-name
from zotero_fastapi_server import __version__
from zotero_fastapi_server.zotero_fastapi_server_interface import GreeterInterface
from zotero_fastapi_server.zotero_fastapi_server_impl import HelloWorld

def test_version():
    """Sample pytest test function."""
    assert __version__ == "0.0.1"

def test_GreeterInterface():
    """ testing the formal interface (GreeterInterface)
    """
    assert issubclass(HelloWorld, GreeterInterface)

def test_HelloWorld():
    """ Testing HelloWorld class
    """
    hw = HelloWorld()
    name = 'yvain'
    assert hw.greet_the_world(name) == f"Hello world, {name} !"

