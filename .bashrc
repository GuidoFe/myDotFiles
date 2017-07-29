#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias weather='curl wttr.in/ferrara'
#TYPES
#di = directory; 
#fi = file; 
#ln = symbolicLink; 
#pi = fifo file; 
#so = socket file; 
#bd = block special file; 
#cd = character special file; 
#or = orphan symbolic link; 
#mi = non existent file pointed by a symbolic link;
#ex = executable file;i
#*.ext = file ending with ext

#EFFECTS
#0   = default colour
#1   = bold
#4   = underlined
#5   = flashing text
#7   = reverse field
#8   = concealed

#COLOURS
#30  = black
#31  = red
#32  = green
#33  = orange
#34  = blue
#35  = purple
#36  = cyan
#37  = grey

#BACKGROUNDS
#40  = black background
#41  = red background
#42  = green background
#43  = orange background
#44  = blue background
#45  = purple background
#46  = cyan background
#47  = grey background

#EXTRA COLOURS
#90  = dark grey
#91  = light red
#92  = light green
#93  = yellow
#94  = light blue
#95  = light purple
#96  = turquoisie
#97  = white
#100 = dark grey background
#101 = light red background
#102 = light green background
#103 = yellow background
#104 = light blue background
#105 = light purple background
#106 = turquoise background
LS_COLORS=$LS_COLORS:'di=1;36:pi=0;33:ex=0,91' ; export LS_COLORS

PS1='[\u@\h \W]\$ '

PATH="/home/guidofe/perl5/bin${PATH:+:${PATH}}"; export PATH;
PERL5LIB="/home/guidofe/perl5/lib/perl5${PERL5LIB:+:${PERL5LIB}}"; export PERL5LIB;
PERL_LOCAL_LIB_ROOT="/home/guidofe/perl5${PERL_LOCAL_LIB_ROOT:+:${PERL_LOCAL_LIB_ROOT}}"; export PERL_LOCAL_LIB_ROOT;
PERL_MB_OPT="--install_base \"/home/guidofe/perl5\""; export PERL_MB_OPT;
PERL_MM_OPT="INSTALL_BASE=/home/guidofe/perl5"; export PERL_MM_OPT;
