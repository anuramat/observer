#!/usr/bin/env bash

yq '{ "type": "json_schema", "json_schema": { "name": "user_activity", "schema": . }}' -py schema.yaml -oj >schema.json
