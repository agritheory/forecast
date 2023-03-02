from collections import OrderedDict
import datetime
from decimal import Decimal
import pytest

# Adjust system path for pytest to find modules (avoid ImportError)
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

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
    return [
        1550,  # Jan (31*50)
        2100,  # Feb (28*75)
        3100   # Mar (31*100)
    ]


class TestBins:
    """
    Tests for Period().get_dates() functionality
    """
    # Input Error Handling and Edge Case Tests
    def test_no_start_date(self, date_dec_31_23):
        with pytest.raises(ValueError):
            Period().get_dates(start_date=None, end_date=date_dec_31_23)
    
    def test_no_end_date(self, date_jan_2_23):
        with pytest.raises(ValueError):
            Period().get_dates(start_date=date_jan_2_23, end_date=None)

    def test_end_date_before_start_date(self, date_dec_31_23, date_jan_2_23):
        with pytest.raises(ValueError):
            Period().get_dates(date_dec_31_23, date_jan_2_23)
    
    def test_inclusive_end_date_is_new_period_start(self, date_nov_1_23, date_nov_1_25):
        cal_inc_ed_new_period_output = [
            (datetime.date(2023, 11, 1), datetime.date(2024, 10, 31)),
            (datetime.date(2024, 11, 1), datetime.date(2025, 10, 31)),
            (datetime.date(2025, 11, 1), datetime.date(2025, 11, 1))
        ]
        bins = Period().get_dates(date_nov_1_23, date_nov_1_25, "Annually", inclusive=False)
        for index, b in enumerate(bins):
            assert b == cal_inc_ed_new_period_output[index]

    # Default Parameters and Partial Period Tests
    def test_default_iso_week(self, date_jan_2_23):
        default_output = [
            (datetime.date(2023, 1, 2), datetime.date(2023, 1, 8))
        ]
        ed = datetime.date(2023, 1, 9)
        bins = Period().get_dates(date_jan_2_23, ed)
        for index, b in enumerate(bins):
            assert b == default_output[index]

    def test_partial_period(self, date_jan_5_23, date_jan_7_23):
        partial_output = [
            (datetime.date(2023, 1, 5), datetime.date(2023, 1, 6))
        ]
        bins = Period().get_dates(date_jan_5_23, date_jan_7_23)
        for index, b in enumerate(bins):
            assert b == partial_output[index]

    def test_inclusive_end_date(self, date_jan_5_23, date_jan_7_23):
        inclusive_end_output = [
            (datetime.date(2023, 1, 5), datetime.date(2023, 1, 7))
        ]
        bins = Period().get_dates(date_jan_5_23, date_jan_7_23, inclusive=True)
        for index, b in enumerate(bins):
            assert b == inclusive_end_output[index]

    # ISO Period Tests
    def test_iso_week_standard(self, date_jan_2_23, date_dec_31_23):
        iso_week_standard_output = [
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
            (datetime.date(2023, 12, 25), datetime.date(2023, 12, 31))
        ]
        bins = Period().get_dates(date_jan_2_23, date_dec_31_23, "ISO Week", inclusive=True)
        for index, b in enumerate(bins):
            assert b == iso_week_standard_output[index]
    
    def test_iso_week_stub(self, date_jan_1_23, date_mar_15_23):
        iso_week_stub_output = [
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
            (datetime.date(2023, 3, 13), datetime.date(2023, 3, 15))
        ]
        bins = Period().get_dates(date_jan_1_23, date_mar_15_23, "ISO Week", inclusive=True)
        for index, b in enumerate(bins):
            assert b == iso_week_stub_output[index]
    
    def test_iso_month_454(self, date_jan_2_23, date_dec_31_23):
        iso_month_454_output = [
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
            (datetime.date(2023, 12, 4), datetime.date(2023, 12, 31))
        ]
        bins = Period().get_dates(date_jan_2_23, date_dec_31_23, "ISO Month (4 + 5 + 4)", inclusive=True)
        for index, b in enumerate(bins):
            assert b == iso_month_454_output[index]
    
    def test_iso_month_445(self, date_jan_2_23, date_dec_31_23):
        iso_month_445_output = [
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
            (datetime.date(2023, 11, 27), datetime.date(2023, 12, 31))
        ]
        bins = Period().get_dates(date_jan_2_23, date_dec_31_23, "ISO Month (4 + 4 + 5)", inclusive=True)
        for index, b in enumerate(bins):
            assert b == iso_month_445_output[index]
    
    def test_iso_month_4_standard(self, date_jan_2_23, date_dec_31_23):
        iso_month_4_standard_output = [
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
            (datetime.date(2023, 12, 4), datetime.date(2023, 12, 31))
        ]
        bins = Period().get_dates(date_jan_2_23, date_dec_31_23, "ISO Month (4 Weeks)", inclusive=True)
        for index, b in enumerate(bins):
            assert b == iso_month_4_standard_output[index]
    
    def test_iso_month_4_stub(self, date_jan_5_23, date_mar_15_23):
        iso_month_4_stub_output = [
            (datetime.date(2023, 1, 5), datetime.date(2023, 1, 29)),
            (datetime.date(2023, 1, 30), datetime.date(2023, 2, 26)),
            (datetime.date(2023, 2, 27), datetime.date(2023, 3, 15))
        ]
        bins = Period().get_dates(date_jan_5_23, date_mar_15_23, "ISO Month (4 Weeks)", inclusive=True)
        for index, b in enumerate(bins):
            assert b == iso_month_4_stub_output[index]
    
    def test_iso_quarter_standard(self, date_jan_2_23, date_dec_31_23):
        iso_quarter_standard_output = [
            (datetime.date(2023, 1, 2), datetime.date(2023, 4, 2)),
            (datetime.date(2023, 4, 3), datetime.date(2023, 7, 2)),
            (datetime.date(2023, 7, 3), datetime.date(2023, 10, 1)),
            (datetime.date(2023, 10, 2), datetime.date(2023, 12, 31))
        ]
        bins = Period().get_dates(date_jan_2_23, date_dec_31_23, "ISO Quarter (13 Weeks)", inclusive=True)
        for index, b in enumerate(bins):
            assert b == iso_quarter_standard_output[index]
    
    def test_iso_quarter_stub(self, date_jan_5_23, date_jun_30_23):
        iso_quarter_stub_output = [
            (datetime.date(2023, 1, 5), datetime.date(2023, 4, 2)),
            (datetime.date(2023, 4, 3), datetime.date(2023, 6, 30))
        ]
        bins = Period().get_dates(date_jan_5_23, date_jun_30_23, "ISO Quarter (13 Weeks)", inclusive=True)
        for index, b in enumerate(bins):
            assert b == iso_quarter_stub_output[index]
    
    def test_iso_annual_standard(self, date_jan_2_23, date_dec_29_24):
        iso_annual_standard_output = [
            (datetime.date(2023, 1, 2), datetime.date(2023, 12, 31)),
            (datetime.date(2024, 1, 1), datetime.date(2024, 12, 29))
        ]
        bins = Period().get_dates(date_jan_2_23, date_dec_29_24, "ISO Annual", inclusive=True)
        for index, b in enumerate(bins):
            assert b == iso_annual_standard_output[index]

    def test_iso_annual_pre_yr_start_date(self, date_jan_1_23, date_dec_29_24):
        iso_annual_pre_yr_sd_output = [
            (datetime.date(2023, 1, 1), datetime.date(2023, 1, 1)),
            (datetime.date(2023, 1, 2), datetime.date(2023, 12, 31)),
            (datetime.date(2024, 1, 1), datetime.date(2024, 12, 29))
        ]
        bins = Period().get_dates(date_jan_1_23, date_dec_29_24, "ISO Annual", inclusive=True)
        for index, b in enumerate(bins):
            assert b == iso_annual_pre_yr_sd_output[index]

    def test_iso_annual_post_yr_start_date(self, date_jun_30_23, date_dec_29_24):
        iso_annual_post_yr_sd_output = [
            (datetime.date(2023, 6, 30), datetime.date(2023, 12, 31)),
            (datetime.date(2024, 1, 1), datetime.date(2024, 12, 29))
        ]
        bins = Period().get_dates(date_jun_30_23, date_dec_29_24, "ISO Annual", inclusive=True)
        for index, b in enumerate(bins):
            assert b == iso_annual_post_yr_sd_output[index]

    def test_iso_annual_early_end_date(self, date_jan_2_23, date_jun_30_24):
        iso_annual_early_ed_output = [
            (datetime.date(2023, 1, 2), datetime.date(2023, 12, 31)),
            (datetime.date(2024, 1, 1), datetime.date(2024, 6, 30))
        ]
        bins = Period().get_dates(date_jan_2_23, date_jun_30_24, "ISO Annual", inclusive=True)
        for index, b in enumerate(bins):
            assert b == iso_annual_early_ed_output[index]

    # Calendar Period Tests
    def test_cal_weekly_standard(self, date_jan_2_23, date_feb_13_23):
        cal_weekly_standard_output = [
            (datetime.date(2023, 1, 2), datetime.date(2023, 1, 8)),
            (datetime.date(2023, 1, 9), datetime.date(2023, 1, 15)),
            (datetime.date(2023, 1, 16), datetime.date(2023, 1, 22)),
            (datetime.date(2023, 1, 23), datetime.date(2023, 1, 29)),
            (datetime.date(2023, 1, 30), datetime.date(2023, 2, 5)),
            (datetime.date(2023, 2, 6), datetime.date(2023, 2, 12))
        ]
        bins = Period().get_dates(date_jan_2_23, date_feb_13_23, "Weekly", inclusive=False)
        for index, b in enumerate(bins):
            assert b == cal_weekly_standard_output[index]
    
    def test_cal_weekly_non_mon_start(self, date_jan_5_23, date_feb_13_23):
        cal_weekly_non_mon_start_output = [
            (datetime.date(2023, 1, 5), datetime.date(2023, 1, 8)),
            (datetime.date(2023, 1, 9), datetime.date(2023, 1, 15)),
            (datetime.date(2023, 1, 16), datetime.date(2023, 1, 22)),
            (datetime.date(2023, 1, 23), datetime.date(2023, 1, 29)),
            (datetime.date(2023, 1, 30), datetime.date(2023, 2, 5)),
            (datetime.date(2023, 2, 6), datetime.date(2023, 2, 12))
        ]
        bins = Period().get_dates(date_jan_5_23, date_feb_13_23, "Weekly", inclusive=False)
        for index, b in enumerate(bins):
            assert b == cal_weekly_non_mon_start_output[index]
    
    @pytest.mark.skip("Unable to modify the week_start contextvar set in date_binning module here.")
    def test_cal_weekly_thu_week_standard(self, date_jan_5_23, date_feb_13_23):
        cal_weekly_thu_week_standard_output = [
            (datetime.date(2023, 1, 5), datetime.date(2023, 1, 11)),
            (datetime.date(2023, 1, 12), datetime.date(2023, 1, 18)),
            (datetime.date(2023, 1, 19), datetime.date(2023, 1, 25)),
            (datetime.date(2023, 1, 26), datetime.date(2023, 2, 1)),
            (datetime.date(2023, 2, 2), datetime.date(2023, 2, 8)),
            (datetime.date(2023, 2, 9), datetime.date(2023, 2, 12))
        ]
        bins = Period().get_dates(date_jan_5_23, date_feb_13_23, "Weekly", inclusive=False)
        for index, b in enumerate(bins):
            assert b == cal_weekly_thu_week_standard_output[index]

    @pytest.mark.skip("Unable to modify the week_start contextvar set in date_binning module here.")
    def test_cal_weekly_thu_week_pre_thu_start(self, date_jan_2_23, date_feb_13_23):
        cal_weekly_thu_week_pre_thu_start_output = [
            (datetime.date(2023, 1, 2), datetime.date(2023, 1, 4)),
            (datetime.date(2023, 1, 5), datetime.date(2023, 1, 11)),
            (datetime.date(2023, 1, 12), datetime.date(2023, 1, 18)),
            (datetime.date(2023, 1, 19), datetime.date(2023, 1, 25)),
            (datetime.date(2023, 1, 26), datetime.date(2023, 2, 1)),
            (datetime.date(2023, 2, 2), datetime.date(2023, 2, 8)),
            (datetime.date(2023, 2, 9), datetime.date(2023, 2, 12))
        ]
        bins = Period().get_dates(date_jan_2_23, date_feb_13_23, "Weekly", inclusive=False)
        for index, b in enumerate(bins):
            assert b == cal_weekly_thu_week_pre_thu_start_output[index]
    
    @pytest.mark.skip("Unable to modify the week_start contextvar set in date_binning module here.")
    def test_cal_weekly_thu_week_post_thu_start(self, date_jan_7_23, date_feb_13_23):
        cal_weekly_thu_week_post_thu_start_output = [
            (datetime.date(2023, 1, 7), datetime.date(2023, 1, 11)),
            (datetime.date(2023, 1, 12), datetime.date(2023, 1, 18)),
            (datetime.date(2023, 1, 19), datetime.date(2023, 1, 25)),
            (datetime.date(2023, 1, 26), datetime.date(2023, 2, 1)),
            (datetime.date(2023, 2, 2), datetime.date(2023, 2, 8)),
            (datetime.date(2023, 2, 9), datetime.date(2023, 2, 12))
        ]
        bins = Period().get_dates(date_jan_7_23, date_feb_13_23, "Weekly", inclusive=False)
        for index, b in enumerate(bins):
            assert b == cal_weekly_thu_week_post_thu_start_output[index]

    def test_cal_biweekly_standard(self, date_jan_2_23, date_feb_13_23):
        cal_biweekly_standard_output = [
            (datetime.date(2023, 1, 2), datetime.date(2023, 1, 15)),
            (datetime.date(2023, 1, 16), datetime.date(2023, 1, 29)),
            (datetime.date(2023, 1, 30), datetime.date(2023, 2, 12))
        ]
        bins = Period().get_dates(date_jan_2_23, date_feb_13_23, "Biweekly", inclusive=False)
        for index, b in enumerate(bins):
            assert b == cal_biweekly_standard_output[index]
    
    def test_cal_biweekly_stub(self, date_jan_7_23, date_feb_13_23):
        cal_biweekly_stub_output = [
            (datetime.date(2023, 1, 7), datetime.date(2023, 1, 15)),
            (datetime.date(2023, 1, 16), datetime.date(2023, 1, 29)),
            (datetime.date(2023, 1, 30), datetime.date(2023, 2, 12))
        ]
        bins = Period().get_dates(date_jan_7_23, date_feb_13_23, "Biweekly", inclusive=False)
        for index, b in enumerate(bins):
            assert b == cal_biweekly_stub_output[index]
    
    def test_cal_month(self, date_jan_7_23, date_mar_15_23):
        cal_month_output = [
            (datetime.date(2023, 1, 7), datetime.date(2023, 1, 31)),
            (datetime.date(2023, 2, 1), datetime.date(2023, 2, 28)),
            (datetime.date(2023, 3, 1), datetime.date(2023, 3, 15))
        ]
        bins = Period().get_dates(date_jan_7_23, date_mar_15_23, "Calendar Month", inclusive=True)
        for index, b in enumerate(bins):
            assert b == cal_month_output[index]

    def test_cal_quarter_standard(self, date_jan_1_23, date_dec_31_23):
        cal_quarter_standard_output = [
            (datetime.date(2023, 1, 1), datetime.date(2023, 3, 31)),
            (datetime.date(2023, 4, 1), datetime.date(2023, 6, 30)),
            (datetime.date(2023, 7, 1), datetime.date(2023, 9, 30)),
            (datetime.date(2023, 10, 1), datetime.date(2023, 12, 31))
        ]
        bins = Period().get_dates(date_jan_1_23, date_dec_31_23, "Calendar Quarter", inclusive=True)
        for index, b in enumerate(bins):
            assert b == cal_quarter_standard_output[index]
    
    def test_cal_quarter_stub(self, date_jan_7_23, date_aug_10_23):
        cal_quarter_stub_output = [
            (datetime.date(2023, 1, 7), datetime.date(2023, 3, 31)),
            (datetime.date(2023, 4, 1), datetime.date(2023, 6, 30)),
            (datetime.date(2023, 7, 1), datetime.date(2023, 8, 10))    
        ]
        bins = Period().get_dates(date_jan_7_23, date_aug_10_23, "Calendar Quarter", inclusive=True)
        for index, b in enumerate(bins):
            assert b == cal_quarter_stub_output[index]

    def test_cal_quarter_oct_fy(self, date_nov_1_23, date_apr_30_24):
        cal_quarter_oct_fy_output = [
            (datetime.date(2023, 11, 1), datetime.date(2024, 1, 31)),
            (datetime.date(2024, 2, 1), datetime.date(2024, 4, 30))           
        ]
        bins = Period().get_dates(date_nov_1_23, date_apr_30_24, "Calendar Quarter", inclusive=True)
        for index, b in enumerate(bins):
            assert b == cal_quarter_oct_fy_output[index]

    def test_cal_year_standard(self, date_jan_1_23, date_dec_31_25):
        cal_year_standard_output = [
            (datetime.date(2023, 1, 1), datetime.date(2023, 12, 31)),
            (datetime.date(2024, 1, 1), datetime.date(2024, 12, 31)),
            (datetime.date(2025, 1, 1), datetime.date(2025, 12, 31))
        ]
        bins = Period().get_dates(date_jan_1_23, date_dec_31_25, "Calendar Year", inclusive=True)
        for index, b in enumerate(bins):
            assert b == cal_year_standard_output[index]
    
    def test_cal_year_stub(self, date_jun_30_23, date_nov_1_25):
        cal_year_stub_output = [
            (datetime.date(2023, 6, 30), datetime.date(2023, 12, 31)),
            (datetime.date(2024, 1, 1), datetime.date(2024, 12, 31)),
            (datetime.date(2025, 1, 1), datetime.date(2025, 10, 31))
        ]
        bins = Period().get_dates(date_jun_30_23, date_nov_1_25, "Calendar Year", inclusive=False)
        for index, b in enumerate(bins):
            assert b == cal_year_stub_output[index]

    def test_cal_annually(self, date_nov_1_23, date_nov_1_25):
        cal_annually_output = [
            (datetime.date(2023, 11, 1), datetime.date(2024, 10, 31)),
            (datetime.date(2024, 11, 1), datetime.date(2025, 10, 31))
        ]
        bins = Period().get_dates(date_nov_1_23, date_nov_1_25, "Annually", inclusive=False)
        for index, b in enumerate(bins):
            assert b == cal_annually_output[index]


