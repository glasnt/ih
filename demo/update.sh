#!/bin/bash

update=${1:-p}
# WARNING ERRORONOUS

echo "We will be releasing a $update update ($(git vb $update -d))"

read -r -p "Are you sure? [y/N] " response
if [[ "$response" =~ ^(yes|y)$ ]]
then

  echo "processing"
  sleep 1

  echo "Update CLI usage"
  python demo/update_readme.py

  git add . && git commit -m "update cli usage"

  echo "bump"
  git version-bump $update

  echo "use new version"
  source venv/bin/activate
  pip install -e . 
  ih --version
  ih -p alpaca -r -c 4 demo/demo_image.png -f demo/ 
  deactivate 

  echo "Update demo render"
  node demo/update_render.js

  git add . && git commit -m "update demo render"

  git release
else
  echo "Not continuing"

fi
