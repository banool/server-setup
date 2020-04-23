import asyncio
import argparse
import json
import sys
import urllib.request


VARS_FILE = "vars.json"


async def check_site(url):
    if not url.startswith("http://"):
        url = f"http://{url}"
    try: 
        ret = urllib.request.urlopen(url)
        code = ret.status
    except urllib.error.HTTPError as e:
        code = e.code
    return url, code


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", nargs="*")
    parser.add_argument("--read-from-vars", action="store_true")
    args = parser.parse_args()

    if args.read_from_vars:
        with open(VARS_FILE, "r") as f:
            d = json.load(f)
            args.urls = [d["domains"]]

    urls = set()
    for u in args.urls:
        urls |= set(u.split(","))

    tasks = [check_site(url) for url in urls]
    ret = await asyncio.gather(*tasks)

    bad = [(url, code) for url, code in ret if code >= 400 and code != 401]
    for url, code in bad:
        print(f"{code} {url}")

    return bad


sys.exit(1) if asyncio.run(main()) else sys.exit(0)

