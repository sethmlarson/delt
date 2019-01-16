import io
import six


try:
    from gzip import compress
except ImportError:
    from gzip import GzipFile

    def compress(data, compresslevel=9):
        buf = io.BytesIO()
        with GzipFile(fileobj=buf, mode="wb", compresslevel=compresslevel) as f:
            f.write(data)
        return buf.getvalue()


def merge_dict(old, new):
    for name, value in six.iteritems(new):
        if name in old and old[name] != value:
            if isinstance(old[name], dict) and isinstance(value, dict):
                old[name] = merge_dict(old[name], value)
            else:
                raise ValueError("Could not merge dicts '%r' and '%r'" % (old, new))
        else:
            old[name] = value
    return old
