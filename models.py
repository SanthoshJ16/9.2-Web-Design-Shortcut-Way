from django.db import models

class ckdModel(models.Model):

    ApplicantIncome = models.FloatField()
    CoapplicantIncome = models.FloatField()
    LoanAmount = models.FloatField()
    Loan_Amount_Term = models.FloatField()
    Credit_History = models.CharField(max_length=100)
    Gender = models.CharField(max_length=100)
    Education = models.CharField(max_length=100)
    Married = models.CharField(max_length=100)
    Dependents = models.CharField(max_length=100)
    Property_Area = models.CharField(max_length=100)
