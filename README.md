Sad Puppet
==========

Remove Puppet agents, all leftover files, and directories.

Dependencies
------------

None.

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

    puppet_apt_keys:
      - http://yum.puppetlabs.com/RPM-GPG-KEY-puppet
      - http://yum.puppetlabs.com/RPM-GPG-KEY-puppetlabs
      - http://yum.puppetlabs.com/RPM-GPG-KEY-reductive

    puppet_el_yum_keys:
      - http://yum.puppetlabs.com/RPM-GPG-KEY-puppet
      - http://yum.puppetlabs.com/RPM-GPG-KEY-puppetlabs
      - http://yum.puppetlabs.com/RPM-GPG-KEY-reductive

Example Playbook
----------------

    - hosts: servers
      roles:
         - deekayen.sadpuppet

License
-------

BSD
