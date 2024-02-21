import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import json
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="notesdb"
)
cursor = db.cursor()


def delete_note(note_id):
    cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    db.commit()
    return {"message": "Note deleted successfully"}


def update_note(note_id, title, content):
    cursor.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s", (title, content, note_id))
    db.commit()
    return {"message": "Note updated successfully"}


def add_note(title, content):
    cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
    db.commit()
    return {"message": "Note added successfully"}


def get_note(note_id):
    cursor.execute("SELECT * FROM notes WHERE id = %s", (note_id,))
    note = cursor.fetchone()
    if note:
        return {"id": note[0], "title": note[1], "content": note[2]}
    else:
        return None


def get_notes():
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    return [{"id": note[0], "title": note[1], "content": note[2]} for note in notes]


# HTTP request handler
class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self, status=200, content_type='text/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        params = parse_qs(parsed_path.query)

        if path == '/notes':
            self._set_response()
            self.wfile.write(json.dumps(get_notes()).encode())
        elif path == '/note' and 'id' in params:
            note_id = params['id'][0]
            self._set_response()
            self.wfile.write(json.dumps(get_note(note_id)).encode())
        else:
            self._set_response(404, 'text/plain')
            self.wfile.write("Not Found".encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        if 'title' in data and 'content' in data:
            self._set_response()
            self.wfile.write(json.dumps(add_note(data['title'], data['content'])).encode())
        else:
            self._set_response(400, 'text/plain')
            self.wfile.write("Bad Request".encode())

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        data = json.loads(put_data.decode())

        if 'id' in data and ('title' in data or 'content' in data):
            self._set_response()
            self.wfile.write(json.dumps(update_note(data['id'], data['title'], data['content'])).encode())
        else:
            self._set_response(400, 'text/plain')
            self.wfile.write("Bad Request".encode())

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        params = parse_qs(parsed_path.query)

        if path == '/note' and 'id' in params:
            note_id = params['id'][0]
            self._set_response()
            self.wfile.write(json.dumps(delete_note(note_id)).encode())
        else:
            self._set_response(404, 'text/plain')
            self.wfile.write("Not Found".encode())


# Run the server
if __name__ == "__main__":
    PORT = 8000
    handler = MyRequestHandler
    httpd = socketserver.TCPServer(("0.0.0.0", PORT), handler)
    print(f"Server running on port {PORT}")
    httpd.serve_forever()
