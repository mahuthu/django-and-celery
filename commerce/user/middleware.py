from django.core.cache import cache

class CustomerCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/customer/10/"):
            cache_key = f"customer_10_data"
            cached_customer = cache.get(cache_key)

            if not cached_customer:
                try:
                    customer = Customer.objects.get(customer_id = 10)
                    cache.set(cache_key, customer, timeout = 300)
                except Customer.DoesNotExist:
                    pass
        response = self.get_response(request)
        return response

# initialization (__init__):
# The __init__ method initializes the middleware with the get_response parameter, which is a callable that will later be used to pass the request through the middleware stack and ultimately to the view.
# Processing Incoming Request (__call__):
# When a request comes in, the middleware's __call__ method is invoked.
# It first constructs a cache key based on the request's path. This key is used to identify the cached response related to the specific view.
# It then attempts to retrieve a cached response associated with the cache key using cache.get(cache_key).
# If a cached response is found (cached_response is not None), the middleware returns this cached response immediately, bypassing the actual view execution. This saves processing time and resources.
# If no cached response is found, the middleware proceeds to execute the rest of the request-response cycle by calling self.get_response(request), which passes the request through the middleware stack to reach the corresponding view.
# After receiving the response from the view, the middleware caches this response using cache.set(cache_key, response, timeout=300). Here, timeout=300 specifies that the response should be cached for 5 minutes (300 seconds).
# Finally, the middleware returns the response to the client.

# The middleware checks if there is a cached response for the current request using cache.get(cache_key).
# If a cached response is found (cached_response is not None), the middleware immediately returns this cached response using return cached_response.
# The code after the return cached_response line will not be executed in this case.
# If there is no cached response (cached_response is None), the middleware continues executing and calls self.get_response(request) to get the response from the view or other middleware.
# After obtaining the response, the middleware caches this response using cache.set(cache_key, response, timeout=300) and then returns the response