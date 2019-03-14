# microservice-tutorial
A simple tutorial on microservices leveraging Docker, Ansible, and Python/flask

# Documentation
* Check out the Github wiki: https://github.com/charlesj68/microservice-tutorial/wiki

# Setup
The tutorial has been tested on Ubuntu 18.04. 
Assuming starting from a fresh install the following packages must be 
present to provide a working environment for this tutorial:
1. `sudo apt-get install git`
2. `sudo apt-get install docker.io`
   * If you just installed docker then make sure your user is a member of
   the docker group to avoid having to prefix every docker command invocation
   with `sudo`:
   `sudo usermod -a -G docker $USER`
   * Logout and back in to get group membership change to take effect. Simply
   closing the terminal window and opening a new one is not sufficient!
3. `sudo apt-get install ansible`
4. `sudo apt-get install python-dockerpty`
5. `sudo -H apt-get install openssh-server`
6. Set up ssh so that your user can ssh into localhost without a password. Ansible
   utilizes this functionality when it runs.
    * Reference: https://www.linuxbabe.com/linux-server/setup-passwordless-ssh-login

# Running
1. `git clone https://github.com/charlesj68/microservice-tutorial`
2. `cd microservice-tutorial`
3. `ansible-playbook -i hosts playbook.yaml`
