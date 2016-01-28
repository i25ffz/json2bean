'''
Created on 2015-12-01

@author: Fufz
'''

import sys
import json
import getopt

# upper first char of str
def upperStr(str):
    return str[0].capitalize() + str[1:]

def parseJson(jdict, pkg, clzName):
    if len(clzName) > 0:
        fclz = open(upperStr(clzName) + '.java', 'w')

        # write comment warnings
        fclz.write('/*\n * This file is auto-generated.  DO NOT MODIFY.\n */\n\n')

        # write package
        fclz.write('package %s;\n\n' % pkg)

        # print bean.capitalize()
        # write class name
        fclz.write('public class %s {\n\n' % upperStr(clzName))

    flds = {}

    for key in jdict.keys():
        print key, type(jdict[key])
        if isinstance(jdict[key], dict):
            parseJson(jdict[key], pkg, key)
            continue

        val = jdict[key]
        if type(val) is unicode or type(val) is str:
            fclz.write('\tprivate String %s;\n' % key)
            flds[key] = 'String'
        elif type(val) is int:
            fclz.write('\tprivate int %s;\n' % key)
            flds[key] = 'int'
        elif type(val) is bool:
            fclz.write('\tprivate boolean %s;\n' % key)
            flds[key] = 'boolean'
        elif type(val) is long:
            fclz.write('\tprivate long %s;\n' % key)
            flds[key] = 'long'
        elif type(val) is float:
            fclz.write('\tprivate float %s;\n' % key)
            flds[key] = 'float'
        else:
            print key + ':' + str(type(jdict[key]))

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

    '''

        # write fields
        for fld in jlist[bean]:
            # print fld, type(jlist[bean][fld]) is bool
            val = jlist[bean][fld]
            if type(val) is unicode or type(val) is str:
                fbean.write('\tprivate String %s;\n' % fld)
                flds[fld] = 'String'
            elif type(val) is int:
                fbean.write('\tprivate int %s;\n' % fld)
                flds[fld] = 'int'
            elif type(val) is bool:
                fbean.write('\tprivate boolean %s;\n' % fld)
                flds[fld] = 'boolean'
            elif type(val) is long:
                fbean.write('\tprivate long %s;\n' % fld)
                flds[fld] = 'long'
            elif type(val) is float:
                fbean.write('\tprivate float %s;\n' % fld)
                flds[fld] = 'float'
            else:
                print fld + ':' + str(type(jlist[bean][fld]))

        # gen setter & getter
        for k in flds:
            # getter fun
            if flds[k] == 'boolean':
                if k.startswith('is') or k.startswith('has'):
                    fbean.write('\n\tpublic %s %s() {\n' % (flds[k], k))
                else:
                    fbean.write('\n\tpublic %s is%s() {\n' % (flds[k], upperStr(k)))
            else:
                fbean.write('\n\tpublic %s get%s() {\n' % (flds[k], upperStr(k)))

            fbean.write('\t\treturn this.%s;\n\t}\n' % k)

            # setter fun
            if k.startswith('is'):
                fbean.write('\n\tpublic void set%s(%s %s) {\n' % (k[2:], flds[k], k))
            elif k.startswith('has'):
                fbean.write('\n\tpublic void set%s(%s %s) {\n' % (k[3:], flds[k], k))
            else:
                fbean.write('\n\tpublic void set%s(%s %s) {\n' % (upperStr(k), flds[k], k))
            fbean.write('\t\tthis.%s = %s;\n\t}\n' % (k, k))

        fbean.write('\n}\n')
        '''
        # print '--------------------------------'

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2:
        print 'usage: %s json [-p,--package= package name ]' % sys.argv[0]
        sys.exit(1)

    opts, args = getopt.getopt(sys.argv[2:], 'p:', ['package='])
    pkg = 'cn.ninegame.model'
    for o, a in opts:
        if o in ('-p', '--package'):
            pkg = a

    # print open(sys.argv[1]).read()
    rootDict = json.loads(open(sys.argv[1]).read())
    parseJson(rootDict, pkg, '')


