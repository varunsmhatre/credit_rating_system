import ijson
from typing import Dict, List
from multiprocessing import Pool
from time import time
import os
from typing import Dict
from .utils import logging
from .mortgage import Mortgage
from .worker_manager import WorkerManager

class CreditRating:

    def __init__(
        self,
        file_path: str=None,
        mortgages: List[dict]=None,
        chunk_size: int = 2,
        rejection_threshold: float = 0.3,
        mortgage_class=None,
    ):
        self.file_path = file_path
        self.mortgages = mortgages or []
        self.num_workers = WorkerManager.get_optimal_workers()
        self.chunk_size = chunk_size
        self.rejection_threshold = rejection_threshold
        self.total_risk_score = 0
        self.credit_score_sum = 0
        self.valid_count = 0
        self.invalid_count = 0
        if mortgage_class:
            self.mortgage_class = mortgage_class
        else:
            self.mortgage_class: Mortgage = Mortgage
        if not file_path and not mortgages:
            logging.warning("No valid file path or List of Mortgages Provided!")
            logging.warning("Setting Mortgages to Empty List")
            


    def read_mortgages_in_chunks(self):
        if self.file_path:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File not found: {self.file_path}")

            with open(self.file_path, "r", encoding="utf-8") as file:
                file.seek(0)
                mortgages = []
                for mortgage in ijson.items(file, "mortgages.item"):
                    mortgages.append(mortgage)
                    if len(mortgages) >= self.chunk_size:
                        yield mortgages
                        mortgages = []
                if mortgages:
                    yield mortgages
        elif self.mortgages and isinstance(self.mortgages, list):
            for i in range(0, len(self.mortgages), self.chunk_size):
                yield self.mortgages[i:i + self.chunk_size]
        else:
            yield []

    def process_mortgage_batch(self, mortgages: List[Dict]):
        total_risk = 0
        credit_score_sum = 0
        valid_count = 0
        invalid_count = 0

        for mortgage_data in mortgages:
            try:
                MortgageClass: Mortgage = self.mortgage_class
                mortgage = MortgageClass(mortgage_data)
                risk_score, credit_score = mortgage.calculate_total_risk()
                total_risk += risk_score
                credit_score_sum += credit_score
                valid_count += 1
            except ValueError:
                invalid_count += 1

        return {
            "total_risk": total_risk,
            "credit_score_sum": credit_score_sum,
            "valid_count": valid_count,
            "invalid_count": invalid_count,
        }

    def process_mortgages_parallel(self):
        start_time = time()
        with Pool(processes=self.num_workers) as pool:
            results = pool.map(
                self.process_mortgage_batch, self.read_mortgages_in_chunks()
            )

        if not results:
            logging.warning("No Valid Mortgage Record Found!!")
            return
        
        for result in results:
            self.total_risk_score += result["total_risk"]
            self.credit_score_sum += result["credit_score_sum"]
            self.valid_count += result["valid_count"]
            self.invalid_count += result["invalid_count"]

        self.check_data_quality()

        self.compute_average_credit_score()

        logging.info(
            f"Processed {self.valid_count} valid mortgages in {time() - start_time:.2f} seconds"
        )
        logging.info(f"Flagged {self.invalid_count} invalid mortgages")

    def check_data_quality(self):
        total_records = self.valid_count + self.invalid_count
        if total_records == 0:
            logging.warning("No mortgage records available for data quality check.")
            return

        invalid_percentage = self.invalid_count / total_records
        if invalid_percentage > self.rejection_threshold:
            logging.error(
                f"High invalid data rate: {invalid_percentage:.2%}. Please Review the Input Data/File!"
            )

    def compute_average_credit_score(self):
        if self.valid_count == 0:
            return
        avg_score = self.credit_score_sum / self.valid_count
        if avg_score >= 700:
            self.total_risk_score -= 1
        elif avg_score < 650:
            self.total_risk_score += 1

    def calculate_final_rating(self):
        if self.valid_count == 0:
            return "C"
        
        if self.total_risk_score <= 2:
            return "AAA"
        elif 3 <= self.total_risk_score <= 5:
            return "BBB"
        else:
            return "C"


    def get_rating(self):
        self.process_mortgages_parallel()
        return self.calculate_final_rating()
