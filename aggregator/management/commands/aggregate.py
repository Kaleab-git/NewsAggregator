# # aggregator/management/commands/aggregator.py
# from django.core.management.commands.runserver import Command as RunserverCommand
# from ....aggregator import Aggregator
#
#
# class Command(RunserverCommand):
#     help = 'Run the news aggregator'
#
#     def run_aggregator(self):
#         try:
#             # aggregator = Aggregator()
#             # aggregator.run()
#             self.stdout.write(self.style.SUCCESS('Successfully ran the aggregator'))
#         except Exception as e:
#             self.stderr.write(self.style.ERROR(f'Error running aggregator: {e}'))
#
#     def handle(self, *args, **options):
#         # Call the parent runserver command
#         super().handle(*args, **options)
#
#         try:
#             self.run_aggregator()
#             self.stdout.write(self.style.SUCCESS('Aggregator Running'))
#         except Exception as e:
#             self.stderr.write(self.style.ERROR(f'Error scheduling aggregator task: {e}'))
