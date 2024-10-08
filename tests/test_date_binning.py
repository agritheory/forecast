import datetime
from collections import OrderedDict
from decimal import Decimal

import pytest

from date_binning import Period


@pytest.fixture
def date_jan_1_23():
	return datetime.date(2023, 1, 1)


@pytest.fixture
def date_jan_2_23():
	return datetime.date(2023, 1, 2)


@pytest.fixture
def date_jan_5_23():
	return datetime.date(2023, 1, 5)


@pytest.fixture
def date_jan_7_23():
	return datetime.date(2023, 1, 7)


@pytest.fixture
def date_feb_13_23():
	return datetime.date(2023, 2, 13)


@pytest.fixture
def date_feb_16_23():
	return datetime.date(2023, 2, 16)


@pytest.fixture
def date_mar_15_23():
	return datetime.date(2023, 3, 15)


@pytest.fixture
def date_mar_31_23():
	return datetime.date(2023, 3, 31)


@pytest.fixture
def date_jun_30_23():
	return datetime.date(2023, 6, 30)


@pytest.fixture
def date_aug_10_23():
	return datetime.date(2023, 8, 10)


@pytest.fixture
def date_nov_1_23():
	return datetime.date(2023, 11, 1)


@pytest.fixture
def date_dec_31_23():
	return datetime.date(2023, 12, 31)


@pytest.fixture
def date_apr_30_24():
	return datetime.date(2024, 4, 30)


@pytest.fixture
def date_jun_30_24():
	return datetime.date(2024, 6, 30)


@pytest.fixture
def date_dec_29_24():
	return datetime.date(2024, 12, 29)


@pytest.fixture
def date_nov_1_25():
	return datetime.date(2025, 11, 1)


@pytest.fixture
def date_dec_31_25():
	return datetime.date(2025, 12, 31)


@pytest.fixture
def data_3_cal_months():
	return [1550, 2100, 3100]  # Jan (31*50)  # Feb (28*75)  # Mar (31*100)


