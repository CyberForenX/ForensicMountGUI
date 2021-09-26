**Warning:**

This product does have some limitations at the momment with the type of forensic images it can handle, for example:
- Any images that are of USB mass storage or mobile devices may have complications. I am not sure why but any feedback that can help would be appreciated.
- The size of the image doesnt seem to be too much of a problem, the only thing that happens is it may take a little bit to show as mounted. Reasoning behind this most likely comes from the hashing process.
- If the image is split into multiple segments this will not play well with that. Since this is becoming more common though due to the constent increase in forensic image size, any pointers towards how to do this would again be appreciated.
- This is a complete first build, but as shown there are extra features I would like to add and bugs that are present


**Installation:**

The first thing that needs to be done is the installation of xmount(https://www.pinguin.lu/xmount), leveraging the following commands below:

**sudo wget -P /etc/apt/sources.list.d/ http://deb.pinguin.lu/pinguin.lu.list**

**wget -q http://deb.pinguin.lu/debsign_public.key -O- | sudo apt-key add -**

**sudo apt-get update**

**sudo apt-get install xmount**

With xmount installed Python 3.8 needs to be installed on the Linux machine being leveraged, to do this the following commands can be ran:

**sudo apt-get update**

**sudo apt-get install python3.8**

Now that Python 3.8 is installed, then the respective libraries for the tool need to be installed. To do this the following command can be ran with the requirements.txt file:

**pip3 install -r requirements.txt**

Everything should now be installed, finally to run the tool the following can be ran:

**Python3 MountingGUI.py**
