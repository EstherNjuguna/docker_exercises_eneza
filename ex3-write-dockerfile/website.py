import os
from fastapi import FastAPI
import platform
import uvicorn
import psutil

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the System Info API"}

@app.get("/system_info")
def get_system_info():
    return {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Architecture": platform.architecture()
    }

@app.get("/cpu_info")
def get_cpu_info():
    cpufreq = psutil.cpu_freq()
    return {
        "Physical cores": psutil.cpu_count(logical=False),
        "Total cores": psutil.cpu_count(logical=True),
        "Max Frequency": f"{cpufreq.max:.2f}Mhz",
        "Min Frequency": f"{cpufreq.min:.2f}Mhz",
        "Current Frequency": f"{cpufreq.current:.2f}Mhz",
        "CPU Usage Per Core": {f"Core {i}": f"{percentage}%" for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1))},
        "Total CPU Usage": f"{psutil.cpu_percent()}%"
    }

@app.get("/memory_info")
def get_memory_info():
    svmem = psutil.virtual_memory()
    return {
        "Total": get_size(svmem.total),
        "Available": get_size(svmem.available),
        "Used": get_size(svmem.used),
        "Percentage": f"{svmem.percent}%"
    }

@app.get("/swap_info")
def get_swap_info():
    swap = psutil.swap_memory()
    return {
        "Total": get_size(swap.total),
        "Free": get_size(swap.free),
        "Used": get_size(swap.used),
        "Percentage": f"{swap.percent}%"
    }

@app.get("/disk_info")
def get_disk_info():
    partitions_info = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        partitions_info.append({
            "Device": partition.device,
            "Mountpoint": partition.mountpoint,
            "File system type": partition.fstype,
            "Total Size": get_size(partition_usage.total),
            "Used": get_size(partition_usage.used),
            "Free": get_size(partition_usage.free),
            "Percentage": f"{partition_usage.percent}%"
        })
    return {"Partitions": partitions_info}

@app.get("/network_info")
def get_network_info():
    if_addrs = psutil.net_if_addrs()
    interfaces_info = {}
    for interface_name, interface_addresses in if_addrs.items():
        addresses = []
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                addresses.append({
                    "IP Address": address.address,
                    "Netmask": address.netmask,
                    "Broadcast IP": address.broadcast
                })
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                addresses.append({
                    "MAC Address": address.address,
                    "Netmask": address.netmask,
                    "Broadcast MAC": address.broadcast
                })
        interfaces_info[interface_name] = addresses
    net_io = psutil.net_io_counters()
    return {
        "Interfaces": interfaces_info,
        "Total Bytes Sent": get_size(net_io.bytes_sent),
        "Total Bytes Received": get_size(net_io.bytes_recv)
    }

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


if __name__ == '__main__':
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port, reload=True)