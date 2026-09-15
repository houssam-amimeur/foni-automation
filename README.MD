# FONI AUTOMATION 

## Project Description 
This project uses Netmiko to connect to Cisco and Linux devices to obtain device inforamation

## Target Devices 
1 CISCO 8000V 
7 LINUX AWS-EC2 servers 


## How to run program
### Set up virtual environment 
Run the following command: `python -m venv venv`
Install NETMIKO and NAPALM:

```
Python -m pip install netmiko
Python -m pip install napalm

```


### cisco_interface_check.py
To run the `cisco_interface_check.py` file, use `python cisco_interface_check.py`

### multi_system_check.py
To run the `multi_system_check.py` file, use `python multi_system_check.py`

## Expected output
`cisco_interface_check.py` will output information about whether the loopback interfaces are operational, or a check is required 

`multi_system_check.py`
