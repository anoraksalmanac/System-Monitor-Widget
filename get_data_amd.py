import os
import time
import cmd
import sys
import multiprocessing


current_pid = os.getpid()
lines = 10

file_gpu_edge = "/sys/class/hwmon/hwmon0/temp1_input" #may only work with dedicated gpu, idk
file_gpu_hotspot = "/sys/class/hwmon/hwmon0/temp2_input" #may only work with dedicated gpu, idk
file_gpu_avrage_use_perc = "/sys/class/drm/card1/device/gpu_busy_percent" #may only work with dedicated gpu, idk
file_gpu_mem_avrage_use_perc = "/sys/class/drm/card1/device/mem_busy_percent" #may only work with dedicated gpu, idk

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
    global gpu_edge
    global gpu_hotspot
    global gpu_wattage
    global gpu_used_perc
    global gpu_mem_used_perc
    global cpu_temp
    global cpu_used
    global ram_percent
    global swap_percent

    gpu_edge = float(open(file_gpu_edge).read()) / 1000
    gpu_hotspot = float(open(file_gpu_hotspot).read()) / 1000
    gpu_wattage = float(open(file_gpu_wattage).read()) / 1000000
    gpu_used_perc = float(open(file_gpu_avrage_use_perc).read())
    gpu_mem_used_perc = float(open(file_gpu_mem_avrage_use_perc).read())
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
    