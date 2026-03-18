#!/bin/bash
#SBATCH --account=ehros042
#SBATCH --job-name=seaeyes_yolo
#SBATCH --partition=aoraki_gpu
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=logs/yolo_%j.out
#SBATCH --error=logs/yolo_%j.err

module load cuda
module load python

source se/bin/activate

python train.py