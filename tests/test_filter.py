from datetime import datetime, date, timedelta

from django.utils import timezone
from mock import Mock, call, ANY, patch
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import ugettext as _
from daterange_filter.filter import DateRangeFilterBaseForm, DateRangeForm, DateTimeRangeForm, \
    DateRangeFilterAdminSplitDateTime, DateRangeFilter, DateTimeRangeFilter
from tests import BaseTest


class DateRangeFilterBaseFormTest(BaseTest):
    def setUp(self):
        self.request = Mock()

    def test_form_returns_all_media(self):
        del self.request.daterange_filter_media_included
        form = DateRangeFilterBaseForm(self.request)

        self.assertEqual(str(form.media), str(forms.Media(
            js=['admin/js/calendar.js', 'admin/js/admin/DateTimeShortcuts.js'],
            css={'all': ['admin/css/widgets.css']}
        )))

    def test_form_returns_empty_media_if_another_form_has_already_been_instantiated(self):
        del self.request.daterange_filter_media_included

        form_1 = DateRangeFilterBaseForm(self.request)
        form_2 = DateRangeFilterBaseForm(self.request)

        self.assertNotEqual(str(form_1.media), '')
        self.assertEqual(str(form_2.media), '')


class DateRangeFormTest(BaseTest):
    def test_create_fields(self):
        form = DateRangeForm(Mock(), field_name='spam')

        self.assertIsInstance(form.fields['spam__gte'], forms.DateField)
        self.assertIsInstance(form.fields['spam__lte'], forms.DateField)

    def test_field_attributes(self):
        form = DateRangeForm(Mock(), field_name='ham')

        self.assertEqual(form.fields['ham__gte'].label, '')
        self.assertEqual(form.fields['ham__gte'].localize, True)
        self.assertEqual(form.fields['ham__gte'].required, False)
        self.assertIsInstance(form.fields['ham__gte'].widget, AdminDateWidget)
        self.assertDictContainsSubset({'placeholder': _('From date')},
                                      form.fields['ham__gte'].widget.attrs)

        self.assertEqual(form.fields['ham__lte'].label, '')
        self.assertEqual(form.fields['ham__lte'].localize, True)
        self.assertEqual(form.fields['ham__lte'].required, False)
        self.assertIsInstance(form.fields['ham__lte'].widget, AdminDateWidget)
        self.assertDictContainsSubset({'placeholder': _('To date')},
                                      form.fields['ham__lte'].widget.attrs)


class DateTimeRangeFormTest(BaseTest):

    class DummyForm(DateTimeRangeForm):
        pass

    def test_create_fields(self):
        form = self.DummyForm(Mock(), field_name='spam')

        self.assertIsInstance(form.fields['spam__gte'], forms.DateTimeField)
        self.assertIsInstance(form.fields['spam__lte'], forms.DateTimeField)

    def test_field_attributes(self):
        form = self.DummyForm(Mock(), field_name='ham')

        self.assertEqual(form.fields['ham__gte'].label, '')
        self.assertEqual(form.fields['ham__gte'].localize, True)
        self.assertEqual(form.fields['ham__gte'].required, False)
        self.assertIsInstance(form.fields['ham__gte'].widget, DateRangeFilterAdminSplitDateTime)
        self.assertDictContainsSubset({'placeholder': _('From date')},
                                      form.fields['ham__gte'].widget.attrs)

        self.assertEqual(form.fields['ham__lte'].label, '')
        self.assertEqual(form.fields['ham__lte'].localize, True)
        self.assertEqual(form.fields['ham__lte'].required, False)
        self.assertIsInstance(form.fields['ham__lte'].widget, DateRangeFilterAdminSplitDateTime)
        self.assertDictContainsSubset({'placeholder': _('To date')},
                                      form.fields['ham__lte'].widget.attrs)


