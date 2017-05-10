from config import *

def os_file_exist(file):
    my_file = Path(file)
    if my_file.is_file():
        return True
    else:
        return False

def os_append_json(data, file,text=''):
    saveFile = open(file,'a')
    json.dump(data,saveFile)
    saveFile.write('\n')
    saveFile.close()
    print "\t OS Successfully Written"+text

def os_write_json(data, file,text=''):
    saveFile = open(file,'w')
    json.dump(data,saveFile)
    saveFile.write('\n')
    saveFile.close()
    print "\t OS Successfully Written"+text
