## YOUR CODE HERE
import json

with open("vars.json", "r") as f:
    content = f.read()
    
d = json.loads(content)

def blah(d):
    for k, v in d.items():
        if isinstance(v, dict):
            blah(v)
        else:
            d[k] = "fake"

blah(d)

with open('fake_vars.json', 'w') as f:
    json.dump(d, f)
