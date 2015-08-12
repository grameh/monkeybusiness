import random
import time
import utils

VAGRANT_FILE = "/Users/mga/Documents/thesis/ers-utils"
target_interface = "eth1"


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
