# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "omnios-r151008f"
  config.vm.box_url = "http://omnios.omniti.com/media/OmniOS_r151008f-r1.box"

  config.vm.synced_folder ".", "/opt/scripts"
  config.vm.provision :shell, :path => 'provision.sh'
end
