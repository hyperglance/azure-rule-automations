#!/bin/bash 
./rm-state.sh
./terraform init 
./terraform apply --auto-approve