class DateRangeFilterTest(BaseTest):
    def setUp(self):
        self.request = Mock()
        self.filter_ = DateRangeFilter('spam', self.request, [], Mock(), Mock(), 'egg')

    def test_use_correctly_template(self):
        self.assertEqual(self.filter_.template, 'daterange_filter/filter.html')

    def test_form_uses_request(self):
        self.assertEqual(self.filter_.form.request, self.request)

    def test_choices_is_empty(self):
        self.assertEqual(self.filter_.choices(Mock()), [])

    def test_expected_params(self):
        self.assertItemsEqual(self.filter_.expected_parameters(), ['egg__lte', 'egg__gte'])

    @patch('daterange_filter.filter.DateRangeForm')
    def test_get_form(self, DateRangeForm):
        self.filter_.get_form(self.request)

        self.assertEqual([call(self.request, data=ANY, field_name='egg')],
                          DateRangeForm.call_args_list)

    def test_queryset_ignore_null_fields(self):
        queryset = Mock()
        params = {'ham__gte': None, 'ham__lte': None}
        filter_ = DateRangeFilter('spam', self.request, params, Mock(), Mock(), 'ham')

        return_value = filter_.queryset(self.request, queryset)

        self.assertEqual(return_value, queryset.filter.return_value)
        self.assertItemsEqual([call()], queryset.filter.call_args_list)

    def test_queryset_filters_by_date_from(self):
        queryset = Mock()
        params = {'ham__gte': date(2014, 1, 3), 'ham__lte': None}
        filter_ = DateRangeFilter('spam', self.request, params, Mock(), Mock(), 'ham')

        return_value = filter_.queryset(self.request, queryset)

        self.assertEqual(return_value, queryset.filter.return_value)
        self.assertItemsEqual([call(ham__gte=date(2014, 1, 3))], queryset.filter.call_args_list)

    def test_queryset_filters_by_date_to(self):
        queryset = Mock()
        data_end = date(2014, 1, 3)
        params = {'ham__gte': None, 'ham__lte': data_end}
        filter_ = DateRangeFilter('spam', self.request, params, Mock(), Mock(), 'ham')

        return_value = filter_.queryset(self.request, queryset)

        self.assertEqual(return_value, queryset.filter.return_value)
        self.assertEqual((data_end + timedelta(days=1)).strftime('%s'),
                          queryset.filter.call_args_list[0][1]['ham__lt'].strftime('%s'))

    def test_return_raw_queryset_if_form_is_invalid(self):
        queryset = Mock()
        params = {'ham__gte': 'Yay!', 'ham__lte': None}
        filter_ = DateRangeFilter('spam', self.request, params, Mock(), Mock(), 'ham')

        return_value = filter_.queryset(self.request, queryset)

        self.assertEqual(return_value, queryset)


class DateTimeRangeFilterTest(BaseTest):
    def setUp(self):
        self.request = Mock()
        self.filter_ = DateTimeRangeFilter('spam', self.request, {'egg__lte_0': None, 'egg__lte_1': None}, Mock(),
                                           Mock(), 'egg')

    def test_use_correctly_template(self):
        self.assertEqual(self.filter_.template, 'daterange_filter/filter.html')

    def test_form_uses_request(self):
        self.assertEqual(self.filter_.form.request, self.request)

    def test_choices_is_empty(self):
        self.assertEqual(self.filter_.choices(Mock()), [])

    def test_expected_params(self):
        self.assertItemsEqual(self.filter_.expected_parameters(), ['egg__lte_0', 'egg__lte_1', 'egg__gte_0', 'egg__gte_1'])

    @patch('daterange_filter.filter.DateTimeRangeForm')
    def test_get_form(self, DateTimeRangeForm):
        self.filter_.get_form(self.request)

        self.assertEqual([call(self.request, data={'egg__lte_0': None, 'egg__lte_1': None}, field_name='egg')],
                          DateTimeRangeForm.call_args_list)

    def test_queryset_ignore_null_fields(self):
        queryset = Mock()
        params = {'ham__gte_0': None, 'ham__gte_1': None, 'ham__lte_0': None, 'ham__lte_1': None}
        filter_ = DateTimeRangeFilter('spam', self.request, params, Mock(), Mock(), 'ham')

        return_value = filter_.queryset(self.request, queryset)

        self.assertEqual(return_value, queryset.filter.return_value)
        self.assertItemsEqual([call()], queryset.filter.call_args_list)

    def test_queryset_filters_by_date_from(self):
        queryset = Mock()
        params = {'ham__gte_0': '2014-01-02', 'ham__gte_1': '03:04:05', 'ham__lte_0': None, 'ham__lte_1': None}
        filter_ = DateTimeRangeFilter('spam', self.request, params, Mock(), Mock(), 'ham')

        return_value = filter_.queryset(self.request, queryset)
        timezoned_expected_result = timezone.make_aware(datetime(2014, 1, 2, 3, 4, 5), timezone.get_current_timezone())

        self.assertEqual(return_value, queryset.filter.return_value)
        self.assertItemsEqual([call(ham__gte=timezoned_expected_result)], queryset.filter.call_args_list)

    def test_queryset_filters_by_date_to(self):
        queryset = Mock()
        data_end = timezone.make_aware(datetime(2014, 1, 2, 3, 4, 5), timezone.get_current_timezone())
        params = {'ham__lte_0': data_end.strftime('%Y-%m-%d'), 'ham__lte_1': data_end.strftime('%H:%M:%S'),
                  'ham__gte_0': None, 'ham__gte_1': None}
        filter_ = DateTimeRangeFilter('spam', self.request, params, Mock(), Mock(), 'ham')

        return_value = filter_.queryset(self.request, queryset)

        self.assertEqual(return_value, queryset.filter.return_value)
        self.assertEqual(data_end, queryset.filter.call_args_list[0][1]['ham__lte'])

    def test_return_raw_queryset_if_form_is_invalid(self):
        queryset = Mock()
        params = {'ham__gte_0': 'Yay!', 'ham__gte_1': None, 'ham__lte_0': None, 'ham__lte_1': None}
        filter_ = DateTimeRangeFilter('spam', self.request, params, Mock(), Mock(), 'ham')

        return_value = filter_.queryset(self.request, queryset)

        self.assertEqual(return_value, queryset)
