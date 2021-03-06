#!/usr/bin/env python
# encoding:utf-8
#
# Copyright [2014] [Yoshihiro Tanaka]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    extList  = []
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
                                    try:
                                        tagDict[tag] += 1
                                    except:
                                        tagDict[tag]  = 1
    for k in tagDict.keys():
        if tagDict[k] >= 5:
            tagnames.append(k)
            extList.append(k)
    tarDict[dirname.split("tag_")[1]] = extList

tagnames = [r.encode('utf-8') for r in list(set(tagnames))]

output = ["word"] + tagnames
print("\t".join(output))
for k, extList in tarDict.items():
    output = [k]
    for tag in tagnames:
        if tag.decode('utf-8') in extList:
            output.append(str(1))
        else:
            output.append(str(0))
    print("\t".join(output))
