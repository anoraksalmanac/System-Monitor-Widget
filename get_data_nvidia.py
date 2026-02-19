import os
import time
import sys
import os
import subprocess


current_pid = os.getpid()
lines = 10

def safe_float(x):
    if x == "N/A":
        return None
    try:
        return float(x)
    except ValueError:
        return None


def get_nvidia_gpu():
    cmd = [
        "nvidia-smi",
        "--query-gpu=temperature.gpu,power.draw,memory.used,memory.total,utilization.gpu",
        "--format=csv,noheader,nounits"
    ]
    out = subprocess.check_output(cmd, text=True).strip()
    gpus = []
    for line in out.splitlines():
        parts = line.split(", ")
        t = safe_float(parts[0])
        p = safe_float(parts[1])
        mu = safe_float(parts[2])
        mt = safe_float(parts[3])
        util = safe_float(parts[4])

        mem_perc = round(float(mu/mt)*100, 2)
        gpus.append({
            "temp": t,
            "power": p,
            "mem_perc": mem_perc,
            "mem_used": mu,
            "mem_total": mt,
            "util": util,
        })
    return gpus




file_cpu_temp_avrage = "/sys/class/hwmon/hwmon1/temp1_input"

file_memory = "/proc/meminfo"

print(f"The current process ID is: {current_pid}")
def get_memory():
    with open (file_memory, "r") as f:
        for line in f:
            if line:
                info_lines = line.split(":")
                if len(info_lines) == 2:
                    key = info_lines[0]
                    data = info_lines[1]
                    str_data = ''.join(filter(str.isdigit, data))
                    int_data = int(str_data)
                    data = int_data/1000000
                    if key == "MemTotal":
                        global MemTotal
                        MemTotal = data
                    elif key == "MemAvailable":
                        global MemAvailable
                        MemAvailable = data
                    elif key == "SwapTotal":
                        global SwapTotal
                        SwapTotal = data
                    elif key == "SwapFree":
                        global SwapFree
                        SwapFree = data
                        # untested - may not work but concept is there


def get_cpu():

    def read_cpu():
        with open("/proc/stat") as f:
            line = f.readline()
        parts = line.split()[1:]
        nums = list(map(int, parts))
        idle = nums[3] + nums[4]  # idle + iowait
        total = sum(nums[:8])     # user+nice+system+idle+iowait+irq+softirq+steal
        return idle, total

    idle1, total1 = read_cpu()
    time.sleep(1)
    idle2, total2 = read_cpu()

    delta_idle = idle2 - idle1
    delta_total = total2 - total1

    cpu_percent = (delta_total - delta_idle) / delta_total * 100
    return cpu_percent

def get_temps ():
    get_nvidia_gpu()
    gpus = get_nvidia_gpu()
    gpu_dict = gpus[0]

    global gpu_edge
    global gpu_wattage
    global gpu_used_perc
    global gpu_hotspot
    global gpu_mem_used_perc
    global cpu_temp
    global cpu_used
    global ram_percent
    global swap_percent
    
    gpu_hotspot = "NA"
    gpu_edge = gpu_dict["temp"]
    gpu_wattage = gpu_dict["power"]
    gpu_used_perc = gpu_dict["util"]
    gpu_mem_used_perc = gpu_dict["mem_perc"]
    cpu_temp = float(open(file_cpu_temp_avrage).read()) / 1000
    cpu_used = round(get_cpu(), 2)
    get_memory()
    ram_percent = ((MemTotal-MemAvailable)/MemTotal)*100
    swap_percent = ((SwapTotal-SwapFree)/SwapTotal)*100



def read_temps(queue):
    while True:
        get_temps()
        data = {
            "gpu_edge": gpu_edge,
            "gpu_hotspot": gpu_hotspot,
            "gpu_wattage": gpu_wattage,
            "gpu_used": gpu_used_perc,
            "gpu_mem_used": gpu_mem_used_perc,
            "cpu_temp": cpu_temp,
            "cpu_used": cpu_used,
            "swap_percent": swap_percent,
            "ram_percent": ram_percent,
            }

        queue.put(data)
        time.sleep(.2)

def main():
    while True:
        get_temps()
        print(
        f"GPU main temp:    {gpu_edge}   \n"
        f"GPU Hotspot temp: {gpu_hotspot}\n"
        f"GPU wattage:      {gpu_wattage}\n"
        f"GPU used:         {gpu_used_perc}\n"
        f"GPU mem used:     {gpu_mem_used_perc}\n"
        f"CPU temp:         {cpu_temp}\n"
        f"CPU used:         {cpu_used}\n"
        f"RAM:              {MemAvailable:.2f} free of {MemTotal:.2f}\n"
        f"RAM:              {SwapTotal:.2f} free of {SwapFree:.2f}\n"
        f"RAM:              {ram_percent}"

    )
        sys.stdout.write("\033[F\033[K" * lines)
        
        time.sleep(.2)

if __name__ == '__main__':
    main()
    