class TestBins:
	"""
	Tests for Period().get_date_bins() functionality
	"""

	# Input Error Handling and Edge Case Tests
	def test_no_start_date(self, date_dec_31_23):
		with pytest.raises(ValueError):
			Period().get_date_bins(start_date=None, end_date=date_dec_31_23)

	def test_no_end_date(self, date_jan_2_23):
		with pytest.raises(ValueError):
			Period().get_date_bins(start_date=date_jan_2_23, end_date=None)

	def test_end_date_before_start_date(self, date_dec_31_23, date_jan_2_23):
		with pytest.raises(ValueError):
			Period().get_date_bins(date_dec_31_23, date_jan_2_23)

	def test_no_custom_days_provided(self, date_jan_2_23, date_dec_31_23):
		with pytest.raises(ValueError):
			Period().get_date_bins(date_jan_2_23, date_dec_31_23, "Custom Days")

	def test_inclusive_end_date_is_new_period_start(self, date_nov_1_23, date_nov_1_25):
		output = [
			(datetime.date(2023, 11, 1), datetime.date(2024, 10, 31)),
			(datetime.date(2024, 11, 1), datetime.date(2025, 10, 31)),
			(datetime.date(2025, 11, 1), datetime.date(2025, 11, 1)),
		]
		bins = Period().get_date_bins(date_nov_1_23, date_nov_1_25, "Annually", inclusive=True)
		assert bins == output

	# Default Parameters and Partial Period Tests
	def test_class_instantiation(self, date_jan_2_23, date_feb_13_23):
		p = Period(date_jan_2_23, date_feb_13_23)
		assert p.start_date == date_jan_2_23
		assert p.end_date == date_feb_13_23
		assert p.periodicity == "ISO Week"
		assert len(p.get_date_bins()) == 6

	def test_default_iso_week(self, date_jan_2_23):
		output = [(datetime.date(2023, 1, 2), datetime.date(2023, 1, 8))]
		ed = datetime.date(2023, 1, 9)
		bins = Period().get_date_bins(date_jan_2_23, ed, inclusive=False)
		assert bins == output

	def test_partial_period_and_exclusive_end_date(self, date_jan_5_23, date_jan_7_23):
		output = [(datetime.date(2023, 1, 5), datetime.date(2023, 1, 6))]
		bins = Period().get_date_bins(date_jan_5_23, date_jan_7_23)
		assert bins == output

	def test_inclusive_end_date(self, date_jan_5_23, date_jan_7_23):
		output = [(datetime.date(2023, 1, 5), datetime.date(2023, 1, 7))]
		bins = Period().get_date_bins(date_jan_5_23, date_jan_7_23, inclusive=True)
		assert bins == output

	# ISO Period Tests
	def test_iso_week_standard(self, date_jan_2_23, date_dec_31_23):
		output = [
			(datetime.date(2023, 1, 2), datetime.date(2023, 1, 8)),
			(datetime.date(2023, 1, 9), datetime.date(2023, 1, 15)),
			(datetime.date(2023, 1, 16), datetime.date(2023, 1, 22)),
			(datetime.date(2023, 1, 23), datetime.date(2023, 1, 29)),
			(datetime.date(2023, 1, 30), datetime.date(2023, 2, 5)),
			(datetime.date(2023, 2, 6), datetime.date(2023, 2, 12)),
			(datetime.date(2023, 2, 13), datetime.date(2023, 2, 19)),
			(datetime.date(2023, 2, 20), datetime.date(2023, 2, 26)),
			(datetime.date(2023, 2, 27), datetime.date(2023, 3, 5)),
			(datetime.date(2023, 3, 6), datetime.date(2023, 3, 12)),
			(datetime.date(2023, 3, 13), datetime.date(2023, 3, 19)),
			(datetime.date(2023, 3, 20), datetime.date(2023, 3, 26)),
			(datetime.date(2023, 3, 27), datetime.date(2023, 4, 2)),
			(datetime.date(2023, 4, 3), datetime.date(2023, 4, 9)),
			(datetime.date(2023, 4, 10), datetime.date(2023, 4, 16)),
			(datetime.date(2023, 4, 17), datetime.date(2023, 4, 23)),
			(datetime.date(2023, 4, 24), datetime.date(2023, 4, 30)),
			(datetime.date(2023, 5, 1), datetime.date(2023, 5, 7)),
			(datetime.date(2023, 5, 8), datetime.date(2023, 5, 14)),
			(datetime.date(2023, 5, 15), datetime.date(2023, 5, 21)),
			(datetime.date(2023, 5, 22), datetime.date(2023, 5, 28)),
			(datetime.date(2023, 5, 29), datetime.date(2023, 6, 4)),
			(datetime.date(2023, 6, 5), datetime.date(2023, 6, 11)),
			(datetime.date(2023, 6, 12), datetime.date(2023, 6, 18)),
			(datetime.date(2023, 6, 19), datetime.date(2023, 6, 25)),
			(datetime.date(2023, 6, 26), datetime.date(2023, 7, 2)),
			(datetime.date(2023, 7, 3), datetime.date(2023, 7, 9)),
			(datetime.date(2023, 7, 10), datetime.date(2023, 7, 16)),
			(datetime.date(2023, 7, 17), datetime.date(2023, 7, 23)),
			(datetime.date(2023, 7, 24), datetime.date(2023, 7, 30)),
			(datetime.date(2023, 7, 31), datetime.date(2023, 8, 6)),
			(datetime.date(2023, 8, 7), datetime.date(2023, 8, 13)),
			(datetime.date(2023, 8, 14), datetime.date(2023, 8, 20)),
			(datetime.date(2023, 8, 21), datetime.date(2023, 8, 27)),
			(datetime.date(2023, 8, 28), datetime.date(2023, 9, 3)),
			(datetime.date(2023, 9, 4), datetime.date(2023, 9, 10)),
			(datetime.date(2023, 9, 11), datetime.date(2023, 9, 17)),
			(datetime.date(2023, 9, 18), datetime.date(2023, 9, 24)),
			(datetime.date(2023, 9, 25), datetime.date(2023, 10, 1)),
			(datetime.date(2023, 10, 2), datetime.date(2023, 10, 8)),
			(datetime.date(2023, 10, 9), datetime.date(2023, 10, 15)),
			(datetime.date(2023, 10, 16), datetime.date(2023, 10, 22)),
			(datetime.date(2023, 10, 23), datetime.date(2023, 10, 29)),
			(datetime.date(2023, 10, 30), datetime.date(2023, 11, 5)),
			(datetime.date(2023, 11, 6), datetime.date(2023, 11, 12)),
			(datetime.date(2023, 11, 13), datetime.date(2023, 11, 19)),
			(datetime.date(2023, 11, 20), datetime.date(2023, 11, 26)),
			(datetime.date(2023, 11, 27), datetime.date(2023, 12, 3)),
			(datetime.date(2023, 12, 4), datetime.date(2023, 12, 10)),
			(datetime.date(2023, 12, 11), datetime.date(2023, 12, 17)),
			(datetime.date(2023, 12, 18), datetime.date(2023, 12, 24)),
			(datetime.date(2023, 12, 25), datetime.date(2023, 12, 31)),
		]
		bins = Period().get_date_bins(date_jan_2_23, date_dec_31_23, "ISO Week", inclusive=True)
		assert bins == output

	def test_iso_week_stub(self, date_jan_1_23, date_mar_15_23):
		output = [
			(datetime.date(2023, 1, 1), datetime.date(2023, 1, 1)),
			(datetime.date(2023, 1, 2), datetime.date(2023, 1, 8)),
			(datetime.date(2023, 1, 9), datetime.date(2023, 1, 15)),
			(datetime.date(2023, 1, 16), datetime.date(2023, 1, 22)),
			(datetime.date(2023, 1, 23), datetime.date(2023, 1, 29)),
			(datetime.date(2023, 1, 30), datetime.date(2023, 2, 5)),
			(datetime.date(2023, 2, 6), datetime.date(2023, 2, 12)),
			(datetime.date(2023, 2, 13), datetime.date(2023, 2, 19)),
			(datetime.date(2023, 2, 20), datetime.date(2023, 2, 26)),
			(datetime.date(2023, 2, 27), datetime.date(2023, 3, 5)),
			(datetime.date(2023, 3, 6), datetime.date(2023, 3, 12)),
			(datetime.date(2023, 3, 13), datetime.date(2023, 3, 15)),
		]
		bins = Period().get_date_bins(date_jan_1_23, date_mar_15_23, "ISO Week", inclusive=True)
		assert bins == output

	def test_iso_month_454(self, date_jan_2_23, date_dec_31_23):
		output = [
			(datetime.date(2023, 1, 2), datetime.date(2023, 1, 29)),
			(datetime.date(2023, 1, 30), datetime.date(2023, 3, 5)),
			(datetime.date(2023, 3, 6), datetime.date(2023, 4, 2)),
			(datetime.date(2023, 4, 3), datetime.date(2023, 4, 30)),
			(datetime.date(2023, 5, 1), datetime.date(2023, 6, 4)),
			(datetime.date(2023, 6, 5), datetime.date(2023, 7, 2)),
			(datetime.date(2023, 7, 3), datetime.date(2023, 7, 30)),
			(datetime.date(2023, 7, 31), datetime.date(2023, 9, 3)),
			(datetime.date(2023, 9, 4), datetime.date(2023, 10, 1)),
			(datetime.date(2023, 10, 2), datetime.date(2023, 10, 29)),
			(datetime.date(2023, 10, 30), datetime.date(2023, 12, 3)),
			(datetime.date(2023, 12, 4), datetime.date(2023, 12, 31)),
		]
		bins = Period().get_date_bins(
			date_jan_2_23, date_dec_31_23, "ISO Month (4 + 5 + 4)", inclusive=True
		)
		assert bins == output

	def test_iso_month_445(self, date_jan_2_23, date_dec_31_23):
		output = [
			(datetime.date(2023, 1, 2), datetime.date(2023, 1, 29)),
			(datetime.date(2023, 1, 30), datetime.date(2023, 2, 26)),
			(datetime.date(2023, 2, 27), datetime.date(2023, 4, 2)),
			(datetime.date(2023, 4, 3), datetime.date(2023, 4, 30)),
			(datetime.date(2023, 5, 1), datetime.date(2023, 5, 28)),
			(datetime.date(2023, 5, 29), datetime.date(2023, 7, 2)),
			(datetime.date(2023, 7, 3), datetime.date(2023, 7, 30)),
			(datetime.date(2023, 7, 31), datetime.date(2023, 8, 27)),
			(datetime.date(2023, 8, 28), datetime.date(2023, 10, 1)),
			(datetime.date(2023, 10, 2), datetime.date(2023, 10, 29)),
			(datetime.date(2023, 10, 30), datetime.date(2023, 11, 26)),
			(datetime.date(2023, 11, 27), datetime.date(2023, 12, 31)),
		]
		bins = Period().get_date_bins(
			date_jan_2_23, date_dec_31_23, "ISO Month (4 + 4 + 5)", inclusive=True
		)
		assert bins == output

	def test_iso_month_4_standard(self, date_jan_2_23, date_dec_31_23):
		output = [
			(datetime.date(2023, 1, 2), datetime.date(2023, 1, 29)),
			(datetime.date(2023, 1, 30), datetime.date(2023, 2, 26)),
			(datetime.date(2023, 2, 27), datetime.date(2023, 3, 26)),
			(datetime.date(2023, 3, 27), datetime.date(2023, 4, 23)),
			(datetime.date(2023, 4, 24), datetime.date(2023, 5, 21)),
			(datetime.date(2023, 5, 22), datetime.date(2023, 6, 18)),
			(datetime.date(2023, 6, 19), datetime.date(2023, 7, 16)),
			(datetime.date(2023, 7, 17), datetime.date(2023, 8, 13)),
			(datetime.date(2023, 8, 14), datetime.date(2023, 9, 10)),
			(datetime.date(2023, 9, 11), datetime.date(2023, 10, 8)),
			(datetime.date(2023, 10, 9), datetime.date(2023, 11, 5)),
			(datetime.date(2023, 11, 6), datetime.date(2023, 12, 3)),
			(datetime.date(2023, 12, 4), datetime.date(2023, 12, 31)),
		]
		bins = Period().get_date_bins(
			date_jan_2_23, date_dec_31_23, "ISO Month (4 Weeks)", inclusive=True
		)
		assert bins == output

	def test_iso_month_4_stub(self, date_jan_5_23, date_mar_15_23):
		output = [
			(datetime.date(2023, 1, 5), datetime.date(2023, 1, 29)),
			(datetime.date(2023, 1, 30), datetime.date(2023, 2, 26)),
			(datetime.date(2023, 2, 27), datetime.date(2023, 3, 15)),
		]
		bins = Period().get_date_bins(
			date_jan_5_23, date_mar_15_23, "ISO Month (4 Weeks)", inclusive=True
		)
		assert bins == output

	def test_iso_quarter_standard(self, date_jan_2_23, date_dec_31_23):
		output = [
			(datetime.date(2023, 1, 2), datetime.date(2023, 4, 2)),
			(datetime.date(2023, 4, 3), datetime.date(2023, 7, 2)),
			(datetime.date(2023, 7, 3), datetime.date(2023, 10, 1)),
			(datetime.date(2023, 10, 2), datetime.date(2023, 12, 31)),
		]
		bins = Period().get_date_bins(
			date_jan_2_23, date_dec_31_23, "ISO Quarter (13 Weeks)", inclusive=True
		)
		assert bins == output

	def test_iso_quarter_stub(self, date_jan_5_23, date_jun_30_23):
		output = [
			(datetime.date(2023, 1, 5), datetime.date(2023, 4, 2)),
			(datetime.date(2023, 4, 3), datetime.date(2023, 6, 30)),
		]
		bins = Period().get_date_bins(
			date_jan_5_23, date_jun_30_23, "ISO Quarter (13 Weeks)", inclusive=True
		)
		assert bins == output

	def test_iso_annual_standard(self, date_jan_2_23, date_dec_29_24):
		output = [
			(datetime.date(2023, 1, 2), datetime.date(2023, 12, 31)),
			(datetime.date(2024, 1, 1), datetime.date(2024, 12, 29)),
		]
		bins = Period().get_date_bins(date_jan_2_23, date_dec_29_24, "ISO Annual", inclusive=True)
		assert bins == output

	def test_iso_annual_pre_yr_start_date(self, date_jan_1_23, date_dec_29_24):
		output = [
			(datetime.date(2023, 1, 1), datetime.date(2023, 1, 1)),
			(datetime.date(2023, 1, 2), datetime.date(2023, 12, 31)),
			(datetime.date(2024, 1, 1), datetime.date(2024, 12, 29)),
		]
		bins = Period().get_date_bins(date_jan_1_23, date_dec_29_24, "ISO Annual", inclusive=True)
		assert bins == output

	def test_iso_annual_post_yr_start_date(self, date_jun_30_23, date_dec_29_24):
		output = [
			(datetime.date(2023, 6, 30), datetime.date(2023, 12, 31)),
			(datetime.date(2024, 1, 1), datetime.date(2024, 12, 29)),
		]
		bins = Period().get_date_bins(date_jun_30_23, date_dec_29_24, "ISO Annual", inclusive=True)
		assert bins == output

	def test_iso_annual_early_end_date(self, date_jan_2_23, date_jun_30_24):
		output = [
			(datetime.date(2023, 1, 2), datetime.date(2023, 12, 31)),
			(datetime.date(2024, 1, 1), datetime.date(2024, 6, 30)),
		]
		bins = Period().get_date_bins(date_jan_2_23, date_jun_30_24, "ISO Annual", inclusive=True)
		assert bins == output

	# Calendar Period Tests
	def test_custom_days(self, date_mar_15_23, date_mar_31_23):
		output = [
			(datetime.date(2023, 3, 15), datetime.date(2023, 3, 19)),
			(datetime.date(2023, 3, 20), datetime.date(2023, 3, 24)),
			(datetime.date(2023, 3, 25), datetime.date(2023, 3, 29)),
			(datetime.date(2023, 3, 30), datetime.date(2023, 3, 31)),
		]
		bins = Period().get_date_bins(
			date_mar_15_23, date_mar_31_23, "Custom Days", inclusive=True, custom_days=5
		)
		assert bins == output

	def test_cal_weekly_standard(self, date_jan_2_23, date_feb_13_23):
		output = [
			(datetime.date(2023, 1, 2), datetime.date(2023, 1, 8)),
			(datetime.date(2023, 1, 9), datetime.date(2023, 1, 15)),
			(datetime.date(2023, 1, 16), datetime.date(2023, 1, 22)),
			(datetime.date(2023, 1, 23), datetime.date(2023, 1, 29)),
			(datetime.date(2023, 1, 30), datetime.date(2023, 2, 5)),
			(datetime.date(2023, 2, 6), datetime.date(2023, 2, 12)),
		]
		bins = Period().get_date_bins(date_jan_2_23, date_feb_13_23, "Weekly", inclusive=False)
		assert bins == output

	def test_cal_weekly_non_mon_start(self, date_jan_5_23, date_feb_13_23):
		output = [
			(datetime.date(2023, 1, 5), datetime.date(2023, 1, 11)),
			(datetime.date(2023, 1, 12), datetime.date(2023, 1, 18)),
			(datetime.date(2023, 1, 19), datetime.date(2023, 1, 25)),
			(datetime.date(2023, 1, 26), datetime.date(2023, 2, 1)),
			(datetime.date(2023, 2, 2), datetime.date(2023, 2, 8)),
			(datetime.date(2023, 2, 9), datetime.date(2023, 2, 12)),
		]
		bins = Period().get_date_bins(date_jan_5_23, date_feb_13_23, "Weekly", inclusive=False)
		assert bins == output

	def test_cal_biweekly_monday_week_start(self, date_jan_2_23, date_feb_13_23):
		output = [
			(datetime.date(2023, 1, 2), datetime.date(2023, 1, 15)),
			(datetime.date(2023, 1, 16), datetime.date(2023, 1, 29)),
			(datetime.date(2023, 1, 30), datetime.date(2023, 2, 12)),
		]
		bins = Period().get_date_bins(date_jan_2_23, date_feb_13_23, "Biweekly", inclusive=False)
		assert bins == output

	def test_cal_biweekly_non_monday_start(self, date_jan_5_23, date_feb_16_23):
		output = [
			(datetime.date(2023, 1, 5), datetime.date(2023, 1, 18)),
			(datetime.date(2023, 1, 19), datetime.date(2023, 2, 1)),
			(datetime.date(2023, 2, 2), datetime.date(2023, 2, 15)),
		]
		bins = Period().get_date_bins(date_jan_5_23, date_feb_16_23, "Biweekly", inclusive=False)
		assert bins == output

	def test_cal_month(self, date_jan_7_23, date_mar_15_23):
		output = [
			(datetime.date(2023, 1, 7), datetime.date(2023, 1, 31)),
			(datetime.date(2023, 2, 1), datetime.date(2023, 2, 28)),
			(datetime.date(2023, 3, 1), datetime.date(2023, 3, 15)),
		]
		bins = Period().get_date_bins(date_jan_7_23, date_mar_15_23, "Calendar Month", inclusive=True)
		assert bins == output

	def test_cal_quarter_standard(self, date_jan_1_23, date_dec_31_23):
		output = [
			(datetime.date(2023, 1, 1), datetime.date(2023, 3, 31)),
			(datetime.date(2023, 4, 1), datetime.date(2023, 6, 30)),
			(datetime.date(2023, 7, 1), datetime.date(2023, 9, 30)),
			(datetime.date(2023, 10, 1), datetime.date(2023, 12, 31)),
		]
		bins = Period().get_date_bins(date_jan_1_23, date_dec_31_23, "Calendar Quarter", inclusive=True)
		assert bins == output

	def test_cal_quarter_stub(self, date_jan_7_23, date_aug_10_23):
		output = [
			(datetime.date(2023, 1, 7), datetime.date(2023, 3, 31)),
			(datetime.date(2023, 4, 1), datetime.date(2023, 6, 30)),
			(datetime.date(2023, 7, 1), datetime.date(2023, 8, 10)),
		]
		bins = Period().get_date_bins(date_jan_7_23, date_aug_10_23, "Calendar Quarter", inclusive=True)
		assert bins == output

	def test_cal_quarter_oct_fy(self, date_nov_1_23, date_apr_30_24):
		output = [
			(datetime.date(2023, 11, 1), datetime.date(2024, 1, 31)),
			(datetime.date(2024, 2, 1), datetime.date(2024, 4, 30)),
		]
		bins = Period().get_date_bins(date_nov_1_23, date_apr_30_24, "Calendar Quarter", inclusive=True)
		assert bins == output

	def test_cal_year_standard(self, date_jan_1_23, date_dec_31_25):
		output = [
			(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31)),
			(datetime.date(2024, 1, 1), datetime.date(2024, 12, 31)),
			(datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)),
		]
		bins = Period().get_date_bins(date_jan_1_23, date_dec_31_25, "Calendar Year", inclusive=True)
		assert bins == output

	def test_cal_year_stub(self, date_jun_30_23, date_nov_1_25):
		output = [
			(datetime.date(2023, 6, 30), datetime.date(2023, 12, 31)),
			(datetime.date(2024, 1, 1), datetime.date(2024, 12, 31)),
			(datetime.date(2025, 1, 1), datetime.date(2025, 10, 31)),
		]
		bins = Period().get_date_bins(date_jun_30_23, date_nov_1_25, "Calendar Year", inclusive=False)
		assert bins == output

	def test_cal_annually(self, date_nov_1_23, date_nov_1_25):
		output = [
			(datetime.date(2023, 11, 1), datetime.date(2024, 10, 31)),
			(datetime.date(2024, 11, 1), datetime.date(2025, 10, 31)),
		]
		bins = Period().get_date_bins(date_nov_1_23, date_nov_1_25, "Annually", inclusive=False)
		assert bins == output

	# Entire Period
	def test_entire_period_inclusive_end(self, date_nov_1_23, date_nov_1_25):
		output = [(date_nov_1_23, date_nov_1_25)]
		bins = Period().get_date_bins(date_nov_1_23, date_nov_1_25, "Entire Period", inclusive=True)
		assert bins == output

	def test_entire_period_exclusive_end(self, date_nov_1_23, date_nov_1_25):
		output = [(date_nov_1_23, datetime.date(2025, 10, 31))]
		bins = Period().get_date_bins(date_nov_1_23, date_nov_1_25, "Entire Period", inclusive=False)
		assert bins == output


