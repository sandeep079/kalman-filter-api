from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import pandas as pd
import io

from aifellowshipkfapi.kalman import kalman_filter
from models.schemas import SensorInput, FusedPose  

class FilteredResult(BaseModel):
    x: float
    y: float
    theta: float

app = FastAPI(
    title="Sensor Fusion API for ABU Robocon 2025",
    description="Fuses IMU and Odometry data using Kalman Filter and returns estimated robot pose.",
    version="1.0"
)

@app.post("/estimate", response_model=FusedPose)
def estimate_pose(sensor_data: SensorInput):
    fused_pose = kalman_filter(sensor_data)
    return fused_pose

@app.post("/estimate_batch_csv", response_model=List[FilteredResult])
async def estimate_from_csv(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        required_cols = {
            'ax', 'ay', 'az', 'roll', 'pitch', 'yaw',
            'x', 'y', 'theta', 'vx', 'vy', 'omega'
        }

        if not required_cols.issubset(df.columns):
            return JSONResponse(status_code=400, content={
                "error": f"CSV must contain columns: {', '.join(required_cols)}"
            })

        results = []
        for _, row in df.iterrows():
            imu_data = sensor_data.imu.__class__(**row.to_dict())
            odom_data = sensor_data.odom.__class__(**row.to_dict())
            sensor_input = SensorInput(imu=imu_data, odom=odom_data)
            fused = kalman_filter(sensor_input)

            results.append({
                "x": fused.x,
                "y": fused.y,
                "theta": fused.theta
            })

        return results
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def root():
    return {"message": "Sensor Fusion API is up and running 🚀"}
