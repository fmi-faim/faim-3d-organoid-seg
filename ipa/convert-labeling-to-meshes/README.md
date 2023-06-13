# Convert labeling to meshes
The `convert_labeling.py` script converts an unsigned integer image to meshes by applying the [marching cubes](https://scikit-image.org/docs/stable/auto_examples/edges/plot_marching_cubes.html) algorithm. 
All meshes are saved as [`.stl`](https://de.wikipedia.org/wiki/STL-Schnittstelle) and [`.bmf`](https://pypi.org/project/binarymeshformat/) files. 

## Input
The input image data type must be unsigned integer, where 0 indicates background. Each positiv integer value is considered a foreground label for which a mesh representation is computed. The input images are expected to be tiff files.

## Output
* `<input-file-name>_MESH.stl`: Containing all meshes of each object.
* `<input-file-name>_MESH.bmf`: Containing mesh-tracks for each object. 

The meshes are rescaled such that the longest edge of the input volume in real world spacing equals 1 (see [mesh scale factor](https://github.com/PaluchLabUCL/DeformingMesh3D-plugin/issues/11)).

## Requirements
```
scikit-image
binarymeshformat
numpy-stl
```

## Running the script
The script expects a config file with the name `convert_labeling.yaml` in the working directory. The config file can either be built with the `build_config.py` script or manually. The following content is expected:
```yaml
input_dir: ../relative/path/to/label_image_directory
spacing:     # label image spacing 
- 0.6        # Z
- 0.216      # Y
- 0.216      # X
step_size: 3 # used by marchin cubes to generate a coarser mesh
output_dir: ../relative/path/to/output_directory
```

Run the script from the working directory with:
`python ../relative/path/to/ipa/convert-labeling-to-meshes/convert_labeling.py`