class TestConversions:
	"""
	Tests for Period() bin and data conversions
	"""

	# Bin Conversion Tests
	def test_bin_iso_week_to_cal_month(self, date_jan_1_23, date_jun_30_23):
		output = [
			(datetime.date(2023, 1, 1), datetime.date(2023, 1, 31)),
			(datetime.date(2023, 2, 1), datetime.date(2023, 2, 28)),
			(datetime.date(2023, 3, 1), datetime.date(2023, 3, 31)),
			(datetime.date(2023, 4, 1), datetime.date(2023, 4, 30)),
			(datetime.date(2023, 5, 1), datetime.date(2023, 5, 31)),
			(datetime.date(2023, 6, 1), datetime.date(2023, 6, 30)),
		]
		per = Period()
		orig_bins = per.get_date_bins(date_jan_1_23, date_jun_30_23, "ISO Week", inclusive=True)
		bins = per.convert_dates(orig_bins, "Calendar Month")
		assert bins == output

	def test_bin_cal_quarter_to_annually(self, date_nov_1_23, date_nov_1_25):
		output = [
			(datetime.date(2023, 11, 1), datetime.date(2024, 10, 31)),
			(datetime.date(2024, 11, 1), datetime.date(2025, 10, 31)),
		]
		per = Period()
		orig_bins = per.get_date_bins(date_nov_1_23, date_nov_1_25, "Calendar Quarter", inclusive=False)
		bins = per.convert_dates(orig_bins, "Annually")
		assert bins == output

	# Data Conversion Tests
	def test_data_cal_month_to_cal_month(self, date_jan_1_23, date_mar_31_23, data_3_cal_months):
		output = OrderedDict(
			[
				((datetime.date(2023, 1, 1), datetime.date(2023, 1, 31)), Decimal("1550")),
				((datetime.date(2023, 2, 1), datetime.date(2023, 2, 28)), Decimal("2100")),
				((datetime.date(2023, 3, 1), datetime.date(2023, 3, 31)), Decimal("3100")),
			]
		)
		per = Period()
		orig_bins = per.get_date_bins(date_jan_1_23, date_mar_31_23, "Calendar Month", inclusive=True)
		new_data = per.redistribute_data(data_3_cal_months, orig_bins, "Calendar Month")
		assert new_data == output

	def test_data_cal_month_to_cal_quarter(self, date_jan_1_23, date_mar_31_23, data_3_cal_months):
		output = OrderedDict(
			[((datetime.date(2023, 1, 1), datetime.date(2023, 3, 31)), Decimal("6750"))]
		)
		per = Period()
		orig_bins = per.get_date_bins(date_jan_1_23, date_mar_31_23, "Calendar Month", inclusive=True)
		new_data = per.redistribute_data(data_3_cal_months, orig_bins, "Calendar Quarter")
		assert new_data == output

	def test_data_cal_month_to_iso_week(self, date_jan_1_23, date_mar_31_23, data_3_cal_months):
		output = OrderedDict(
			[
				((datetime.date(2023, 1, 1), datetime.date(2023, 1, 1)), Decimal("50")),
				((datetime.date(2023, 1, 2), datetime.date(2023, 1, 8)), Decimal("350")),
				((datetime.date(2023, 1, 9), datetime.date(2023, 1, 15)), Decimal("350")),
				((datetime.date(2023, 1, 16), datetime.date(2023, 1, 22)), Decimal("350")),
				((datetime.date(2023, 1, 23), datetime.date(2023, 1, 29)), Decimal("350")),
				((datetime.date(2023, 1, 30), datetime.date(2023, 2, 5)), Decimal("475")),
				((datetime.date(2023, 2, 6), datetime.date(2023, 2, 12)), Decimal("525")),
				((datetime.date(2023, 2, 13), datetime.date(2023, 2, 19)), Decimal("525")),
				((datetime.date(2023, 2, 20), datetime.date(2023, 2, 26)), Decimal("525")),
				((datetime.date(2023, 2, 27), datetime.date(2023, 3, 5)), Decimal("650")),
				((datetime.date(2023, 3, 6), datetime.date(2023, 3, 12)), Decimal("700")),
				((datetime.date(2023, 3, 13), datetime.date(2023, 3, 19)), Decimal("700")),
				((datetime.date(2023, 3, 20), datetime.date(2023, 3, 26)), Decimal("700")),
				((datetime.date(2023, 3, 27), datetime.date(2023, 3, 31)), Decimal("500")),
			]
		)
		per = Period()
		orig_bins = per.get_date_bins(date_jan_1_23, date_mar_31_23, "Calendar Month", inclusive=True)
		new_data = per.redistribute_data(data_3_cal_months, orig_bins, "ISO Week")
		assert new_data == output


