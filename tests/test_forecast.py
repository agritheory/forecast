from decimal import Decimal

import pytest

from forecast import Forecast, calculate_seasonality_factors


@pytest.fixture
def example_data():
	return Forecast(
		data=[
			[
				Decimal("128"),
				Decimal("117"),
				Decimal("115"),
				Decimal("125"),
				Decimal("122"),
				Decimal("137"),
				Decimal("140"),
				Decimal("129"),
				Decimal("131"),
				Decimal("114"),
				Decimal("119"),
				Decimal("137"),
			],
			[
				Decimal("125"),
				Decimal("123"),
				Decimal("115"),
				Decimal("137"),
				Decimal("122"),
				Decimal("130"),
				Decimal("141"),
				Decimal("128"),
				Decimal("118"),
				Decimal("123"),
				Decimal("139"),
				Decimal("133"),
			],
		]
	)


@pytest.fixture
def example_data_with_zeros():
	return Forecast(
		data=[
			[
				Decimal("128"),
				Decimal("117"),
				Decimal("115"),
				Decimal("125"),
				Decimal("122"),
				Decimal("137"),
				Decimal("140"),
				Decimal("129"),
				Decimal("131"),
				Decimal("114"),
				Decimal("119"),
				Decimal("137"),
			],
			[
				Decimal("125"),
				Decimal("123"),
				Decimal("115"),
				Decimal("137"),
				Decimal("122"),
				Decimal("130"),
				Decimal("141"),
				Decimal("128"),
				Decimal("118"),
				Decimal("123"),
				Decimal("0"),
				Decimal("0"),
			],
		]
	)


@pytest.fixture
def example_data_short():
	return Forecast(
		data=[
			[
				Decimal("90"),
				Decimal("100"),
				Decimal("110"),
				Decimal("90"),
			],
			[
				Decimal("100"),
				Decimal("105"),
				Decimal("120"),
				Decimal("90"),
			],
		]
	)


def test_percent_over_previous_period(example_data, example_data_short):
	percent = Decimal("10.00")
	output = [
		Decimal("137.5"),
		Decimal("135.3"),
		Decimal("126.5"),
		Decimal("150.7"),
		Decimal("134.2"),
		Decimal("143.0"),
		Decimal("155.1"),
		Decimal("140.8"),
		Decimal("129.8"),
		Decimal("135.3"),
		Decimal("152.9"),
		Decimal("146.3"),
	]
	fc = example_data.percent_over_previous_period(percent=percent)
	for index, period in enumerate(fc.forecast):
		assert period == output[index]

	n_output = [
		Decimal("110"),
		Decimal("115.5"),
		Decimal("132"),
		Decimal("99"),
		Decimal("110"),
		Decimal("115.5"),
	]

	fc = example_data_short.percent_over_previous_period(percent=percent, n=6)
	for index, period in enumerate(fc.forecast):
		assert period == n_output[index]


def test_previous_period_to_current_period(example_data, example_data_short):
	output = [
		Decimal("125"),
		Decimal("123"),
		Decimal("115"),
		Decimal("137"),
		Decimal("122"),
		Decimal("130"),
		Decimal("141"),
		Decimal("128"),
		Decimal("118"),
		Decimal("123"),
		Decimal("139"),
		Decimal("133"),
	]
	fc = example_data.previous_period_to_current_period()
	for index, period in enumerate(fc.forecast):
		assert period == output[index]

	n_output = [
		Decimal("100"),
		Decimal("105"),
		Decimal("120"),
		Decimal("90"),
		Decimal("100"),
		Decimal("105"),
	]

	fc = example_data_short.previous_period_to_current_period(n=6)
	for index, period in enumerate(fc.forecast):
		assert period == n_output[index]


