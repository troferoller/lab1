import sys 
import os
import requests
import json

HOST = "localhost"
PORT = "9870"
username = "dmitrijdulger"
global PATH
PATH = "/"
global localPath
localPath = "/Users/dmitrijdulger/Desktop/"

def checklist(i):
    if len(i) > 0:
        return True

def del_slash(PATH):
    if PATH[0] =="/":
        PATH = PATH[1:]
    return PATH

def mkdir(i):
    folder = "".join(i)
    r = requests.put(f"http://{HOST}:{PORT}/webhdfs/v1{PATH}{folder}?user.name={username}&op=MKDIRS")
    if r.status_code == 200:
        print("Folder created")
    else:
        print("Error code: ", r.status_code)

def ls():
    r = requests.get(f"http://{HOST}:{PORT}/webhdfs/v1{PATH}?op=LISTSTATUS")
    r = r.json()["FileStatuses"]["FileStatus"]
    for l in r :
        print(l.get("pathSuffix"), end = "\n")
        
def lls():
    files = os.listdir(localPath)
    for l in files:
        if not l.startswith("."):
            print(l, end="\n")
    
def delete(i):
    clear = "".join(i)
    r = requests.delete(f"http://{HOST}:{PORT}/webhdfs/v1{PATH}{clear}?user.name={username}&op=DELETE&recursive=true")
    if r.status_code == 200:
        print("Object deleted ")
    else:
        print("Error code: ", r.status_code)

def cd(i):
    global PATH
    change = "".join(i)
    if change == "..":
        PATH = "/".join(PATH.split("/")[:-2]) + "/"
        if change == "//":
            PATH = "/"
    else:
        r = requests.get(f"http://{HOST}:{PORT}/webhdfs/v1{PATH}{change}?op=GETFILESTATUS")
        if r.status_code == 200:
            PATH = PATH + del_slash(change) + "/"
            
def lcd(i):
    global localPath
    local = "".join(i)
    if local == "..":
        localPath = "/".join(localPath.split("/")[:-2]) + "/"
        if local == "//":
            localPath = "/"
    else:
        if os.path.exists(localPath + local):
            localPath = localPath + del_slash(local) + "/"
            
def get(i):
    file = "".join(i)
    r = requests.get(f"http://{HOST}:{PORT}/webhdfs/v1/{PATH}{file}?op=OPEN&user.name={username}")
    if r.status_code == 200:
        f = open(localPath + file, "w")
        f.write(r.text)
        f.close()
        print(f"File \"{file}\" downloaded")
    else:
        print("Error code ", r.status_code)
        
def put(i):
    file = "".join(i)
    r = requests.put(f"http://{HOST}:{PORT}/webhdfs/v1{PATH}{file}?op=CREATE&overwrite=true&replication=1&user.name={username}&noredirect=true")
    link = json.loads(r.text)["Location"]
    print(link)
    r = requests.put(link, data=open(localPath+file))
    if r.status_code == 201:
        print(f"File \"{file}\" uploaded")
    else:
        print("Error code ", r.status_code)

def append(i):
    localfile = "".join(i[0])
    hdfsfile = "".join(i[1])
    r = requests.post(f"http://{HOST}:{PORT}/webhdfs/v1{PATH}{hdfsfile}?op=SETREPLICATION&replication=1")
    r = requests.post(f"http://{HOST}:{PORT}/webhdfs/v1{PATH}{hdfsfile}?op=APPEND&user.name={username}&noredirect=true")
    link = json.loads(r.text)["Location"]
    print(link)
    r2 = requests.post(link, data=open(localPath + localfile))
    if r2.status_code == 200:
        print(f"File \"{localfile}\" was append to \"{hdfsfile}\"")
    else:
        print("Error code ", r2.status_code)

while True:
    i = input(": ")
    i = i.split()
    if i[0] == "mkdir":
        i.remove("mkdir")
        mkdir(i)
    elif i[0] == "ls":
        i.remove("ls")
        ls()
    elif i[0] == "lls":
        i.remove("lls")
        lls()
    elif i[0] == "delete":
        i.remove("delete")
        delete(i)
    elif i[0] == "cd":
        i.remove("cd")
        cd(i)
    elif i[0] == "lcd":
        i.remove("lcd")
        lcd(i)
    elif i[0] == "get":
        i.remove("get")
        get(i)
    elif i[0] == "put":
        i.remove("put")
        put(i)
    elif i[0] == "append":
        i.remove("append")
        append(i)
    elif i[0] == "exit":
        break
