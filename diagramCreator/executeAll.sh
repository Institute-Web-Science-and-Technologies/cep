#!/bin/bash
python ChunkSizesCompEffort.py ../processedValues ../diagrams latex
python ChunkSizesCompEffort.py ../processedValues ../diagrams svg

python CompEffortPerChunk.py ../processedValues ../diagrams latex
python CompEffortPerChunk.py ../processedValues ../diagrams svg

python ChunkSizesMatch.py ../processedValues ../diagrams latex
python ChunkSizesMatch.py ../processedValues ../diagrams svg

python MatchesPerChunk.py ../processedValues ../diagrams latex
python MatchesPerChunk.py ../processedValues ../diagrams svg

python LoadingTime_10VMs20VM40VMs_1000M_HHMCovers.py ../processedValues ../diagrams latex
python LoadingTime_10VMs20VM40VMs_1000M_HHMCovers.py ../processedValues ../diagrams svg

python LoadingTime_20VMs_500M1000M2000M_HHMCovers.py ../processedValues ../diagrams latex
python LoadingTime_20VMs_500M1000M2000M_HHMCovers.py ../processedValues ../diagrams svg

python 10VMs_1000M_AllCovers.py ../processedValues ../diagrams latex
python 10VMs_1000M_AllCovers.py ../processedValues ../diagrams svg

python 10VMs_1000M_HHMVCovers.py ../processedValues ../diagrams latex
python 10VMs_1000M_HHMVCovers.py ../processedValues ../diagrams svg

python 10VMs_1000M_HHMV2CCovers.py ../processedValues ../diagrams latex
python 10VMs_1000M_HHMV2CCovers.py ../processedValues ../diagrams svg

python 10VMs_1000M_HHMCCovers.py ../processedValues ../diagrams latex
python 10VMs_1000M_HHMCCovers.py ../processedValues ../diagrams svg

python 10VMs_1000M_HHMCovers.py ../processedValues ../diagrams latex
python 10VMs_1000M_HHMCovers.py ../processedValues ../diagrams svg

#python 10VMs_1000M_HaCovers_BLRType.py ../processedValues ../diagrams latex
#python 10VMs_1000M_HaCovers_BLRType.py ../processedValues ../diagrams svg

#python 10VMs_1000M_HiCovers_BLRType.py ../processedValues ../diagrams latex
#python 10VMs_1000M_HiCovers_BLRType.py ../processedValues ../diagrams svg

#python 10VMs_1000M_MCovers_BLRType.py ../processedValues ../diagrams latex
#python 10VMs_1000M_MCovers_BLRType.py ../processedValues ../diagrams svg

#python 10VMs_1000M_HHMCovers_LL.py ../processedValues ../diagrams latex
#python 10VMs_1000M_HHMCovers_LL.py ../processedValues ../diagrams svg

#python 10VMs_1000M_HHMCovers_RL.py ../processedValues ../diagrams latex
#python 10VMs_1000M_HHMCovers_RL.py ../processedValues ../diagrams svg

python 10VMs_1000M_H2Covers.py ../processedValues ../diagrams latex
python 10VMs_1000M_H2Covers.py ../processedValues ../diagrams svg

python 20VMs_1000M_HHMCCovers.py ../processedValues ../diagrams latex
python 20VMs_1000M_HHMCCovers.py ../processedValues ../diagrams svg

python 20VMs_1000M_HHMCovers.py ../processedValues ../diagrams latex
python 20VMs_1000M_HHMCovers.py ../processedValues ../diagrams svg

#python 20VMs_1000M_HHMCovers_LL.py ../processedValues ../diagrams latex
#python 20VMs_1000M_HHMCovers_LL.py ../processedValues ../diagrams svg

#python 20VMs_1000M_HHMCovers_RL.py ../processedValues ../diagrams latex
#python 20VMs_1000M_HHMCovers_RL.py ../processedValues ../diagrams svg

python 20VMs_500M_HHMCovers.py ../processedValues ../diagrams latex
python 20VMs_500M_HHMCovers.py ../processedValues ../diagrams svg

python 20VMs_2000M_HHMCovers.py ../processedValues ../diagrams latex
python 20VMs_2000M_HHMCovers.py ../processedValues ../diagrams svg

python 40VMs_1000M_HHMCovers.py ../processedValues ../diagrams latex
python 40VMs_1000M_HHMCovers.py ../processedValues ../diagrams svg

python 40VMs_1000M_HHMCCovers.py ../processedValues ../diagrams latex
python 40VMs_1000M_HHMCCovers.py ../processedValues ../diagrams svg

python 10VMs20VMs40VMs_1000M_HaCovers.py ../processedValues ../diagrams latex
python 10VMs20VMs40VMs_1000M_HaCovers.py ../processedValues ../diagrams svg

python 10VMs20VMs40VMs_1000M_HiCovers.py ../processedValues ../diagrams latex
python 10VMs20VMs40VMs_1000M_HiCovers.py ../processedValues ../diagrams svg

python 10VMs20VMs40VMs_1000M_MCovers.py ../processedValues ../diagrams latex
python 10VMs20VMs40VMs_1000M_MCovers.py ../processedValues ../diagrams svg

python 20VMs_500M1000M2000M_HaCovers.py ../processedValues ../diagrams latex
python 20VMs_500M1000M2000M_HaCovers.py ../processedValues ../diagrams svg

python 20VMs_500M1000M2000M_HiCovers.py ../processedValues ../diagrams latex
python 20VMs_500M1000M2000M_HiCovers.py ../processedValues ../diagrams svg

python 20VMs_500M1000M2000M_MCovers.py ../processedValues ../diagrams latex
python 20VMs_500M1000M2000M_MCovers.py ../processedValues ../diagrams svg