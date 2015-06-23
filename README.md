# netkiller
Kills all processes using network connections

Note: this is going to be buggy as hell, and I intend on fixing issues.
I knocked this up in a few hours, and I know there are things that could be MUCH better
I just wanted to put up something

<h3> Usage </h3>

netkiller.py -d=<devices> -k or -9

if you specify '*' for -d, it will kill everything.
usage: prog.py -d=<devices> -9/k/l

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICES, --devices DEVICES
                        Device names to operate on
  -k, --kill            Standard kill, equivalent to 'kill PID'
  -9, --dash-nine       The equivalent of 'kill -9 PID'
