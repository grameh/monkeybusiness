import vagrant

class VagrantChaos(AbstractChaos):
    def __init__(self, vagrant_file_path):
        self.vagrant_instance = vagrant.Vagrant(VAGRANT_FILE)

    def turn_off_node(node_name):
        self.vagrant_instance.halt(vm_name = node_name)

