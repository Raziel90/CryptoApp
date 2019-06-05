import os
import string
import unittest
from random import choice

from src.Cypher.Cypher import CypherAES

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


def GenPasswd2(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])


class testEncrypt(unittest.TestCase):

    def test_statictext(self):
        """Test case that verifies that the encryption/decryption operations on a static text proceed with no
        problem and are invertible. This text verifies that the text generated from the encription -> decryption
        operations is the same as the original """
        cypher = CypherAES('password')

        cyphertext = cypher.encrypt_text(text)
        retext = cypher.decrypt_text(cyphertext).decode()
        self.assertEqual(retext.rstrip(), text, 'Input text doesn''t correspond to output text')

    def test_randomtext(self):
        """Test that verifies that the encryption/decryption operations on a randomly generated text proceed with no
        problem and are invertible. This text verifies that the text generated from the encription -> decryption
        operations is the same as the original """
        cypher = CypherAES('password')
        ratext = GenPasswd2(length=100000)
        cyphertext = cypher.encrypt_text(ratext)
        retext = cypher.decrypt_text(cyphertext).decode()
        self.assertEqual(retext.rstrip(), ratext, 'Input text doesn''t correspond to output text')

    def test_text_file(self):
        """Test that verifies that the encryption/decryption operations on a text file proceed with no problem and
        are invertible. This text verifies that the text generated from the encription -> decryption operations is
        the same as the original """
        cypher = CypherAES('password')

        filepath = '../tests/'
        filename = 'dark_chronicle'

        cypher.encrypt_file(filepath + filename)
        cypher.decrypt_file(filepath + '(encrypted) ' + filename)
        with open(filepath + filename, 'rb') as original:
            with open(filepath + '(decrypted) ' + filename, 'rb') as decrypted:
                orig = original.read()
                dec = decrypted.read()
                self.assertEqual(orig, dec, 'Input text doesn''t correspond to output text')
        os.remove(filepath + '(decrypted) ' + filename)
        os.remove(filepath + '(encrypted) ' + filename)

    def test_bin_file(self):
        """Test that verifies that the encryption/decryption operations on a binary file proceed with no problem and
        are invertible. This text verifies that the text generated from the encription -> decryption operations is
        the same as the original """
        cypher = CypherAES('password')

        filepath = '../tests/'
        filename = 'robot-clipart.png'

        cypher.encrypt_file(filepath + filename)
        cypher.decrypt_file(filepath + '(encrypted) ' + filename)
        with open(filepath + filename, 'rb') as original:
            with open(filepath + '(decrypted) ' + filename, 'rb') as decrypted:
                orig = original.read()
                dec = decrypted.read()
                self.assertEqual(orig, dec, 'Input text doesn''t correspond to output text')
        os.remove(filepath + '(decrypted) ' + filename)
        os.remove(filepath + '(encrypted) ' + filename)


if __name__ == '__main__':
    unittest.main()
