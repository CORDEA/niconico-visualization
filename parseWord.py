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
__date__   =  "2014-12-01"


import sys, MeCab

def parseWord(word):
    tagger = MeCab.Tagger("-Ochasen")
    node = tagger.parseToNode(word.encode('utf-8'))
    parts = []
    while node:
        part = [r.decode('utf-8') for r in node.feature.split(",")]
        if part[0] == u"動詞" and part[1] == u"自立":
            parts.append(part[6])
        elif part[0] == u"名詞":
            parts.append(part[6])
        node = node.next
    return parts
