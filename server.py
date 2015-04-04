import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from PIL import Image
import io

define("port", default=8889, help="run on the given port", type=int)


class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/upload.html')

    def post(self):
        if 'file' in self.request.files.keys():
            for file in self.request.files['file']:
                image = Image.open(io.BytesIO(file['body']))
                image.save('images/' + file['filename'])

        self.write('uploading')

class IcemanHandler(tornado.web.RequestHandler):
    def get(self):
        """serve the Iceman for now, other stuff later"""
        f = Image.open('images/iceman.jpg')
        o = io.BytesIO()
        f.save(o, format="JPEG")
        s = o.getvalue()
        self.set_header('Content-type', 'image/jpg')
        self.set_header('Content-length', len(s))
        self.write(s)

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        ("/", UploadHandler),
        ('/iceman', IcemanHandler),
    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
