from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode('utf-8'))

        question_database = data["question_database"]
        return_format = data["return_format"]
        unmarked_csv = data["unmarked_csv"]

        # 返回响应
        self.send_response(200)
        self.end_headers()


        # 这里放大模型的代码


        # response_string是经过大模型打分后的csv文件
        response_string = "This is the response from the server."
        # 返回打分后的csv文件
        self.wfile.write(response_string.encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()