from setuptools import setup, find_packages

setup(name="h_tats",
      version='0.0.1',
      packages=['api/v1/endpoints','services','api','domain', 'models', 'models/engine', 'repository','domain/client',
                'domain/room', 'tests', 'tests/models', 'tests/services', 'tests/api', 'api/v1/endpoints/room', 'services/customer/adapter',
                'services/room_service','api/v1/endpoints/room', 'api.v1', 'domain/client', 'api/v1/endpoints/client','services/customer/port',
                'services/room_service/room_category_manager/adapter', 'services/room_service/room_category_manager/port',
                'services/room_service/room_category_manager', 'services/room_service/room/port', 'services/room_service/room/adapter'
                ])