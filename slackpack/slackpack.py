import subprocess
import sqlite3
import sys

# Current database model has been designed like this :
#   Table : package ( id, pkg_name,version,author,depends,descripcion,type,content,id_provider)
#   Table:  deps    ( id_package,id_file, filename,type)
#   Table:  content ( id,filename,size,version,type)  
#   Table:  type(id,name)
#   Table:  provider(id,name,url)
#   Table:  Repository(id,name,url,provider)


def init_db():
    c = sqlite3.Connection('packages.db')
    run_query(c,"create table package (id integer primary key,name,version,author,depends,description,type,content,provider)")
    run_query(c,"Select * from package")
    return c

def run_query(conn,query):
    cur = conn.cursor()
    print cur.execute(query)





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


def get_description_from_slack_file(file,pkgname):
    o=0
    l=[]
    with open(file) as f:
        lines = f.readlines()
        for i in lines:
            if i.find('#')  == -1 :
                if i.find('handy') == -1:
                    o = o +1
                    if o >= 3 and i[0] != '\n':
                       s= i.replace(pkgname+":","",1)
                       l.append( s.strip())
                    
    return l


# out=pkg_contents("sbcl.tgz")
# out=filterbydir("bin",out,"executable")
# out = check_libraries(out[0])
# print out

out=get_description_from_slack_file('slack-desc','sbcl')

print str(out)

for i in out:
    print i.strip()

init_db()

