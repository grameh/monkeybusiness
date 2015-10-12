import random
import subprocess
import time
import utils

from DockerLatency import DockerLatency

VAGRANT_FILE = "/Users/mga/Documents/thesis/ers-utils"
target_interface = "eth1"
docker_path = '/usr/bin/docker'


def active_node_names_list(vagrant_instance):
    status_list = vagrant_instance.status()
    name_list = []
    for status in status_list:
        if status.state == 'running':
            name_list.append(status.name)
    return name_list

def toggle_with_delay(vagrant_instance, node_name, sleep_duration):
    turn_off_node(v, node_name)
    time.sleep(sleep_duration)
    turn_on_node(v, node_name)

def running_containers_list():
    running_containers_command = (docker_path + ' ps -q').split(' ')

    result = subprocess.check_output(running_containers_command)
    containers_list = []
    for container_id in result.split():
		if container_id[-1] == '\n':
			container_id = container_id[:-1]
		containers_list.append(container_id)
    return containers_list


def main():
	node_list = running_containers_list()
	dl = DockerLatency("unix://var/run/docker.sock")
	for node in node_list:
		#dl.add_latency(node, 'eth1', 100, 0)
		#dl.add_latency(node, 'eth0', 100, 0)
                #dl.add_loss(node, 'eth0', 15)
                #dl.add_loss(node, 'eth1', 15)
                #dl.add_duplication(node, 'eth0', 60)
                #dl.add_duplication(node, 'eth1', 60)
                #dl.add_corruption(node, 'eth0', 15)
                #dl.add_corruption(node, 'eth1', 15)
                dl.add_reorder(node, 'eth0', 100, 25, 50)
                dl.add_reorder(node, 'eth1', 100, 25, 50)
	import pdb;pdb.set_trace()


        
        for node in node_list:
            dl.reset(node, 'eth0')
            dl.reset(node, 'eth1')


def main_vagrant():
    v = vagrant.Vagrant(VAGRANT_FILE)

    nodes = active_node_names_list(v)

    nr_runs = 3
    start = time.time()
    import pdb;pdb.set_trace()
    for i in range(nr_runs):
        node = random.choice(nodes)
        sleep_duration = random.uniform(1,5)
        print "toggling" + str(node) + "with sleep duration " + str(sleep_duration)
        toggle_with_delay(v,node,sleep_duration)

if __name__ == "__main__":
    main()
