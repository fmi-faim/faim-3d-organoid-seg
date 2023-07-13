import imagej
import logging
import os
import xarray as xr
import yaml

from datetime import datetime
from pathlib import Path
from scyjava import config, jimport
from tifffile.tifffile import imread
from tqdm import tqdm

logger = logging.Logger('Convert Labeling')
now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
handler = logging.FileHandler(f"{now}-convert_labeling.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def deform_meshes(options: dict):
    ij = imagej.init(["paluchlab:Deformable_Mesh:0.9.9-SNAPSHOT","net.imagej:imagej"])
    image = imread(options.pop("image_path"))
    data_array = xr.DataArray(image, dims=["z","y","x"])
    options["intensity_image"] = data_array
    with open("Mesh_Deformation.groovy") as f:
        script = f.read()
    ij.py.run_script(language="groovy", script=script, args=options)


if __name__ == "__main__":
    with open('deform_meshes.yaml', 'r') as f:
        config = yaml.safe_load(f)

    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Run deform_meshes with the following parameters: {config}")


    deform_meshes(
        options=config,
    )

    logger.info("Done!")
