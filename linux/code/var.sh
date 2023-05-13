#!/bin/bash

cur_pid=$$

echo "echo \$\$ > tt.pid" > tmp.sh
chmod +x tmp.sh

if [[ "$1" == "source" ]]; then
    # shellcheck source=/dev/null
    source tmp.sh
else
    bash tmp.sh
fi


if [ -f "tt.pid" ]; then
    s_pid=$(cat tt.pid)
    rm "tt.pid"
fi

if [ -f "tmp.sh" ]; then
    rm "tmp.sh"
fi

echo "$s_pid"


if (( cur_pid == s_pid )); then
    printf "one process %6d\n" $cur_pid
else
    printf "not a process: %6d and %6d\n" $cur_pid "$s_pid"
fi
