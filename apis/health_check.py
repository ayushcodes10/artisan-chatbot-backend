# Import necessary modules from FastAPI
from fastapi import APIRouter

# Create a new instance of APIRouter, which is used to define a set of routes (endpoints)
# that will be grouped together. This helps in organizing routes logically within the application.
router = APIRouter()

# Define a route for a GET request at the root ("/") of this router.
# This route is typically used for health checks to ensure that the API is up and running.
# When a request is made to this endpoint, it returns a JSON response with a "status" key set to "healthy".
@router.get("/")
def health_check():
    # The response is a dictionary with a key "status" and value "healthy".
    # This indicates that the API is functioning properly.
    return {"status": "healthy"}
