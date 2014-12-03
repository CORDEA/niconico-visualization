#!/usr/bin/env python
# encoding:utf-8
#

__Author__ =  "Yoshihiro Tanaka"
__date__   =  "2014-11-21"

import json, urllib2
import os, sys, re, commands, time, datetime

def getJSON(arg, start, end):
    # ref. http://search.nicovideo.jp/docs/api/contest.html
    data = {
    "query"   : sys.argv[1],
    "service" : ["video"],
    "search"  : [
        "title",
        "description",
        "tags"
        ],
    "join" : [
        "tags"
        #"cmsid",
        #"title",
        #"start_time",
        #"view_counter",
        #"comment_counter",
        #"mylist_counter",
        #"length_seconds"
        ],
    "sort_by" : "view_counter",
    "order"   : "desc",
    "from"    : start,
    "size"    : end,
    "issuer"  : "api",
    "reason"  : "ma10"
    }

    # ref. http://stackoverflow.com/questions/9746303/how-do-i-send-a-post-request-as-a-json
    req = urllib2.Request('http://api.search.nicovideo.jp/api/')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data)).read()
    return response

if __name__ == '__main__':
    arg = str(sys.argv[1]).rstrip("/")
    try:
        start = int(sys.argv[2])
        print("start from " + str(start))
    except Exception as e:
        start = 0
    escapes = {'"': "%dq", "'": "%sq", ";": "%sc", "/": "%sl", " ": "_", "|": "%pp", "<": "%lt", ">": "%gt"}
    escapeArg = ""
    for s in arg:
        if s in escapes:
            escapeArg += escapes[s]
        else:
            escapeArg += s
    _HOME = "animes"
    _DIR = _HOME + "/tag_" + escapeArg
    print _DIR
    exists = commands.getoutput('mkdir ' + _DIR)
    if len(exists) != 0:
        _DIR = _HOME + "/tag_" + escapeArg + "_" + str(2)
        exists = commands.getoutput('mkdir ' + _DIR)
        if len(exists) != 0:
            overlap = int(commands.getoutput('find ' + _HOME + '/ -name "tag_' + escapeArg + '_*"').split("_")[-1])
            _DIR = _HOME + "/tag_" + escapeArg + "_" + str(overlap + 1)
            os.system('mkdir ' + _DIR)
    
    i = start
    end = 1
    response = getJSON(arg, i, end)
    total = int(re.split('"total":|}', response)[1])
    print("total: " + str(total))

    end = 100
    err = 0
    while True:
        if i == 1700:
            break
        if total - i < 100:
            end = total - i
        response = getJSON(arg, i, end)
        if "errid" in response:
            code = re.split('"errid":"|"}', response)[1]
            err += 1
            if err >= 5:
                print "Error was repeated 5 times."
                break
            print("Error was returned. code: " + str(code))
            with open(_HOME + "/log/" + str(datetime.datetime.today().strftime("%Y-%m-%d_%H:%M:%S_%f")) + ".log", "w") as f:
                f.write(response)
            time.sleep(30.0)
        else:
            with open(_DIR + "/" + str(datetime.datetime.today().strftime("%Y-%m-%d_%H:%M:%S_%f")) + ".json", "w") as f:
                f.write(response)
            i += 100
            if end == 100:
                print(str(i) + ' items get the data about the "' + arg + '".')
            else:
                print(str(i + end - 100) + ' items get the data about the "' + arg + '".')
                break
            err = 0
        time.sleep(0.5)
