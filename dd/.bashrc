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
# Phone mirror
alias phoneScreen='scrcpy --fullscreen --rotation=3'
# Starting python venv
alias startVenv='source ~/venv/bin/activate'
alias endVenv='deactivate'
# Pipx
alias rich='pipx run rich-cli'
PS1='[\u@\h \W]\$ '

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# GithubKey
GithubKey="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"

if pgrep -x "Xorg" > /dev/null; then
  neofetch 
else
  startx
fi
