#! /bin/sh
for f in `ls`;do grep 'START\|SCREEN_ON\|SCREEN_OFF' $f > $f.filtered1; done;

