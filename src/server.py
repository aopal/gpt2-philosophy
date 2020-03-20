import sys
import gpt_2_simple as gpt2
import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler

def textGenHandler(request):
    try:
        # print(request.headers)
        content_length = int(request.headers.get('Content-Length', '0'))
        body = request.rfile.read(content_length)
        prefix = body.decode('utf-8')

        response_text = gpt2.generate(sess, prefix=prefix, model_name=model_name, length=50, return_as_list=True)[0]
        response_text += "\n"
        response_bytes = response_text.encode('utf-8')

        request.send_response(200)
        request.end_headers()
        request.wfile.write(response_bytes)
    except:
        request.send_response(500)
        request.end_headers()
        request.wfile.write(b'An unexpected error occured')

def rootHandler(request):
    request.send_response(200)
    request.end_headers()
    request.wfile.write(index_html)

def notFoundHandler(request):
    request.send_response(404)
    request.end_headers()
    request.wfile.write(b'Not Found\n')

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        handler = routes.get(self.path, notFoundHandler)
        handler(self)
    
    def do_POST(self):
        handler = routes.get(self.path, notFoundHandler)
        handler(self)

PORT = int(sys.argv[1])
model_name = "124M"

f = open("src/index.html", "rb")
index_html = f.read() 
f.close()

routes = {
    "/": rootHandler,
    "/gpt": textGenHandler,
    "/gpt/": textGenHandler
}

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, model_name=model_name)

httpd = HTTPServer(("", PORT), RequestHandler)
httpd.serve_forever()

###########

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, model_name=model_name)

print("\n----------MODEL OUTPUT----------\n")
single_text = gpt2.generate(sess, model_name=model_name, length=50, return_as_list=True)[0]
print(single_text)
