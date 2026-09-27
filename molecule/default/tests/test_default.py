"""Testinfra checks for the sadpuppet role."""

import os

import pytest
import yaml

DEFAULTS = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "defaults", "main.yml"
)
with open(DEFAULTS) as defaults_file:
    ROLE_DEFAULTS = yaml.safe_load(defaults_file)


@pytest.mark.parametrize("name", ROLE_DEFAULTS["puppet_packages"])
def test_packages_removed(host, name):
    assert not host.package(name).is_installed


def test_puppet_command_gone(host):
    assert not host.exists("puppet")


def test_service_gone(host):
    assert not host.service("puppet").is_enabled


@pytest.mark.parametrize("path", ROLE_DEFAULTS["puppet_paths"])
def test_paths_removed(host, path):
    assert not host.file(path).exists
