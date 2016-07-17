# from celery.task import periodic_task
# from datetime import timedelta
# from celery.schedules import crontab
from djcelery import celery

# @periodic_task(run_every=crontab(minute=0, hour='05')) #runs at 5 am everyday
# @periodic_task(run_every=timedelta(seconds = 10)) #runs every 20 seconds from start of the task
# @periodic_task(run_every=crontab(minute=0, hour='*/1')) #runs every hour which can be divided by 1
# @periodic_task(run_every=crontab(minute='*/1')) #runs every minute which can be divided by 1
# @periodic_task #runs when the task is called by this code hourly_task.delay(some_variable_can_be_here)
@celery.task
def hourly_task():
    print "task was launched"
    #some other code