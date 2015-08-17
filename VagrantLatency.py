from fabric.api import *
import vagrant
import utils
from AbstractLatency import AbstractLatency

class VagrantLatency(AbstractLatency):
    def __init__(self, vagrant_file_path=None):
        self.vagrant_instance = vagrant.Vagrant(vagrant_file_path)

    @task
    def add_latency(self, node_name, target_interface, mean, dev):
        with settings(host_string= self.vagrant_instance.user_hostname_port(vm_name=node_name),
                    key_filename = self.vagrant_instance.keyfile(vm_name=node_name),
                    disable_known_hosts = True):
            run(utils.latency_command.format(target_interface,mean,dev))

    @task
    def add_duplication(self, node_name, target_interface, percentage_duplicate):
        with settings(host_string= self.vagrant_instance.user_hostname_port(vm_name=node_name),
                        key_filename = self.vagrant_instance.keyfile(vm_name=node_name),
                        disable_known_hosts = True):
                run(utils.duplication_command.format(target_interface, percentage_duplicate))


    @task
    def add_reorder(self, node_name, target_interface, delay_time, percentage_packets, correlation_percentage ):
        # see documentation in utils.py for explanation of these parameters
        with settings(host_string= self.vagrant_instance.user_hostname_port(vm_name=node_name),
                        key_filename = self.vagrant_instance.keyfile(vm_name=node_name),
                        disable_known_hosts = True):
                run(utils.reorder_command.format(target_interface, delay_time, percentage_packets, correlation_percentage))

    @task
    def add_loss(self, node_name, target_interface, percentage_loss):
        with settings(host_string= self.vagrant_instance.user_hostname_port(vm_name=node_name),
                        key_filename = self.vagrant_instance.keyfile(vm_name=node_name),
                        disable_known_hosts = True):
                run(utils.packet_loss_command.format(target_interface, percentage_loss))

    @task
    def add_corruption(self, node_name, percentage_corrupt):
        with settings(host_string= self.vagrant_instance.user_hostname_port(vm_name=node_name),
                        key_filename = self.vagrant_instance.keyfile(vm_name=node_name),
                        disable_known_hosts = True):
                run(utils.corruption_command.format(target_interface, percentage_corrupt))

    @task
    def clear_config(self, node_name, target_interface):
        with settings(host_string= self.vagrant_instance.user_hostname_port(vm_name=node_name),
                        key_filename = self.vagrant_instance.keyfile(vm_name=node_name),
                        disable_known_hosts = True):
                run(utils.reset_command.format(target_interface))
