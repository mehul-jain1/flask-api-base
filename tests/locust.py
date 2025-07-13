from locust import HttpUser, task, between
import random

token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTQ5OTMwOTksImlhdCI6MTc1MjQwMTA5OSwidXNlckVtYWlsIjoiYWRtaW5AdGVzdDIuY29tIiwidXNlcklkIjoxLCJ1c2VyTmFtZSI6ImFkbWluIiwidXNlclJvbGUiOiJhZG1pbiJ9.RfibrDwJXQXE4Lt-jir_Z5lFqAWYlz-m4XMjzdUsrOA"

# locust --host=http://localhost:9000/ -f tests/locust.py --headless -u 100 -r 10 --run-time 15m
# simulate with 100 users: each user will make requests with 1-3 second intervals

class QuickstartUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    @task(weight=3)
    def get_users(self):
        """Test GET /api/users endpoint"""
        response = self.client.get(
            "/api/users",
            headers={"Authorization": token, "Content-Type": "application/json"}
        )
        if response.status_code != 200:
            print(f"GET /api/users failed with status: {response.status_code}")

    # @task(weight=1)
    # def create_user(self):
    #     """Test POST /api/users endpoint"""
    #     user_id = random.randint(1000, 9999)
    #     response = self.client.post(
    #         "/api/users",
    #         headers={"Authorization": token, "Content-Type": "application/json"},
    #         json={
    #             "name": f"perf-test-user-{user_id}",
    #             "email": f"perf-test-user-{user_id}@test.com",
    #             "role": "admin"
    #         }
    #     )
    #     if response.status_code not in [200, 201]:
    #         print(f"POST /api/users failed with status: {response.status_code}")

    @task(weight=2)
    def get_user_by_id(self):
        """Test GET /api/users/<id> endpoint"""
        user_id = random.randint(1, 4)  # Assuming you have users with IDs 1-4
        response = self.client.get(
            f"/api/users/{user_id}",
            headers={"Authorization": token, "Content-Type": "application/json"}
        )
        if response.status_code not in [200, 404]:  # 404 is acceptable if user doesn't exist
            print(f"GET /api/users/{user_id} failed with status: {response.status_code}")

    @task(weight=1)
    def get_token(self):
        """Test POST /token endpoint"""
        response = self.client.post(
            "/api/token",
            headers={"Content-Type": "application/json"},
            json={
                "email": "admin@test2.com"
            }
        )
        if response.status_code not in [200, 202]:
            print(f"POST /api/token failed with status: {response.status_code}")

    def on_start(self):
        """Called when a user starts - can be used for setup"""
        print("User started")
        
    def on_stop(self):
        """Called when a user stops - can be used for cleanup"""
        print("User stopped")
