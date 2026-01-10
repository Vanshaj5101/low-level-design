"""
Http Request
"""


class HttpRequest:
    def __init__(self, builder):
        self.url = builder._url
        self.method = builder._method
        self.headers = builder._headers
        self.query_params = builder._query_params
        self.body = builder._body
        self.timeout = builder._timeout

    def __str__(self):
        return (
            f"HttpRequest(url={self.url}, method={self.method}, headers={self.headers}, "
            f"query_params={self.query_params}, body={self.body}, timeout={self.timeout})"
        )

    class Builder:
        def __init__(self, url):
            self._url = url
            self._method = "GET"
            self._headers = {}
            self._query_params = {}
            self._body = None
            self._timeout = 30000

        def method(self, method):
            self._method = method
            return self

        def add_header(self, key, value):
            self._headers[key] = value
            return self

        def add_query_param(self, key, value):
            self._query_params[key] = value
            return self

        def body(self, body):
            self._body = body
            return self

        def timeout(self, timeout):
            self._timeout = timeout
            return self

        def build(self):
            return HttpRequest(self)

if __name__ == "__main__":
    request1 = HttpRequest.Builder("https://api.example.com/data").build()

    request2 = (
        HttpRequest.Builder("https://api.example.com/submit")
        .method("POST")
        .body('{"key":"value"}')
        .timeout(15000)
        .build()
    )

    request3 = (
        HttpRequest.Builder("https://api.example.com/config")
        .method("PUT")
        .add_header("X-API-Key", "secret")
        .add_query_param("env", "prod")
        .body("config_payload")
        .timeout(5000)
        .build()
    )

    print(request1)
    print(request2)
    print(request3)
