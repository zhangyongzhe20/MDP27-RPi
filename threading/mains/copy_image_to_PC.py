from paramiko import SSHClient
from scp import SCPClient

# pi@192.168.27.27:/home/pi/images/
# /Users/yongzhe/Documents/GitHub/CZ3004-MDP/MDP27-RPi/outputs/


def copy_image_to_PC():
    client = SSHClient()
    client.load_system_host_keys()
    client.load_host_keys('/Users/yongzhe/.ssh/authorized_keys')
    # client.set_missing_host_key_policy(AutoAddPolicy())

    # client.look_for_keys(True)
    client.connect('pi@192.168.27.27')
    client.close()

copy_image_to_PC()