def test_calculated_percent_over_previous_period(example_data, example_data_short):
	output = [
		Decimal("126.6512549537648612945838838"),
		Decimal("124.6248348745046235138705416"),
		Decimal("116.5191545574636723910171730"),
		Decimal("138.8097754293262879788639366"),
		Decimal("123.6116248348745046235138705"),
		Decimal("131.7173051519154557463672391"),
		Decimal("142.8626155878467635402906209"),
		Decimal("129.6908850726552179656538970"),
		Decimal("119.5587846763540290620871863"),
		Decimal("124.6248348745046235138705416"),
		Decimal("140.8361955085865257595772787"),
		Decimal("134.7569352708058124174372523"),
	]
	fc = example_data.calculated_percent_over_previous_period()
	for index, period in enumerate(fc.forecast):
		assert period == output[index]

	n_output = [
		Decimal("105"),
		Decimal("110.25"),
		Decimal("126"),
		Decimal("94.5"),
		Decimal("105"),
		Decimal("110.25"),
	]

	fc = example_data_short.calculated_percent_over_previous_period(periods=2, n=6)
	for index, period in enumerate(fc.forecast):
		assert period == n_output[index]


def test_calculated_percent_over_previous_period_with_zeros(example_data_with_zeros):
	output = [
		Decimal("104.1941875825627476882430647"),
		Decimal("102.5270805812417437252311757"),
		Decimal("95.85865257595772787318361955"),
		Decimal("114.1968295904887714663143989"),
		Decimal("101.6935270805812417437252312"),
		Decimal("108.3619550858652575957727873"),
		Decimal("117.5310435931307793923381770"),
		Decimal("106.6948480845442536327608983"),
		Decimal("98.35931307793923381770145310"),
		Decimal("102.5270805812417437252311757"),
		Decimal("0E-28"),
		Decimal("0E-28"),
	]
	fc = example_data_with_zeros.calculated_percent_over_previous_period()
	for index, period in enumerate(fc.forecast):
		assert period == output[index]


def test_moving_average(example_data, example_data_short):
	output = [
		Decimal("127.8333333333333285963817615993320941925048828125"),
		Decimal("128.0694444444444440496984802"),
		Decimal("128.4918981481481477205066868"),
		Decimal("129.6162229938271600305489108"),
		Decimal("129.000908243312756699761320"),
		Decimal("129.5843172635888197580747633"),
		Decimal("129.5496770355545547379143269"),
		Decimal("128.5954834551841009660738542"),
		Decimal("128.6451070764494427132466752"),
		Decimal("129.5321993328202296060172315"),
		Decimal("130.0765492772219154065186675"),
		Decimal("129.3329283836570750237285565"),
	]
	fc = example_data.moving_average(12)
	for index, period in enumerate(fc.forecast):
		assert abs(period - output[index]) < Decimal("1e-13")

	n_output = [
		Decimal("105"),
		Decimal("97.5"),
		Decimal("101.25"),
		Decimal("99.375"),
		Decimal("100.3125"),
		Decimal("99.84375"),
	]

	fc = example_data_short.moving_average(periods=2, n=6)
	for index, period in enumerate(fc.forecast):
		assert period == n_output[index]


def test_linear_approximation(example_data, example_data_short):
	output = [
		Decimal("138"),
		Decimal("143"),
		Decimal("148"),
		Decimal("153"),
		Decimal("158"),
		Decimal("163"),
		Decimal("168"),
		Decimal("173"),
		Decimal("178"),
		Decimal("183"),
		Decimal("188"),
		Decimal("193"),
	]
	fc = example_data.linear_approximation(3)
	for index, period in enumerate(fc.forecast):
		assert abs(period - output[index]) < Decimal("1e-13")

	n_output = [
		Decimal("82.5"),
		Decimal("75.0"),
		Decimal("67.5"),
		Decimal("60.0"),
		Decimal("52.5"),
		Decimal("45.0"),
	]

	fc = example_data_short.linear_approximation(periods=2, n=6)
	for index, period in enumerate(fc.forecast):
		assert period == n_output[index]


