from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
import os


def upload(file):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("auth.json")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()

    elif gauth.access_token_expired:
        gauth.Refresh()

    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("auth.json")

    drive = GoogleDrive(gauth)

    # file = 'script.log'

    file1 = drive.CreateFile({'title': os.path.basename(file)})
    file1.SetContentFile(file)
    file1.Upload()  # Files.insert()


if __name__ == "__main__":
    file = sys.argv[1]

    upload(file)
