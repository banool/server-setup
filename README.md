# Server Setup
The plan of this repo is to set up all of my websites and services with Docker and Ansible. I have done automated server set up before in [my previous server-setup](https://github.com/banool/server-setup-old) repo, but that was all just janky shell scripts. Here we go!

## Most useful resources
- https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html
  - Especially the part about listening to generic topics.

## Expected conditions of the remote server to begin with
- A user called `daniel` with sudo power exists with SSH key based access already set up

## Roles
```
ansible-galaxy install nginxinc.nginx
```

## Run these commands on the control host
```
export ANSIBLE_CONFIG=ansible.cfg
ansible-playbook --ask-become-pass -i hosts everything.yaml --extra-vars "@vars.json"
```

Deprecated:
```
mkdir ~/bin
export PATH="$PATH:~/bin"
brew install mysql-client
echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.bash_profile
. ~/.bash_profile
```


