"""
Run the Human Design API server.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("human_design.api:app", host="0.0.0.0", port=8000, reload=True)
    print("Human Design API running at http://localhost:8000")
    print("API documentation available at http://localhost:8000/docs")
