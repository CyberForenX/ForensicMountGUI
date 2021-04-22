The first thing that needs to be done is the installation of xmount(https://www.pinguin.lu/xmount), leveraging the following commands below:

sudo wget -P /etc/apt/sources.list.d/ http://deb.pinguin.lu/pinguin.lu.list
wget -q http://deb.pinguin.lu/debsign_public.key -O- | sudo apt-key add -
sudo apt-get update
sudo apt-get install xmount

With xmount installed Python 3.8 needs to be installed on the Linux machine being leveraged, to do this the following commands can be ran:

sudo apt-get update
sudo apt-get install python3.8

Now that Python 3.8 is installed, then the respective libraries for the tool need to be installed. To do this the following command can be ran with the requirements.txt file:

pip3 install -r requirements.txt

Everything should now be installed, finally to run the tool the following can be ran:

Python3 MountingGUI.py
