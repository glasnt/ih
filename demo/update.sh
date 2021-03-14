#!/bin/bash

update=${1:-p}
# WARNING ERRORONOUS AND CONTAINS SIDEEFFECTS

if [[ $(git diff --stat) != '' ]]; then
   echo "dirty git. will not continue"
   exit 0
fi

branch=$(git branch | grep '*' | cut -d' ' -f2)

if [[ "$branch" != 'latest' ]]; then
    echo "not on latest branch. will not continue"
    exit 0
fi

echo "We will be releasing a $update update ($(git vb $update -d))"

read -r -p "Are you sure? [y/N] " response
if [[ "$response" =~ ^(yes|y)$ ]]
then
  echo "processing"
  sleep 1

  echo "Update CLI usage"

  source venv/bin/activate
  pip install -e . 
  ih --version

  python demo/update_readme.py

  git add README.md && git commit -m "update cli usage"

  echo "bump"
  git version-bump $update

  echo "use new version"
  ih --version

  # Hard-copy from README.md example
  ih -p alpaca -r -c 4 demo/demo_image.png -f demo/ 

  deactivate 

  echo "Update demo render"
  node demo/update_render.js

  git add demo/demo_render.png && git commit -m "update demo render"

  git release
else
  echo "user bailed. will not continue"
fi
