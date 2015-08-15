from docker import Client

class DockerChaos(AbstractChaos):
    def __init__(self, base_url):
        self.client = Client(base_url=base_url)

    def turn_off_node(node_name, timeout = 5):
        self.client.stop(node_name, timeout)

