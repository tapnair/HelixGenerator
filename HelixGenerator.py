import adsk.core, adsk.fusion, traceback
import math
from . import Fusion360CommandBase

# Helix Command Parameters
commandName1 = 'Helix'
commandDescription1 = 'Create a Helix Curve'
cmdId1 = 'cmd_Helix'
commandResources1 = './resources'
myWorkspace1 = 'FusionSolidEnvironment'
myToolbarPanelID1 = 'SketchPanel'

# Turn on for some helpful messages when debugging your app
debug = False

def getInputs(inputs):
    for input_ in inputs:
        if input_.id == 'radius':
            radius = input_.value
        elif input_.id == 'revolutions':
            revolutions = input_.value
        elif input_.id == 'pitch':
            pitch = input_.value
        elif input_.id == 'resolution':
            resolution = input_.value
        elif input_.id == 'PlaneSelect':
            plane = input_.selection(0).entity
    return (radius, revolutions, pitch, resolution, plane)


# Generic Math Function to generate a point on a helix
def HelixPoint(radius, pitch, resolution, t):
        
    # Helix math
    x = radius * math.cos(2*math.pi*t/resolution)
    y = radius * math.sin(2*math.pi*t/resolution)
    z = pitch * t / resolution
    
    # Create Fusion point
    point = adsk.core.Point3D.create(x, y, z)
    return point


# Generates a Helix in Fusion    
def helixMaker (radius, revolutions, pitch, resolution, plane):
    
    # Get Fusion Objects                    
    app = adsk.core.Application.get()
    design = app.activeProduct
    
    # Get the root component of the active design.
    rootComp = design.rootComponent
    
    # Get Sketches Collection for Root component
    sketches = rootComp.sketches
    
    # Add sketch to selected plane
    sketch = sketches.add(plane)
    
    # Collection to hold helix points
    points = adsk.core.ObjectCollection.create()

    # Iterate based on revolutions and resolution
    for t in range(0, int(revolutions*resolution)+1):
        
        # Add Point to collection
        points.add(HelixPoint(radius, pitch, resolution, t))
    
    # Create Spline through points
    sketch.sketchCurves.sketchFittedSplines.add(points);
    
    
# Command Code
class HelixCommand(Fusion360CommandBase.Fusion360CommandBase):
    
    # Runs when Fusion command would generate a preview after all inputs are valid or changed
    def onPreview(self, command, inputs):
        
        # Get user inputs
        (radius, revolutions, pitch, resolution, plane) = getInputs(inputs)
        
        # create a helix based on inputs
        helixMaker(radius, revolutions, pitch, resolution, plane)
    
    # Runs when the command is destroyed.  Sometimes useful for cleanup after the fact
    def onDestroy(self, command, inputs, reason_):    
        pass
    
    # Runs when when any input in the command dialog is changed
    def onInputChanged(self, command, inputs, changedInput):
        pass
    
    # Runs when the user presses ok button
    def onExecute(self, command, inputs):        
        
        # Get user inputs
        (radius, revolutions, pitch, resolution, plane) = getInputs(inputs)
        
        # create a helix based on inputs 
        helixMaker(radius, revolutions, pitch, resolution, plane)
        
        #A cleaner way would be simply: helixMaker(*getInputs(inputs))
    
    # Runs when user selects your command from Fusion UI, Build UI here
    def onCreate(self, command, inputs):
        app = adsk.core.Application.get()
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        unitsMgr = design.unitsManager
        
        # Create the Selection input to have a planar face or construction plane selected.  
        selInput = inputs.addSelectionInput('PlaneSelect', 'Plane', 'Select sketch plane.')
        selInput.addSelectionFilter('PlanarFaces')
        selInput.addSelectionFilter('ConstructionPlanes')
        selInput.setSelectionLimits(1,1)
        
        # Radius of the helix
        radius_input = adsk.core.ValueInput.createByReal(2.54)
        inputs.addValueInput('radius', 'Radius', unitsMgr.defaultLengthUnits , radius_input)
        
        # Pitch of the helix
        pitch_input = adsk.core.ValueInput.createByReal(2.54)
        inputs.addValueInput('pitch', 'Pitch', unitsMgr.defaultLengthUnits , pitch_input)
        
        # Define points per revolution -> resolution
        inputs.addIntegerSpinnerCommandInput('resolution', 'Resolution', 0, 1000, 1, 10)
        
        # Number of revolutions
        inputs.addIntegerSpinnerCommandInput('revolutions', 'Revolutions', 0, 1000, 1, 1)
        

# Setup and run the Command
newCommand1 = HelixCommand(commandName1, commandDescription1, commandResources1, cmdId1, myWorkspace1, myToolbarPanelID1, debug)


def run(context):
    newCommand1.onRun()


def stop(context):
    newCommand1.onStop()