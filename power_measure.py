# By: Ahmed El-Maghrabi
# Email: a.elmaghrabi@ieee.org

import paramiko
import os
import json
import matplotlib.pyplot as plt

x = []
y = []
counter = 0;
blocking = True

def on_key(event):
    global blocking 
    blocking = False

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
ssh.connect("192.168.1.21", username="ubnt", password="ubnt1234")

fig, axes = plt.subplots(nrows=1, num="Loco M5 Power Meter")

plt.ion()
plt.title("Signal Power(dBm) vs Time Sample")
plt.xlabel('Time sample')
plt.ylabel('Signal Power (dB)')

while blocking:
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('wstalist')
    exit_code = ssh_stdout.channel.recv_exit_status() # handles async exit error 
    opt = ssh_stdout.readlines()
    opt = "".join(opt)
    jsonObj = json.loads(opt.strip())
    signalPowerdB = jsonObj[0]["remote"]["signal"]
    
    x.append(counter)
    y.append(signalPowerdB)
    plt.draw()
    plt.pause(0.1)
    plt.show(block=False)
    counter = counter + 1
    fig.canvas.mpl_connect('key_press_event', on_key)


