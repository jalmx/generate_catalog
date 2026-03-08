import ftplib
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

FTP_HOST = os.getenv("FTP_HOST")
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")


def upload(full_path: str, name_file: str | None = None):
    # Connect and login
    if not name_file:
        name_file = Path(full_path).name

    with ftplib.FTP(FTP_HOST) as ftp:
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        print(f"Connected to {FTP_HOST}")

        # Upload a binary file
        with open(full_path, 'rb') as f_upload:
            ftp.cwd('/htdocs')
            ftp.storbinary(f"STOR {name_file}", f_upload)
            print(f"Uploaded {name_file}")

        ftp.quit()
        print("Connection closed.")


def bulk_upload(full_path: str, name_file: str | None = None):
    if not name_file:
        pass


def main():
    file1 = "lista.csv"
    upload("../catalogo/lista.csv")


if __name__ == "__main__":
    main()
