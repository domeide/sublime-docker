#!/bin/bash


export OSX_PKG_FOLDER=~/Library/Application\ Support/Sublime\ Text\ 3/Packages/Docker\ Based\ Build\ Systems/


cp *.sublime-build DockerBuild.py DockerClojureBuild.py DockerJavaBuild.py dockerutils.py "$OSX_PKG_FOLDER"

