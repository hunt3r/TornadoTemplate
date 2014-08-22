#!/usr/bin/env python
import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.web
from tornado.options import options
from fabric.colors import green, red
from settings import settings
from url_patterns import url_patterns

class App(tornado.web.Application):

    def __init__(self):
        """App wrapper constructor, global objects within our Tornado platform should be managed here."""
        self.logger = logging.getLogger(self.__class__.__name__)

        tornado.web.Application.__init__(self, url_patterns, **settings)


# The app variable is used via module import into gunicorn, thus the module scope
# It is also used below in standalone mode using the standard tornado http server in
# the main method below.
app = App()

def main():
    """Main function for running stand alone"""

    logger = logging.getLogger()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)

    logger.info(green('Tornado server started on port %s' % options.port))

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.info(red("\nStopping server on port %s" % options.port))

if __name__ == "__main__":
    main()