from fastapi.testclient import TestClient
from sqlmodel import Session
import pytest
from unittest.mock import patch

from app.main import app
from app.database import test_create_db_and_tables, test_engine, get_session

# #### ==================== fixture ==================== #####

# # https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/?h=test

# ## Fixtures

@pytest.fixture(name="session")
def session_fixture():
    test_create_db_and_tables()
    with Session(test_engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):   
    def get_session_override():
        return session  
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# #### ========================== *** ========================== #####    
    
# # Test Root Endpoint 
    
def test_read_main():
    #create TestClind for the fastapi app
    clinet = TestClient(app=app)
    response = clinet.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "This is just an authentication service. Please visit http://localhost:8000/docs to see the API documentation."}

#### ========================== *** ========================== ##### 

## Test login

def test_user_login(client: TestClient, session: Session):
    # Mock user data for registration and verification
    login_data = {
        "username": "raheelam98@gmail.com",
        "password": "raheela"
    }

    response = client.post("/api/v1/user/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

#### ========================== *** ========================== #####  
        
## Test profile
    
def test_user_login_and_get_profile(client: TestClient):
    # User login
    login_data = {
        "username": "raheelam98@gmail.com",  # FastAPI uses `username` for OAuth2PasswordRequestForm
        "password": "raheela"
    }
    
    # Log in the user to get the token
    login_response = client.post("/api/v1/user/login", data=login_data)
    assert login_response.status_code == 200
    login_data = login_response.json()
    access_token = login_data["access_token"]

    # Use the token to access the profile
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    profile_response = client.get("/api/v1/user/profile", headers=headers)
    assert profile_response.status_code == 200
    data = profile_response.json()
    assert "email" in data
    assert "full_name" in data    

#### ========================== *** ========================== #####

## Update Profile

def test_update_profile(client: TestClient):
    # First, log in to get the authentication token
    login_data = {
        "username": "raheelam98@gmail.com",  # FastAPI expects 'username' field for OAuth2PasswordRequestForm
        "password": "raheela"
    }
    
    # Log in and get the access token
    login_response = client.post("/api/v1/user/login", data=login_data)
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]
    
    # Now, update the profile with the authentication token
    profile_data = {
        "full_name": "Raheela M",
        "affiliation": "Panaversity"
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Send the profile update request with the access token
    response = client.patch("/api/v1/user/profile", json=profile_data, headers=headers)
    assert response.status_code == 200
    
    # Adjusting the test to match the actual response message
    assert response.json() == {"message": "Profile updated successfully."}

#### ========================== *** ========================== ##### 

# def test_user_registration(client: TestClient):
#     new_user_data = {
#         "full_name": "",
#         "email": "raheelam98@gmail.com",   
#         "phone": "923323067013",
#         "affiliation": "Piaic",
#         "password": "raheela",
#         "user_type": "admin"
#     }

#     # Mock both email and WhatsApp sending functions to prevent actual API calls
#     with patch('app.services.email_message.send_user_signup_email') as mock_send_email, \
#          patch('app.services.whatsapp_message.create_and_send_magic_link') as mock_send_whatsapp:
        
#         # Set return values for the mocked functions
#         mock_send_email.return_value = None
#         mock_send_whatsapp.return_value = None

#         # Execute the registration API call
#         response = client.post("/api/v1/user/register", json=new_user_data)
        
#         # Assert the response is successful
#         assert response.status_code == 200

#         # Verify the returned data
#         data = response.json()
#         assert data["email"] == new_user_data["email"]
#         assert data["full_name"] == new_user_data["full_name"]
#         assert data["is_verified"] is False


#### ========================== *** ========================== #####  
#### ========================== *** ========================== #####
#### ========================== *** ========================== #####       


# # https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#override-a-dependency

# # https://fastapi.tiangolo.com/tutorial/testing/
# # https://realpython.com/python-assert-statement/
# # https://understandingdata.com/posts/list-of-python-assert-statements-for-unit-tests/


    