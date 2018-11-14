import io


try:
    from gzip import compress
except ImportError:
    from gzip import GzipFile

    def compress(data, compresslevel=9):
        buf = io.BytesIO()
        with GzipFile(fileobj=buf, mode="wb", compresslevel=compresslevel) as f:
            f.write(data)
        return buf.getvalue()
