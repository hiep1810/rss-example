# Celery Configuration File

# Broker settings
broker_url = 'redis://localhost:6379/0'

# Result backend settings
result_backend = 'redis://localhost:6379/0'

# Task serialization
task_serializer = 'json'

# Result serialization
result_serializer = 'json'
accept_content = ['json']

# Other settings
task_ignore_result = False
result_expires = 86400