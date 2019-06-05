import os

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


class CypherAES:

    def __init__(self, password: str):
        self.chunksize = 64 * 1024
        self.__hasher = SHA256.new(password.encode('utf-8'))

    def __getKey(self):
        return self.__hasher.digest()

    def encrypt_text(self, data, IV='0' * 16) -> bytes:
        key = self.__getKey()
        if type(data) != bytes:
            data = data.encode()
        encryptor = AES.new(key, AES.MODE_CBC, IV)
        chunksize = 64 * 1024
        cyphertext = bytes()
        for i in range(int(len(data) / chunksize) + 1):
            chunk = data[i * chunksize:min((i + 1) * chunksize, len(data))]
            if len(chunk) % 16 != 0:
                chunk += b' ' * (16 - (len(chunk) % 16))
            cyphertext += encryptor.encrypt(chunk)
        return cyphertext

    def decrypt_text(self, cyphertext: bytes, IV='0' * 16) -> str:
        key = self.__getKey()
        decryptor = AES.new(key, AES.MODE_CBC, IV)
        chunksize = 64 * 1024
        retext = bytes()
        for i in range(int(len(cyphertext) / chunksize) + 1):
            chunk = cyphertext[
                    i * chunksize:
                    min((i + 1) * chunksize, len(cyphertext))]
            retext += decryptor.decrypt(chunk)
        return retext

    def encrypt_file(self, filename):

        key = self.__getKey()
        outputfile = '(encrypted) ' + filename.split('/')[-1]
        filesize = str(os.path.getsize(filename=filename)).zfill(16)
        IV = Random.new().read(16)
        encryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(filename, 'rb') as infile:
            with open(outputfile, 'wb') as outfile:
                outfile.write(filesize.encode('utf-8'))
                outfile.write(IV)
                while True:
                    chunk = infile.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (len(chunk) % 16))  # padding
                    outfile.write(encryptor.encrypt(chunk))

    def decrypt_file(self, filename):

        key = self.__getKey()
        outputfile = '(decrypted)' + filename.split('/')[-1].lstrip('(encrypted)')
        with open(filename, 'rb') as infile:
            filesize = int(infile.read(16))
            IV = infile.read(16)

            decryptor = AES.new(key, AES.MODE_CBC, IV)

            with open(outputfile, 'wb') as outfile:

                while True:
                    chunk = infile.read(self.chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (len(chunk) % 16))  # padding
                    outfile.write(decryptor.decrypt(chunk))
                    outfile.truncate(filesize)


if __name__ == '__main__':
    text = "\t\tKain: At last...  \n\
           I must say I'm disappointed in your progress. I imagined you would be here sooner. \n\
           Tell me - did it trouble you to murder your brothers? \n\
           Raziel slowly descends the stairway, keeping his eyes locked on Kain. \n\
           Raziel: \n\
           Did it trouble you when you ordered me into the Abyss?\n\
           Kain's only response is ironic laughter. He steps back toward one of the arcane dials and prepares to turn it.\n\
           Kain:\n\
           Eternity is relentless, Raziel. \n\
           When I first stole into this chamber, centuries ago, I did not fathom the true power of knowledge.\n\
           Kain throws the switch, and the Chronoplast device responds."

    cypher = CypherAES('banana')

    cyphertext = cypher.encrypt_text(text)
    retext = cypher.decrypt_text(cyphertext)

    print('The encryption and decryption of the algorithm worked: ', retext.rstrip() == text)
    print()
    print(retext)
