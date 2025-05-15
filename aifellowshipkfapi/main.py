from fastapi import FastAPI
from pydantic import BaseModel
from kalman import kalman_filter
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import io


app = FastAPI(
    title="Sensor Fusion API for ABU Robocon 2025",
    description="Fuses IMU and Odometry data using Kalman Filter and returns estimated robot pose.",
    version="1.0"
)

# ----- Request Models -----

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

# ----- Response Model -----

class FusedPose(BaseModel):
    x: float
    y: float
    theta: float

@app.post("/estimate_batch_csv")
async def estimate_from_csv(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        required_cols = {
            'ax', 'ay', 'az',
            'roll', 'pitch', 'yaw',
            'x', 'y', 'theta',
            'vx', 'vy', 'omega'
        }

        if not required_cols.issubset(df.columns):
            return JSONResponse(status_code=400, content={
                "error": f"CSV must contain columns: {', '.join(required_cols)}"
            })

        results = []

        for _, row in df.iterrows():
            imu_data = IMUData(
                ax=row['ax'], ay=row['ay'], az=row['az'],
                roll=row['roll'], pitch=row['pitch'], yaw=row['yaw']
            )
            odom_data = OdomData(
                x=row['x'], y=row['y'], theta=row['theta'],
                vx=row['vx'], vy=row['vy'], omega=row['omega']
            )
            sensor_input = SensorInput(imu=imu_data, odom=odom_data)
            fused = kalman_filter(sensor_input)

            results.append({
                "x": fused.x,
                "y": fused.y,
                "theta": fused.theta
            })

        return {"filtered_results": results}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ----- API Endpoint -----

@app.post("/estimate", response_model=FusedPose)
def estimate_pose(sensor_data: SensorInput):
    fused_pose = kalman_filter(sensor_data)
    return fused_pose


# ----- Health Check -----

@app.get("/")
def root():
    return {"message": "Sensor Fusion API is up and running "}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

