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
        self.render('upload.html')

    def post(self):
        if 'file' in self.request.files.keys():
            for file in self.request.files['file']:
                image = Image.open(io.BytesIO(file['body']))
                image.save('images/' + file['filename'])

        self.write('uploading')


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        ("/", UploadHandler),
    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
