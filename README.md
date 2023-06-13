# FAIM 3D Organoid Segmentation

This repo contains a collection of scripts which might be useful for 3D organoid segmentation. 

## infrastructure
In this sub-directory installation instructions/scripts for the different tools are available. 

The setup idea is that you would clone this repo and run the the installation scripts in their respective directories. For example for micromamba you would change directory to `infrastructure/apps` and run the installation script with `sh install_micromamba_linux.sh`. This will download micromamba and install it into `infrastructure/apps/micromamba`.

### Create environments
After micromamba is installed you must initialize your current command line. Simply copy paste the commands from [micromamba initialization](#micromamba-initialization). 

Once micromamba is initialized you can create the required environment with:
```shell
micromamba env create -f infrastructure/environment.yaml
```

Once the environment is created you can activate it with:
```shell
micromamba activate organoid-seg
```

## ipa
Image processing and analysis (ipa) scripts are stored in sub-directories of `ipa/`

## runs
In this directory individual processing run configurations and log-files are stored. 

# Micromamba initialization
The following commands will initialize the local micromamba (in `infrastrucutre/apps`) in you current command line. This step must be repeated in every new shell or after every remote login.

```shell
export MAMBA_EXE="$(pwd)/infrastructure/apps/micromamba/bin/micromamba"
export MAMBA_ROOT_PREFIX="$(pwd)/infrastructure/apps/micromamba"
export MAMBA_ROOT_ENVIRONMENT="$(pwd)/infrastructure/apps/micromamba"

eval "$($MAMBA_ROOT_ENVIRONMENT/bin/micromamba shell hook -s posix)"

export PIP_CACHE_DIR="$(pwd)/infrastructure/apps/micromamba/PIP_CACHE"
```

__Note:__ Don't forget to activate the environment with `micromamba activate organoid-seg`.