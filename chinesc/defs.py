defs = {
    'and': '以及',
    'bool': '布爾',
    'break': '斷',
    'case': '狀況',
    'catch': '抓',
    'cerr': '吸不到',
    'char': '字元',
    'cin': '吸入',
    'class': '類別',
    'const': '常數',
    'continue': '繼續',
    'cout': '吸出',
    'do': '做',
    'double': '雙',
    'else': '否則',
    'endl': '換行',
    'false': '假',
    'float': '浮點數',
    'for': '對於',
    'goto': '去',
    'if': '若',
    'inline': '在線',
    'int': '整數',
    'long': '長',
    'main': '主要', 
    'namespace': '名字洞',
    'new': '新的',
    'not': '不是',
    'or': '或',
    'private': '私有',
    'public': '公有',
    'return': '傳回',
    'short': '短',
    'signed': '有向',
    'stataic': '靜止',
    'std': '標準',
    'string': '繩子',
    'switch': '開關',
    'template': '模板',
    'this': '這個',
    'throw': '丟',
    'true': '真',
    'unsigned': '無向',
    'using': '使用',
    'void': '虛無',
    'while': '當',
}

def htmlConvert(s):
    for key, value in defs.items():
        s = s.replace('>{}<'.format(key), '>{}<'.format(value))
    return s