'''
Created on 2015-12-01

@author: Fufz
'''

import sys
import json
import getopt
import os


DEBUG = False
def debugLog(*s):
    if DEBUG:
        print s

# upper first char of str
def upperStr(str):
    return str[0].capitalize() + str[1:]

# replace char '_'
def replaceStr(fld):
    c_pos = fld.find('_')
    if c_pos > 0:
        fld = fld[:c_pos] + upperStr(fld[c_pos + 1:])
        return replaceStr(fld)
    else:
        return fld

# gen javabean from json file

# @     jdict json obj to be parse
# @       pkg java class package name
# @   clzname java class Name, java file name
# @parentName if B in A, parentName is A 
def parseJson(jdict, pkg, clzName, parentName):
    # create java file
    fclz = open(upperStr(clzName) + '.java', 'w')
    # write comment warnings
    fclz.write('/*\n * This file is auto-generated.  DO NOT MODIFY.\n */\n\n')
    # write package
    fclz.write('package %s;\n\n' % pkg)

    # for gen import packaga
    tmpBuf = 'public class %s {\n\n' % upperStr(clzName)
    isFirstObj = True
    # for gen setter & getter
    flds = {}

    # gen import package, class properties
    for key in jdict.keys():
        print key, type(jdict[key])

        if isinstance(jdict[key], list):
            print key, ' is list'
            nAryLen = len(jdict[key])
            if parentName != '':
                clsName = '%s%s' % (upperStr(parentName), upperStr(key))
                objName = '%s%s' % (parentName, upperStr(key))  
            else:
                clsName = '%s' % upperStr(key)
                objName = '%s' % key
                        
            if isFirstObj:    
                tmpBuf = 'import %s.%s;\n\n' % (pkg, clsName) + tmpBuf
                isFirstObj = False
            else:
                tmpBuf = 'import %s.%s;\n' % (pkg, clsName) + tmpBuf

            tmpBuf = tmpBuf + '\tprivate %s %s[%d];\n' % (clsName, objName, nAryLen)
            parseJson(jdict[key][0], pkg, clsName, key)
            continue
        
        if isinstance(jdict[key], dict):
            print key, ' is dict'
            if parentName != '':
                clsName = '%s%s' % (upperStr(parentName), upperStr(key))
                objName = '%s%s' % (parentName, upperStr(key))  
            else:
                clsName = '%s' % upperStr(key)
                objName = '%s' % key
            
            if isFirstObj:    
                tmpBuf = 'import %s.%s;\n\n' % (pkg, clsName) + tmpBuf
                isFirstObj = False
            else:
                tmpBuf = 'import %s.%s;\n' % (pkg, clsName) + tmpBuf

            tmpBuf = tmpBuf + '\tprivate %s %s;\n' % (clsName, objName)
            parseJson(jdict[key], pkg, clsName, key)          
            continue            

        val = jdict[key]

        # replace char '_'
        key = replaceStr(key)

        if type(val) is unicode or type(val) is str:
            tmpBuf = tmpBuf + '\tprivate String %s;\n' % key
            flds[key] = 'String'
        elif type(val) is int:
            tmpBuf = tmpBuf + '\tprivate int %s;\n' % key
            flds[key] = 'int'
        elif type(val) is bool:
            tmpBuf = tmpBuf + '\tprivate boolean %s;\n' % key
            flds[key] = 'boolean'
        elif type(val) is long:
            tmpBuf = tmpBuf + '\tprivate long %s;\n' % key
            flds[key] = 'long'
        elif type(val) is float:
            tmpBuf = tmpBuf + '\tprivate float %s;\n' % key
            flds[key] = 'float'
        else:
            print key + ':' + str(type(jdict[key]))

    fclz.write(tmpBuf)

    # gen setter & getter
    for k in flds:
        # getter fun
        if flds[k] == 'boolean':
            if k.startswith('is') or k.startswith('has'):
                fclz.write('\n\tpublic %s %s() {\n' % (flds[k], k))
            else:
                fclz.write('\n\tpublic %s is%s() {\n' % (flds[k], upperStr(k)))
        else:
            fclz.write('\n\tpublic %s get%s() {\n' % (flds[k], upperStr(k)))
        fclz.write('\t\treturn this.%s;\n\t}\n' % k)

        # setter fun
        if k.startswith('is'):
            fclz.write('\n\tpublic void set%s(%s %s) {\n' % (k[2:], flds[k], k))
        elif k.startswith('has'):
            fclz.write('\n\tpublic void set%s(%s %s) {\n' % (k[3:], flds[k], k))
        else:
            fclz.write('\n\tpublic void set%s(%s %s) {\n' % (upperStr(k), flds[k], k))
        fclz.write('\t\tthis.%s = %s;\n\t}\n' % (k, k))

    fclz.write('\n}\n')
    fclz.close()        
        

def removeFiles(path):
    for f in os.listdir(path):
        try:
            wholePath = os.path.join(path, f)
            #print wholePath
            if f.endswith('java') and os.path.isfile(wholePath):
                os.remove(wholePath)
                print('delete file ' + wholePath)
        except Exception, e:
            print e        


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2:
        print 'usage: %s jsonfile [-p,--package = package name, default is cn.ninegame.model ]' % sys.argv[0]
        sys.exit(1)

    #delete java file
    print '-------------1 delete java file'
    curPath = sys.path[0]
    removeFiles(curPath)
        
    #parse param
    opts, args = getopt.getopt(sys.argv[2:], 'p:', ['package='])
    pkg = 'cn.ninegame.model'
    for o, a in opts:
        if o in ('-p', '--package'):
            pkg = a

    #parse json
    print '\n-------------2 parse json'
    debugLog(sys.argv[0])
    debugLog(sys.argv[1])
    rootDict = json.loads(open(sys.argv[1]).read())
    clsName = os.path.basename(sys.argv[1]).split('.')[0]
    parseJson(rootDict, pkg, clsName, "")
    
    print '\n-------------3 Done'