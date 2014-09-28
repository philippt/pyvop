# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "xezpeleta/wheezy64"

  config.vm.network "private_network", ip: "192.168.42.11" #, auto_config: false #, virtualbox__intnet: true
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  config.ssh.forward_agent = true

  config.vm.provider "virtualbox" do |vb|
      vb.name = "pyvop"

      vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  config.vm.provision :shell, path: "bootstrap/bootstrap.sh", args: ["pyvop"]
end
