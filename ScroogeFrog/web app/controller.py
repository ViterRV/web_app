from http.server import BaseHTTPRequestHandler
import urllib.parse
import socketserver
from model import create_profile, db_start, read_db, delete, update
from jinja2 import Environment, FileSystemLoader

def generate_profiles_html(profiles,template_file):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)
    return template.render(profiles=profiles)

def set_header(func):
    def wrapper(self, *args, **kwargs):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        func(self, *args, **kwargs)
    return wrapper

def check_id(id):
    profiles = read_db()
    for profile in profiles:
        if str(profile[0]) == id:
            return True
    return False

class MyHandler(BaseHTTPRequestHandler):

    @set_header
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if self.path == '/':
            with open('templates/view.html', 'rb') as file:
                content = file.read()
            self.wfile.write(content)

        elif self.path.startswith('/create'):
            with open('templates/create.html', 'rb') as file:
                content = file.read()
            self.wfile.write(content)

        elif self.path.startswith('/update'):
            profiles = read_db()
            profiles_html = generate_profiles_html(profiles, 'templates/update.html')
            self.wfile.write(profiles_html.encode('utf-8'))

        elif self.path.startswith('/read'):
            sort_param = query_params.get('sort', [''])[0]
            profiles = read_db()

            if sort_param == 'name':
                profiles = read_db(order_by='name')
            elif sort_param == 'email':
                profiles = read_db(order_by='email')

            profiles_html = generate_profiles_html(profiles, 'templates/read.html')
            self.wfile.write(profiles_html.encode('utf-8'))

        elif self.path.startswith('/delete'):
            profiles = read_db()
            profiles_html = generate_profiles_html(profiles, 'templates/delete.html')
            self.wfile.write(profiles_html.encode('utf-8'))

        elif self.path.startswith('/error'):
            with open('templates/error.html', 'rb') as file:
                content = file.read()
            self.wfile.write(content)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)

        action = parsed_data.get('action', [''])[0]

        if action == 'create':
            name = parsed_data.get('name', [''])[0]
            email = parsed_data.get('email', [''])[0]
            phone = parsed_data.get('phone', [''])[0]
            if not name or not email or not phone:
                self.send_response(303)
                self.send_header('Location', '/error')
                self.end_headers()
                return

            elif '@' not in email:
                self.send_response(303)
                self.send_header('Location', '/error')
                self.end_headers()

            else:
                create_profile(contact_name=name, email=email, phone_number=phone)
                self.send_response(303)
                self.send_header('Location', '/create')
                self.end_headers()

        if action == 'read':
            profiles = read_db()
            profiles_html = generate_profiles_html(profiles, 'templates/read.html')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(profiles_html.encode('utf-8'))

        if action == 'update':
            id = parsed_data.get('id', [''])[0]
            name = parsed_data.get('name', [''])[0]
            email = parsed_data.get('email', [''])[0]
            phone = parsed_data.get('phone', [''])[0]

            if not check_id(id):
                self.send_response(303)
                self.send_header('Location', '/error')
                self.end_headers()
                return

            if not name or not email or not phone:
                self.send_response(303)
                self.send_header('Location', '/error')
                self.end_headers()
                return

            elif '@' not in email:
                self.send_response(303)
                self.send_header('Location', '/error')
                self.end_headers()
            else:
                update(id, name, email, phone)
                profiles = read_db()
                profiles_html = generate_profiles_html(profiles, 'templates/update.html')
                self.send_response(303)
                self.send_header('Location', '/update')
                self.end_headers()
                self.wfile.write(profiles_html.encode('utf-8'))

        if action == 'delete':
            id = parsed_data.get('id', [''])[0]
            delete(id)
            profiles = read_db()
            profiles_html = generate_profiles_html(profiles, 'templates/delete.html')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(profiles_html.encode('utf-8'))

if __name__ == '__main__':
    db_start()
    PORT = 8000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server started at http://localhost:8000")
        httpd.serve_forever()
