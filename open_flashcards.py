import http.server
import socketserver
import webbrowser
import threading
import time
from pathlib import Path
from typing import Any

DIRECTORY: Path = Path(__file__).parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

def main() -> None:
    """Starts a local HTTP server and opens the flashcards HTML page in the default web browser."""
    # Using port 0 lets the operating system automatically pick an available, unused port.
    with socketserver.TCPServer(("", 0), Handler) as httpd:
        port: int = httpd.server_address[1]
        url: str = f"http://localhost:{port}/flashcards.html"
        
        print(f"Serving flashcards at: {url}")
        print("Press Ctrl+C in this terminal to stop the server.")
        
        def open_browser() -> None:
            """Waits briefly for the server to start, then opens the web browser."""
            time.sleep(0.5)
            webbrowser.open(url)
            
        # Start a background thread to open the browser so we don't block the server
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()

if __name__ == "__main__":
    main()
