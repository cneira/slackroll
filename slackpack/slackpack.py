import subprocess
import sqlite3

# Current database model has been designed like this :
#   Table : package ( id, pkg_name,version,author,depends,descripcion,type,content,id_provider)
#   Table:  deps    ( id_package,id_file, filename,type)
#   Table:  content ( id,filename,size,version,type)  
#   Table:  type(id,name)
#   Table:  provider(id,name,url)
#   Table:  Repository(id,name,url,provider)





def pkg_contents(p):
    out =[]
    out=subprocess.check_output(["/sbin/explodepkg", p])
    return out.split('\n')


def filterbydir(exp, l,what):
    f = []
    out=''
    for i in l:
        print i
        if i.find(exp) != -1:
           out = subprocess.check_output(["/usr/bin/file", i])
           if out.find(what) != -1:
                f.append(i)

    return f

def check_libraries(elf):
    needed=[]
    out=[]
    out=subprocess.check_output(["/usr/bin/objdump","-x",elf])
    out = out.split('\n')
    for i in out:
        if i.find("NEEDED")!=-1:
            needed.append(i.split()[1])
    return needed








out=pkg_contents("sbcl.tgz")
out=filterbydir("bin",out,"executable")
out = check_libraries(out[0])
print out
