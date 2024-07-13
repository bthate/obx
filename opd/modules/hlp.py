# This file is placed in the Public Domain.


"help"


SEP = "/"
NAME = __file__.split(SEP)[-3]
TXT = f"""{NAME.upper()}

    {NAME} <cmd> [key=val] [key==val]

OPTIONS

    -c     run console
    -d     switch to background
    -h     show help
    -i     start services
    -v     use verbose

COMMANDS
    
    $ {NAME} cmd
    cfg,cmd,dpl,err,exp,imp,mod,mre,nme,pwd,rem,res,rss,thr

MODULES

    $ {NAME} mod
    cmd,err,hlp,irc,log,mod,req,rss,tdo,thr,upt

SPLG is Public Domain."""


def hlp(event):
    "show help"
    event.reply(TXT)
