import numpy as np
from models import SensorInput, FusedPose

# ----- Kalman Filter Logic -----
def kalman_filter(sensor_data: SensorInput) -> FusedPose:
    # Extract IMU data
    ax = sensor_data.imu.ax
    ay = sensor_data.imu.ay
    az = sensor_data.imu.az
    roll = sensor_data.imu.roll
    pitch = sensor_data.imu.pitch
    yaw = sensor_data.imu.yaw

    # Extract Odometry data
    x = sensor_data.odom.x
    y = sensor_data.odom.y
    theta = sensor_data.odom.theta
    vx = sensor_data.odom.vx
    vy = sensor_data.odom.vy
    omega = sensor_data.odom.omega

    # Initialize Kalman filter variables
    dt = 0.1  # Time step (could be adjusted based on actual sensor rate)

    # State vector [x, y, theta, vx, vy, omega]
    state = np.array([x, y, theta, vx, vy, omega], dtype=float)

    # State transition matrix (for position and velocity)
    F = np.array([
        [1, 0, 0, dt, 0, 0],
        [0, 1, 0, 0, dt, 0],
        [0, 0, 1, 0, 0, dt],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1]
    ])

    # Process noise covariance matrix
    Q = np.eye(6) * 0.1  # Adjust based on system dynamics

    # Measurement matrix (for sensor measurements)
    H = np.array([
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0]
    ])

    # Measurement noise covariance (sensor noise)
    R = np.eye(3) * 0.2  # Adjust based on sensor noise

    # Initial estimate covariance
    P = np.eye(6) * 1.0

    # Simulate a simple measurement vector [position x, y, theta]
    z = np.array([x, y, theta], dtype=float)

    # Prediction step
    state_pred = F.dot(state)  # Predicted state
    P_pred = F.dot(P).dot(F.T) + Q  # Predicted covariance

    # Measurement update (Correction step)
    y = z - H.dot(state_pred)  # Measurement residual
    S = H.dot(P_pred).dot(H.T) + R  # Residual covariance
    K = P_pred.dot(H.T).dot(np.linalg.inv(S))  # Kalman gain

    # Updated state estimate
    state_upd = state_pred + K.dot(y)

    # Updated state covariance
    P_upd = (np.eye(6) - K.dot(H)).dot(P_pred)

    # Extract the fused position and orientation
    fused_x = state_upd[0]
    fused_y = state_upd[1]
    fused_theta = state_upd[2]

    # Return the fused pose
    return FusedPose(x=fused_x, y=fused_y, theta=fused_theta)
