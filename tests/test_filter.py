from unittest import TestCase
from django import forms
from daterange_filter.filter import DateRangeFilterBaseForm
from mock import Mock


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
