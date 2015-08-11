# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.provision :shell, path: "bootstrap.sh"
    config.vm.provider "virtualbox" do |v|
        v.customize ["modifyvm", :id, "--memory", 1024, "--ioapic", "on", "--cpus", 1]
    end
end
