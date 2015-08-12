#networking commands to simulate bad network behavior

#format with average and std dev for latency
latency_command = "sudo tc qdisc add dev {} root netem delay {}ms {}ms"
#format with percentage of packates to drop
packet_loss_command = "sudo tc qdisc add dev {} root netem loss {}%"
#format with duplicate percentage
duplication_command = "sudo tc qdisc add dev {} root netem duplicate {}%"
#format with percentage of corrupted packets
corruption_command = "sudo tc qdisc add dev {} root netem corrupt {}%"
#format with delay_time, percentage of packages and correlation percentage
#e.g. tc qdisc change dev eth0 root netem delay 10ms reorder 25% 50%
#^ 25% of packets (with a correlation of 50%) will get sent immediately, others will be delayed by 10ms.
reorder_command = "sudo tc qdisc add dev {} root netem delay {}ms reorder {}% {}%"
#delete the custom ones, and the pfifo_fast will replace them :)
reset_command = "sudo tc qdisc del dev {} root"
