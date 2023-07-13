import os
from os.path import join

import questionary
import yaml


def build_config():
    cwd = os.getcwd()

    intensity_image = questionary.path("Path to intensity image:").ask()
    intensity_image = os.path.relpath(intensity_image, cwd)

    input_mesh_file = questionary.path("Path to mesh file:").ask()
    input_mesh_file = os.path.relpath(input_mesh_file, cwd)

    output_mesh_file = questionary.path("Path to mesh output file (will be created):").ask()
    output_mesh_file = os.path.relpath(output_mesh_file, cwd)

    gamma = float(questionary.text(
        "Gamma:",
        default="200.0",
        validate=lambda v: v.replace(".", "").isdigit()
    ).ask())
    alpha = float(questionary.text(
        "Alpha:",
        default="3.0",
        validate=lambda v: v.replace(".", "").isdigit()
    ).ask())
    pressure = float(questionary.text(
        "Pressure:",
        default="0.0",
        validate=lambda v: v.replace(".", "").isdigit(),
    ).ask())
    steric_neighbors = float(questionary.text(
        "Steric neighbors:",
        default="0.0",
        validate=lambda v: v.replace(".", "").isdigit(),
    ).ask())
    image_weight = float(questionary.text(
        "Image weight:",
        default="0.0002",
        validate=lambda v: v.replace(".", "").isdigit(),
    ).ask())
    divisions = int(questionary.text(
        "Divisions:",
        default="2",
        validate=lambda v: v.isdigit(),
    ).ask())
    beta = float(questionary.text(
        "Beta:",
        default="5.0",
        validate=lambda v: v.replace(".", "").isdigit(),
    ).ask())
    n_iterations = int(questionary.text(
        "Number of iterations:",
        default="100",
        validate=lambda v: v.isdigit(),
    ).ask())
    n_batches = int(questionary.text(
        "Number of batches (re-meshing):",
        default="5",
        validate=lambda v: v.isdigit(),
    ).ask())

    config = {
        "intensity_image": intensity_image,
        "input_mesh_file": input_mesh_file,
        "output_mesh_file": output_mesh_file,
        "gamma": gamma,
        "alpha": alpha,
        "pressure": pressure,
        "steric_neighbors": steric_neighbors,
        "image_weight": image_weight,
        "divisions": divisions,
        "beta": beta,
        "n_iterations": n_iterations,
        "n_batches": n_batches,
    }

    with open(join(cwd, "deform_meshes.yaml"), "w") as f:
        yaml.safe_dump(config, f, sort_keys=False)

if __name__ == "__main__":
    build_config()
