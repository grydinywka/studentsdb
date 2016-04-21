import logging

class DatabaseHandler(logging.Handler):
    def __init__(self):
        # run the regular Handler __init__
        logging.Handler.__init__(self)

    def emit(self, record):
        
        try:
            from students.models import LogEntry
            import datetime

            time = record.asctime[:-4] + '.' + record.asctime[-3:]
            time2 = datetime.datetime.strptime(record.asctime, '%Y-%m-%d %H:%M:%S,%f')

            logentry = LogEntry(level=record.levelname,
                                asctime=time2,
                                module=record.module,
                                message=record.message)
            logentry.save()
        except Exception as e:
            print e
