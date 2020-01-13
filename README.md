# ih

A very persuasive package, for creating embroidery patterns. 

[As seen at PyCon US 2019](https://us.pycon.org/2019/schedule/presentation/229/)

## Setup

### Using Pipenv

```
$ pipenv sync
$ pipenv shell
(ih) $ python ./ih
Usage: ih [OPTIONS] IMAGE
Try "ih --help" for help.

Error: Missing argument "IMAGE".
$
```

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

## As A Service

See [ih-aas](https://github.com/glasnt/ih-aas)


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


