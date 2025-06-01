from typing import Awaitable, AnyStr

import redis

from ..core import TTLCacheBackend


def generate_ttl_kwargs(ttl, unit: AnyStr = 's'):
    kwargs = {}
    match unit:  # 根据不同单位设置不同的ttl值
        case 's':
            kwargs['ex'] = ttl
        case 'ms':
            kwargs['px'] = ttl
        case 'h':
            kwargs['ex'] = ttl * 3600
        case 'm':
            kwargs['ex'] = ttl * 60
        case 'd':
            kwargs['ex'] = ttl * 86400
        case _:
            raise ValueError('Invalid unit')

    return kwargs


class RedisCacheBackend(TTLCacheBackend):
    def __init__(self, host, port, db=0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)

    async def get(self, key, index=None, rindex=None, pyobject=False, string_decode=False) -> Awaitable | None:
        """
        :param pyobject: 当设置时,尝试将结果解析为 Python 对象
        :param string_decode: 当设置时,尝试将结果解析为字符串,允许设置为解码方式字符串
        :param index: 见下
        :param rindex: 索引,对不同的数据类型产生不同效果,不设置时,获取所有值
            分类:
                - string: 无效果
                - hash: 获取指定键的值
                - list: 获取指定索引的值
                - set: 测试指定元素是否存在
                - zset: 获取指定元素的"分数"
                - stream: 获取指定区间内的元素
                - others: 无效果
        :return:
        """
        if not await self.redis.exists(key):
            return None

        match await self.redis.type(key):
            case 'string':
                result = await self.redis.get(key)
            case 'hash':
                if index is not None:
                    result = await self.redis.hget(key, index)
                else:
                    result = await self.redis.hgetall(key)
            case 'list':
                if index is not None:
                    result = await self.redis.lindex(key, index)
                else:
                    result = await self.redis.lrange(key, 0, -1)
            case 'set':
                if index is not None:
                    result = await self.redis.sismember(key, index)
                else:
                    result = await self.redis.smembers(key)
            case 'zset':
                if index is not None:
                    result = await self.redis.zscore(key, index)
                else:
                    result = await self.redis.zrange(key, 0, -1)
            case "stream":
                index = index or '-'
                rindex = rindex or '+'

                result = await self.redis.xrange(key, index, rindex)
            case _:
                return None

        if string_decode:
            if isinstance(string_decode, str):
                result = result.decode(string_decode)
            else:
                result = result.decode()

        return result

    async def set(self, key, value, ttl=None, unit='s'):
        kwargs = {}
        if ttl is not None:  # 如果ttl不为None，则根据ttl和单位设置缓存过期时间
            kwargs = generate_ttl_kwargs(ttl, unit)
        # else:
        #     不设置过期时间即永久保存

        await self.redis.set(key, value, **kwargs)

    async def add(self, key, value):
        match await self.redis.type(key):
            case 'hash':
                return await self.redis.hset(key, value)
            case 'list':
                return await self.redis.rpush(key, value)
            case 'set':
                return await self.redis.sadd(key, value)
            case 'zset':
                return await self.redis.zadd(key, value)
            case _:
                return None

    async def delete(self, key):
        return await self.redis.delete(key)

    async def clear(self):
        await self.redis.flushdb()

    async def ttl(self, key, ttl=None, unit='s'):
        if ttl is None:
            return await self.redis.ttl(key)
        return await self.redis.expire(key, **generate_ttl_kwargs(ttl, unit))
