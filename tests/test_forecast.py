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


def test_percent_over_previous_period(example_data):
	percent_over_previous_period_output = [
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
	fc = example_data.percent_over_previous_period(Decimal("10.0"))
	for index, period in enumerate(fc.forecast):
		assert period == percent_over_previous_period_output[index]


def test_previous_period_to_current_period(example_data):
	percent_over_previous_period_output = [
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
		assert period == percent_over_previous_period_output[index]


def test_calculated_percent_over_previous_period(example_data):
	calculated_percent_over_previous_period_output = [
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
		assert period == calculated_percent_over_previous_period_output[index]


def test_calculated_percent_over_previous_period_with_zeros(example_data_with_zeros):
	calculated_percent_over_previous_period_with_zeros_output = [
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
		assert period == calculated_percent_over_previous_period_with_zeros_output[index]


def test_moving_average(example_data):
	calculated_percent_over_previous_period_output = [
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
		assert abs(period - calculated_percent_over_previous_period_output[index]) < Decimal("1e-14")


def test_linear_approximation(example_data):
	linear_approximation_output = [
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
		assert abs(period - linear_approximation_output[index]) < Decimal("1e-15")


def test_least_squares_regression(example_data):
	least_squares_regression_output = [
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
		assert abs(period - least_squares_regression_output[index]) < Decimal("1e-13")


def test_second_degree_approximation(example_data):
	second_degree_approximation_output = [
		Decimal("132.181818181818385937731363810598850250244140625"),
		Decimal("132.63636363636391024556360207498073577880859375"),
		Decimal("133.044955044955344192203483544290065765380859375"),
		Decimal("133.407592407592773042779299430549144744873046875"),
		Decimal("133.72427572427613995387218892574310302734375"),
		Decimal("133.995004995005473347191582433879375457763671875"),
		Decimal("134.219780219780801644446910358965396881103515625"),
		Decimal("134.398601398602039580509881488978862762451171875"),
		Decimal("134.531468531469243998799356631934642791748046875"),
		Decimal("134.618381618382414899315335787832736968994140625"),
		Decimal("134.65934065934152386034838855266571044921875"),
		Decimal("134.654345654346656147026806138455867767333984375"),
	]
	fc = example_data.second_degree_approximation(12)
	for index, period in enumerate(fc.forecast):
		assert abs(period - second_degree_approximation_output[index]) < Decimal("1e-11")

	second_degree_approximation_output_2 = [
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
	fc = Forecast(data=input_data).second_degree_approximation(3)
	for index, period in enumerate(fc.forecast):
		assert abs(period - second_degree_approximation_output_2[index]) < Decimal("1e-11")


def test_flexible_method(example_data):
	flexible_method_output = [
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
	fc = example_data.flexible_method(Decimal("10.00"), 12)
	for index, period in enumerate(fc.forecast):
		assert abs(period - flexible_method_output[index]) < Decimal("1e-13")


def test_weighted_moving_average(example_data):
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
	weighted_moving_average_output = [
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
	fc = example_data.weighted_moving_average(12, weights)
	for index, period in enumerate(fc.forecast):
		assert abs(period - weighted_moving_average_output[index]) < Decimal("1e-13")


def test_linear_smoothing(example_data):
	linear_smoothing_output = [
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
	fc = example_data.linear_smoothing(12)
	for index, period in enumerate(fc.forecast):
		assert abs(period - linear_smoothing_output[index]) < Decimal("1e-13")


def test_exponential_smoothing(example_data):
	exponential_smoothing_output = [
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
	fc = example_data.exponential_smoothing(12, Decimal("0.3"))
	for index, period in enumerate(fc.forecast):
		assert abs(period - exponential_smoothing_output[index]) < Decimal("1e-13")


def test_exponential_smoothing_with_trend_and_seasonality(example_data):
	exponential_smoothing__with_trend_and_seasonality_output = [
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
	fc = example_data.exponential_smoothing_with_trend_and_seasonality(Decimal(0.3), Decimal(0.4))
	for index, period in enumerate(fc.forecast):
		assert abs(period - exponential_smoothing__with_trend_and_seasonality_output[index]) < Decimal(
			"1e-13"
		)


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


# Error testing
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

	# Test provided seasonality data different length than recent provided data
	with pytest.raises(Exception):
		s = [Decimal(1), Decimal(0.995), Decimal(1.005)]
		fc = example_data.exponential_smoothing_with_trend_and_seasonality(alpha, beta, seasonality=s)

	# Test provided seasonality factors aren't centered around (average) 1
	with pytest.raises(Exception):
		s = [Decimal(1), Decimal(2), Decimal(1)]
		fc = example_data.exponential_smoothing_with_trend_and_seasonality(alpha, beta, seasonality=s)


def test_seasonality_errors():
	# Test no data provided
	with pytest.raises(Exception):
		s = calculate_seasonality_factors([[], [Decimal(1)]])

	# Test non-Decimal data
	with pytest.raises(TypeError):
		s = calculate_seasonality_factors([[1, Decimal(2)]])

	# Test data of unequal lengths (different number of periods)
	with pytest.raises(Exception):
		d = [
			[Decimal(1), Decimal(2), Decimal(3)],
			[Decimal(0), Decimal(2)],
		]
		s = calculate_seasonality_factors(d)
