# Diary Locker
**Note, this project is no longer being maintained.**
## Introduction
Diary Locker let's allows you monitor a directory for new videos recorded with your computer's webcam application and encrypt it with AES-128. It also comes with a command line utility capable of encrypting/decrypting any binary file.

## Security Details
For the file encryption, I am using `AES-128` as implemented in [`pycryptodome`](https://pycryptodome.readthedocs.io/en/latest/). As AES relies on a key to decrypt the file and an initialization vector to offset the initial data block for encryption, the key is generated through using `pbkdf2_hmac` which generates an `sha256` hash (to get a 16 byte key) by running through 500000 hashes and uses the initialization vector as the salt. Because of my decision to place the initialization vector in the filename, the number of possible initialization vectors is drastically reduced, but it is random and there are still 2<sup>62</sup> possible initialization vectors, which is like 4,611,686,018,427,387,904 possible keys.
## Usage
1. Configure the location of your webcam videos and the destination of the encrypted videos in the `config.json` file
```javascript
{
    "DES_PATH": "path\to\video",
    "SRC_PATH": "\path\to\diary"
}
```
2. Create a virtual environment and install the dependencies in `requirements.txt` 
```powershell
$ \path\to\python.exe -m venv venv
$ .\venv\Scripts\Activate.ps1
(venv) $ pip -r install requirements.txt
```
Note that the `pycryptodome` module may need additional setup (particularly the need for a C compiler on Windows).

3. Schedule a task to run this script at startup as follows

![Click Create New Task > Under general, provide the name of the task under Name> Go to the action tab, add a new action and under Program/script, enter \path\to\venv\Scripts\pythonw.exe and under add Arguments add \path\to\encryption_monitor.py > Under the Triggers tab, click New and set Begin the Task to At log On > Specify the user and click ok and ok again. Right Click on the new task and click Run](how-to-add-task.gif)

4. When you are making your video, `encryption_monitor.py` will wait until you are done recording the video and prompt if you want to encrypt it. If so, you will then be prompted to enter the passphrase. Your video will then be saved to the `DES_PATH` you specified in `config.json`

The command line options are as follows
```powershell
usage: cryptionhub.py [-h] [-t TARGET] [-d | -e] file

positional arguments:
  file                  file subject to encryption/decryption

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        sets the target path of encrypted/encrypted file
                        otherwise saved to filename.iv.aes
  -d, --decrypt         marks the file for decryption
  -e, --encrypt         marks the file for encryption
```
So to decrypt the file, you would do as follows
```powershell
(venv) $ python .\cryptionhub.py \path\to\file -d
Please enter your password.
Please provide a 16 character Initialization Vector (leave blank to inver initialization vector based on *.iv.aes).
Your file has been decrypted to \path\to\decrypted\file
```
## (Many) Limitations and considerations
* I've only tested it on Windows. I don't know if it will work elsewhere
* This isn't really vetted for security so I wouldn't trust this with anything really sensitive
* Logging doesn't work (at least as a scheduled task)
* This probably only works in Python 3.6
* Only binary files are supported for now
* Only `.mp4` videos are supported for now
* When encrypting, the Initialization vector is stored in the file extension (for example, `WIN_20170514_22_09_15.mp4` will be saved as WIN_20170514_22_09_15.mp4.[initialization vector].aes`). This makes it incompatible with other AES solutions, unless you find a way to supply it with an initialization vector
