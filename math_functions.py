import numpy as np

def calculate_angle(A, B, C):
    # Convert points to NumPy arrays
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    
    # Vectors BA and BC
    BA = A - B
    BC = C - B
    
    # Dot product of BA and BC
    dot_product = np.dot(BA, BC)
    
    # Magnitudes of BA and BC
    mag_BA = np.linalg.norm(BA)
    mag_BC = np.linalg.norm(BC)
    
    # Cosine of the angle
    cos_theta = dot_product / (mag_BA * mag_BC)
    
    # Clamp cos_theta to avoid numerical errors leading to values outside the range of [-1, 1]
    cos_theta = np.clip(cos_theta, -1, 1)
    
    # Angle in radians
    angle_radians = np.arccos(cos_theta)
    
    # Convert angle to degrees
    angle_degrees = np.degrees(angle_radians)
    
    return angle_degrees
