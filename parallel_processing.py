from multiprocessing.dummy import Pool as ThreadPool


def ioBoundMap(function,iterator,processes=10):
    pool = ThreadPool(processes=processes)
    results = pool.map(function, iterator)
    pool.close()
    pool.join()
    return results