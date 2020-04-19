# Server Setup
The plan of this repo is to set up all of my websites and services with Docker and Ansible. I have done automated server set up before in [my previous server-setup](https://github.com/banool/server-setup-old) repo, but that was all just janky shell scripts. Here we go!

## How to use
Firstly, you need to set a million variables in vars.json. See fake_vars.json to see what kvs you need.

```
pipenv install
pipenv shell
export ANSIBLE_CONFIG=ansible.cfg
ansible-playbook -i hosts everything.yaml --extra-vars "@vars.json"
ansible-playbook -i hosts interactive.yaml 
```
If you want to make your life easier for developing this, throw this in: `--extra-vars='ansible_become_pass=<sudopassword>`.

Similarly, this playbook will make testing and whatnot easier (it opens ports to the control host):
```
ansible-playbook -i hosts open_dev_ports.yaml
```

**Note:** To make this production ready, make sure to set development_mode to prod in vars.json

## Most useful resources
- https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html
  - Especially the part about listening to generic topics.

## Expected conditions of the remote server to begin with
- A user called `daniel` with sudo power exists with SSH key based access already set up

