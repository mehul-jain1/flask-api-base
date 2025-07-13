from app import celery


@celery.task(acks_late=True)
def example_task(content):
    print(f"printing inside worker {content}")
