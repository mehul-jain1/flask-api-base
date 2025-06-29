from locust import HttpUser, task, between

token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODAxNjAwMDUsImlhdCI6MTY3NzU2ODAwNSwidXNlcklkIjoiMCIsInVzZXJOYW1lIjoiTG9jdXN0IHVzZXIiLCJ1c2VyRW1haWwiOiJsb2N1c3RfdGVzdEBzd3pkLmNvbSIsInVzZXJSb2xlIjoiYWRtaW4ifQ.OnmV73TpAjifLY7wAj2EIEdmHmSglkbKrIoXh_uewaQ"
# locust --host=http://localhost:3000/ -f tests/locust.py --headless -u 1 -r 1 --run-time 10h
# simulate with 5 users: send 5 request per user  and wait for 10-12 min and then send again 5 request
#test
class QuickstartUser(HttpUser):
  wait_time = between(600, 700)


  @task(weight=1)
  def runAPI(self):
    while True:
      for i in range(5):
        response = self.client.post(
              "/api/users", 
              headers = {"Authorization": token, "Content-Type": 'application/json'},
              json = {
                "name": "perf-test-job-from-locust-v2",
                "email": "perf-test-job-from-locust-v2@test.com",
                "role": "admin"
              }
        )
      self.wait()
