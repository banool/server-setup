import asyncio
import argparse
import functools
import json
import sys
import urllib.request


VARS_FILE = "vars.json"


async def check_site(url, debug=False):
    if not url.startswith("http://"):
        url = f"http://{url}"
    try: 
        loop = asyncio.get_event_loop()
        f = functools.partial(urllib.request.urlopen, timeout=15)
        ret = await loop.run_in_executor(None, f, url)
        code = ret.status
        if debug:
            print("Success", ret.url)
    except urllib.error.HTTPError as e:
        code = e.code
        if debug:
            print("HTTPError:", e)
    except urllib.error.URLError as e:
        # Timeout
        code = 999
        if debug:
            print("URLError (timeout):", e)
    return url, code


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", nargs="*")
    parser.add_argument("--read-from-vars", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    if not args.urls and not args.read_from_vars:
        print("Please pass either --urls or --read-from-vars")
        sys.exit(1)

    if args.read_from_vars:
        with open(VARS_FILE, "r") as f:
            d = json.load(f)
            args.urls = [d["domains"]]

    urls = set()
    for u in args.urls:
        urls |= set(u.split(","))

    tasks = [check_site(url, debug=args.debug) for url in urls]
    ret = await asyncio.gather(*tasks)

    bad = [(url, code) for url, code in ret if code >= 400 and code != 401]
    for url, code in bad:
        print(f"{code} {url}")

    return bad


sys.exit(1) if asyncio.run(main()) else sys.exit(0)

