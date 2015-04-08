#!/bin/bash

#set -x

java=$1
class=${java%.java}
class=${class##*/}

javac ${java}

cd /src
ls -altr ${class}.class
java -cp . ${class}

