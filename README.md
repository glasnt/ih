*A very persuasive package, for creating embroidery patterns.*

`ih` is a Python command-line tool for generating cross-stitch patterns from source images. 

Would you prefer to use a website instead? Try [`ih` as a Service](https://github.com/glasnt/ih-aas)

[As seen at PyCon US 2019](https://us.pycon.org/2019/schedule/presentation/229/)

## How to cross-stitch

Check out this amazing [Cross Stitch Carpentry](https://sgibson91.github.io/cross-stitch-carpentry/index.html) lesson!

# `ih` technical details  

## Installation

Requires [Python 3.7+](https://www.python.org/downloads/) and [`pip`](https://pip.pypa.io/en/stable/installing/):

```
pip install ih
```

`ih` is now usable as a CLI. 

## CLI Usage

```
Usage: ih [OPTIONS] IMAGE

Options:
  -p, --palette TEXT     Choices: lego, floss, perler, alpaca, wool. Default:
                         wool
  -s, --scale INTEGER    Rescale factor. Default: 1
  -c, --colours INTEGER  Limit palette to at most N colors. Default: 256
  -r, --render           Render a preview (using thread images)
  -g, --guidelines       Render guidelines
  --help                 Show this message and exit.
```

Example usage:  

```
ih -p alpaca -s 16 -r -c 4 demo_image.png
```

> For the [demo image](demo_image.png) ([source](https://picsart.com/i/sticker-pixel-pixelart-pixelated-pixels-llama-rainbow-bow-268615356021211), freetoedit) 
> using the alpaca palette, 
> and scaling the input image x16 smaller, 
> render the result in up to 4 colours

Open `demo_image.html` to see the result. 

![sample render](https://user-images.githubusercontent.com/813732/72396688-68d7f800-3735-11ea-8a86-198931db374b.jpg)


## Install from source

Using [`git`](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and [`virtualenv`](https://virtualenv.pypa.io/en/latest/installation/):

```
git clone git@github.com:glasnt/ih
cd ih
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## `ih` as a module

See its use in [`ih-aas`](https://github.com/glasnt/ih-aas/blob/master/app.py)

## Package name origin

Disney's [_Lilo and Stitch_](https://www.youtube.com/watch?v=ItYmxezZ7QA): 

> Jumba: What?! After all you put me through you expect me to help you just like that?! Just like that?!<br>
> Stitch: Ih.<br>
> Jumba: Fine.<br>
> Pleakley: Fine? You're doing what he says?<br>
> Jumba: Uh, he's very persuasive.



## Attributions

LILO & STITCH is a trademark of Disney Enterprises, Inc.

LEGO® is a registered trademark of The Lego Group. 

PERLER BEADS is a trademark of Stitch Acquisition Group. 

