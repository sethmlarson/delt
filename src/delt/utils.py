from six.moves.urllib.parse import urljoin as urllib_urljoin


def urljoin(base, *parts):
    for part in parts:
        base = urllib_urljoin(base, part)
    return base
