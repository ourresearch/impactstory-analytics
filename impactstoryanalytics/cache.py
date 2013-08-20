import os
import pylibmc
import hashlib
import logging
import json
from cPickle import PicklingError

#from totalimpact.utils import Retry

# set up logging
logger = logging.getLogger("ti.cache")

class CacheException(Exception):
    pass

class Cache(object):
    """ Maintains a cache of URL responses in memcached """

    def __init__(self, max_cache_age=60*60):  #one hour
        self.max_cache_age = max_cache_age
        self.mc = self._get_memcached_client()
        self.enabled = True 
        if not self.mc:
            logger.info("MEMCACHIER env variables aren't set, so DISABLING CACHING")
            self.enabled = False            
        if (os.environ.get('DISABLE_CACHE', "0") == "1"):
            logger.info("found DISABLE_CACHE so disabling cache")
            self.enabled = False
        if self.enabled:
            logger.info("caching is ENABLED")

    def _get_memcached_client(self):
        try:
            mc = pylibmc.Client(
                    servers=[os.environ.get('MEMCACHIER_SERVERS')],
                    username=os.environ.get('MEMCACHIER_USERNAME'),
                    password=os.environ.get('MEMCACHIER_PASSWORD'),
                    binary=True)
        except AttributeError:
            logger.info("MEMCACHIER env variables aren't set, so no valid cache client")
            mc = None
        return mc

    def flush_cache(self):
        #empties the cache
        self.mc.flush_all()

    def _build_hash_key(self, key):
        json_key = json.dumps(key)
        hash_key = hashlib.md5(json_key.encode("utf-8")).hexdigest()
        return hash_key

    def get_cache_entry(self, key):
        """ Get an entry from the cache, returns None if not found """

        if not self.enabled:
            return None

        hash_key = self._build_hash_key(key)
        response = self.mc.get(hash_key)
        return response

    def set_cache_entry(self, key, data, max_cache_age=None):
        """ Store a cache entry """

        if not self.enabled:
            return None

        if not max_cache_age:
            max_cache_age = self.max_cache_age  # use default

        hash_key = self._build_hash_key(key)
        try:
            set_response = self.mc.set(hash_key, data, time=max_cache_age)
            if not set_response:
                raise CacheException("Unable to store into Memcached. Make sure memcached server is running.")
        except PicklingError:
            # This happens when trying to cache a thread.lock object, for example.  Just don't cache.
            logger.debug("In set_cache_entry but got PicklingError")
            set_response = None
        return (set_response)
  
        
        
