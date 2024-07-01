if status is-interactive
    # Commands to run in interactive sessions can go here
end
set -g fish_greeting

alias ll "ls -la"
alias l "ls -l"

export PATH=":$PATH"

alias k kubectl
alias tree2 "tree -L 2"
alias gc gcloud 

alias gitlog "git log --pretty=format:"%h%x09%an%x09%ad%x09%s""
alias gl "git log --pretty=format:"%h%x09%an%x09%ad%x09%s""
alias glh "git log --pretty=format:"%h%x09%an%x09%ad%x09%s" | head -n"
alias gb "bash ~/.config/fish/scripts/show-git-branches.sh"

alias v vim

alias t "tail -n"
alias h "head -n"

alias dut "du -sh"