class TestConversions:
    """
    Tests for Period() bin and data conversions
    """
    # Input Error Handling Tests
    def test_no_bins(self, date_jan_7_23, date_jan_1_23):
        with pytest.raises(ValueError):
            per = Period()
            orig_bins = per.get_dates(date_jan_7_23, date_jan_1_23, "Weekly", inclusive=True)
            bins = per.convert_dates(orig_bins, "Calendar Month")

    # Bin Conversion Tests
    def test_bin_iso_week_to_cal_month(self, date_jan_1_23, date_jun_30_23):
        bin_iso_week_to_cal_month_output = [
            (datetime.date(2023, 1, 1), datetime.date(2023, 1, 31)),
            (datetime.date(2023, 2, 1), datetime.date(2023, 2, 28)),
            (datetime.date(2023, 3, 1), datetime.date(2023, 3, 31)),
            (datetime.date(2023, 4, 1), datetime.date(2023, 4, 30)),
            (datetime.date(2023, 5, 1), datetime.date(2023, 5, 31)),
            (datetime.date(2023, 6, 1), datetime.date(2023, 6, 30))
        ]
        per = Period()
        orig_bins = per.get_dates(date_jan_1_23, date_jun_30_23, "ISO Week", inclusive=True)
        bins = per.convert_dates(orig_bins, "Calendar Month")
        for index, b in enumerate(bins):
            assert b == bin_iso_week_to_cal_month_output[index]
    
    def test_bin_cal_quarter_to_annually(self, date_nov_1_23, date_nov_1_25):
        bin_cal_quarter_to_annually_output = [
            (datetime.date(2023, 11, 1), datetime.date(2024, 10, 31)),
            (datetime.date(2024, 11, 1), datetime.date(2025, 10, 31))
        ]
        per = Period()
        orig_bins = per.get_dates(date_nov_1_23, date_nov_1_25, "Calendar Quarter", inclusive=False)
        bins = per.convert_dates(orig_bins, "Annually")
        for index, b in enumerate(bins):
            assert b == bin_cal_quarter_to_annually_output[index]

    # Data Conversion Tests
    def test_data_cal_month_to_cal_month(self, date_jan_1_23, date_mar_31_23, data_3_cal_months):
        cal_month_to_cal_month_output = OrderedDict(
            [((datetime.date(2023, 1, 1), datetime.date(2023, 1, 31)),
               Decimal('1550')),
             ((datetime.date(2023, 2, 1), datetime.date(2023, 2, 28)),
               Decimal('2100')),
             ((datetime.date(2023, 3, 1), datetime.date(2023, 3, 31)),
               Decimal('3100'))]
        )
        per = Period()
        orig_bins = per.get_dates(date_jan_1_23, date_mar_31_23, "Calendar Month", inclusive=True)
        new_data = per.redistribute_data(data_3_cal_months, orig_bins, "Calendar Month")
        assert new_data == cal_month_to_cal_month_output
    
    def test_data_cal_month_to_cal_quarter(self, date_jan_1_23, date_mar_31_23, data_3_cal_months):
        cal_month_to_cal_quarter_output = OrderedDict(
            [((datetime.date(2023, 1, 1), datetime.date(2023, 3, 31)),
               Decimal('6750'))]
        )
        per = Period()
        orig_bins = per.get_dates(date_jan_1_23, date_mar_31_23, "Calendar Month", inclusive=True)
        new_data = per.redistribute_data(data_3_cal_months, orig_bins, "Calendar Quarter")
        assert new_data == cal_month_to_cal_quarter_output
    
    def test_data_cal_month_to_iso_week(self, date_jan_1_23, date_mar_31_23, data_3_cal_months):
        cal_month_to_iso_week_output = OrderedDict(
            [((datetime.date(2023, 1, 1), datetime.date(2023, 1, 1)),
               Decimal('50')),
             ((datetime.date(2023, 1, 2), datetime.date(2023, 1, 8)),
               Decimal('350')),
             ((datetime.date(2023, 1, 9), datetime.date(2023, 1, 15)),
               Decimal('350')),
             ((datetime.date(2023, 1, 16), datetime.date(2023, 1, 22)),
               Decimal('350')),
             ((datetime.date(2023, 1, 23), datetime.date(2023, 1, 29)),
               Decimal('350')),
             ((datetime.date(2023, 1, 30), datetime.date(2023, 2, 5)),
               Decimal('475')),
             ((datetime.date(2023, 2, 6), datetime.date(2023, 2, 12)),
               Decimal('525')),
             ((datetime.date(2023, 2, 13), datetime.date(2023, 2, 19)),
               Decimal('525')),
             ((datetime.date(2023, 2, 20), datetime.date(2023, 2, 26)),
               Decimal('525')),
             ((datetime.date(2023, 2, 27), datetime.date(2023, 3, 5)),
               Decimal('650')),
             ((datetime.date(2023, 3, 6), datetime.date(2023, 3, 12)),
               Decimal('700')),
             ((datetime.date(2023, 3, 13), datetime.date(2023, 3, 19)),
               Decimal('700')),
             ((datetime.date(2023, 3, 20), datetime.date(2023, 3, 26)),
               Decimal('700')),
             ((datetime.date(2023, 3, 27), datetime.date(2023, 3, 31)),
               Decimal('500'))])
        per = Period()
        orig_bins = per.get_dates(date_jan_1_23, date_mar_31_23, "Calendar Month", inclusive=True)
        new_data = per.redistribute_data(data_3_cal_months, orig_bins, "ISO Week")
        assert new_data == cal_month_to_iso_week_output
