# deekayen.sadpuppet

[![CI](https://github.com/deekayen/ansible-role-sadpuppet/actions/workflows/ci.yml/badge.svg)](https://github.com/deekayen/ansible-role-sadpuppet/actions/workflows/ci.yml) [![Ansible Galaxy](https://img.shields.io/badge/galaxy-deekayen.sadpuppet-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/deekayen/sadpuppet/) [![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive) ![BSD 3-Clause license](https://img.shields.io/badge/license-BSD%203--Clause-blue)

An Ansible role that uninstalls the Puppet agent from Linux hosts, deletes the files and directories Puppet leaves behind, and removes the Puppet Labs package signing keys.

The role removes the packages in `puppet_packages` with the system package manager, then deletes every path in `puppet_paths`. On Debian-family hosts it removes each fingerprint in `puppet_keys` from the legacy apt keyring with `ansible.builtin.apt_key`; on RedHat-family hosts it removes them from the RPM database with `ansible.builtin.rpm_key`.

## Requirements

- ansible-core 2.15 or newer on the controller.
- Privilege escalation on the target. Run the play with `become: true`; the role removes packages and deletes paths under `/etc`, `/usr`, and `/var`.
- Fact gathering left on. The role picks the key removal tasks from `ansible_facts.os_family`.

## Supported platforms

From `meta/main.yml`, and each one runs through Molecule in CI:

| Platform | Versions |
| --- | --- |
| EL (Rocky Linux in CI) | 9 |
| Debian | 12 (bookworm), 13 (trixie) |
| Ubuntu | 22.04 (jammy), 24.04 (noble), 26.04 (resolute) |

## Installation

From Ansible Galaxy:

```bash
ansible-galaxy role install deekayen.sadpuppet
```

Or pin it in `requirements.yml`:

```yaml
---
roles:
  - name: deekayen.sadpuppet
    src: https://github.com/deekayen/ansible-role-sadpuppet.git
    scm: git
    version: main
```

```bash
ansible-galaxy role install -r requirements.yml
```

## Role variables

| Variable | Default | Description |
| --- | --- | --- |
| `puppet_packages` | `[puppet, puppet-agent]` | Package names removed on every platform. Debian 12+ and Ubuntu 24.04+ ship the agent as `puppet-agent`, with `puppet` only a transitional package, so both are listed. |
| `puppet_paths` | 13 paths, see `defaults/main.yml` | Files and directories deleted after package removal: `/etc/puppet`, `/usr/share/puppet`, `/usr/lib/puppet`, `/var/log/puppet`, `/var/run/puppet`, `/usr/bin/puppet`, `/usr/share/ruby/vendor_ruby/puppet`, the `puppet.service` and `puppetagent.service` systemd units, the Puppet Labs yum repository files, and logrotate and tmpfiles entries. The role asserts that every entry is an absolute path. Overriding the list replaces it. |
| `puppet_keys` | Three Puppet Labs fingerprints | Signing keys to remove. The role asserts that every entry is a full 40-hex-digit fingerprint. |

## Behavior

- On Debian-family hosts, key removal runs only when both `/usr/bin/apt-key` and `/usr/bin/gpg` exist. Debian 13 and Ubuntu 26.04 no longer ship `apt-key`, so the role skips key removal there.
## Dependencies

None.

## Example playbook

```yaml
---
- name: Remove Puppet after the move to Ansible.
  hosts: legacy_puppet_nodes
  become: true

  roles:
    - deekayen.sadpuppet
```

## Development

CI runs on every push to `main` and every pull request (see `.github/workflows/ci.yml`):

1. Lint: `ansible-lint --profile production` and `flake8 molecule/`.
2. Molecule: `prepare.yml` installs the distribution `puppet` package (from EPEL on EL), then Molecule runs converge, idempotence, and testinfra verification in Docker against each distribution in the table above.

To run the same checks locally with Docker available:

```bash
pip3 install ansible-core ansible-lint flake8 molecule "molecule-plugins[docker]" docker pytest-testinfra
ansible-lint --profile production
flake8 molecule/
MOLECULE_DISTRO=rockylinux9 molecule test
```

`MOLECULE_DISTRO` selects a `geerlingguy/docker-<distro>-ansible` image. The values CI uses are `rockylinux9`, `ubuntu2204`, `ubuntu2404`, `ubuntu2604`, `debian12`, and `debian13`. The testinfra checks in `molecule/default/tests/test_default.py` read `defaults/main.yml` and confirm that every package in `puppet_packages` is gone, the `puppet` command is no longer on the path, the `puppet` service is not enabled, and every path in `puppet_paths` is absent.

The repository also has a `.pre-commit-config.yaml`; run `pre-commit run --all-files` before pushing.

### Repository layout

| Path | Purpose |
| --- | --- |
| `tasks/main.yml` | Input validation, package removal, path cleanup, and the per-family key include. |
| `tasks/assert.yml` | Checks `puppet_paths` and `puppet_keys`, tagged `always`. |
| `tasks/debian.yml` | apt key removal, guarded by the `apt-key` and `gpg` checks. |
| `tasks/redhat.yml` | RPM key removal. |
| `defaults/main.yml` | Every user-facing variable. |
| `meta/argument_specs.yml` | Argument spec for the three variables. |
| `molecule/default/` | Molecule scenario: `prepare.yml` installs Puppet, `converge.yml` applies the role, and testinfra tests check the result. |
| `.github/workflows/` | `ci.yml` for lint and Molecule, `release.yml` for Galaxy import. |

## Releases

Pushing a git tag runs `.github/workflows/release.yml`, which imports the tagged commit into Ansible Galaxy as `deekayen.sadpuppet`. The import needs a `GALAXY_API_KEY` repository or organization secret.

## License

BSD 3-Clause. See [LICENSE](LICENSE).

## Author

[David Norman](https://github.com/deekayen). Sponsorship links are in [.github/FUNDING.yml](.github/FUNDING.yml).
