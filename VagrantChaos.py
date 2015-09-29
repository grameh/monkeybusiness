import vagrant
from AbstractChaos import AbstractChaos

class VagrantChaos(AbstractChaos):
    def __init__(self, vagrant_file_path = None):
        self.vagrant_instance = vagrant.Vagrant(vagrant_file_path)

    def turn_off_node(self,node_name):
        self.vagrant_instance.halt(vm_name = node_name)
    def turn_on_node(self,node_name):
        self.vagrant_instance.up(vm_name = node_name)
    def status(self):
        return self.vagrant_instance.status()

    def active_nodes_list(self):
        status_list = self.vagrant_instance.status()
        name_list = []
        for status in status_list:
            if status.state == 'running':
                name_list.append(status.name)
        return name_list



