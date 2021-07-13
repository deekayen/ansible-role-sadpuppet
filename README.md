Sad Puppet
==========

[![CI](https://github.com/deekayen/ansible-role-sadpuppet/actions/workflows/ci.yml/badge.svg)](https://github.com/deekayen/ansible-role-sadpuppet/actions/workflows/ci.yml) [![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive)

Remove Puppet agents, all leftover files, and directories.

Dependencies
------------

Be sure you install the galaxy role in your runtime server.

```
ansible-galaxy install deekayen.sadpuppet
```

Default Variables
-----------------

    puppet_paths:
      - /etc/logrotate.d/puppet
      - /etc/yum.repos.d/puppetlabs-deps.repo
      - /etc/yum.repos.d/puppetlabs-products.repo
      - /etc/puppet
      - /etc/tmpfiles.d/puppet.conf
      - /usr/bin/puppet
      - /usr/share/puppet
      - /usr/lib/systemd/system/puppet.service
      - /usr/lib/systemd/system/puppetagent.service
      - /usr/share/ruby/vendor_ruby/puppet
      - /usr/lib/puppet
      - /var/log/puppet
      - /var/run/puppet

    puppet_keys:
      - 6F6B15509CF8E59E6E469F327F438280EF8D349F
      - 47B320EB4C7C375AA9DAE1A01054B7A24BD6EC30
      - 9C6C545246912EE700FB5682FFAC86588347A27F

Example Playbook
----------------

    - hosts: servers
      roles:
         - deekayen.sadpuppet

License
-------

BSD
