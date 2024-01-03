from setuptools import setup, find_packages

setup(name="h_tats",
      version='0.0.1',
      packages=['api/v1/endpoints','services','api','domain', 'models', 'models/engine', 'repository','domain/client','api/v1/endpoints/occupation',
                'domain/room', 'tests', 'tests/models', 'tests/services', 'tests/api', 'api/v1/endpoints/room', 'services/customer/adapter', 'services/occupation', 'domain/settlement',
                'services/room_service','api/v1/endpoints/room', 'api.v1', 'domain/client', 'api/v1/endpoints/client','services/customer/port','domain/occupation', 'api/v1/endpoints/settlements',
                'services/room_service/room_category_manager/adapter', 'services/room_service/room_category_manager/port', 'api/v1/endpoints/user', 'worker_task', 'worker_task/consumer',
                'services/room_service/room_category_manager', 'services/room_service/room/port', 'services/room_service/room/adapter', 'services/user','domain/users', 'worker_task/producer', 'services/settlement',
                ])