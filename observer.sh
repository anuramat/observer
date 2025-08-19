#!/usr/bin/env bash

rect=$(swaymsg -t get_tree | jq -r '..|select(.focused? == true) | .rect | "\(.x),\(.y) \(.width)x\(.height)"')
grim -g "$rect" ./screenshot.png