def test_least_squares_regression(example_data, example_data_short):
	output = [
		Decimal("132.8787878787878753428230993449687957763671875"),
		Decimal("133.6550116550116626967792399227619171142578125"),
		Decimal("134.431235431235421629025950096547603607177734375"),
		Decimal("135.207459207459208982982090674340724945068359375"),
		Decimal("135.98368298368296791522880084812641143798828125"),
		Decimal("136.75990675990675526918494142591953277587890625"),
		Decimal("137.53613053613054262314108200371265411376953125"),
		Decimal("138.312354312354301555387792177498340606689453125"),
		Decimal("139.088578088578088909343932755291461944580078125"),
		Decimal("139.8648018648018478415906429290771484375"),
		Decimal("140.641025641025635195546783506870269775390625"),
		Decimal("141.41724941724942254950292408466339111328125"),
	]
	fc = example_data.least_squares_regression(12)
	for index, period in enumerate(fc.forecast):
		assert abs(period - output[index]) < Decimal("1e-13")

	n_output = [
		Decimal("90.0"),
		Decimal("82.5"),
		Decimal("75.0"),
		Decimal("67.5"),
		Decimal("60.0"),
		Decimal("52.5"),
	]

	fc = example_data_short.least_squares_regression(periods=3, n=6)
	for index, period in enumerate(fc.forecast):
		assert period == n_output[index]


def test_second_degree_approximation(example_data, example_data_short):
	output = [
		Decimal("132.1818181818181818181818183"),
		Decimal("132.6363636363636363636363638"),
		Decimal("133.0449550449550449550449552"),
		Decimal("133.4075924075924075924075927"),
		Decimal("133.7242757242757242757242760"),
		Decimal("133.9950049950049950049950054"),
		Decimal("134.2197802197802197802197806"),
		Decimal("134.3986013986013986013986020"),
		Decimal("134.5314685314685314685314692"),
		Decimal("134.6183816183816183816183823"),
		Decimal("134.6593406593406593406593415"),
		Decimal("134.6543456543456543456543465"),
	]
	fc = example_data.second_degree_approximation(periods=12)
	for index, period in enumerate(fc.forecast):
		assert abs(period - output[index]) < Decimal("1e-13")

	output_2 = [
		Decimal("294.0000000000000000000000047"),
		Decimal("172.0000000000000000000000116"),
		Decimal("4.0000000000000000000000216"),
	]
	input_data = [
		[
			Decimal("384"),
			Decimal("400"),
			Decimal("370"),
		]
	]
	fc = Forecast(data=input_data).second_degree_approximation(periods=3)
	for index, period in enumerate(fc.forecast):
		assert abs(period - output_2[index]) < Decimal("1e-13")

	n_output = [
		Decimal("97.00000000000000000000000017"),
		Decimal("92.57142857142857142857142901"),
		Decimal("87.07142857142857142857142923"),
		Decimal("80.50000000000000000000000103"),
		Decimal("72.85714285714285714285714422"),
		Decimal("64.14285714285714285714285899"),
	]

	fc = example_data_short.second_degree_approximation(periods=6, n=6)
	for index, period in enumerate(fc.forecast):
		assert abs(period - n_output[index]) < Decimal("1e-13")


def test_flexible_method(example_data, example_data_short):
	percent = Decimal("10.00")
	output = [
		Decimal("137.5000000000000111022302463"),
		Decimal("135.3000000000000109245945623"),
		Decimal("126.5000000000000102140518266"),
		Decimal("150.7000000000000121680443499"),
		Decimal("134.2000000000000108357767203"),
		Decimal("143.0000000000000115463194561"),
		Decimal("155.1000000000000125233157178"),
		Decimal("140.8000000000000113686837722"),
		Decimal("129.8000000000000104805053525"),
		Decimal("135.3000000000000109245945623"),
		Decimal("152.9000000000000123456800338"),
		Decimal("146.3000000000000118127729820"),
	]
	fc = example_data.flexible_method(percent=percent, periods=12)
	for index, period in enumerate(fc.forecast):
		assert abs(period - output[index]) < Decimal("1e-13")

	n_output = [
		Decimal("99.0"),
		Decimal("108.90"),
		Decimal("119.790"),
		Decimal("131.7690"),
		Decimal("144.94590"),
		Decimal("159.440490"),
	]

	fc = example_data_short.flexible_method(percent=percent, periods=1, n=6)
	for index, period in enumerate(fc.forecast):
		assert abs(period - n_output[index]) < Decimal("1e-13")


