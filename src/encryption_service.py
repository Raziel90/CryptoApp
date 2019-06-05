import getopt
import logging
import sys

import tornado.ioloop
import tornado.web
from ServiceHandlers.CryptoRequestHandlers import TextRequestHandler, FileRequestHandler


def main(argv):
    # default values
    port = 8881
    logfolder = '../log'
    uploadpath = './uploads/'

    opts = []
    try:
        opts, args = getopt.getopt(argv, "hp:u:l", ["port", "upload-folder", "logfile"])
    except getopt.GetoptError as err:
        print(str(err))
        exit(-1)

    for o, a in opts:

        if o in ('-p', '--port'):
            port = a
        elif o in ('-l', '--logfile'):
            logfolder = a
        elif o in ('-u', '--upload-folder'):
            uploadpath = a
        else:
            assert False, "unhandled option!"

    logging.basicConfig(filename=logfolder, level=logging.DEBUG)

    app = tornado.web.Application([
        (r"/", TextRequestHandler),
        (r"/FileCrypt", FileRequestHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": uploadpath})
    ])

    app.listen(port)
    logging.info('-' * 100)
    logging.info('Listening on port: ' + str(port))
    logging.info('logging in: ' + logfolder)
    logging.info('tmp files saved in: ' + uploadpath)
    logging.info('-' * 100)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main(sys.argv[1:])
