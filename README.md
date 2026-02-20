# system-monitor
a temperature / system utility monitor widget
<p align="left">
    <img width="245" height="366" src="images/temp-sensor.png">
</p>


## about
This project came from a lack of convenient and cross compatible utility monitors. I wanted something standard that would work on my personal computer as well as my laptop and the family computer. I honestly never imagined that I would create something that I wanted to share so it has some weird development choices and many places to improve. I welcome any and all advice and help I could get on this project as well as info about compatibility on any hardware it does work on. 

## dev note
This widget is more or less just a window that updates so it floats and interacts like a normal window. if you would like to force it over other windows, use any built in tools from your DE. 

## how it works
This program has 2 files that grab your system information depending on if you have an AMD or NVIDIA GPU. Intel support not tested.
The AMD version looks through your file system and grabs data from some specific files where both AMD GPUs and -maybe all- CPUs store their data. 
The NVIDIA version uses the nvidia-smi command to communicate with your driver and request the needed data. do note - NVIDIA does not share their gpu hotspot information
The main file records what gpu you have and decides which file to use to gather its required information. It then formats it for dearpygui and makes the GUI. 

## compatibility
I made this compatible with both NVIDIA and AMD GPUs and both AMD and INTEL CPU compatibility however, I have limited access to hardware so I am unable to confirm universal compatibility.

I wrote this in python 3.14 however I do not believe I used any techniques specific to this version so there should be a fair amount of wiggle room. 
### current tested hardware
* GPUs
- AMD 5700xt
- NVIDIA 1650 mobile max-q
- NVIDIA 1030 (ddr4 version)
* CPUs
- AMD 5700x
- AMD 3600
- INTEL i5-11400H

### currently tested OS
- linux mint
- ubuntu
- pop os (note, you will need to update your drivers manually if you have a older nvidia gpu)
- arch (requires manual install)

### currently tested DE
- cinnamon 
- hyprland
- pop os "cosmic"

## installation
This project assumes you are using a debian based system and have python and pip installed. If you are missing that software, the deb should install it but if you are just pulling the project, you will need to ensure you have that. 

### instructions
I have included a .deb that should do all the installation for you as well and I am working on making an apt repository, I just have my name attached to it currently and I don't enjoy that so that's coming soon. 
make sure to cd into your downloads folder - or wherever you placed the .deb - and run the install command. 

```
sudo apt install ./temp-sensor_<version>_all.deb
```
