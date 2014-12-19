import subprocess
import _sqlite3

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
