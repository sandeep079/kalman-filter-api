from pydantic import BaseModel

class IMUData(BaseModel):
    ax: float
    ay: float
    az: float
    roll: float
    pitch: float
    yaw: float

class OdomData(BaseModel):
    x: float
    y: float
    theta: float
    vx: float
    vy: float
    omega: float

class SensorInput(BaseModel):
    imu: IMUData
    odom: OdomData

class FusedPose(BaseModel):
    x: float
    y: float
    theta: float
