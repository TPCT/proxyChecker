from sys import argv
from os import path
from concurrent.futures import ThreadPoolExecutor, as_completed
import proxyCheckerModule

pool = []

if len(argv) == 6:
    executor = ThreadPoolExecutor(max_workers=int(argv[4]))
    timeout = argv[5]
    if path.isfile(argv[2]):
        with open(argv[2], 'r') as reader:
            for proxy in reader.readlines()[:-1]:
                proxy = proxy.strip()
                thread = executor.submit(proxyCheckerModule.isValid, proxy, argv[1], int(timeout))
                pool.append(thread)

        with open(argv[3], 'a+') as writer:
            for future in as_completed(pool):
                result = future.result()
                print(result)
                if result[0]:
                    writer.write("%s\n" % str(result))

