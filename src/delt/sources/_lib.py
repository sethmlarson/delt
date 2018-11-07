from ._base import DataSource


class LibrarySource(DataSource):
    pass


class OpenSSLSource(DataSource):
    key_prefix = "openssl"
    display_name = "OpenSSL"

    def is_active(self):
        return self.check_call("openssl version")

    def get_values(self):
        return {
            "version": self.get_from_popen("openssl version", pattern=r"OpenSSL\s+([\d\.a-zA-F]+)")
        }
