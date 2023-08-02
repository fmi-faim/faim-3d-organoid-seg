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

logger = logging.Logger('Deform Meshes')
now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
handler = logging.FileHandler(f"{now}-deform_meshes.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def deform_meshes(options: dict):
    config.set_m2_repo(options.pop("m2_repo"))
    config.set_cache_dir(options.pop("jgo_cache_dir"))
    ij = imagej.init(["paluchlab:Deformable_Mesh:0.9.10","net.imagej:imagej"])
    image = imread(options.pop("image_path"))
    data_array = xr.DataArray(image, dims=["z","y","x"])
    options["intensity_image"] = data_array
    script_path = Path(__file__).with_name("Mesh_Deformation.groovy")
    with script_path.open("r") as f:
        script = f.read()
    label_image = ij.py.run_script(language="groovy", script=script, args=options).getOutput("label_image")
    logger.info(label_image.shape)


if __name__ == "__main__":
    with open('deform_meshes.yaml', 'r') as f:
        options = yaml.safe_load(f)

    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Run deform_meshes with the following parameters: {config}")


    deform_meshes(
        options=options,
    )

    logger.info("Done!")
