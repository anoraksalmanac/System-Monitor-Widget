#!/usr/bin/env python3
import dearpygui.dearpygui as dpg
import multiprocessing
import time
import os
import subprocess
import shutil

# amd_test_file = "/sys/class/hwmon/hwmon0/temp1_input"
nvidia_command = "nvidia-detector"
path_to_command = shutil.which(nvidia_command)

if path_to_command is None:
    nvidia = False
else:
    nvidia = True

if nvidia:
    import get_data_nvidia as get_data
else:
    import get_data_amd as get_data

width = 250
height = 335

if __name__ == "__main__":
    multiprocessing.freeze_support()

    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=get_data.read_temps, args=(queue,))
    p.start()

    dpg.create_context()
    dpg.create_viewport(title="Temp Monitor", width=width, height=height)
    dpg.set_viewport_resizable(False)
    dpg.set_viewport_width(width)
    dpg.set_viewport_height(height)
    dpg.set_global_font_scale(1.5)




    with dpg.window(label="Temps", tag="main_window"):

        dpg.add_text("GPU main temp: --", tag="gpu_edge")
        dpg.add_text("GPU hotspot:   --", tag="gpu_hotspot")
        dpg.add_text("GPU wattage:   --", tag="gpu_wattage")
        dpg.add_text("GPU used:   --", tag="gpu_used")
        dpg.add_text("~~~~~~~~~~~~~~~~~~~~~~")
        dpg.add_text("CPU temp:      --", tag="cpu_temp")
        dpg.add_text("CPU used:      --", tag="cpu_used")
        dpg.add_text("~~~~~~~~~~~~~~~~~~~~~~")
        dpg.add_text("VRAM used:   --", tag="gpu_mem_used")
        dpg.add_text("RAM used:   --", tag="ram_percent")
        dpg.add_text("SWAP used:   --", tag="swap_percent")



    dpg.set_primary_window("main_window", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_item_pos("main_window", (0, 0))
    dpg.set_item_width("main_window", width)
    dpg.set_item_height("main_window", height)

    while dpg.is_dearpygui_running():
        if not queue.empty():
            data = queue.get()
            dpg.set_value(
                "gpu_edge",
                f"GPU main temp: {data['gpu_edge']:.2f}°C"
            )
            if nvidia:
                dpg.set_value(
                    "gpu_hotspot",
                    f"GPU hotspot: {data['gpu_hotspot']:}°C"
                )
                dpg.set_value(
                    "gpu_used",
                    f"GPU used: {data['gpu_used']:.2f}%"
            )
            else:
                dpg.set_value(
                    "gpu_hotspot",
                    f"GPU hotspot: {data['gpu_hotspot']}°C"
                )
                dpg.set_value(
                    "gpu_used",
                    f"GPU used: {int(data['gpu_used'])}%"
            )
            dpg.set_value(
                "gpu_wattage",
                f"GPU wattage: {data['gpu_wattage']:}W"
            )
            dpg.set_value(
                "gpu_mem_used",
                f"VRAM used: {data['gpu_mem_used']:.2f}%"
            )
            dpg.set_value(
                "cpu_temp",
                f"CPU temp: {data['cpu_temp']:.2f}°C"
            )
            dpg.set_value(
                "cpu_used",
                f"CPU used: {data['cpu_used']:.2f}%"
            )
            dpg.set_value(
                "ram_percent",
                f"RAM used: {data['ram_percent']:.2f}%"
            )
            dpg.set_value(
                "swap_percent",
                f"SWAP used: {data['swap_percent']:.2f}%"
            )

        dpg.render_dearpygui_frame()

    p.terminate()
    p.join()
    dpg.destroy_context()
