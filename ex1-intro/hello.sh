#!/bin/bash

# Print hostname
hostname=$(hostname)
echo "Hostname: $hostname"

# Print operating system and kernel version
os=$(uname -s)
kernel=$(uname -r)
echo "Operating System: $os $kernel"

# Print CPU information
cpu_info=$(cat /proc/cpuinfo | grep "model name" | head -n 1 | cut -d ":" -f 2 | sed 's/^ *//')
cpu_cores=$(nproc --all)
echo "CPU: $cpu_info ($cpu_cores cores)"

# Print memory information
total_mem=$(free -h | awk '/^Mem/ {print $2}')
used_mem=$(free -h | awk '/^Mem/ {print $3}')
echo "Memory: Total: $total_mem, Used: $used_mem"

# Print disk usage
disk_usage=$(df -h / | awk 'NR==2 {print "Total: " $2 ", Used: " $3 ", Free: " $4}')
echo "Disk Usage: $disk_usage"

# Print uptime
uptime=$(uptime -p)
echo "Uptime: $uptime"
