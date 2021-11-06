import time
from django.core.cache import cache as default_cache

class NexusUserThrottle():
    cache = default_cache
    timer = time.time
    cache_format = 'throttle_user_%(ident)s'

    def allow_request(self, request, view):
        if request.user.is_authenticated:
            self.key = request.user.pk
        else:
            return False
        
        if request.user.is_staff:
            return True

        num_requests = request.user.nexususer.quota
        self.duration = 86400

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= num_requests:
            return False
        return self.throttle_success()

    def throttle_success(self):
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)
        return True

    def wait(self):
        return None