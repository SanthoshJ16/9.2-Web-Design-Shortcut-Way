from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import ckdForm
from . import pipeline

class dataUploadView(View):

    form_class = ckdForm
    template_name = 'create.html'
    failure_url = reverse_lazy('fail')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            # ✅ Extract data from form
            data_income = form.cleaned_data['ApplicantIncome']
            data_co_income = form.cleaned_data['CoapplicantIncome']
            data_loan_amt = form.cleaned_data['LoanAmount']
            data_loan_term = form.cleaned_data['Loan_Amount_Term']
            data_credit_history = form.cleaned_data['Credit_History']
            data_gender = form.cleaned_data['Gender']
            data_education = form.cleaned_data['Education']
            data_married = form.cleaned_data['Married']
            data_dependents = form.cleaned_data['Dependents']
            data_area = form.cleaned_data['Property_Area']

            # ✅ Prepare raw input (same as Jupyter)
            raw_data = [
                data_income,
                data_co_income,
                data_loan_amt,
                data_loan_term,
                data_credit_history,
                data_gender,
                data_education,
                data_married,
                data_dependents,
                data_area
            ]

            # ✅ Display context (original values)
            context = {
                'data_income': data_income,
                'data_co_income': data_co_income,
                'data_loan_amt': data_loan_amt,
                'data_loan_term': data_loan_term,
                'data_credit_history': data_credit_history,
                'data_gender': data_gender,
                'data_education': data_education,
                'data_married': data_married,
                'data_dependents': data_dependents,
                'data_area': data_area,
            }

            # ✅ Prediction
            prediction, probability = pipeline.get_prediction(raw_data)

            context.update({
                'prediction': prediction,
                'probability': probability
            })

            return render(request, "succ_msg.html", context)

        return redirect(self.failure_url)
