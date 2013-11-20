# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "omnios"
  config.vm.box_url = "http://omnios.omniti.com/media/OmniOS_r151006c-r1.box"

  config.vm.synced_folder ".", "/opt/scripts"
end
