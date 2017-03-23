import traceback
import adsk.core
import adsk.fusion
import math
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase
from .Fusion360Utilities.Fusion360Utilities import get_app_objects


# You could change back to this function to create the variable helix
# you will want to do something about adjusting for the resolution in the t multiplier
# As it is now the higher the resolution the wider the curve will get.  
# need to do something like t/resolution probably
def variable_helix_point(radius, pitch, resolution, t):
    # Helix math
    x = (.25*t+.5)*radius * math.cos(2*math.pi*t/resolution)
    y = (.25*t+.5)*radius * math.sin(2*math.pi*t/resolution)
    z = pitch * t / resolution
    
    # Create Fusion point
    point = adsk.core.Point3D.create(x, y, z)
    return point


# Generic Math Function to generate a point on a helix
def helix_point(radius, pitch, resolution, t):
        
    # Helix math
    x = radius * math.cos(2*math.pi*t/resolution)
    y = radius * math.sin(2*math.pi*t/resolution)
    z = pitch * t / resolution
    
    # Create Fusion point
    point = adsk.core.Point3D.create(x, y, z)
    return point


# Generates a Helix in Fusion    
def helix_maker(radius, revolutions, pitch, resolution, plane):

    # Gets necessary application objects
    app_objects = get_app_objects()
    
    # Get the root component of the active design.
    root_comp = app_objects['design'].rootComponent
    
    # Get Sketches Collection for Root component
    sketches = root_comp.sketches
    
    # Add sketch to selected plane
    sketch = sketches.add(plane)
    
    # Collection to hold helix points
    points = adsk.core.ObjectCollection.create()

    # Iterate based on revolutions and resolution
    for t in range(0, int(revolutions*resolution)+1):
        
        # Add Point to collection
        points.add(helix_point(radius, pitch, resolution, t))
        
        # use this instead to create the variable helix
        # points.add(variable_helix_point(radius, pitch, resolution, t))
    
    # Create Spline through points
    sketch.sketchCurves.sketchFittedSplines.add(points)
    
    
# THis is the class that contains the information about your command.
class HelixCommand(Fusion360CommandBase):
    
    # Runs when Fusion command would generate a preview after all inputs are valid or changed
    def on_preview(self, command, inputs, args, input_values):

        # create a helix based on user inputs
        helix_maker(input_values['radius'],
                    input_values['revolutions'],
                    input_values['pitch'],
                    input_values['resolution'],
                    input_values['plane'][0])

    # Runs when the user presses ok button
    def on_execute(self, command, inputs, args, input_values):

        # create a helix based on user inputs
        helix_maker(input_values['radius'],
                    input_values['revolutions'],
                    input_values['pitch'],
                    input_values['resolution'],
                    input_values['plane'][0])
    
    # Runs when user selects your command from Fusion UI, Build UI here
    def on_create(self, command, inputs):

        # Gets necessary application objects
        app_objects = get_app_objects()

        # Get users current units
        default_units = app_objects['units_manager'].defaultLengthUnits
        
        # Create the Selection input to have a planar face or construction plane selected.  
        selection_input = inputs.addSelectionInput('plane', 'Plane', 'Select sketch plane.')
        selection_input.addSelectionFilter('PlanarFaces')
        selection_input.addSelectionFilter('ConstructionPlanes')
        selection_input.setSelectionLimits(1, 1)
        
        # Radius of the helix
        radius_input = adsk.core.ValueInput.createByReal(2.54)
        inputs.addValueInput('radius', 'Radius', default_units, radius_input)
        
        # Pitch of the helix
        pitch_input = adsk.core.ValueInput.createByReal(2.54)
        inputs.addValueInput('pitch', 'Pitch', default_units, pitch_input)
        
        # Define points per revolution -> resolution
        inputs.addIntegerSpinnerCommandInput('resolution', 'Resolution', 0, 1000, 1, 10)
        
        # Number of revolutions
        inputs.addIntegerSpinnerCommandInput('revolutions', 'Revolutions', 0, 1000, 1, 1)