def test_weighted_moving_average(example_data, example_data_short):
	weights = [
		Decimal("0.03"),
		Decimal("0.03"),
		Decimal("0.04"),
		Decimal("0.05"),
		Decimal("0.05"),
		Decimal("0.05"),
		Decimal("0.10"),
		Decimal("0.10"),
		Decimal("0.10"),
		Decimal("0.15"),
		Decimal("0.15"),
		Decimal("0.15"),
	]
	output = [
		Decimal("129.43999999999999772626324556767940521240234375"),
		Decimal("129.385999999999995679900166578590869903564453125"),
		Decimal("129.16390000000001236912794411182403564453125"),
		Decimal("130.01848499999999830833985470235347747802734375"),
		Decimal("130.079257749999982252120389603078365325927734375"),
		Decimal("129.821846412499979805943439714610576629638671875"),
		Decimal("129.826928374375000885265762917697429656982421875"),
		Decimal("129.688043380531240700292983092367649078369140625"),
		Decimal("129.707987000110932740426505915820598602294921875"),
		Decimal("129.954897729502562242487329058349132537841796875"),
		Decimal("130.141461720209207442167098633944988250732421875"),
		Decimal("129.9160559217140189502970315515995025634765625"),
	]
	fc = example_data.weighted_moving_average(periods=12, weights=weights)
	for index, period in enumerate(fc.forecast):
		assert abs(period - output[index]) < Decimal("1e-13")

	n_weights = [
		Decimal("0.25"),
		Decimal("0.75"),
	]
	n_output = [
		Decimal("97.50"),
		Decimal("95.6250"),
		Decimal("96.093750"),
		Decimal("95.97656250"),
		Decimal("96.0058593750"),
		Decimal("95.998535156250"),
	]

	fc = example_data_short.weighted_moving_average(periods=2, weights=n_weights, n=6)
	for index, period in enumerate(fc.forecast):
		assert abs(period - n_output[index]) < Decimal("1e-13")


def test_linear_smoothing(example_data, example_data_short):
	output = [
		Decimal("129.256410256410248393876827321946620941162109375"),
		Decimal("129.47534516765284706707461737096309661865234375"),
		Decimal("129.673393010671105685105430893599987030029296875"),
		Decimal("129.81889250687612502588308416306972503662109375"),
		Decimal("129.798656117745082383407861925661563873291015625"),
		Decimal("129.86737191865955765024409629404544830322265625"),
		Decimal("129.846676610512901106631034053862094879150390625"),
		Decimal("129.82449776882236847086460329592227935791015625"),
		Decimal("129.94189812314726850672741420567035675048828125"),
		Decimal("130.05396907340900725102983415126800537109375"),
		Decimal("130.030180450337383035730454139411449432373046875"),
		Decimal("129.9122965381596941369934938848018646240234375"),
	]
	fc = example_data.linear_smoothing(periods=12)
	for index, period in enumerate(fc.forecast):
		assert abs(period - output[index]) < Decimal("1e-13")

	n_output = [
		Decimal("103.0"),
		Decimal("102.70"),
		Decimal("101.980"),
		Decimal("101.2020"),
		Decimal("101.91480"),
		Decimal("101.792520"),
	]

	fc = example_data_short.linear_smoothing(periods=4, n=6)
	for index, period in enumerate(fc.forecast):
		assert abs(period - n_output[index]) < Decimal("1e-13")


def test_exponential_smoothing(example_data, example_data_short):
	alpha = Decimal("0.3")
	output = [
		Decimal("130.520404130059972658273181878030300140380859375"),
		Decimal("130.520404130059972658273181878030300140380859375"),
		Decimal("130.520404130059972658273181878030300140380859375"),
		Decimal("130.520404130059972658273181878030300140380859375"),
		Decimal("130.520404130059972658273181878030300140380859375"),
		Decimal("130.520404130059972658273181878030300140380859375"),
		Decimal("130.520404130059972658273181878030300140380859375"),
		Decimal("130.520404130059972658273181878030300140380859375"),
		Decimal("130.520404130059972658273181878030300140380859375"),
		Decimal("130.520404130059972658273181878030300140380859375"),
		Decimal("130.520404130059972658273181878030300140380859375"),
		Decimal("130.520404130059972658273181878030300140380859375"),
	]
	fc = example_data.exponential_smoothing(periods=12, alpha=alpha)
	for index, period in enumerate(fc.forecast):
		assert abs(period - output[index]) < Decimal("1e-13")

	n_output = [
		Decimal("111.0"),
		Decimal("111.0"),
		Decimal("111.0"),
		Decimal("111.0"),
		Decimal("111.0"),
		Decimal("111.0"),
	]

	fc = example_data_short.exponential_smoothing(periods=2, alpha=alpha, n=6)
	for index, period in enumerate(fc.forecast):
		assert abs(period - n_output[index]) < Decimal("1e-13")


