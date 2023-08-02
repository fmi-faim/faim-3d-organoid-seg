#@ File (style="extension:bmf") input_mesh_file
#@ ImagePlus intensity_image
#@ LogService log
#@ Double (value=200.0) gamma
#@ Double (value=3.0) alpha
#@ Double (value=0.0) pressure
#@ Double (value=0.0) steric_neighbors
#@ Double (value=0.0002) image_weight
#@ Integer (value=2) divisions
#@ Double (value=5.0) beta

#@ Integer (value=100) n_iterations
#@ Integer (value=5) n_batches

#@output label_image

import deformablemesh.DeformableMesh3DTools
import deformablemesh.MeshImageStack
import deformablemesh.SegmentationModel 
import deformablemesh.externalenergies.ImageEnergyType
import deformablemesh.geometry.ConnectionRemesher
import deformablemesh.io.MeshReader
import deformablemesh.io.MeshWriter

def remesh(previous) {
	minConnectionLength = 0.01
	maxConnectionLength = 0.02
	return meshes.collect {
		remesher = new ConnectionRemesher()
		remesher.setMinAndMaxLengths(minConnectionLength, maxConnectionLength)
		remesher.remesh(it)
	}
}

reader = new MeshReader(input_mesh_file)
tracks = reader.loadMeshes()

// Map list of tracks to list of meshes on frame 0
FRAME = 0
meshes = tracks.collect {
	it.getMesh(FRAME)
}
log.info( meshes.size() + " meshes loaded." )


// Start mesh deformation
model = new SegmentationModel()
log.info( "Deforming meshes on image " + intensity_image.getTitle() + "(" + intensity_image.getWidth() + "," + intensity_image.getHeight() + "," + intensity_image.getNSlices() + "," + intensity_image.getNChannels() + ")")

model.setGamma(gamma)
model.setAlpha(alpha)
model.setPressure(pressure)
model.setOriginalPlus(intensity_image)
model.setStericNeighborWeight(steric_neighbors)
model.setWeight(image_weight)
model.setDivisions(divisions)
model.setBeta(beta)
model.setImageEnergyType(ImageEnergyType.PerpendicularIntensity)

for (i in 1..n_batches) {
	// deform
	log.info("Batch #" + i + ": deforming with " + n_iterations + " iterations")
	model.deformMeshes(meshes, n_iterations)
	// remesh
	log.info("Batch #" + i + ": remeshing")
	meshes = remesh(meshes)
}


// Add new meshes to tracks object
[tracks, meshes].transpose().each {
	it[0].addMesh(FRAME, it[1])
}

// Convert meshes to label image
log.info("Creating label image...")
mesh_image_stack = new MeshImageStack(intensity_image)
label_image = DeformableMesh3DTools.createUniqueLabelsRepresentation(mesh_image_stack, tracks)
log.info("Done.")
