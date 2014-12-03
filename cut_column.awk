#!/bin/awk -f
#encoding: utf-8

function output(once, name, word) {
    if (once) {
        printf "%s\t%s", name, word
        once = 0
    } else {
        printf "\t%s", word
    }
    return once
}

BEGIN {
    OFS = "\t"
}
{
    if (NR == FNR) {
        arr[$1] = NR
    } else {
        once = 1
        if (FNR == 1) {
            for (i=2;i<=NF;i++) {
                if ($i in arr) {
                    once = output(once, "word", $i)
                    indexes[i] = i
                }
            }
        } else {
            for (i=1;i<=NF;i++) {
                if (i in indexes) {
                    if ($i == 0) {
                        key = 0
                    } else {
                        key = 1
                    }
                    once = output(once, $1, $i)
                }
            }
        }
        printf "\n"
    }
}
