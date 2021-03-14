#!/bin/bash

update=${1:-p}
# WARNING ERRORONOUS

echo "We will be releasing a $update update ($(git vb $update -d))"

read -r -p "Are you sure? [y/N] " response
if [[ "$response" =~ ^(yes|y)$ ]]
then

  echo "processing"
  sleep 1

  python demo/update_readme.py

  echo g vb $update

  ih -p alpaca -r -c 4 demo/demo_image.png -f demo/

  node demo/update_render.js

  git add . && git commit -m "update"

  echo git release
else
  echo "Not continuing"

fi
