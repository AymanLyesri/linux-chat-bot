#!/bin/bash

# get the first parametre
# $1 is the first parameter passed to the script
query=$1

# This script is used to search for a query on Google
googler --json $query
