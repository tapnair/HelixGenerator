__author__ = 'Patrick Rainsberry'

import adsk.core
import adsk.fusion
import traceback


# Externally usable function to get all relevant application objects easily in a dictionary
def get_app_objects():

    app = adsk.core.Application.cast(adsk.core.Application.get())

    # Get import manager
    import_manager = app.importManager

    # Get User Interface
    ui = app.userInterface

    # Get active design
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    document = app.activeDocument

    # Get Design specific elements
    units_manager = design.unitsManager
    export_manager = design.exportManager
    root_comp = design.rootComponent
    time_line = product.timeline

    # Get top level collections
    all_occurrences = root_comp.allOccurrences
    all_components = design.allComponents

    app_objects = {
        'app': app,
        'design': design,
        'import_manager': import_manager,
        'ui': ui,
        'units_manager': units_manager,
        'all_occurrences': all_occurrences,
        'all_components': all_components,
        'root_comp': root_comp,
        'time_line': time_line,
        'export_manager': export_manager,
        'document': document
    }
    return app_objects


# Starts a time line group
def start_group():
    # Gets necessary application objects
    app_objects = get_app_objects()

    # Start time line group
    start_index = app_objects['time_line'].markerPosition

    return start_index


# Ends a time line group
def end_group(start_index):

    # Gets necessary application objects
    app_objects = get_app_objects()

    end_index = app_objects['time_line'].markerPosition - 1

    app_objects['time_line'].timelineGroups.add(start_index, end_index)


# Import dxf file with one sketch per layer
def import_dxf(dxf_file, component, plane):

    # Get import manager
    import_manager = get_app_objects()['import_manager']

    # Import dxf file to the component
    dxf_options = import_manager.createDXF2DImportOptions(dxf_file, plane)
    import_manager.importToTarget(dxf_options, component)

    # Return reference to created sketches
    sketches = dxf_options.results
    return sketches


# Get Sketch by name
def sketch_by_name(sketches, name):

    return_sketch = None

    for sketch in sketches:
        if sketch.name == name:
            return_sketch = sketch

    return return_sketch


# Create extrude features of all profiles in a sketch into the given component by a distance
def extrude_all_profiles(sketch, distance, component, operation):

    # Create Collection for all Profiles
    profile_collection = adsk.core.ObjectCollection.create()
    for profile in sketch.profiles:
        profile_collection.add(profile)

    # Create an extrusion
    extrudes = component.features.extrudeFeatures
    ext_input = extrudes.createInput(profile_collection, operation)
    distance_input = adsk.core.ValueInput.createByReal(distance)
    ext_input.setDistanceExtent(False, distance_input)
    extrudes.add(ext_input)


# Creates a new component in the target component
def create_component(target_component, name):
    transform = adsk.core.Matrix3D.create()
    new_occurrence = target_component.occurrences.addNewComponent(transform)
    new_occurrence.component.name = name

    return new_occurrence