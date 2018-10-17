

import subprocess

orders = ["l","m"]


for i in orders:
    subprocess.call("python3 Limit.py {}".format(i),shell=True)
    break


