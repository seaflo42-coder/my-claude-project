#!/usr/bin/env python3
"""
한국 문화유산 AI 이미지 프롬프트 생성기 (웹 버전)

실행 방법:
    python web_generator.py

그러면 브라우저에서 http://localhost:8080 으로 접속하면 됩니다.
"""

import json
import os
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs
import threading

PORT = 8080
HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HTML_PATH, **kwargs)

    def log_message(self, format, *args):
        # 로그 간소화
        pass


def main():
    os.makedirs(HTML_PATH, exist_ok=True)
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║                                                      ║")
    print("║    한국 문화유산 AI 이미지 프롬프트 생성기            ║")
    print("║                                                      ║")
    print(f"║    브라우저에서 접속하세요:                            ║")
    print(f"║    http://localhost:{PORT}                             ║")
    print("║                                                      ║")
    print("║    종료하려면 Ctrl+C 를 누르세요                     ║")
    print("║                                                      ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()

    # 브라우저 자동 열기
    threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  서버를 종료합니다.")
        server.shutdown()


if __name__ == "__main__":
    main()
