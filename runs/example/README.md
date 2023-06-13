# Convert Labeling
## Pre-requisits
* Make sure that micromamba is initialized (see [root-README.md](../../README.md)).
* Activate environment with the required packages installed (`micromamba activate organoid-seg`).

## Build Config
From this directory (`runs/example`):

```shell
python ../../ipa/convert-labeling-to-meshes/build_config.py
```

This command will write the `convert_labeling.yaml` to the current directory. 

## Run Script
From this directory (`runs/example`):

```shell
python ../../ipa/convert-labeling-t-meshes/convert_labeling.py
```

This will compute the meshes and store them in the configure `output_dir`. Additionally a log file is written in this directory (`runs/example`).
