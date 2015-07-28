import unittest
import vagrant
import basic
import os
import subprocess
import re

class BasicTests(unittest.TestCase):
    def setUp(self):
        #defaults to vagrantfile in current directory
        self.vagrant_instance = vagrant.Vagrant()
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
        basic.turn_on_node(self.vagrant_instance, self.node_name)
        status_list = self.vagrant_instance.status()
        name_list = []
        for status in status_list:
            if status.state == 'running':
                name_list.append(status.name)
        self.assertEqual(name_list, ["node1"])

    def test_active_nodes_list(self):
        self.vagrant_instance.up(vm_name = self.node_name)
        status_list = self.vagrant_instance.status()
        name_list = basic.active_node_names_list(self.vagrant_instance)
        self.assertEqual(name_list, ["node1"])

    def test_turn_off(self):
        self.vagrant_instance.up(vm_name = self.node_name)
        node_state = self.vagrant_instance.status(vm_name = self.node_name)[0].state
        self.assertEqual(node_state, "running")
        basic.turn_off_node(self.vagrant_instance, self.node_name)

        node_state = self.vagrant_instance.status(vm_name = self.node_name)[0].state
        self.assertEqual(node_state, "poweroff")

    def test_add_latency(self):
        self.vagrant_instance.up(vm_name = self.node_name)
        command = "ping -c 1  " + self.node_ip
        output = subprocess.check_output(command, shell=True)
        regex = "round-trip min/avg/max/stddev = (?P<min>\d+\.\d+)/(?P<avg>\d+\.\d+)/(?P<max>\d+\.\d+)"
        (_, _, old_ping_avg) = re.search(regex, output).groups()

        basic.add_latency(self.vagrant_instance, self.node_name, 100, 0)

        output = subprocess.check_output(command, shell=True)
        regex = "round-trip min/avg/max/stddev = (?P<min>\d+\.\d+)/(?P<avg>\d+\.\d+)/(?P<max>\d+\.\d+)"
        (_, _, new_ping_avg) = re.search(regex, output).groups()

        self.assertTrue(new_ping_avg > old_ping_avg)
        self.assertTrue(new_ping_avg > 100)
        basic.clear_config(self.vagrant_instance, self.node_name)

if __name__ == "__main__":
    unittest.main()
