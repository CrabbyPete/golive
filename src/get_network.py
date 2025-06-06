import subprocess

def get_network():
    cmd = "sudo iwgetid -r"
    result = subprocess.check_output(cmd, shell=True)
    network = result.decode('utf-8').replace('\n','')
    cmd = f"sudo grep psk /etc/NetworkManager/system-connections/{network}.nmconnection"
    result = subprocess.check_output(cmd, shell=True)
    password = result.decode('utf-8').split('=')[-1].replace('\n','')
    return network, password

if __name__ == "__main__":
    get_network()