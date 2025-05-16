

# Kalman Filter API for Sensor Fusion (ABU Robocon 2025)

This project implements a FastAPI-based web service that performs sensor fusion using a Kalman Filter. It fuses **IMU** and **Odometry** data to estimate the robot’s pose (`x`, `y`, `theta`).

Designed as a backend for robotics applications such as **ABU Robocon 2025**, it supports both JSON input and batch CSV file uploads.

---

##  Features

-  Sensor Fusion using Kalman Filter
-  Supports JSON-based POST requests
-  Supports CSV batch upload and returns list of fused pose estimates
-  Built-in API docs via Swagger UI
-  Docker support for easy deployment

---

##  Installation (Local)

```bash
git clone https://github.com/sandeep079/kalman-filter-api.git
cd kalman-filter-api
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
uvicorn aifellowshipkfapi.main:app --reload

```

## Usage
1. JSON API: /estimate

    Method: POST

    URL: http://localhost:8000/estimate

   ### Request Body:
```bash

{
  "imu": {
    "ax": 0.01,
    "ay": 0.02,
    "az": 9.81,
    "roll": 0.01,
    "pitch": 0.01,
    "yaw": 0.05
  },
  "odom": {
    "x": 1.0,
    "y": 2.0,
    "theta": 0.1,
    "vx": 0.2,
    "vy": 0.3,
    "omega": 0.05
  }
}
```


   ### Response:
```bash

{
  "x": 1.05,
  "y": 2.03,
  "theta": 0.11
}
```

2. Batch CSV API: /estimate_batch_csv

    Method: POST

    URL: http://localhost:8000/estimate_batch_csv

    Form Data: Upload .csv file with required columns.

    CSV Column Headers:
```bash
ax, ay, az, roll, pitch, yaw, x, y, theta, vx, vy, omega
```

    Response:
```bash
[
  {"x": 1.0, "y": 2.0, "theta": 0.1},
  {"x": 1.1, "y": 2.2, "theta": 0.12}
]
```

 ## Docker Support

Build and run using Docker:
```bash

docker build -t kalman-filter-api .
docker run -d -p 8000:8000 kalman-filter-api
```

Then open: http://localhost:8000/docs
 ## Project Structure
```bash

kalman-filter-api/
│
├── aifellowshipkfapi/
│   ├── main.py                # FastAPI app
│   ├── kalman.py              # Kalman filter logic
│   └── modeling/              # CSV test logic
│
├── models/
│   └── schemas.py             # Pydantic models
├── requirements.txt
├── Dockerfile
└── README.md
```

 ## Author

Sandeep Yadav
Electrical Engineering @ Pulchowk Campus
GitHub: sandeep079
 ## License

MIT License - use freely for research and education purposes.