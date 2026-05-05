import hashlib
import os

secret = os.getenv("DNB_ROS_RUNTIME_SECRET")

client = "anyrobot-lib"
dest = "ros"
rand = "<random-value>"
timestamp = 0
level = "admin"
end = 0

raw = secret + client + dest + rand + str(timestamp) + level + str(end)
mac = hashlib.sha512(raw.encode()).hexdigest()

auth_msg = {
    "op": "auth",
    "client": client,
    "dest": dest,
    "end": end,
    "level": level,
    "mac": mac,
    "rand": rand,
    "t": timestamp,
}
