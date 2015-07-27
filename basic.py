import vagrant
import random
import time
from fabric.api import *

VAGRANT_FILE = "/Users/mga/Documents/thesis/ers-utils"
target_interface = "eth1"
#format with average and std dev for latency
latency_command = "sudo tc qdisc add dev "+ target_interface  + " root netem delay {}ms {}ms"
#format with percentage of packates to drop
packet_loss_command = "sudo tc qdisc add dev " + target_interface + " root netem loss {}%"
#format with duplicate percentage
duplication_command = "sudo tc qdisc add dev " + target_interface + " root netem duplicate {}%"
#format with percentage of corrupted packets
corruption_command = "sudo tc qdisc add dev " + target_interface + " root netem corrupt {}%"
#format with delay_time, percentage of packages and correlation percentage
#e.g. tc qdisc change dev eth0 root netem delay 10ms reorder 25% 50%
#^ 25% of packets (with a correlation of 50%) will get sent immediately, others will be delayed by 10ms.
reorder_command = "sudo tc qdisc add dev " + target_interface + " root netem delay {}ms reorder {}% {}%"
#delete the custom ones, and the pfifo_fast will replace them :)
reset_command = "sudo tc qdisc del dev " + target_interface + " root"



def active_node_names_list(vagrant_instance):
    status_list = vagrant_instance.status()
    name_list = []
    for status in status_list:
        if status.state == 'running':
            name_list.append(status.name)
    return name_list

def turn_off_node(vagrant_instance, node_name):
    vagrant_instance.halt(vm_name = node_name)

def turn_on_node(vagrant_instance, node_name):
    vagrant_instance.up(vm_name = node_name)

def toggle_with_delay(vagrant_instance, node_name, sleep_duration):
    turn_off_node(v, node_name)
    time.sleep(sleep_duration)
    turn_on_node(v, node_name)


#latency, loss, duplication, corruption, reorder
@task
def add_latency(vagrant_instance, node_name, mean, dev):
    #first remove old netems
    with settings(host_string= vagrant_instance.user_hostname_port(vm_name=node_name),
                    key_filename = vagrant_instance.keyfile(vm_name=node_name),
                    disable_known_hosts = True):
        run(reset_command)
    with settings(host_string= vagrant_instance.user_hostname_port(vm_name=node_name),
                    key_filename = vagrant_instance.keyfile(vm_name=node_name),
                    disable_known_hosts = True):
        run(latency_command.format(mean,dev))



def main():
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
