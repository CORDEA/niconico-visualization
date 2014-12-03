#!/usr/bin/env python
#encoding:utf-8
#

__Author__ =  "Yoshihiro Tanaka"
__date__   =  "2014-11-21"

import json, sys, os, commands

dirs = commands.getoutput("ls " + sys.argv[1]).split("\n")
readDirs = []
for i in range(len(dirs)):
    if "tag_" in dirs[i]:
        dirname = sys.argv[1].rstrip("/") + "/" + dirs[i]
        if os.path.isdir(dirname):
            readDirs.append(dirname)
dirs = readDirs

tarDict  = {}
tagnames = []
for dirname in dirs: 
    files = [dirname + "/" + r for r in commands.getoutput("ls " + dirname + "/").split("\n") if len(r) != 0]
    header = True
    tagDict = {}
    for filename in files:
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                try:
                    data = json.loads(line)
                except Exception as e:
                    sys.stderr.write(e + "\n")
                    continue
                if "values" in data:
                    if "tags" in data["values"][0]:
                        for values in data["values"]:
                            if u"アニメ" in values["tags"]:
                                tags = values["tags"].split()
                                for tag in tags:
                                    tagnames.append(tag)
                                    try:
                                        tagDict[tag] += 1
                                    except:
                                        tagDict[tag] = 1
    SUM = sum(tagDict.values())
    tarDict[dirname.split("tag_")[1]] = {key: tagDict[key]/float(SUM) for key in tagDict.keys()}

tagnames = [r.encode('utf-8') for r in list(set(tagnames))]

output = ["word"] + tagnames
print("\t".join(output))
for k, tagDict in tarDict.items():
    output = [k]
    for tag in tagnames:
        if tag.decode('utf-8') in tagDict:
            output.append(str(tagDict[tag.decode('utf-8')]))
        else:
            output.append(str(0))
    print("\t".join(output))
