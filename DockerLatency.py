from docker import Client
import os
from AbstractLatency import AbstractLatency
import utils

class DockerLatency(AbstractLatency):
    def __init__(self, base_url):
        self.client = Client(base_url=base_url)

    def add_latency(self, node_name, target_interface, mean, dev):
        res = self.client.exec_create(node_name, utils.latency_command.format(target_interface,mean,dev))
        self.client.exec_start(res['Id'])

    def add_duplication(self, node_name, target_interface, percentage_duplicate):
        res = self.client.exec_create(node_name, utils.duplication_command.format(target_interface, percentage_duplicate))
        self.client.exec_start(res['Id'])


    def add_reorder(self, node_name, target_interface, delay_time, percentage_packets, correlation_percentage ):
        # see documentation in utils.py for explanation of these parameters
        res = self.client.exec_create(node_name, utils.reorder_command.format(target_interface, delay_time, percentage_packets, correlation_percentage))
        self.client.exec_start(res['Id'])

    def add_loss(self, node_name, target_interface, percentage_loss):
        res = self.client.exec_create(node_name, utils.packet_loss_command.format(target_interface, percentage_loss))
        self.client.exec_start(res['Id'])

    def add_corruption(self, node_name, target_interface, percentage_corrupt):
        res = self.client.exec_create(node_name, utils.corruption_command.format(target_interface, percentage_corrupt))
        self.client.exec_start(res['Id'])
    def reset(self, node_name, target_interface):
        res = self.client.exec_create(node_name, utils.reset_command.format(target_interface))
        self.client.exec_start(res['Id'])

