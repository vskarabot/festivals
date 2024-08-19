import pusher, os

pusher_client = pusher.Pusher(
  app_id=os.environ.get('APP_ID'),
  key=os.environ.get('KEY'),
  secret=os.environ.get('SECRET'),
  cluster='eu',
  ssl=False
)