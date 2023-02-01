#!/bin/bash

# Request resources:
#SBATCH -c 32     # 1 entire node
#SBATCH --time=04:00:0  # 6 hours (hours:minutes:seconds)
#SBATCH --mem=16G      # 1 GB RAM
#SBATCH -p shared

module load gcc
module load mkl

echo "Running code"
rm output/*

sbcl --dynamic-space-size 16000 --load "notch.lisp" --quit
