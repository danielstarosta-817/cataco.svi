#!/usr/bin/env python3
"""
Serve the Puerto Rico SVI Tool over localhost so census tract data loads correctly.
file:// pages can't make external requests in Chrome; localhost has no such restriction.

Run this script, then open the URL it prints.
Press Ctrl+C to stop.
"""
import http.server
import os
import webbrowser

PORT = 8080
FILE = "index.html"

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # quiet

url = f"http://localhost:{PORT}/{FILE}"
print(f"\n  Puerto Rico SVI Tool → {url}\n")
print("  Press Ctrl+C to stop.\n")

try:
    webbrowser.open(url)
except Exception:
    pass

with http.server.HTTPServer(("localhost", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
