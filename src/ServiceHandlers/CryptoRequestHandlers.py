import logging
import os

import tornado.web
from Cypher.Cypher import CypherAES, Random


class FileRequestHandler(tornado.web.RequestHandler):
    BASE_CHUNK = 16

    def get(self, *args, **kwargs):
        logging.info(self.request)
        self.render('./html/fileenc.html')

    def post(self):

        # ... maybe add a check that checks whether the user is allowed to upload anything ...
        # the file(s) that should get uploaded
        files = []
        # check whether the request contains files that should get uploaded
        uploadfol = './uploads'
        password = self.get_body_argument("pass")
        method = self.get_body_argument("act")
        try:
            if not os.path.exists(uploadfol):
                os.makedirs(uploadfol)
            files = self.request.files['files']
        except Exception as FileError:
            logging.error(FileError)
            pass
        # for each file that should get uploaded
        for xfile in files:
            # get the default file name
            file = xfile['filename']
            # the filename should not contain any "evil" special characters
            # basically "evil" characters are all characters that allows you to break out from the upload directory
            index = file.rfind(".")
            filename = file[:index].replace(".", "") + '(' + method + 'ed)' + file[index:]
            filename = filename.replace("/", "")
            try:
                if method == 'encrypt':
                    self.__encrypt__(filename, xfile['body'], password)
                elif method == 'decrypt':
                    self.__decrypt__(filename, xfile['body'], password)
            except Exception as CryptoException:
                logging.error(CryptoException)
                raise CryptoException
            finally:
                self.finish()

    def __encrypt__(self, filename, data, password):

        # save the file in the upload folder
        with open("uploads/%s.bin" % (filename.split('.')[0]), "bw") as outfile:
            # Be aware, that the user may have uploaded something evil like an executable script ...
            # so it is a good idea to check the file content (xfile['body']) before saving the file

            IV = Random.new().read(16)
            filesize = str(len(data)).zfill(16)

            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)
            if len(filename.split('.')) > 1:
                extension = filename.split('.')[-1].encode('utf-8')
                extension += b' ' * (16 - (len(extension) % 16))
                outfile.write(extension)
            else:
                outfile.write(" " * 16)
            cypher = CypherAES(password)
            cyphertext = cypher.encrypt_text(data, IV)
            logging.info('filesize:    ' + str(len(cyphertext)))

            outfile.write(cyphertext)
        self.write('Success!')
        self.write('http://localhost:8881/' + "static/%s.bin" % (filename.split('.')[0]))
        self.redirect("../static/%s.bin" % (filename.split('.')[0]))

    def __decrypt__(self, filename, data, password):

        filesize = int(data[0:self.BASE_CHUNK])
        IV = data[self.BASE_CHUNK: 2 * self.BASE_CHUNK]
        extension = data[2 * self.BASE_CHUNK: 3 * self.BASE_CHUNK].decode().rstrip()
        # print(extension)
        # save the file in the upload folder
        with open("uploads/%s.%s" % (filename.split('.')[0], extension), "bw") as outfile:
            # Be aware, that the user may have uploaded something evil like an executable script ...
            # so it is a good idea to check the file content (xfile['body']) before saving the file

            cypher = CypherAES(password)
            cyphertext = cypher.decrypt_text(data[3 * self.BASE_CHUNK:], IV)
            logging.info('filesize:    ' + str(len(cyphertext)))
            outfile.write(cyphertext)
            self.write('Success!')
            self.write("../static/%s.bin" % (filename.split('.')[0]))
            self.redirect("../static/%s.%s" % (filename.split('.')[0], extension))


class TextRequestHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        logging.info(self.request)
        self.render('./html/textenc.html')

    def post(self):

        self.set_header("Content-Type", "application/octet-streamSection")
        text = self.get_body_argument("text")
        password = self.get_body_argument("pass")
        action = self.get_body_argument("act")

        cypher = CypherAES(password)
        # self.write("You are going to " + action + " " + text)
        # self.write('\n')
        # self.write("using " + password)
        logging.info('*' * 100)
        logging.info(self.request)
        logging.info(('text', self.get_body_arguments('text')))
        logging.info(('action', self.get_body_arguments('act')))
        if action == 'encrypt':
            print('Encrypting:')
            print(cypher.encrypt_text(text))
            # self.write(cypher.encrypt_text(text))

        elif action == 'decrypt':
            print('Decrypting:')
            print(cypher.decrypt_text(text.encode()))
            # self.write(cypher.decrypt_text(text.encode('ascii')))
