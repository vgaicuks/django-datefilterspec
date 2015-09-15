from mock import Mock
from unittest import TestCase
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import ugettext as _
from daterange_filter.filter import DateRangeFilterBaseForm, DateRangeForm, DateTimeRangeForm, \
    DateRangeFilterAdminSplitDateTime


class DateRangeFilterBaseFormTest(TestCase):

    class DummyForm(DateRangeFilterBaseForm):
        pass

    def setUp(self):
        self.request = Mock()

    def test_form_returns_all_media(self):
        del self.request.daterange_filter_media_included
        form = self.DummyForm(self.request)

        self.assertEquals(str(form.media), str(forms.Media(
            js=['admin/js/calendar.js', 'admin/js/admin/DateTimeShortcuts.js'],
            css={'all': ['admin/css/widgets.css']}
        )))

    def test_form_returns_empty_media_if_another_form_has_already_been_instantiated(self):
        del self.request.daterange_filter_media_included

        form_1 = self.DummyForm(self.request)
        form_2 = self.DummyForm(self.request)

        self.assertNotEqual(str(form_1.media), '')
        self.assertEquals(str(form_2.media), '')


class DateRangeFormTest(TestCase):

    class DummyForm(DateRangeForm):
        pass

    def test_create_fields(self):
        form = self.DummyForm(Mock(), field_name='spam')

        self.assertIsInstance(form.fields['spam__gte'], forms.DateField)
        self.assertIsInstance(form.fields['spam__lte'], forms.DateField)

    def test_field_attributes(self):
        form = self.DummyForm(Mock(), field_name='ham')

        self.assertEquals(form.fields['ham__gte'].label, '')
        self.assertEquals(form.fields['ham__gte'].localize, True)
        self.assertEquals(form.fields['ham__gte'].required, False)
        self.assertIsInstance(form.fields['ham__gte'].widget, AdminDateWidget)
        self.assertDictContainsSubset({'placeholder': _('From date')},
                                      form.fields['ham__gte'].widget.attrs)

        self.assertEquals(form.fields['ham__lte'].label, '')
        self.assertEquals(form.fields['ham__lte'].localize, True)
        self.assertEquals(form.fields['ham__lte'].required, False)
        self.assertIsInstance(form.fields['ham__lte'].widget, AdminDateWidget)
        self.assertDictContainsSubset({'placeholder': _('To date')},
                                      form.fields['ham__lte'].widget.attrs)


class DateTimeRangeFormTest(TestCase):

    class DummyForm(DateTimeRangeForm):
        pass

    def test_create_fields(self):
        form = self.DummyForm(Mock(), field_name='spam')

        self.assertIsInstance(form.fields['spam__gte'], forms.DateTimeField)
        self.assertIsInstance(form.fields['spam__lte'], forms.DateTimeField)

    def test_field_attributes(self):
        form = self.DummyForm(Mock(), field_name='ham')

        self.assertEquals(form.fields['ham__gte'].label, '')
        self.assertEquals(form.fields['ham__gte'].localize, True)
        self.assertEquals(form.fields['ham__gte'].required, False)
        self.assertIsInstance(form.fields['ham__gte'].widget, DateRangeFilterAdminSplitDateTime)
        self.assertDictContainsSubset({'placeholder': _('From date')},
                                      form.fields['ham__gte'].widget.attrs)

        self.assertEquals(form.fields['ham__lte'].label, '')
        self.assertEquals(form.fields['ham__lte'].localize, True)
        self.assertEquals(form.fields['ham__lte'].required, False)
        self.assertIsInstance(form.fields['ham__lte'].widget, DateRangeFilterAdminSplitDateTime)
        self.assertDictContainsSubset({'placeholder': _('To date')},
                                      form.fields['ham__lte'].widget.attrs)