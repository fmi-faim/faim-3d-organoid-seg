import os
from os.path import join

import questionary
import yaml


def build_config():
    cwd = os.getcwd()

    input_dir = questionary.path("Path to directory:").ask()
    input_dir = os.path.relpath(input_dir, cwd)

    z_spacing = float(questionary.text("Z spacing [um]:",
                                 validate=lambda v: v.replace(".", "").isdigit()).ask())
    y_spacing = float(questionary.text("Y spacing [um]:",
                                 validate=lambda v: v.replace(".", "").isdigit()).ask())
    x_spacing = float(questionary.text("X spacing [um]:",
                                 validate=lambda v: v.replace(".", "").isdigit()).ask())
    
    step_size = int(questionary.text("Marching cube step_size:",
                                     default="4",
                                     validate=lambda v: v.isdigit()).ask())
    
    output_dir = questionary.path("Path to output directory:").ask()
    output_dir = os.path.relpath(output_dir, cwd)
    
    config = {
        "input_dir": input_dir,
        "spacing": [z_spacing, y_spacing, x_spacing],
        "step_size": step_size,
        "output_dir": output_dir,
    }

    with open(join(cwd, "convert_labeling.yaml"), "w") as f:
        yaml.safe_dump(config, f, sort_keys=False)

if __name__ == "__main__":
    build_config()
    