import glob
import os
from time import sleep

import yaml
from stl import mesh
import binarymeshformat as bmf

import numpy as np

from tifffile import imread

from skimage.measure import label, marching_cubes

from numpy.typing import ArrayLike

from tqdm import tqdm
import logging
from datetime import datetime


logger = logging.Logger('Convert Labeling')
now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
handler = logging.FileHandler(f"{now}-convert_labeling.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def create_stl_mesh(vertices: ArrayLike, faces: ArrayLike):
    """
    Build stl mesh from vertices and faces.
    """
    obj = mesh.Mesh(np.zeros((faces.shape[0]), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            obj.vectors[i][j] = vertices[f[j]]

    return obj


def create_bmf_mesh_track(cell_verts_and_faces: list[tuple[ArrayLike, ArrayLike]]):
    tracks = []
    for i, (verts, faces) in enumerate(cell_verts_and_faces):
        bmf_track = bmf.Track(name=f"track_{i}")
        connections = set()
        for f in faces:
            if f[0] < f[1]:
                connections.add((f[0], f[1]))
            else:
                connections.add((f[1], f[0]))

            if f[1] < f[2]:
                connections.add((f[1], f[2]))
            else:
                connections.add((f[2], f[1]))

            if f[2] < f[0]:
                connections.add((f[2], f[0]))
            else:
                connections.add((f[0], f[2]))

        connections = np.array(list(connections))
        bmf_cell = bmf.Mesh(
            positions=tuple(verts[:, ::-1].reshape(-1) ),
            triangles=tuple(faces.reshape(-1)),
            connections=tuple(connections.reshape(-1))
            )
        
        bmf_track.addMesh(0, bmf_cell)
        tracks.append(bmf_track)

    return tracks



def convert_labeling(file: str, spacing: tuple[float], step_size: int, output_dir: str):
    logger.info(f"Convert {file}.")
    # Pad with 0 to avoid open meshes.
    labeling = np.pad(imread(file), 4, mode='constant', constant_values=0)

    shape = np.array(labeling.shape) - 2 * 4
    factor = 1/np.max(shape * np.array(spacing))

    cells = []
    cell_verts_and_faces = []
    for label_id in filter(None, np.unique(labeling)):
        mask = labeling == label_id

        try:
            verts, faces, _, _ = marching_cubes(mask, spacing=spacing, step_size=step_size)
        except:
            logger.warning(f"Object {label_id} is too small for coarse mesh computation.")
            logger.info("Retry mesh computation with step_size = 1.")
            verts, faces, _, _ = marching_cubes(mask, spacing=spacing, step_size=1)
        
        # Shift to origin.
        verts[:, 0] -= ( labeling.shape[0] // 2 ) * spacing[0]
        verts[:, 1] -= ( labeling.shape[1] // 2 ) * spacing[1]
        verts[:, 2] -= ( labeling.shape[2] // 2 ) * spacing[2]
        # Scale: Don't know why this factor is required.
        verts *= factor

        stl_cell = create_stl_mesh(verts, faces)
        cells.append(stl_cell)
        cell_verts_and_faces.append((verts, faces))

    stl_organoid = mesh.Mesh(np.concatenate([c.data for c in cells]))
    bmf_organoid = create_bmf_mesh_track(cell_verts_and_faces)

    name, _ = os.path.splitext(os.path.basename(file))
    stl_organoid.save(os.path.join(output_dir, f"{name}_MESH.stl"))
    bmf.saveMeshTracks(bmf_organoid, os.path.join(output_dir, f"{name}_MESH.bmf"))


if __name__ == "__main__":
    with open('convert_labeling.yaml', 'r') as f:
        config = yaml.safe_load(f)

    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Run segment_background with the following parameters: {config}")

    files = glob.glob(os.path.join(config["input_dir"], "*.tif"))
    logger.info(f"Found {len(files)} images to process.")

    for file in tqdm(files):
        convert_labeling(
            file=file,
            spacing=config['spacing'],
            step_size=config['step_size'],
            output_dir=config['output_dir'],
        )

    logger.info("Done!")