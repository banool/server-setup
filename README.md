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

To update the containers:
```
ansible-playbook -i hosts containers.yaml
```

To check that your sites are up, use this:
```
python3 check.py --read-from-vars
```

To get notified at 10am every day if one of the sites is down, put something like this in your crontab:
```
#!/bin/bash

MAILTO=""

0 10 * * * $HOME/.bash_profile; cd /Users/dport/github/server-setup && output=`python3 check.py --read-from-vars` || bash -c 'printf "$output" > /tmp/broken_sites && /usr/local/bin/terminal-notifier -title "Some of your sites are broken" -message "$output" -open file:///tmp/broken_sites'
```

**Note:** To make this production ready, make sure to set development_mode to prod in vars.json

## Most useful resources
- https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html
  - Especially the part about listening to generic topics.

## Expected conditions of the remote server to begin with
- A user called `daniel` with sudo power exists with SSH key based access already set up

## Other useful stuff
See the `/sys/` related answer [at this link](https://askubuntu.com/questions/149054)
to decrease the brightness / turn off the screen.

There is a bug with podman and slirp4netns right now. To fix it, see this comment: https://github.com/containers/libpod/issues/5420#issuecomment-603355711.

If you use the systemd file generated by podman, you can't see the logs in journalctl. Instead, don't use forking mode and don't use `-d`: https://github.com/containers/libpod/issues/4720#issuecomment-567334627.

Make sure to put something in the root crontab that mounts your exeternal harddrive if you have attached.

Make sure to tigthen up the SSH login config