def test_exponential_smoothing_with_trend_and_seasonality(example_data, example_data_short):
	output = [
		Decimal("128.8400382301657645281364115"),
		Decimal("122.6708414308079670929446625"),
		Decimal("117.9918052604130600843835623"),
		Decimal("134.9004442921930858549136128"),
		Decimal("126.0910345281789885708767265"),
		Decimal("138.4784494121616627408695564"),
		Decimal("146.2675870854856559345304901"),
		Decimal("134.2579729329414964077694516"),
		Decimal("130.5466928275680732250305588"),
		Decimal("124.7006902345101966873732121"),
		Decimal("136.2349889762650722004090835"),
		Decimal("143.0789227005269950440901538"),
	]
	fc = example_data.exponential_smoothing_with_trend_and_seasonality(
		alpha=Decimal("0.3"), beta=Decimal("0.4")
	)
	for index, period in enumerate(fc.forecast):
		assert abs(period - output[index]) < Decimal("1e-13")

	seasonality = [
		Decimal("0.95"),
		Decimal("1.00"),
		Decimal("1.15"),
		Decimal("0.90"),
	]
	n_output = [
		Decimal("95"),
		Decimal("100"),
		Decimal("115"),
		Decimal("90"),
		Decimal("95"),
		Decimal("100"),
	]

	fc = example_data_short.exponential_smoothing_with_trend_and_seasonality(
		alpha=Decimal("1"), beta=Decimal("0"), seasonality=seasonality, n=6
	)
	for index, period in enumerate(fc.forecast):
		assert abs(period - n_output[index]) < Decimal("1e-13")


def test_seasonality(example_data):
	# Test correct output
	seasonality_output = [
		Decimal("0.9960629921259842519685039370"),
		Decimal("0.9448818897637795275590551181"),
		Decimal("0.9055118110236220472440944882"),
		Decimal("1.031496062992125984251968504"),
		Decimal("0.9606299212598425196850393701"),
		Decimal("1.051181102362204724409448819"),
		Decimal("1.106299212598425196850393701"),
		Decimal("1.011811023622047244094488189"),
		Decimal("0.9803149606299212598425196851"),
		Decimal("0.9330708661417322834645669291"),
		Decimal("1.015748031496062992125984252"),
		Decimal("1.062992125984251968503937008"),
	]
	data = example_data.data
	seasonality = calculate_seasonality_factors(data)
	for index, s in enumerate(seasonality):
		assert abs(s - seasonality_output[index]) < Decimal("1e-13")

	# Test if data has sequences of unequal length, seasonality is same length as shorter of two
	data = [
		[Decimal("95"), Decimal("105"), Decimal("90")],
		[Decimal("90"), Decimal("110")],
	]
	seasonality = calculate_seasonality_factors(data)
	assert len(seasonality) == 2
	assert abs(sum(seasonality) - 2) < Decimal("1e-13")


# Error testing
def test_no_data_provided_error():
	with pytest.raises(Exception):
		fc = Forecast().previous_period_to_current_period()


def test_non_decimal_data_error():
	with pytest.raises(TypeError):
		fc = Forecast(data=[[Decimal(1), Decimal(3), 5, Decimal(0)]])


def test_percent_over_previous_period_errors(example_data):
	# Test non-Decimal percent
	with pytest.raises(TypeError):
		fc = example_data.percent_over_previous_period(percent=10.0)


def test_calculated_percent_over_previous_period_errors(example_data):
	# Test only one period of historical data given (needs 2+)
	with pytest.raises(Exception):
		fc = Forecast(data=[[Decimal(2), Decimal(3)]]).calculated_percent_over_previous_period()

	# Test too many periods
	with pytest.raises(Exception):
		fc = example_data.calculated_percent_over_previous_period(periods=100)

	# Test warning if user gives different length provided data
	with pytest.warns(UserWarning):
		d = [[Decimal(1), Decimal(2), Decimal(3)], [Decimal(4), Decimal(5)]]
		fc = Forecast(data=d).calculated_percent_over_previous_period(periods=2)


