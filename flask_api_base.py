from app import factory
import app

app = factory.create_app(celery=app.celery)

if __name__ == "__main__":
  app.run(host ="localhost", port=9000, threaded=True, debug=True)