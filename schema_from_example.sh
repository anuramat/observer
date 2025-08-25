#!/usr/bin/env bash

yq . example.yaml -py -oj | quicktype --lang schema | yq '.definitions.TopLevel' -pj -oy >schema.yaml
