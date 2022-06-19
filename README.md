## RK Manager

RK manager is a simple manager/monitor for the linux kernel. Comes with GUI (From https://github.com/rdbende/Azure-ttk-theme).

## What can you do with this tool?

Built with python resources you can:

- Look at the CPU structure and usage information;
- Look at RAM usage;
- Look at the governor and frequency settings.
- Change CPU governor

## Download and run

  the following steps are basic and can be performed in a lot of alternative ways, altrought if you don't know what you're doing just follow the guide to make sure everithing will work fine
  
### Clone this repo:

    git clone https://github.com/Peppe289/RK-Manager.git

### Move into the folder and give exec permissions
    
    cd RK-Manager
    chmod +x main.py
    
### Install dependencies

Install TK. For Ubuntu:

    sudo apt install python3-tk

For other, you can install all modules with `sudo` or without.

#### Install with sudo

Install all the modules with

    sudo pip3 install -r requirements.txt


#### Install without sudo
Install all the modules without sudo:

If you don't have python3.8-venv packages installed.

    sudo apt install python3.8-venv

After install python3.8-venv create your user environment with python libs:

    python3 -m venv venv
    ./venv/bin/python3 -m pip install -r requirements.txt
    
### Enjoy!

    sudo ./main.py

or

    sudo ./venv/bin/python3 main.py

## Notes

Monitoring takes place via the main cluster (policy0). On multi-cluster linux devices with different settings, the information displayed is not reliable.
