#!/usr/bin/env bash

yq . example.yaml -oj | quicktype --lang schema | jq '{ type: "json_schema", json_schema: { name: "user_activity", schema: .definitions.TopLevel }}' >schema.json
