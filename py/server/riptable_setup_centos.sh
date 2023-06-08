#!/usr/bin/env bash

set -ex

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p ./miniconda3
eval "./miniconda3/bin/conda shell.bash hook" > .bashrc
source .bashrc
conda init
conda config --set auto_activate_base false
rt_env="/usr/illumon/dnd/rt_env"
req_txt="/usr/illumon/dnd/io.deephaven.enterprise.dnd-0.24.2-1.20230511.058/py/resources/requirements.txt"
conda create -q -y --override-channels -c conda-forge -p $rt_env python=3.8 abseil-cpp=='20220623.*' benchmark'>=1.7,<1.8' tbb-devel=='2021.6.*' zstd'>=1.5.2,<1.6'
conda activate $rt_env 
pip install -r $req_txt
#apt update
#apt install -y g++ cmake
pip install --upgrade pip
#sudo yum install -y centos-release-scl
#sudo yum install -y devtoolset-8
#scl enable devtoolset-8 bash
pip install -v --upgrade riptide_cpp
pip install riptable
python -c "import riptable"
#pip install deephaven_core-0.24.2-py3-none-any.whl[autocomplete]
#echo "/opt/deephaven/rt_env/lib" >> /etc/ld.so.conf
#ldconfig
