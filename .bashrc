#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return
alias ls='ls --color=auto'
alias weather='curl wttr.in/ferrara'

LS_COLORS=$LS_COLORS:'di=1;36:pi=0;33:ex=0;91' ; export LS_COLORS

#sym is the separator symbol
#Colors:
#Foreground: 30 black; 31 red; 32 green; 33 yellow; 34 blue; 35 purple; 36 cyan; 37 white; 90 lblack; 91 lred; 92 lgreen; 93 lyellow; 94 lblue; 95 lmagenta; 96 lcyan
#Background: Foreground+10
sym='\ue0b4'

git_line(){
	#It should be placed in the line to show current git repo, but doesn't work
	git_path=""
	if [ -d .git ]; then
		git_path=".git"
	else
		git_path=`git rev-parse --git-dir 2> /dev/null`
	fi
	if [ $git_path = "" ]; then
		echo $'\\001\e[1;37m\\002'
	else
		string=""
		branch=`git branch | grep \* | cut -d ' ' -f2`
		git diff --exit-code > /dev/null
		unstaged=$?
		git diff --cached --exit-code > /dev/null
		uncommitted=$?
		if [ $unstaged = 1 ] || [ $uncommitted = 1 ]; then
			string=$'\\001\e[101;93m\\002 `echo -e $sym` \\001\e[1,90m\\002${branch} \\001\e[100;1;91m\\002'
		else
			string=$'\\001\e[102;93m\\002 `echo -e $sym` \\001\e[1,90m\\002${branch} \\001\e[100;1;92m\\002'
		fi
		echo $string
	fi
	
}

case ${TERM} in
	*termite | *term | rxvt )	
		PS1=$'\\[\e[106;1;90m\\] \u@\h '
		PS1=${PS1}$'\\[\e[103;96m\\]`echo -e $sym`'
		PS1=${PS1}$'\\[\e[1;90m\\] \W '
		PS1=${PS1}$'\\[\e[100;93m\\]`echo -e $sym`'
		PS1=${PS1}$'\\[\e[1;37m\\] \$ '
		PS1=${PS1}$'\\[\e[40;90m\\]`echo -e $sym`'
		PS1=${PS1}$'\\[\e[0m\\] '
		;;
	*)
		PS1='\u@\h | \W | \$ '
		;;
esac

#case ${TERM} in
#	*termite | *term | rxvt )	
#		PS1=$'\\[\e[106;1;90m\\] \u@\h '
#		PS1=${PS1}$'\\[\e[103;96m\\]`echo -e $sym`'
#		PS1=${PS1}$'\\[\e[1;90m\\] \W '
#		PS1=${PS1}$'\\[\e[100;93m\\]`echo -e $sym`'
#		PS1=${PS1}$'\\[\e[1;37m\\] \$ '
#		PS1=${PS1}$'\\[\e[40;90m\\]`echo -e $sym`'
#		PS1=${PS1}$'\\[\e[0m\\] '
#		;;
#	*)
#		PS1='\u@\h | \W | \$ '
#		;;
#esac


PATH="/home/guidofe/perl5/bin${PATH:+:${PATH}}"; export PATH;
PERL5LIB="/home/guidofe/perl5/lib/perl5${PERL5LIB:+:${PERL5LIB}}"; export PERL5LIB;
PERL_LOCAL_LIB_ROOT="/home/guidofe/perl5${PERL_LOCAL_LIB_ROOT:+:${PERL_LOCAL_LIB_ROOT}}"; export PERL_LOCAL_LIB_ROOT;
PERL_MB_OPT="--install_base \"/home/guidofe/perl5\""; export PERL_MB_OPT;
PERL_MM_OPT="INSTALL_BASE=/home/guidofe/perl5"; export PERL_MM_OPT;
