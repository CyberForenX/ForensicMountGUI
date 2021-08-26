import sys
import os
import subprocess
import sqlite3
from PyQt5.QtWidgets import *
import getpass
import pytsk3
import hashlib
import datetime
import DatabaseCreator

con = sqlite3.connect("mountdb.db")
cur = con.cursor()

path = ""
password = ""
counter = 0


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(350,150,1200,800)
        self.setWindowTitle("Forensic Image Mounter")
        self.UI()

        self.show()

    def UI(self):
        global counter
        counter = 0
        mainLayout = QVBoxLayout()
        topLayout = QHBoxLayout()
        bottomLayout = QHBoxLayout()
        leftbottomLayout = QHBoxLayout()
        rightbottomLayout = QHBoxLayout()

        self.mountTable = QTableWidget()
        self.mountTable.setRowCount(1)
        self.mountTable.setColumnCount(6)
        self.mountTable.setHorizontalHeaderItem(0,QTableWidgetItem("Mounted Forensic Image"))
        self.mountTable.setHorizontalHeaderItem(1, QTableWidgetItem("Forensic Image Path"))
        self.mountTable.setHorizontalHeaderItem(2, QTableWidgetItem("Forensic Image Type"))
        self.mountTable.setHorizontalHeaderItem(3, QTableWidgetItem("Number of Partitions"))
        self.mountTable.setHorizontalHeaderItem(4, QTableWidgetItem("Mount Time"))
        self.mountTable.setHorizontalHeaderItem(5, QTableWidgetItem("MD5 Hash"))
        self.mountTable.resizeColumnsToContents()
        self.mountTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        topLayout.addWidget(self.mountTable)


        self.imagePathBox = QLineEdit(self)
        self.imagePathBox.setPlaceholderText("Input Path")

        fileButton = QPushButton("Select Disk Image")
        fileButton.clicked.connect(self.filePath)

        mountButton = QPushButton("Mount Image")
        mountButton.clicked.connect(self.mount)

        unmountButton = QPushButton("Unmount Image")
        unmountButton.clicked.connect(self.unmount)


        leftbottomLayout.addWidget(self.imagePathBox)
        leftbottomLayout.addWidget(fileButton)

        rightbottomLayout.addWidget(mountButton)
        rightbottomLayout.addWidget(unmountButton)
        rightbottomLayout.setContentsMargins(50,0,0,0)


        bottomLayout.addLayout(leftbottomLayout)
        bottomLayout.addLayout(rightbottomLayout)
        bottomLayout.setContentsMargins(10, 50, 10, 50)

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)


        self.setLayout(mainLayout)



    def filePath(self):
        global path
        path = QFileDialog.getOpenFileNames(self,"Disk Image","","forensic images(*E01 *dd)",)
        path = str(path[0]).strip("[]'")
        self.imagePathBox.setText(path)

    def mount(self):
        global path
        global password
        global counter
        path = self.imagePathBox.text()
        file = os.path.basename(path)
        fileProperties = os.path.splitext(file)
        fileName = fileProperties[0]
        fileExtension = fileProperties[1]
        mountPath = f"/mnt/{fileName}"

        username = getpass.getuser()
        sudoPassword = password

        createMountPoint = f"mkdir {mountPath}"
        permisionMountPoint = f"chown {username} {mountPath}"
        modPermisionMountPoint = f"chmod 755 {mountPath}"


        if (".E01" in fileExtension):
            print("E01 Image")
            print(fileName)

            os.system(f'echo {sudoPassword}|sudo -S {createMountPoint}')
            os.system(f'echo {sudoPassword}|sudo -S {permisionMountPoint}')
            os.system(f'echo {sudoPassword}|sudo -S {modPermisionMountPoint}')
            os.system(f"xmount --in ewf {path} {mountPath}")


            status = subprocess.call(f"test -e {mountPath}", shell=True)

            if(status == 0):
                newImageName = fileName + ".dd"
                imageObject = pytsk3.Img_Info(f"{mountPath}/{newImageName}")
                volObject = pytsk3.Volume_Info(imageObject)
                numPartitions = volObject.info.part_count -2
                imageObject.close()

                curTime = datetime.datetime.now()

                md5_hash = hashlib.md5()
                imgFile = open(f"{mountPath}/{newImageName}","rb")
                content = imgFile.read()
                md5_hash.update(content)
                hash_ouptut = md5_hash.hexdigest()
                imgFile.close()

                self.mountTable.setItem(counter,0,QTableWidgetItem(str(file)))
                self.mountTable.setItem(counter,1, QTableWidgetItem(str(mountPath)))
                self.mountTable.setItem(counter,2, QTableWidgetItem("ewf"))
                self.mountTable.setItem(counter,3, QTableWidgetItem(str(numPartitions)))
                self.mountTable.setItem(counter,4, QTableWidgetItem(str(curTime)))
                self.mountTable.setItem(counter,5, QTableWidgetItem(str(hash_ouptut)))
                self.mountTable.resizeColumnsToContents()

                try:
                    query = "INSERT INTO mount_images (Mounted_Forensic_Image,Forensic_Image_Path,Forensic_Image_Type,Number_of_Partitions,Mount_Time,Current_MD5_Hash) VALUES(?,?,?,?,?,?)"
                    cur.execute(query,(file,mountPath,"ewf",numPartitions,curTime,hash_ouptut))
                    con.commit()
                    QMessageBox.information(self,"Success",f"Forensic Image {file} Mounted")

                except:
                    QMessageBox.information(self, "Warning", "Forensic image has not been added")


                counter += 1
                self.mountTable.insertRow(counter)


            if(status == 1):
                print("not mounted")

            #if ("fuse.xmount" in os.system(f"mount | grep {mountPath}")):
                #print("mounted")


        elif(".dd" in fileExtension):

            print("raw image")
            print(fileName)

            os.system(f'echo {sudoPassword}|sudo -S {createMountPoint}')
            os.system(f'echo {sudoPassword}|sudo -S {permisionMountPoint}')
            os.system(f'echo {sudoPassword}|sudo -S {modPermisionMountPoint}')
            os.system(f"xmount --in raw {path} {mountPath}")

            status = subprocess.call(f"test -e {mountPath}", shell=True)

            if (status == 0):
                newImageName = fileName + ".dd"
                imageObject = pytsk3.Img_Info(f"{mountPath}/{newImageName}")
                volObject = pytsk3.Volume_Info(imageObject)
                numPartitions = volObject.info.part_count - 2
                imageObject.close()

                curTime = datetime.datetime.now()

                md5_hash = hashlib.md5()
                imgFile = open(f"{mountPath}/{newImageName}", "rb")
                content = imgFile.read()
                md5_hash.update(content)
                hash_ouptut = md5_hash.hexdigest()
                imgFile.close()

                self.mountTable.setItem(counter, 0, QTableWidgetItem(str(file)))
                self.mountTable.setItem(counter, 1, QTableWidgetItem(str(mountPath)))
                self.mountTable.setItem(counter, 2, QTableWidgetItem("raw"))
                self.mountTable.setItem(counter, 3, QTableWidgetItem(str(numPartitions)))
                self.mountTable.setItem(counter, 4, QTableWidgetItem(str(curTime)))
                self.mountTable.setItem(counter, 5, QTableWidgetItem(str(hash_ouptut)))
                self.mountTable.resizeColumnsToContents()


                counter += 1
                self.mountTable.insertRow(counter)

                try:
                    query = "INSERT INTO mount_images (Mounted_Forensic_Image,Forensic_Image_Path,Forensic_Image_Type,Number_of_Partitions,Mount_Time,Current_MD5_Hash) VALUES(?,?,?,?,?,?)"
                    cur.execute(query,(file,mountPath,"raw",numPartitions,curTime,hash_ouptut))
                    con.commit()
                    QMessageBox.information(self,"Success",f"Forensic Image {file} Mounted")

                except:
                    QMessageBox.information(self, "Warning", "Forensic image has not been added")



    def unmount(self):
        global password
        global counter
        sudoPassword = password
        if(self.mountTable.selectedItems()):
            for item in self.mountTable.selectedItems():
                rowNumber = item.row()

            unMount = self.mountTable.item(rowNumber,1).text()
            imageName = self.mountTable.item(rowNumber, 0).text()
            self.mountTable.removeRow(rowNumber)

            unMountCommand = f"umount {unMount}"
            removeMountPoint = f"rmdir {unMount}"


            os.system(f'echo {sudoPassword}|sudo -S {unMountCommand}')
            os.system(f'echo {sudoPassword}|sudo -S {removeMountPoint}')
            counter = counter - 1


            sqlDel = f"DELETE FROM mount_images WHERE Mounted_Forensic_Image LIKE \"{str(imageName)}\""
            cur.execute(sqlDel)
            con.commit()






