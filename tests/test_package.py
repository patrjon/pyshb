import pyshb
import pytest


def test_name(package_name):
    """
    Test the name of the pyshb package
    :return:
    """

    assert pyshb.name == package_name
