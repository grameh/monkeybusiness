class DockerLatency(AbstractLatency):
    def __init__(self, base_url):
        self.client = Client(base_url=base_url)

    def add_latency(self, node_name, target_interface, mean, dev):
        self.client.exec_create(node_name, utils.latency_command.format(target_interface,mean,dev))

    def add_duplication(self, node_name, target_interface, percentage_duplicate):
        self.client.exec_create(node_name, utils.duplication_command.format(target_interface, percentage_duplicate))


    def add_reorder(self, node_name, target_interface, delay_time, percentage_packets, correlation_percentage ):
        # see documentation in utils.py for explanation of these parameters
        self.client.exec_create(node_name, utils.reorder_command.format(target_interface, delay_time, percentage_packets, correlation_percentage))

    def add_loss(self, node_name, target_interface, percentage_loss):
        self.client.exec_create(node_name, utils.packet_loss_command.format(target_interface, percentage_loss))

    def add_corruption(self, node_name, percentage_corrupt):
        self.client.exec_create(node_name, utils.corruption_command.format(target_interface, percentage_corrupt))

