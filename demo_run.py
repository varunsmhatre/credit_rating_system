from credit_rating.credit_rating import CreditRating

if __name__ == "__main__":  
    file_path = "mortgages.json"
    rating_system = CreditRating(file_path=file_path)

    # mortgages = [
    #             {
    #         "credit_score": 720,
    #         "loan_amount": 250000,
    #         "property_value": 300000,
    #         "annual_income": 85000,
    #         "debt_amount": 20000,
    #         "loan_type": "fixed",
    #         "property_type": "single_family"
    #     },
    #     {
    #         "credit_score": 680,
    #         "loan_amount": 350000,
    #         "property_value": 400000,
    #         "annual_income": 95000,
    #         "debt_amount": 35000,
    #         "loan_type": "adjustable",
    #         "property_type": "condo"
    #     },

    # ]
    # rating_system = CreditRating(mortgages=mortgages)

    try:
        final_rating = rating_system.get_rating()
        print(f"Final Credit Rating: {final_rating}")
    except ValueError as e:
        print(f"Processing Error: {e}")