class PasswordPrompt(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Password Prompt")
        self.setGeometry(300,300,300,300)
        self.UI()
        self.show()

    def UI(self):
        passLabel= QLabel("Enter Password",self)
        passLabel.move(100,10)

        self.passwordText = QLineEdit(self)
        self.passwordText.setPlaceholderText("Password")
        self.passwordText.move(90,50)

        enterButton = QPushButton("Enter",self)
        enterButton.move(90, 100)
        enterButton.clicked.connect(self.enterPass)

    def enterPass(self):
        global password
        password = self.passwordText.text()

        self.close()

def checkDatabase(window):
    global counter
    query = "SELECT * FROM mount_images"
    mounted_path = cur.execute(query).fetchall()
    for path in mounted_path:
        status = subprocess.call(f"test -e {path[2]}", shell=True)


        if (status == 0):
            print(f"{path[2]} is mounted")
            window.mountTable.setItem(counter, 0, QTableWidgetItem(str(path[1])))
            window.mountTable.setItem(counter, 1, QTableWidgetItem(str(path[2])))
            window.mountTable.setItem(counter, 2, QTableWidgetItem("raw"))
            window.mountTable.setItem(counter, 3, QTableWidgetItem(str(path[4])))
            window.mountTable.setItem(counter, 4, QTableWidgetItem(str(path[5])))
            window.mountTable.setItem(counter, 5, QTableWidgetItem(str(path[6])))
            window.mountTable.resizeColumnsToContents()
            counter += 1
            window.mountTable.insertRow(counter)

        else:
            sqlDel = f"DELETE FROM mount_images WHERE Mounted_Forensic_Image LIKE \"{path[1]}\""
            cur.execute(sqlDel)
            con.commit()


def main():
    DatabaseCreator
    App = QApplication(sys.argv)
    window = Window()
    passPrompt = PasswordPrompt()
    checkDatabase(window)
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()