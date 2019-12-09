#!/usr/bin/env python3
import argparse
import logging
from getpass import getpass
import hashlib
import os
from tkinter.simpledialog import askstring
from tkinter.messagebox import askyesno
from tkinter import Tk
from Crypto.Cipher import AES
from Crypto.Random import random

logging.basicConfig(level=logging.CRITICAL, format="%(filename)s:%(asctime)s:%(message)s")

#Configuration
HMAC_ITERATIONS = 500000

#logging.info("Guaranteed hashing algorithms: %s" %hashlib.algorithms_guaranteed)
if "sha256" not in hashlib.algorithms_guaranteed:
    raise Exception("sha256 is not available.")

def encrypt(origin, destination, passphrase, iv):
    with open(origin, "rb") as infile, open(destination, "wb") as outfile:
        enc = AES.new(passphrase, AES.MODE_CBC, iv)
        indata = infile.read()
        indata += b'0' * (16 - len(indata) % 16)
        cipher = enc.encrypt(indata)
        outfile.write(cipher)

    logging.info("%s encrypted to %s" % (origin, destination))

def decrypt(origin, destination, passphrase, iv=None):
    if iv == None:
        iv = origin.split(".")[-2].encode() #reliex on the file pattern *.iv.aes
    with open(origin, "rb") as infile, open(destination, "wb") as outfile:
        passhash = hashlib.pbkdf2_hmac("sha256", passphrase, iv, HMAC_ITERATIONS)
        dec = AES.new(passhash, AES.MODE_CBC,iv)
        indata = infile.read()
        cipher = dec.decrypt(indata)
        outfile.write(cipher)

    logging.info("%s decrypted to %s" % (origin, destination))
    
def geniv():
    """
    returns an encoded byte string of 16 bytes
    """
    CHARSET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwzyz1234567890")
    iv = "".join([random.choice(CHARSET) for i in range(16)]).encode()
    logging.debug("%s has been generated as the initialization vector." % iv)

    return iv

def get_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("file", type=str, help="file subject to encryption/decryption")
    parser.add_argument("-t", "--target", type=str, help="sets the target path of encrypted/encrypted file otherwise saved to filename.iv.aes")
    group.add_argument("-d", "--decrypt", action="store_true", help="marks the file for decryption")
    group.add_argument("-e", "--encrypt", action="store_true", help="marks the file for encryption")
    args = parser.parse_args()
    logging.debug(args)

    return args

def main():
    args = get_args()
    if args.encrypt or args.decrypt:
        passphrase = getpass("Please enter your password. ").encode()
        if args.encrypt:
            iv = str(input("Please provide a 16 character Initialization Vector (leave blank for a random initialization vector.)")).encode()
            iv = iv if iv else geniv()
            passhash = hashlib.pbkdf2_hmac("sha256", passphrase, iv, HMAC_ITERATIONS)
            destination = (args.target if args.target else args.file) + "." + iv.decode() + ".aes"
            encrypt(args.file, destination, passhash, iv)
        else:
            iv = str(input("Please provide a 16 character Initialization Vector (leave blank to infer initialization vector based on *.iv.aes). ")).encode()
            destination = args.target if args.target else args.file[:-21]
            decrypt(args.file, destination, passphrase)
            print("You're file has been decrypted to ", destination)

if __name__ == "__main__":
    main()
