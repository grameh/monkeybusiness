import utils
import vagrant
from fabric.api import *

class VagrantResuscitator(AbstractResuscitator):
    def __init__(self, vagrant_file_path):
        self.vagrant_instance = vagrant.Vagrant(VAGRANT_FILE)

    def ressurect_node(self, node_name):
        self.vagrant_instance.up(vm_name = node_name)

    def reset_newtork(self, node_name):
        @task
        def clear_config(self, node_name, target_interface):
            with settings(host_string= self.vagrant_instance.user_hostname_port(vm_name=node_name),
                            key_filename = self.vagrant_instance.keyfile(vm_name=node_name),
                            disable_known_hosts = True):
                run(reset_command.format(target_interface))


