import os

DIR = "templates/nginx/"
SERVER_NAME = "dport.me"

files = os.listdir(DIR)

files = [fname for fname in files if fname.endswith("j2")]

all_sites = []
for fname in files:
    with open(os.path.join(DIR, fname), "r") as f:
        content = f.read().splitlines()
    l = [l for l in content if "server_name" in l][0]
    l = l.replace("{{ ", "{{").replace(" }}", "}}").replace(";", "")
    sites = l.split()
    sites = [s.replace("{{server_name}}", SERVER_NAME) for s in l.split()]
    sites = [s for s in sites if SERVER_NAME in s]
    all_sites += sites

print(",".join(all_sites))
