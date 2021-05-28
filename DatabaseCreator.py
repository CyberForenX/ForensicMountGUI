import sqlite3

con = sqlite3.connect("mountdb.db")
cur = con.cursor()


try:
    query_contents = "SELECT * FROM mount_images"
    contents = cur.execute(query_contents).fetchall()
    for content in contents:
        print(content)

except:

    sql_create_mount_images_table = """ CREATE TABLE IF NOT EXISTS mount_images (
                                        Mount_Number integer PRIMARY KEY,
                                        Mounted_Forensic_Image text NOT NULL,
                                        Forensic_Image_Path text NOT NULL,
                                        Forensic_Image_Type text NOT NULL,
                                        Number_of_Partitions integer NOT NULL,
                                        Mount_Time time NOT NULL,
                                        Current_MD5_Hash text NOT NULL
                                    ); """

    cur.execute(sql_create_mount_images_table)

    print("database has been created")