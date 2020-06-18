"""
Script to update containers.

Sample output:

These containers are up to date:
  docker.pkg.github.com/banool/team_heist_tactics/team_heist_tactics:latest
  quay.io/banool/comp30023-assn2:latest
  quay.io/banool/gomogo:latest
  quay.io/banool/diary-django:latest
  docker.pkg.github.com/banool/amaranta_candles/amaranta_candles_server:latest
  quay.io/banool/pants:latest
  quay.io/banool/trapwords:latest
  quay.io/banool/codenames-pictures:latest
  quay.io/banool/safecycle:latest
  docker.pkg.github.com/banool/amaranta_candles/amaranta_candles_ui:latest
These containers are out of date:
  quay.io/banool/net-worth:latest
Restarting containers that are out of date...
  [DRY-RUN] Would run: systemctl --user restart net-worth
Done!
"""

import argparse
import os
import subprocess

SYSTEMD_UNIT_DIR = "/home/daniel/.config/systemd/user"

parser = argparse.ArgumentParser()
parser.add_argument("--do-not-restart-containers", action="store_true")
parser.add_argument("--do-not-pull-images", action="store_true")
args = parser.parse_args()

# Get current version of each container running
out = subprocess.check_output(
    'podman container ls --format "{{.Image}} {{.ImageID}}"', shell=True
)
out = out.decode("utf-8")
name_to_current_version = {}
for l in out.splitlines():
    name_to_current_version[l.split()[0]] = l.split()[1]

longest_version_str = max(len(v) for v in name_to_current_version.values())

# Pull all the images
if not args.do_not_pull_images:
    for name in name_to_current_version.keys():
        subprocess.check_output("podman pull " + name, shell=True)

# Get latest version of those containers
name_to_latest_version = {}
for name in name_to_current_version.keys():
    latest_version = subprocess.check_output(
        'podman inspect --format "{{.Id}}" ' + name, shell=True
    )
    latest_version = latest_version.decode("utf-8")
    name_to_latest_version[name] = latest_version

up_to_date = []
out_of_date = []
# Check which containers are out of date
for name, current_version in name_to_current_version.items():
    latest_version = name_to_latest_version[name][:longest_version_str]
    if current_version == latest_version:
        up_to_date.append(name)
    else:
        out_of_date.append(name)

# Print containers that are up to date
print("These containers are up to date:")
for name in up_to_date:
    print("  " + name)

print()

# Print containers that are out of date
if out_of_date:
    print("These containers are out of date:")
    for name in out_of_date:
        print("  " + name)
else:
    print("No containers are out of date!")

print()

# Finally, restart containers that are out of date
systemd_unit_names = list(os.listdir(SYSTEMD_UNIT_DIR))
systemd_unit_names = [s for s in systemd_unit_names if s.endswith(".service")]

systemd_unit_name_overrides = {
    "quay.io/banool/comp30023-assn2:latest": "mastermind",
}
if out_of_date:
    print("Restarting containers that are out of date...")
for name in out_of_date:
    # Look up the systemd unit name from the container name by using the
    # overrides dict. If it's not in there, assume the unit name is the
    # container name, replacing underscores for hyphens.
    try:
        systemd_unit_name = systemd_unit_name_overrides[name]
    except KeyError:
        systemd_unit_name = name.split("/")[-1].split(":")[0].replace("_", "-")
    command = "systemctl --user restart " + systemd_unit_name
    if not args.do_not_restart_containers:
        print("  Running " + command)
        subprocess.check_output(command, shell=True)
    else:
        print("  [DRY-RUN] Would run: " + command)

if out_of_date:
    print()
print("Done!")
