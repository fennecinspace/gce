from django.apps import AppConfig
from gce_app.functions import scheduled_operation

class GceAppConfig(AppConfig):
    name = 'gce_app'
    verbose_name = "scheduled_operations"
    def ready(self):
        import schedule
        import time
        from threading import Thread
        from urllib.request import urlopen

        # def job():
        #     with urlopen('http://localhost:8000/scheduled_operation') as response:
        #         print(response.read(), response.code)
            

        def scheduler():
            schedule.every(5).hours.do(scheduled_operation)

            while True:
                schedule.run_pending()
                time.sleep(1)


        t = Thread(target= scheduler)
        t.daemon = True
        t.start() ## not using t.join() because it will block server
