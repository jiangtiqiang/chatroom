#!/bin/bash
ID=$(cat /proc/self/cgroup | grep -o  -e "docker-.*.scope" | head -n 1 | sed "s/docker-\(.*\).scope/\\1/")
curl -H "Content-Type: application/json" -X POST -d '{"containerId":"'${ID}'","appId":"'$1'"}' http://10.16.82.141:8080/register/api/container/register

