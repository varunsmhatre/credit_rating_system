import multiprocessing

class WorkerManager:
    """Determines the optimal number of workers for multiprocessing"""
    @staticmethod
    def get_optimal_workers(min_workers=1, reserve_cores=1):
        total_cores = multiprocessing.cpu_count()
        available_cores = max(min_workers, total_cores - reserve_cores)
        return available_cores
