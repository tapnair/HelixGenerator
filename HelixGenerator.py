#Author-Patrick Rainsberry
#Description-Generates a helical curve

import adsk.core, adsk.fusion, traceback
import math


# global event handlers referenced for the duration of the command
handlers = []

commandName = 'Helix'
commandDescription = 'Create a Helix Curve'
command_id = 'cmd_Helix2'
menu_panel = 'SketchPanel'
commandResources = './resources'

def helixMaker(inputs):
    ui = None
    theta = 2*math.pi
    try:
        # We need access to the inputs within a command during the execute.
        for input in inputs:
            if input.id == 'radius':
                radius = input.value
            elif input.id == 'revolutions':
                revolutions = input.value
            elif input.id == 'pitch':
                pitch = input.value
            elif input.id == 'resolution':
                resolution = input.value
            elif input.id == 'PlaneSelect':
                plane = input.selection(0).entity
                    
        # Get Fusion Objects                    
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        
        # Get the root component of the active design.
        rootComp = design.rootComponent
        
        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches
        #xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(plane)
        
        # Collection to hold CAM Profile points
        points = adsk.core.ObjectCollection.create()
               
        for t in range(0, int(revolutions*resolution)+1):
            x = radius * math.cos(theta*t/resolution)
            y = radius * math.sin(theta*t/resolution)
            z = pitch * t / resolution
            point = adsk.core.Point3D.create(x, y, z)
            points.add(point)
        
        # Create Spline through points
        sketch.sketchCurves.sketchFittedSplines.add(points);

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            
            
def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Handle the input changed event.        
        class executePreviewHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                app = adsk.core.Application.get()
                ui  = app.userInterface
                try:
                    cmd = args.firingEvent.sender
                    inputs = cmd.commandInputs
                    helixMaker(inputs)
                    
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'
                        .format(traceback.format_exc()))
                        
        # Handle the execute event.
        class CommandExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:  
                    # Get values from input form
                    cmd = args.firingEvent.sender
                    inputs = cmd.commandInputs
                    helixMaker(inputs)
                                        
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'
                        .format(traceback.format_exc()))
        
        # Handle the execute event.
        class CommandCreatedEventHandlerPanel(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    product = app.activeProduct
                    design = adsk.fusion.Design.cast(product)
                    unitsMgr = design.unitsManager
                    
                    # Setup Handlers for update and execute                   
                    cmd = args.command
                    onExecute = CommandExecuteHandler()
                    cmd.execute.add(onExecute)
                    onUpdate = executePreviewHandler()
                    cmd.executePreview.add(onUpdate)
                    
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)
                    handlers.append(onUpdate)
                    
                    # Define UI Elements
                    commandInputs_ = cmd.commandInputs                
                  
                    # Add all parameters to the input form
                    # Create the Selection input to have a planar face or construction plane selected.                
                    selInput = commandInputs_.addSelectionInput('PlaneSelect', 'Plane', 'Select sketch plane.')
                    selInput.addSelectionFilter('PlanarFaces')
                    selInput.addSelectionFilter('ConstructionPlanes')
                    selInput.setSelectionLimits(1,1)
                    
                    radius_input = adsk.core.ValueInput.createByReal(2.54)
                    commandInputs_.addValueInput('radius', 'Radius', unitsMgr.defaultLengthUnits , radius_input)

                    pitch_input = adsk.core.ValueInput.createByReal(2.54)
                    commandInputs_.addValueInput('pitch', 'Pitch', unitsMgr.defaultLengthUnits , pitch_input)
                    
                    #resolution_input = adsk.core.ValueInput.createByReal(10)
                    commandInputs_.addIntegerSpinnerCommandInput('resolution', 'Resolution', 0, 1000, 5, 1)
                    
                    #revolutions_input = adsk.core.ValueInput.createByReal(5)
                    commandInputs_.addIntegerSpinnerCommandInput('revolutions', 'Revolutions', 0, 1000, 1, 1)
                                  
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'
                        .format(traceback.format_exc()))
                                       
        # Get the UserInterface object and the CommandDefinitions collection.
        cmdDefs = ui.commandDefinitions
         
        # Create a basic button command definition.
        buttonDef = cmdDefs.addButtonDefinition(command_id, 
                                                commandName, 
                                                commandDescription, 
                                                commandResources)                                               
        # Setup Event Handler
        onCommandCreated = CommandCreatedEventHandlerPanel()
        buttonDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)

        # Add the controls to the Inspect toolbar panel.
        modifyPanel = ui.allToolbarPanels.itemById(menu_panel)
        buttonControl = modifyPanel.controls.addCommand(buttonDef)
        buttonControl.isVisible = True
        

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        commandDef = ui.commandDefinitions.itemById(command_id)
        commandDef.deleteMe()

        panel = ui.allToolbarPanels.itemById(menu_panel)
        control = panel.controls.itemById(command_id)
        control.deleteMe()
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
