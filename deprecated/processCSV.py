import pandas as pd
import numpy as np

###############
## ENTER CSV ##
###############

Duffey_Tyler_2019_FF = pd.read_csv('/root/Trajekt/Duffey_Tyler_2019.csv')

######################################
## CALCULATE SPIN X, SPIN Y, SPIN Z ##
######################################

def calculate_spin_components(data):
    print('CALCULATING SPIN X, SPIN Y, SPIN Z')
    
    # Extract necessary columns from the data
    vx0 = data["vx0"]
    vy0 = data["vy0"]
    vz0 = data["vz0"]
    ax = data["ax"]
    ay = data["ay"]
    az = data["az"]
    
    # Calculate velocity and acceleration magnitudes
    velocity_magnitude = np.sqrt(vx0**2 + vy0**2 + vz0**2)
    acceleration_magnitude = np.sqrt(ax**2 + ay**2 + az**2)
    
    # Calculate velocity and acceleration unit vectors
    velocity_unit_x = vx0 / velocity_magnitude
    velocity_unit_y = vy0 / velocity_magnitude
    velocity_unit_z = vz0 / velocity_magnitude
    acceleration_unit_x = ax / acceleration_magnitude
    acceleration_unit_y = ay / acceleration_magnitude
    acceleration_unit_z = az / acceleration_magnitude

    # Calculate spin axis components
    SpinX = velocity_unit_y * acceleration_unit_z - velocity_unit_z * acceleration_unit_y
    SpinY = velocity_unit_z * acceleration_unit_x - velocity_unit_x * acceleration_unit_z
    SpinZ = velocity_unit_x * acceleration_unit_y - velocity_unit_y * acceleration_unit_x
    
    # Normalize spin axis components
    spin_magnitude = np.sqrt(SpinX**2 + SpinY**2 + SpinZ**2)
    SpinX = SpinX / spin_magnitude
    SpinY = SpinY / spin_magnitude
    SpinZ = SpinZ / spin_magnitude
    
    print('CALCULATED SPIN X, SPIN Y, SPIN Z')
    return SpinX, SpinY, SpinZ

def calculate_spin_axis(data):
    print('CALCULATING SPIN AXIS')
    
    SpinX = data["SpinX"]
    SpinY = data["SpinY"]
    SpinZ = data["SpinZ"]

    spin = np.column_stack((SpinX, SpinY, SpinZ))

    print('CALCULATED SPIN AXIS')
    return spin

def getSimpleLatLon(spin):
    print('CALCULATING SEAM ORIENTATION')
    
    spinAxis = spin / (np.linalg.norm(spin) + 1e-9)
    
    # Assume an identity matrix for hawkeyeRotMat
    hawkeyeRotMat = np.eye(3)
    inverseHawkeyeRotMat = hawkeyeRotMat  # Identity matrix is its own inverse
    
    # Rotate the spin axis from global coordinates to local coordinates
    rotatedSpinAxis = np.dot(inverseHawkeyeRotMat, spinAxis)
    
    # Convert between Trajekt and Hawkeye reference frames (x = -z, y = x, z = -y)
    x, y, z = -rotatedSpinAxis[2], rotatedSpinAxis[0], -rotatedSpinAxis[1]
    
    print('CALCULATED SEAM ORIENTATION')
    return {
        "lon": np.degrees(np.arctan2(y, x)),
        "lat": np.degrees(np.pi/2 - np.arccos(z))
    }
    
#################
## PROCESS CSV ##
#################

def processCSV(data):
    print('PROCESSING CSV')
    
    data = data[['player_name', 'pitch_type', 'release_speed', 'release_spin_rate', 'release_pos_z', 'release_pos_x', 'spin_axis',
                                            'plate_z', 'plate_x', 'pfx_x', 'pfx_z', 'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az']]
    
    spin_x, spin_y, spin_z = calculate_spin_components(data)
    
    # Add spin axis components to the DataFrame
    data["SpinX"] = spin_x
    data["SpinY"] = spin_y
    data["SpinZ"] = spin_z
    
    spin = calculate_spin_axis(data)
    # Add spin axis to the DataFrame
    data["spin"] = list(spin)
    spin_x, spin_y, spin_z = calculate_spin_components(data)
    # Add spin axis components to the DataFrame
    data["SpinX"] = spin_x
    data["SpinY"] = spin_y
    data["SpinZ"] = spin_z
    
    data["SeamLat"] = data["spin"].apply(lambda spin: getSimpleLatLon(np.array(spin))["lat"])
    data["SeamLon"] = data["spin"].apply(lambda spin: getSimpleLatLon(np.array(spin))["lon"])
    
    data = data[['player_name', 'pitch_type', 'release_speed', 'release_spin_rate', 'release_pos_z', 'release_pos_x', 'spin_axis',
                                               'SeamLat', 'SeamLon', 'pfx_x', 'pfx_z', 'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az']]
    
    # Add new columns
    data['PitchTitle'] = data['player_name'] + ' ' + data['pitch_type']
    data['PitchType'] = data['pitch_type']
    data['PitcherFullName'] = data['player_name']
    data['release_pos_y'] = 56.5
    data['PlateLocHeight'] = data['pfx_z']
    data['PlateLocSide'] = data['pfx_x']
    
    # Calculate means of the numerical columns
    mean_values = data[['release_speed', 'release_spin_rate', 'release_pos_z', 'release_pos_x', 'PlateLocHeight', 'PlateLocSide', 
                    'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az', 'SeamLat', 'SeamLon']].mean()
    
    # Use values from the first row for the static values
    first_row = data.iloc[0]
    mean_row = {
        'PitchTitle': first_row['PitcherFullName'] + ' ' + first_row['PitchType'],
        'PitchType': first_row['PitchType'],
        'PitcherFullName': first_row['PitcherFullName'],
        'release_speed': mean_values['release_speed'],
        'release_spin_rate': mean_values['release_spin_rate'],
        'release_pos_z': mean_values['release_pos_z'],
        'release_pos_y': 56.6,
        'release_pos_x': mean_values['release_pos_x'],
        'PlateLocHeight': mean_values['PlateLocHeight'],
        'PlateLocSide': mean_values['PlateLocSide'],
        'vx0': mean_values['vx0'],
        'vy0': mean_values['vy0'],
        'vz0': mean_values['vz0'],
        'ax': mean_values['ax'],
        'ay': mean_values['ay'],
        'az': mean_values['az'],
        'SeamLat': mean_values['SeamLat'],
        'SeamLon': mean_values['SeamLon']
    }
    
    Duffey_Tyler_2023_test = pd.DataFrame([mean_row])
    # Reordering columns to match the desired order
    Duffey_Tyler_2023_test = Duffey_Tyler_2023_test[['PitchTitle', 'PitchType', 'PitcherFullName', 'release_speed', 'release_spin_rate', 
                    'release_pos_z', 'release_pos_y', 'release_pos_x', 'PlateLocHeight', 
                    'PlateLocSide', 'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az', 'SeamLat', 'SeamLon']]
    
    # return Duffey_Tyler_2023_test
    
    Duffey_Tyler_2023_test.to_csv('Duffey_Tyler_2023_test.csv', index=False)
    
if __name__ == '__main__':
    processCSV(Duffey_Tyler_2023_FF)