import hashlib

def make_uid(title, date, link):
    raw = f"{title}|{date}|{link}".lower().encode("utf-8")
    return hashlib.md5(raw).hexdigest()
