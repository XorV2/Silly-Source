echo "Setting up yo shit"
echo "This setup is made for ubuntu, if you're not on ubuntu it won't work for you"

apt-get update -y && apt-get upgrade -y && apt-get update -y
apt-get install python3 -y
apt-get install python3-pip -y
apt-get install ufw

# These should be installed automatically when you install python3, but just in-case
pip3 install socket
pip3 install json
pip3 install time
pip3 install random
pip3 install sys
pip3 install requests
pip3 install threading
pip3 install datetime

# This will allow your server to accept port on the default tcp port for Silly Source 1337
iptables -t mangle -I PREROUTING -p tcp --dport 1337 -j ACCEPT
ufw enable
ufw allow 1337/tcp
ufw reload

echo "Done."
