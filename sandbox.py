import sys, http.server
from urllib.parse import urlparse, parse_qs

urls = {
    "https://github.com/PowerShell/PowerShell/releases/download/v7.4.1/PowerShell-7.4.1-win-x64.msi": "application/octet-stream",
    "https://github.com/Maximus5/ConEmu/releases/download/v23.07.24/ConEmuPack.230724.7z": "application/octet-stream",
    "https://www.7-zip.org/a/7zr.exe": "application/octet-stream",
    "https://raw.githubusercontent.com/PietJankbal/powershell-wrapper-for-wine/master/profile.ps1": "text/plain; charset=utf-8"
}

class SourcesSandbox(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        try:
            url = next(iter(query.get("url", [])))
        except StopIteration:
            self.send_error(400)
            return
        if url not in urls:
            self.send_error(404)
            return
        fname = url.rsplit("/", 1)[-1]
        with open(fname, 'rb') as fp:
            content = fp.read()

        self.send_response(200)
        self.send_header('content-type', urls[url])
        self.send_header('content-length', str(len(content)))
        self.send_header('content-disposition', f'attachment; filename={fname}')
        self.end_headers()
        self.wfile.write(content)

widen = lambda x: bytes(sum(([i, 0] for i in x), []))
placeholder = widen(b'http://127.0.0.1:00000?pad=&url=')

def padded(port):
    assert 0 < int(port) <= 65_535
    pad = 5 - len(str(port))
    res = widen(f"http://127.0.0.1:{port}?pad={'-' * pad}&url=".encode())
    assert len(res) == len(placeholder)
    return res

def patch(port):
    for arch in [32, 64]:
        with open(f"powershell{arch}.exe", 'rb') as fp:
            f = fp.read()
        with open(f"powershell{arch}_.exe", 'wb') as fp:
            fp.write(f.replace(placeholder, padded(port)))
    print(port)
    sys.stdout.flush()

def run_server():
    httpd = http.server.HTTPServer(('', 0), SourcesSandbox)
    patch(httpd.server_address[1])
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
