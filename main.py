from queue import Queue
from watcher import Observer
from worker import Worker
import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler


if __name__ == '__main__':
    path = '.'
    q = Queue()
    list_thead = []
    list_thead += [Worker(q, i) for i in range(4)]
    list_thead += [Observer(q, path), ]
    for thead in list_thead:
        thead.start()
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


