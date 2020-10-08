import asyncio


async def diss(lis):
  x = []
  for i in lis:
    x.append(i + 1)
  return x


async def main():
  lis = [1, 2, 3, 4]
  res = await diss(lis)
  return res


loop = asyncio.get_event_loop()
res = loop.run_until_complete(main())
print(res)

