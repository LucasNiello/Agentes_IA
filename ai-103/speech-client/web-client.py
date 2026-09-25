from dotenv import load_dotenv
import json
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# import namespaces
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

HOST = "127.0.0.1"
PORT = 8000
PAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "index.html")


def main():
    # Get Configuration Settings
    load_dotenv()
    foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')
    agent_name = os.getenv('AGENT_NAME')

    # Get project client
    project_client = AIProjectClient(
        endpoint=foundry_endpoint,
        credential=DefaultAzureCredential(),
    )

    # Get an OpenAI client
    openai_client = project_client.get_openai_client()

    class Handler(BaseHTTPRequestHandler):
        def _send(self, status, body, content_type):
            data = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                with open(PAGE, encoding="utf-8") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            elif self.path == "/api/info":
                self._send(200, json.dumps({"agent": agent_name}), "application/json")
            else:
                self._send(404, "Not found", "text/plain")

        def do_POST(self):
            if self.path != "/api/ask":
                self._send(404, "Not found", "text/plain")
                return
            try:
                length = int(self.headers.get("Content-Length", 0))
                prompt = json.loads(self.rfile.read(length) or b"{}").get("prompt", "").strip()
                if not prompt:
                    self._send(400, json.dumps({"error": "Prompt vazio."}), "application/json")
                    return

                # Use the agent to get a response
                response = openai_client.responses.create(
                    input=[{"role": "user", "content": prompt}],
                    extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
                )
                self._send(200, json.dumps({"agent": agent_name, "text": response.output_text}), "application/json")
            except Exception as ex:
                self._send(500, json.dumps({"error": str(ex)}), "application/json")

        def log_message(self, format, *args):
            print(f"[{self.log_date_time_string()}] {format % args}")

    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}"
    print(f"Speech client web em {url}  (Ctrl+C para parar)")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
