# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.core.validators import FileExtensionValidator

from djtools.fields import BINARY_CHOICES

SICKLE_CELL_RESULTS = (
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
)
DRUG_TEST_RESULTS = (
    ('No positive drug test', 'No positive drug test'),
    ('Positive drug test', 'Positive drug test'),
)
ALLOWED_IMAGE_EXTENSIONS = settings.ALLOWED_IMAGE_EXTENSIONS


class SicklecellForm(forms.Form):
    waive = forms.BooleanField(
        required=False
    )
    proof = forms.BooleanField(
        required=False
    )
    results = forms.ChoiceField(
        choices=SICKLE_CELL_RESULTS,
        widget=forms.RadioSelect(),
        required=False
    )
    results_file = forms.FileField(
        label="Results File",
        help_text="Photo/Scan of your test results",
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
        ],
        required=False
    )

    def clean(self):
        """
        Student must choose one or the other of two checkboxes,
        and the results if they choose "proof".
        """
        cleaned_data = self.cleaned_data

        if not cleaned_data["waive"] and not cleaned_data["proof"]:
            raise forms.ValidationError(
                "Please check one of the checkboxes below."
            )
        elif cleaned_data["proof"] and not cleaned_data["results"]:
            raise forms.ValidationError(
                '''
                Please indicate whether your test results were
                "positive or "negative".
                '''
            )

        return cleaned_data


class DopingForm(forms.Form):
    part1 = forms.BooleanField(
        label="Statement Concerning Eligibility"
    )
    part2 = forms.BooleanField(
        label="Buckley Amendment Consent"
    )
    part3_1 = forms.BooleanField(
        label="Future positive test – all student-athletes sign"
    )
    part3_2 = forms.ChoiceField(
        label="Positive test by NCAA or other sports governing body",
        choices=DRUG_TEST_RESULTS, widget=forms.RadioSelect()
    )
    part3_3 = forms.ChoiceField(
        label="Are you currently under such a drug-testing suspension?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )


class PrivacyForm(forms.Form):
    news_media = forms.BooleanField(required=False)
    parents_guardians = forms.BooleanField(required=False)
    disclose_records = forms.BooleanField()


class ReportingForm(forms.Form):
    agree = forms.BooleanField(
        required=True
    )


class RiskForm(forms.Form):
    agree = forms.BooleanField(
        required=True
    )


class MeniForm(forms.Form):
    agree = forms.BooleanField(
        required=True
    )
