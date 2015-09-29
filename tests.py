import unittest
import vagrant
import basic
import os
import subprocess
import re
from VagrantChaos import *
from VagrantLatency import *

class VagrantChaosTests(unittest.TestCase):
    def setUp(self):
        #defaults to vagrantfile in current directory
        self.vagrant_chaos = VagrantChaos()
        self.node_ip = "172.28.128.199"
        self.node_name = "node1"

    def tearDown(self):
        #cleanup everything
        #halting the machines makes test iteration a bit faster
        #for a more serious deployment change this to
        #self.vagrant_instance.destroy()
        #self.vagrant_instance.halt()
        pass

    def test_turn_on(self):
        self.vagrant_chaos.turn_on_node(self.node_name)
        status_list = self.vagrant_chaos.status()
        name_list = []
        for status in status_list:
            if status.state == 'running':
                name_list.append(status.name)
        self.assertEqual(name_list, ["node1"])

    def test_active_nodes_list(self):
        self.vagrant_chaos.turn_on_node(self.node_name)
        status_list = self.vagrant_chaos.status()
        name_list = self.vagrant_chaos.active_nodes_list()
        self.assertEqual(name_list, ["node1"])

    def test_turn_off(self):
        self.vagrant_chaos.turn_on_node(self.node_name)
        node_state = self.vagrant_chaos.vagrant_instance.status(vm_name = self.node_name)[0].state
        self.assertEqual(node_state, "running")
        self.vagrant_chaos.turn_off_node(self.node_name)

        node_state = self.vagrant_chaos.vagrant_instance.status(vm_name = self.node_name)[0].state
        self.assertEqual(node_state, "poweroff")

class VagrantLatencyTests(unittest.TestCase):
    def setUp(self):
        #defaults to vagrantfile in current directory
        self.vagrant_chaos   = VagrantChaos()
        self.vagrant_latency = VagrantLatency()
        self.node_ip = "172.28.128.199"
        self.node_name = "node1"

    def test_add_latency(self):
        self.vagrant_chaos.turn_on_node(self.node_name)
        command = "ping -c 1  " + self.node_ip
        output = subprocess.check_output(command, shell=True)
        regex = "round-trip min/avg/max/stddev = (?P<min>\d+\.\d+)/(?P<avg>\d+\.\d+)/(?P<max>\d+\.\d+)"
        (_, _, old_ping_avg) = re.search(regex, output).groups()

        self.vagrant_latency.add_latency(self.vagrant_latency, self.node_name, 'eth1', 100, 0)

        output = subprocess.check_output(command, shell=True)
        regex = "round-trip min/avg/max/stddev = (?P<min>\d+\.\d+)/(?P<avg>\d+\.\d+)/(?P<max>\d+\.\d+)"
        (_, _, new_ping_avg) = re.search(regex, output).groups()

        self.vagrant_latency.clear_config(self.vagrant_latency, self.node_name, "eth1")
        self.assertTrue(new_ping_avg > old_ping_avg)
        self.assertTrue(new_ping_avg > 100)

if __name__ == "__main__":
    unittest.main()
