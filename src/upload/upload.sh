#!/bin/bash 
# script to upload blocks and building footprints from Midway to S3.
DATA="/project2/bettencourt/mnp/prclz/data"

# check we have everything we need 
module load python/3.7.0
pip3 install awscli --user
ls ~/.aws/credentials 
aws="python -mawscli"

# create buckets
$aws s3 mb s3://realignment-feasibility-buildings
$aws s3 mb s3://realignment-feasibility-blocks

# upload tables 
for country in "$@"; do 
    $aws s3 cp ${DATA}"/blocks/${country}"    s3://realignment-feasibility-blocks/"${country}"    --recursive
    $aws s3 cp ${DATA}"/buildings/${country}" s3://realignment-feasibility-buildings/"${country}" --recursive
done 