# tested as "other" logger aggregator type
# http://127.0.0.1:9200/test/_doc/
# http/https

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

LOG_FILE = "logs.txt"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/test/_doc/":
            content_length = int(self.headers["Content-Length"])  # Get the size of the POST data
            post_data = self.rfile.read(content_length).decode("utf-8")  # Read and decode the request body

            # Write the request body to a file
            with open(LOG_FILE, "a") as file:
                file.write(post_data + "\n")

            # Send a success response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Data received"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    server_address = ("", 9200)  # Listen on port 9200
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f"Server running on port {server_address[1]}...")
    httpd.serve_forever()
