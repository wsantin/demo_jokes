from hashlib import md5

#crear un State 
def get_state(CONFIG_KEY_POOL_CLIENT_ID, CONFIG_KEY_POOL_ID):
    return md5("{user_pool_client_id}:{user_pool_id}".format(CONFIG_KEY_POOL_CLIENT_ID,CONFIG_KEY_POOL_ID).encode("utf-8")).hexdigest()
