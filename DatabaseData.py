import sqlite3
import subprocess

con = sqlite3.connect("mountdb.db")
cur = con.cursor()


def checkDatabase():
    query = "SELECT Mount_Number,Mounted_Forensic_Image,Forensic_Image_Path FROM mount_images"
    mounted_path = cur.execute(query).fetchall()
    print(mounted_path)
    for path in mounted_path:
        status = subprocess.call(f"test -e {path[2]}", shell=True)

        if (status == 0):
            print(f"{path[2]} is mounted")

checkDatabase()