class TestLabels:
	"""
	Tests for Period() label creation
	"""

	def test_get_iso_week_and_year(self):
		date = datetime.date(2020, 12, 28)
		iso_w, iso_y = Period().get_iso_week_and_year(date)
		assert iso_w == 53 and iso_y == 2020

	def test_iso_week_labels(self, date_jan_2_23, date_feb_13_23):
		output = ["Week 1-23", "Week 2-23", "Week 3-23", "Week 4-23", "Week 5-23", "Week 6-23"]
		p = Period(date_jan_2_23, date_feb_13_23)
		bins = p.get_date_bins(inclusive=False)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_iso_biweekly_labels(self, date_jan_2_23, date_feb_13_23):
		output = ["Weeks 1-2 23", "Weeks 3-4 23", "Weeks 5-6 23"]
		p = Period(date_jan_2_23, date_feb_13_23, "ISO Biweekly")
		bins = p.get_date_bins(inclusive=False)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_iso_month_4_labels(self, date_jan_2_23):
		output = [
			"Jan-23",
			"Feb-23",
			"Mar-23",
			"Apr-23",
			"May-23",
			"Jun-23",
			"Jul-23",
			"Aug-23",
			"Sep-23",
			"Oct-23",
			"Nov-23",
			"Dec-23",
			"M13-23",
		]
		ed = datetime.date(2024, 1, 1)
		p = Period(date_jan_2_23, ed, "ISO Month (4 Weeks)")
		bins = p.get_date_bins(inclusive=False)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_iso_month_454_full_year_labels(self, date_jan_2_23):
		output = [
			"Jan-23",
			"Feb-23",
			"Mar-23",
			"Apr-23",
			"May-23",
			"Jun-23",
			"Jul-23",
			"Aug-23",
			"Sep-23",
			"Oct-23",
			"Nov-23",
			"Dec-23",
		]
		ed = datetime.date(2024, 1, 1)
		p = Period(date_jan_2_23, ed, "ISO Month (4 + 5 + 4)")
		bins = p.get_date_bins(inclusive=False)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_iso_month_454_labels(self, date_jan_2_23):
		output = ["Jan-23", "Feb-23"]
		ed = datetime.date(2023, 3, 6)
		p = Period(date_jan_2_23, ed, "ISO Month (4 + 5 + 4)")
		bins = p.get_date_bins(inclusive=False)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_iso_month_445_labels(self, date_jan_2_23):
		output = ["Jan-23", "Feb-23", "Mar-23"]
		ed = datetime.date(2023, 3, 6)
		p = Period(date_jan_2_23, ed, "ISO Month (4 + 4 + 5)")
		bins = p.get_date_bins(inclusive=False)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_iso_quarter_labels(self, date_jan_2_23, date_dec_31_23):
		output = ["Q1-23", "Q2-23", "Q3-23", "Q4-23"]
		p = Period(date_jan_2_23, date_dec_31_23, "ISO Quarter (13 Weeks)")
		bins = p.get_date_bins(inclusive=True)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_iso_semiannual_labels(self, date_jan_2_23, date_dec_31_23):
		output = ["HY1-23", "HY2-23"]
		p = Period(date_jan_2_23, date_dec_31_23, "ISO Semiannual (26 Weeks)")
		bins = p.get_date_bins(inclusive=True)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_iso_annual_labels(self):
		output = ["2022", "2023"]
		sd = datetime.date(2022, 1, 3)
		ed = datetime.date(2024, 1, 1)
		p = Period(sd, ed, "ISO Annual")
		bins = p.get_date_bins(inclusive=False)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_custom_days_labels(self, date_mar_15_23, date_mar_31_23):
		output = ["03/19/23", "03/24/23", "03/29/23", "03/31/23"]
		p = Period(date_mar_15_23, date_mar_31_23, "Custom Days")
		bins = p.get_date_bins(inclusive=True, custom_days=5)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_weekly_labels(self, date_jan_5_23):
		output = ["01/11/23", "01/18/23", "01/25/23", "02/01/23"]
		ed = datetime.date(2023, 2, 2)
		p = Period(date_jan_5_23, ed, "Weekly")
		bins = p.get_date_bins(inclusive=False)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_biweekly_labels(self, date_jan_5_23):
		output = ["01/18/23", "02/01/23"]
		ed = datetime.date(2023, 2, 2)
		p = Period(date_jan_5_23, ed, "Biweekly")
		bins = p.get_date_bins(inclusive=False)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_cal_month_labels(self, date_jan_1_23, date_mar_31_23):
		output = ["Jan-23", "Feb-23", "Mar-23"]
		p = Period(date_jan_1_23, date_mar_31_23, "Calendar Month")
		bins = p.get_date_bins(inclusive=True)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_cal_quarter_labels(self, date_jan_1_23, date_dec_31_23):
		output = ["03-23Q", "06-23Q", "09-23Q", "12-23Q"]
		p = Period(date_jan_1_23, date_dec_31_23, "Calendar Quarter")
		bins = p.get_date_bins(inclusive=True)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_cal_year_labels(self, date_jan_1_23, date_dec_31_25):
		output = ["12/31/23", "12/31/24", "12/31/25"]
		p = Period(date_jan_1_23, date_dec_31_25, "Calendar Year")
		bins = p.get_date_bins(inclusive=True)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_cal_annually(self, date_nov_1_23, date_nov_1_25):
		output = ["10/31/24", "10/31/25"]
		p = Period(date_nov_1_23, date_nov_1_25, "Annually")
		bins = p.get_date_bins(inclusive=False)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_entire_period_labels(self, date_jan_7_23, date_nov_1_23):
		output = ["01/07/23-11/01/23"]
		p = Period(date_jan_7_23, date_nov_1_23, "Entire Period")
		bins = p.get_date_bins(inclusive=True)
		labels = p.get_period_labels(bins)
		assert labels == output

	def test_custom_date_format(self, date_jan_1_23, date_mar_31_23):
		output = ["Jan", "Feb", "Mar"]
		fmt_str = "%b"
		p = Period(date_jan_1_23, date_mar_31_23, "Calendar Month")
		bins = p.get_date_bins(inclusive=True)
		labels = p.get_period_labels(
			bins, date_format_string=fmt_str, use_bin_start_date_for_label=False
		)
		assert labels == output
