import unittest
from credit_rating.credit_rating import CreditRating
import random
import time

class TestCreditRating(unittest.TestCase):
    def setUp(self):
        self.mortgages = [
            {
                "credit_score": 720,
                "loan_amount": 250000,
                "property_value": 300000,
                "annual_income": 85000,
                "debt_amount": 20000,
                "loan_type": "fixed",
                "property_type": "single_family"
            },
            {
                "credit_score": 680,
                "loan_amount": 350000,
                "property_value": 400000,
                "annual_income": 95000,
                "debt_amount": 35000,
                "loan_type": "adjustable",
                "property_type": "condo"
            },
        ]
        self.rating_system = CreditRating(mortgages=self.mortgages)

    def test_valid_credit_rating(self):
        final_rating = self.rating_system.get_rating()
        expected_rating = "AAA"
        self.assertEqual(final_rating, expected_rating, f"Expected Credit Rating is {expected_rating} while calculated was {final_rating}")

    def test_empty_mortgages(self):
        rating_system = CreditRating(mortgages=[])
        final_rating = rating_system.get_rating()
        expected_rating = "C"
        self.assertEqual(final_rating, expected_rating, f"Expected Credit Rating is {expected_rating} while calculated was {final_rating}")

    def test_high_risk_mortgages(self):
        high_risk_mortgages = [
            {
                "credit_score": 500,
                "loan_amount": 400000,
                "property_value": 410000,
                "annual_income": 30000,
                "debt_amount": 25000,
                "loan_type": "adjustable",
                "property_type": "condo"
            }
        ]
        rating_system = CreditRating(mortgages=high_risk_mortgages)
        final_rating = rating_system.get_rating()
        expected_rating = "C"
        self.assertEqual(final_rating, expected_rating, f"Expected Credit Rating is {expected_rating} while calculated was {final_rating}")

    def test_low_risk_mortgages(self):
        low_risk_mortgages = [
            {
                "credit_score": 800,
                "loan_amount": 100000,
                "property_value": 500000,
                "annual_income": 120000,
                "debt_amount": 5000,
                "loan_type": "fixed",
                "property_type": "single_family"
            }
        ]
        rating_system = CreditRating(mortgages=low_risk_mortgages)
        final_rating = rating_system.get_rating()
        expected_rating = "AAA"
        self.assertEqual(final_rating, expected_rating, f"Expected Credit Rating is {expected_rating} while calculated was {final_rating}")

    def test_medium_risk_mortgages(self):
        medium_risk_mortgages = [
            {
                "credit_score": 670,
                "loan_amount": 250000,
                "property_value": 280000,
                "annual_income": 75000,
                "debt_amount": 30000,
                "loan_type": "adjustable",
                "property_type": "condo"
            }
        ]
        rating_system = CreditRating(mortgages=medium_risk_mortgages)
        final_rating = rating_system.get_rating()
        expected_rating = "BBB"
        self.assertEqual(final_rating, expected_rating, f"Expected Credit Rating is {expected_rating} while calculated was {final_rating}")

    
    def test_stress_large_data(self):
        print("Running stress test with 100,000 mortgage records...")
        large_mortgage_list = [
            {
                "credit_score": random.randint(500, 850), "loan_amount": random.randint(100000, 500000),
                "property_value": random.randint(150000, 600000), "annual_income": random.randint(40000, 150000),
                "debt_amount": random.randint(10000, 50000), "loan_type": random.choice(["fixed", "adjustable"]),
                "property_type": random.choice(["single_family", "condo"])
             }
            for _ in range(100000)
        ]
        credit_rating_large = CreditRating(mortgages=large_mortgage_list)
        start_time = time.time()
        credit_rating_large.process_mortgages_parallel()
        execution_time = time.time() - start_time
        
        self.assertEqual(credit_rating_large.valid_count, 100000)
        self.assertEqual(credit_rating_large.invalid_count, 0)
        self.assertLess(execution_time, 10, "Stress test took too long!")


if __name__ == "__main__":
    unittest.main()
