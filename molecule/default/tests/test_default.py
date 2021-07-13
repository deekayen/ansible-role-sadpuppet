import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_dependencies_installed(host):
    assert not host.package("puppet").is_installed


def test_dependencies_service(host):
    assert not host.service("puppet").is_enabled


def test_meshchat_files(host):
    assert not host.file("/etc/tmpfiles.d/puppet.conf").exists
    assert not host.file("/usr/lib/systemd/system/puppet.service").exists
