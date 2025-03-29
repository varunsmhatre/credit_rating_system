from typing import Dict
import logging


class MortgageConfig:    
    # Validation configurations
    VALIDATION_RULES = {
        "credit_score": {"min": 300, "max": 850, "type": int},
        "loan_amount": {"min": 0, "type": (int, float)},
        "property_value": {"min": 0, "type": (int, float)},
        "annual_income": {"min": 0, "type": (int, float)},
        "debt_amount": {"min": 0, "type": (int, float)},
        "loan_type": {"options": ["fixed", "adjustable"], "type": str},
        "property_type": {"options": ["single_family", "condo"], "type": str}
    }
    
    REQUIRED_FIELDS = ["credit_score", "loan_amount", "property_value", 
                      "annual_income", "debt_amount"]
    
    # Risk calculation configurations
    RISK_PARAMS = {
        "ltv_thresholds": [0.8, 0.9],
        "dti_thresholds": [0.4, 0.5],
        "credit_score_thresholds": [650, 700],
        
        # Risk scores for loan types
        "loan_type_risk_scores": {
            "fixed": -1,
            "adjustable": 1,
        },
        
        # Risk scores for property types
        "property_type_risk_scores": {
            "single_family": 0,
            "condo": 1,
        }
    }


class Mortgage:

    def __init__(self, data: Dict):
        self.config = MortgageConfig()
        if not self.validate(data):
            raise ValueError("Invalid Mortgage Data")

        self.credit_score = data["credit_score"]
        self.loan_amount = data["loan_amount"]
        self.property_value = data["property_value"]
        self.annual_income = data["annual_income"]
        self.debt_amount = data["debt_amount"]
        self.loan_type = data.get("loan_type", "fixed")
        self.property_type = data.get("property_type", "single_family")

    def validate(self, data: Dict) -> bool:
        for field in self.config.REQUIRED_FIELDS:
            if field not in data:
                logging.warning(f"Missing field: {field} in {data}")
                return False
        
        for field, value in data.items():
            if field not in self.config.VALIDATION_RULES:
                continue
                
            rules = self.config.VALIDATION_RULES[field]
            
            # check the type
            if not isinstance(value, rules["type"]):
                logging.warning(f"Invalid type for {field}: {value}")
                return False
                
            # Min/Max check
            if "min" in rules and value < rules["min"]:
                logging.warning(f"value is low for {field}: {value}")
                return False
                
            if "max" in rules and value > rules["max"]:
                logging.warning(f"value is high for {field}: {value}")
                return False
                
            # check Categorical fields
            if "options" in rules and value not in rules["options"]:
                logging.warning(f"invalid option given for {field}: {value}")
                return False
                
        return True

    def calculate_ltv_risk(self):
        ltv = self.loan_amount / self.property_value
        thresholds = self.config.RISK_PARAMS["ltv_thresholds"]
        
        if ltv > thresholds[1]:
            return 2
        elif ltv > thresholds[0]:
            return 1
        return 0

    def calculate_dti_risk(self):
        dti = self.debt_amount / self.annual_income
        thresholds = self.config.RISK_PARAMS["dti_thresholds"]
        
        if dti > thresholds[1]:
            return 2
        elif dti > thresholds[0]:
            return 1
        return 0

    def calculate_credit_score_risk(self):
        low, high = self.config.RISK_PARAMS["credit_score_thresholds"]
        
        if self.credit_score >= high:
            return -1
        elif self.credit_score < low:
            return 1
        return 0

    def calculate_loan_type_risk(self):
        risk_scores = self.config.RISK_PARAMS["loan_type_risk_scores"]        
        return risk_scores.get(self.loan_type, 0)

    def calculate_property_type_risk(self):
        risk_scores = self.config.RISK_PARAMS["property_type_risk_scores"]        
        return risk_scores.get(self.property_type, 0)

    def calculate_total_risk(self):
        risk_score = (
            self.calculate_ltv_risk()
            + self.calculate_dti_risk()
            + self.calculate_credit_score_risk()
            + self.calculate_loan_type_risk()
            + self.calculate_property_type_risk()
        )
        return risk_score, self.credit_score

    # def calculate_total_risk(self):
    #     ltv_risk = self.calculate_ltv_risk()
    #     dti_risk = self.calculate_dti_risk()
    #     credit_score_risk = self.calculate_credit_score_risk()
    #     loan_type_risk = self.calculate_loan_type_risk()
    #     property_type_risk = self.calculate_property_type_risk()

    #     total_risk = ltv_risk + dti_risk + credit_score_risk + loan_type_risk + property_type_risk

    #     logging.info(f"Mortgage Details: Credit Score: {self.credit_score}, Loan Amount: {self.loan_amount}, Property Value: {self.property_value}, Annual Income: {self.annual_income}, Debt Amount: {self.debt_amount}, Loan Type: {self.loan_type}, Property Type: {self.property_type}")
    #     logging.info(f"LTV Risk: {ltv_risk}")
    #     logging.info(f"DTI Risk: {dti_risk}")
    #     logging.info(f"Credit Score Risk: {credit_score_risk}")
    #     logging.info(f"Loan Type Risk: {loan_type_risk}")
    #     logging.info(f"Property Type Risk: {property_type_risk}")
    #     logging.info(f"Total Risk Score: {total_risk}")
    #     logging.info("-------------------------------------------------")

    #     return total_risk, self.credit_score
