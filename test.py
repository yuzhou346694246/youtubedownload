import os
import hashlib
hashfilenames = {}
def filename2hash(name):
    md5 = hashlib.md5()
    md5.update(name.encode(encoding='UTF-8'))
    return md5.hexdigest()[:6]

def init_hashfilenames():
    global hashfilenames
    hashfilenames = {}
    def listdir(path):
        #if os.path.isfile(path):
        #    return None
        filenames = os.listdir(path)
        for filename in filenames:
            tpath = os.path.join(path,filename)
            if os.path.isdir(tpath):
                print(tpath)
                listdir(tpath)

            else:
                h = filename2hash(tpath)
                hashfilenames[h] = { 'filename':filename,'path':tpath}
    basedir = './downloads'
    listdir(basedir)


if __name__=='__main__':
    init_hashfilenames()
    print(hashfilenames)