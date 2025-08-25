#!/usr/bin/env bash

file=$(mktemp --suffix=.png)
while true; do
	rect=$(swaymsg -t get_tree | jq -r '..|select(.focused? == true) | .rect | "\(.x),\(.y) \(.width)x\(.height)"')
	grim -g "$rect" "$file"
	mods --no-cache -q -i "$file" -j "$(<./schema.json)" -a llama-cpp -m dummy 'describe the screenshot in three sentences: what is the user doing right now?'
	sleep 1
done
