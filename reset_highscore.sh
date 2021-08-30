#!/bin/bash
# Hack if want to reset highscore.
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games 
SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR} 
SCRIPT_BASE=$(pwd)

mv ./highscore.p ./highscore.p.bak
touch ./highscore.p
