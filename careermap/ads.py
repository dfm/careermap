import os
import redis
import requests
import lxml.html

ads_api_url = "http://adslabs.org/adsabs/api/search/"
ads_html_url = "http://labs.adsabs.harvard.edu/adsabs/abs/"

rdb = redis.Redis()


def get_dev_key():
    # Credit: Andy Casey
    ads_dev_key_filename = os.path.abspath(
        os.path.expanduser("~/.ads/dev_key"))

    if os.path.exists(ads_dev_key_filename):
        with open(ads_dev_key_filename, "r") as fp:
            dev_key = fp.readline().rstrip()

        return dev_key

    dev_key = os.environ.get("ADS_DEV_KEY", None)
    if dev_key is None:
        raise IOError("no ADS API key found in ~/.ads/dev_key")
    return dev_key


def get_author_locations(author, return_json=False):
    name = sorted([a.strip() for a in author.split(",")], reverse=True,
                  key=lambda n: len(n))[0].lower()

    params = {
        "q": "author:{0}".format(author),
        "dev_key": get_dev_key(),
        "rows": 200,
        "filter": "database:astronomy",
        "fl": "bibcode,year",
    }
    response = requests.post(ads_api_url, params=params)
    if response.status_code != requests.codes.ok:
        response.raise_for_status()

    codes = response.json().get("results", {}).get("docs", None)
    if codes is None:
        return []

    results = [(el.get("bibcode"), el.get("year")) for el in codes]

    affils = []
    for code, year in results:
        text = rdb.get("career:{0}".format(code))
        if text is None:
            url = ads_html_url + code
            r = requests.get(url)
            if r.status_code != requests.codes.ok:
                r.raise_for_status()
            text = r.text
            rdb.set("career:{0}".format(code), text)

        tree = lxml.html.fromstring(text)
        for author in tree.find_class("author"):
            if name in author.find_class("authorName")[0].text.lower():
                a = author.find_class("authorAffiliation")
                if len(a):
                    affils.append((int(year), a[0].text.strip("()").strip()))
                    break

    return affils


if __name__ == "__main__":
    print(get_author_locations("foreman-mackey"))
