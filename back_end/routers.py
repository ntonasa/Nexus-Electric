from rest_framework.routers import Route, DynamicRoute, SimpleRouter

class ApiRouter(SimpleRouter):
	routes = [
		Route(
			url=r'^{prefix}/(?P<area_name>.*)/(?P<resolution>.*)/date/(?P<date>.*)$',
			mapping = {'get' : 'date'},
			name='{basename}-date',
			detail=False,
			initkwargs={}
		),
		
		Route(
			url=r'^{prefix}/(?P<area_name>.*)/(?P<resolution>.*)/month/(?P<date>.*)$',
			mapping = {'get' : 'month'},
			name='{basename}-month',
			detail=False,
			initkwargs={}
		),
		
		Route(
			url=r'^{prefix}/(?P<area_name>.*)/(?P<resolution>.*)/year/(?P<date>.*)$',
			mapping = {'get' : 'year'},
			name='{basename}-year',
			detail=False,
			initkwargs={}
		)
	]

	def get_default_basename(self, viewset):
		return viewset.__name__

class ApiRouterExtended(SimpleRouter):
	routes = [
		Route(
			url=r'^{prefix}/(?P<area_name>.*)/(?P<production_type>.*)/(?P<resolution>.*)/date/(?P<date>.*)$',
			mapping = {'get' : 'date'},
			name='{basename}-date',
			detail=False,
			initkwargs={}
		),
		
		Route(
			url=r'^{prefix}/(?P<area_name>.*)/(?P<production_type>.*)/(?P<resolution>.*)/month/(?P<date>.*)$',
			mapping = {'get' : 'month'},
			name='{basename}-month',
			detail=False,
			initkwargs={}
		),
		
		Route(
			url=r'^{prefix}/(?P<area_name>.*)/(?P<production_type>.*)/(?P<resolution>.*)/year/(?P<date>.*)$',
			mapping = {'get' : 'year'},
			name='{basename}-year',
			detail=False,
			initkwargs={}
		)
	]

	def get_default_basename(self, viewset):
		return viewset.__name__

class AdminRouter(SimpleRouter):
	routes = [
		Route(
			url=r'^{prefix}/users$',
			mapping={'post' : 'create'},
			name='{basename}-list',
			detail=False,
			initkwargs={'suffix': 'List'}
		),
		
		Route(
			url=r'^{prefix}/users/(?P<username>.*)$',
			mapping={'get' : 'retrieve', 'put' : 'update'},
			name='{basename}-detail',
			detail=False,
			initkwargs={'suffix': 'List'}
		),
		
		DynamicRoute(
			url=r'^{prefix}/{url_path}{trailing_slash}?$',
			name='{basename}-{url_name}',
			detail=False,
			initkwargs={}
		)
	]

	def get_default_basename(self, viewset):
		return viewset.__name__
