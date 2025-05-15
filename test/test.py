from fastapi.testclient import TestClient
from aifellowshipkfapi.main import app
from aifellowshipkfapi.models import IMUData, OdomData, SensorInput

# Initialize the test client for FastAPI
client = TestClient(app)

def test_estimate_pose():
    # Prepare valid sensor data
    imu_data = IMUData(
        ax=0.1, ay=0.0, az=9.8,  # Example accelerometer data (m/s^2)
        roll=0.02, pitch=0.01, yaw=1.57  # Example IMU orientation data (radians)
    )
    
    odom_data = OdomData(
        x=0.5, y=0.5, theta=1.5,  # Example position and orientation
        vx=0.2, vy=0.0, omega=0.01  # Example velocity data (m/s, rad/s)
    )
    
    # Create a complete sensor input for the API
    sensor_input = SensorInput(imu=imu_data, odom=odom_data)

    # Send a POST request to the /estimate endpoint
    response = client.post("/estimate", json=sensor_input.dict())
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Parse the response JSON
    response_data = response.json()
    
    # Assert that the response contains the expected keys and values
    assert "x" in response_data
    assert "y" in response_data
    assert "theta" in response_data
    
    # Optionally, verify the fused values fall within a reasonable range
    assert 0.48 <= response_data["x"] <= 0.52  # Check if x is reasonable
    assert 0.48 <= response_data["y"] <= 0.52  # Check if y is reasonable
    assert 1.48 <= response_data["theta"] <= 1.52  # Check if theta is reasonable

def test_health_check():
    # Send a GET request to the root (health check) endpoint
    response = client.get("/")
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response contains the expected message
    assert response.json() == {"message": "Sensor Fusion API is up and running 🚀"}
