# from celery.schedules import crontab
#
# app.conf.beat_schedule = {
#     'batch-update-post-ratings-every-minute': {
#         'task': 'yourapp.tasks.batch_update_post_ratings',
#         'schedule': crontab(minute='*/1'),  # Run every minute
#     },
# }

# app.conf.beat_schedule = {
#     'update-stale-posts-every-day-at-midnight': {
#         'task': 'your_app_name.tasks.update_stale_posts',
#         'schedule': crontab(hour=0, minute=0),
#     },
# }
