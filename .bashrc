#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias l='ls -l'
alias la='ls -A'
alias ll='ls -la'
alias grep='grep --color=auto'
alias cls='clear'
alias crawl='scrapy runspider'
# Phone mirror
alias phoneScreen='scrcpy --fullscreen --rotation=3'
# Starting python venv
alias startVenv='source ~/venv/bin/activate'
alias endVenv='deactivate'
# Pipx
alias rich='pipx run rich-cli'
PS1='[\u@\h \W]\$ '
# Stegseek
alias extract='stegseek --extract'
alias embed='stegseek --embed'
# Audio Player
alias player='python3 ~/Development/scripts/audioPlayer.py &'

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# Monitor setting are in /etc/X11/xorg.conf.d/10-monitor.conf
if pgrep -x "Xorg" > /dev/null; then
  neofetch 
else
  startx
fi
