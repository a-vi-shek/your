"""
Generate UR Script movep motion (blend circular and move linerar in tool-space to target) command 
Vers:20140307
Input:
	target plane [Generic Data] - Target plane to move towards
	base [Generic Data] - A reference plane used as the basis for calculating target pose
	acceleration (in, optional) [Generic Data] - Optional. Tool accel in m/s^2
	velocity (in, optional) [Generic Data] - Optional. Tool speed in m/s
	radius (in, optional) [Generic Data] - Optional. Blend radius in m
Returns:
	out [Text] - The execution information, as output and error streams
	a [Generic Data] - Script variable Python
"""
import scriptcontext as sc
import urscript as ur
import Rhino.Geometry as rg
from Grasshopper.Kernel import GH_RuntimeMessageLevel as gh_msg

error_inputs = []
if not target: error_inputs.append('target')
if not base: error_inputs.append('base')

if not error_inputs:
    target_plane = rg.Plane(target)
    accel = float(accel) if accel else 1.2
    vel = float(vel) if vel else 0.3
    blend = float(radius) if radius else 0.0
    
    matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, base)
    target_plane.Transform(matrix)
    target_pose = ur.pose_by_plane(target_plane)
    a = ur.movep(target_pose,accel,vel, blend)
else:
    error_message = 'Failed to collect data for {0} required input(s): {1}'.format(len(error_inputs), ','.join(error_inputs))
    ghenv.Component.AddRuntimeMessage(gh_msg.Warning, error_message)