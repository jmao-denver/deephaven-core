#!/usr/bin/env bash

set -ex

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b
eval "/root/miniconda3/bin/conda shell.bash hook" > .bashrc
source .bashrc
conda init
conda config --set auto_activate_base false
conda create -q -y --override-channels -c conda-forge -p /opt/deephaven/rt_env python=3.10.6 abseil-cpp=='20220623.*' benchmark'>=1.7,<1.8' tbb-devel=='2021.6.*' zstd'>=1.5.2,<1.6'
conda activate /opt/deephaven/rt_env
apt update
apt install -y g++ cmake
pip install --upgrade pip
pip install -v --upgrade riptide_cpp
pip install riptable
python -c "import riptable"
pip install deephaven_core-0.24.2-py3-none-any.whl[autocomplete]
echo "/opt/deephaven/rt_env/lib" >> /etc/ld.so.conf
ldconfig