def test_moving_average_errors(example_data):
	# Test too many periods
	with pytest.raises(Exception):
		fc = example_data.moving_average(periods=100)


def test_linear_approximation_errors(example_data):
	# Test too many periods
	with pytest.raises(Exception):
		fc = example_data.linear_approximation(periods=100)


def test_least_squares_regression_errors(example_data):
	# Test too many periods
	with pytest.raises(Exception):
		fc = example_data.least_squares_regression(periods=100)


def test_second_degree_approximation_errors(example_data):
	# Test too many periods
	with pytest.raises(Exception):
		fc = example_data.second_degree_approximation(periods=100)


def test_flexible_method_errors(example_data):
	# Test non-Decimal percent
	with pytest.raises(TypeError):
		fc = example_data.flexible_method(percent=10.0, periods=2)

	# Test too many periods
	with pytest.raises(Exception):
		fc = example_data.flexible_method(percent=Decimal(10.0), periods=100)


def test_weighted_moving_average_errors(example_data):
	# Test non-Decimal weights
	with pytest.raises(TypeError):
		fc = example_data.weighted_moving_average(periods=2, weights=[0.5, 0.5])

	# Test too many periods
	with pytest.raises(Exception):
		fc = example_data.weighted_moving_average(periods=100, weights=[Decimal(0.5), Decimal(0.5)])

	# Weights don't add to 1
	with pytest.raises(Exception):
		weights = [Decimal(0.3), Decimal(0.8)]
		fc = example_data.weighted_moving_average(periods=len(weights), weights=weights)

	# Number of periods doesn't match the number of weights
	with pytest.raises(Exception):
		weights = [Decimal(0.3), Decimal(0.7)]
		fc = example_data.weighted_moving_average(periods=3, weights=weights)


def test_linear_smoothing_errors(example_data):
	# Test too many periods
	with pytest.raises(Exception):
		fc = example_data.linear_smoothing(periods=100)


def test_exponential_smoothing_errors(example_data):
	# Test non-Decimal alpha value
	with pytest.raises(TypeError):
		fc = example_data.exponential_smoothing(periods=4, alpha=0.3)

	# Test invalid alpha value
	with pytest.raises(Exception):
		fc = example_data.exponential_smoothing(periods=4, alpha=Decimal(1.2))

	# Test too many periods
	with pytest.raises(Exception):
		fc = example_data.exponential_smoothing(periods=100, alpha=Decimal(0.3))


def test_exponential_smoothing_with_trend_and_seasonality_errors(example_data):
	alpha = Decimal(0.3)
	beta = Decimal(0.4)
	invalid_value = Decimal(1.2)

	# Test non-Decimal alpha value
	with pytest.raises(TypeError):
		fc = example_data.exponential_smoothing_with_trend_and_seasonality(alpha=0.3, beta=beta)

	# Test invalid alpha value
	with pytest.raises(Exception):
		fc = example_data.exponential_smoothing_with_trend_and_seasonality(
			alpha=invalid_value, beta=beta
		)

	# Test non-Decimal beta value
	with pytest.raises(TypeError):
		fc = example_data.exponential_smoothing_with_trend_and_seasonality(alpha, 0.4)

	# Test invalid beta value
	with pytest.raises(Exception):
		fc = example_data.exponential_smoothing_with_trend_and_seasonality(
			alpha=alpha, beta=invalid_value
		)

	# Test non-Decimal seasonality value
	with pytest.raises(TypeError):
		s = [0.995, 0.982, 1.005, 1.028]
		fc = example_data.exponential_smoothing_with_trend_and_seasonality(alpha, beta, seasonality=s)


def test_seasonality_errors():
	# Test no data provided
	with pytest.raises(Exception):
		s = calculate_seasonality_factors([[], [Decimal("1")]])

	# Test non-Decimal data
	with pytest.raises(TypeError):
		s = calculate_seasonality_factors([[0.5, Decimal("0.5")]])
