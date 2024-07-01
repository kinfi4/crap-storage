for branch in $(git branch --format="%(refname:short)"); do
    current_branch=$(git branch --show-current)
    desc=$(git config branch."$branch".description)
    if [ -z "$desc" ]; then
        desc="NO DESCRIPTION"
    fi

    commit=$(git rev-parse --short "$branch")
    commit_msg=$(git log -1 --pretty=format:"%s" "$branch")
    
    if [ "$branch" == "$current_branch" ];
    then
        echo "* $branch [$desc] - $commit - $commit_msg"
    else
        echo "  $branch [$desc] - $commit - $commit_msg"
    fi

done

