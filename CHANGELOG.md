# CHANGELOG


## v0.2.0 (2024-10-29)

### Chores

* chore: fix linting errors ([`f308ccc`](https://github.com/agritheory/forecast/commit/f308ccc1d200b468ed103ee3fbac41b78572c9cf))

* chore: restructure directory so date binning in forecast app folder ([`0ad9cef`](https://github.com/agritheory/forecast/commit/0ad9cefce75a948a36d7b0102dc5ecc8666efe4b))

* chore: black formatting ([`49dcc01`](https://github.com/agritheory/forecast/commit/49dcc014444bc804eae1f3889e270d69292beb46))

* chore: ignore .python-version ([`b7ace56`](https://github.com/agritheory/forecast/commit/b7ace56f434bd88791003021b2f7c25ae0fc8ff1))

* chore: black formatting ([`2be78c3`](https://github.com/agritheory/forecast/commit/2be78c3ebac7337dbb597b516730ed7fcde0baf1))

* chore: fix flake8 errors ([`344c292`](https://github.com/agritheory/forecast/commit/344c292379794b3471e2253c803252cc770ba132))

* chore: add copyright, fix typing ([`f1c972f`](https://github.com/agritheory/forecast/commit/f1c972f5485f79920d6dea54c9b7a003be69b1ae))

* chore: remove date binning testing notebook (moved to pytests) ([`2059caa`](https://github.com/agritheory/forecast/commit/2059caa5726218da726e1c1acf129b069110667b))

* chore: remove html docs ([`ebd30cb`](https://github.com/agritheory/forecast/commit/ebd30cba48808cc7dc8cf8783d406770918852d5))

* chore: rename notebook for clarity ([`e663f62`](https://github.com/agritheory/forecast/commit/e663f6217497b9929028821caeee5451844ef283))

* chore: bump pytest version to avoid attribute error ([`d74e8ef`](https://github.com/agritheory/forecast/commit/d74e8ef97d1e58b2f4bdc4a7bdf361df3b2c9722))

* chore: remove .python-version as tracked file ([`a2cdba4`](https://github.com/agritheory/forecast/commit/a2cdba4756161f51b047b74212154bf01907bbd1))

### Continuous Integration

* ci: add python 3.12, use for linting ([`1890d7b`](https://github.com/agritheory/forecast/commit/1890d7bfb5227c874d7ee949365a3c791e68d418))

* ci: expand permissions for coverage comment ([`672b634`](https://github.com/agritheory/forecast/commit/672b6348609a9931ebc236f778cab47da0eea3dd))

* ci: remove unsupported redirection chars from tox commands ([`924e4a7`](https://github.com/agritheory/forecast/commit/924e4a73d99afdfa1eaf3a6168a1e52fa098d882))

* ci: change pipe to > ([`f73b7f2`](https://github.com/agritheory/forecast/commit/f73b7f2107f13b0fa869b9dc269938dbff2da46d))

* ci: update pytest cov command ([`a6d32f8`](https://github.com/agritheory/forecast/commit/a6d32f89b7cc7938ba967a18b291d3c4a4b0ae49))

* ci: check for coverage file before running comment step ([`730702b`](https://github.com/agritheory/forecast/commit/730702bb4534f740f197883e362ca9022fb6e2ba))

* ci: rename workflow ([`c33096e`](https://github.com/agritheory/forecast/commit/c33096eea8e2a59ec6b8f8f2a9f2d9fd816b7a52))

* ci: add pytest coverage ([`e3be4c9`](https://github.com/agritheory/forecast/commit/e3be4c97622c3807543dcd16e769f6d0b662b288))

* ci: add python 3.11 to ci ([`b98f425`](https://github.com/agritheory/forecast/commit/b98f4250459f192ce656031bdc684b6abb9c8998))

* ci: install poetry, add black linting ([`807808a`](https://github.com/agritheory/forecast/commit/807808ad0a88d89a2063682ec6cf23d61e190a2f))

* ci: add black options ([`526e006`](https://github.com/agritheory/forecast/commit/526e006af2ecd88fc676fc59fde1a2a2af560c41))

* ci: add tox for tests, linting, python semantic release ([`7b3dbd0`](https://github.com/agritheory/forecast/commit/7b3dbd0bd7a358218b711c0b290e2daa4e3242cf))

* ci: add linting config ([`5958e6d`](https://github.com/agritheory/forecast/commit/5958e6d398a9ca2be379ed7bfa1464f794ae118c))

* ci: add pre-commit ([`2ff893d`](https://github.com/agritheory/forecast/commit/2ff893dfdf6d032d468575e563583df8f333ec25))

* ci: add pre-commit and formatting config ([`86ca718`](https://github.com/agritheory/forecast/commit/86ca7181e2943e0f65c13a0db8b94e43172aea2a))

* ci: don't bother moving files ([`4da25c5`](https://github.com/agritheory/forecast/commit/4da25c5cdfe4e4966d050576ee282bbf090fa28c))

* ci: more debug statements ([`6317b65`](https://github.com/agritheory/forecast/commit/6317b65ba1217676a51cfbbafc8ad56a87aefe7e))

* ci: add debug statement ([`73013ef`](https://github.com/agritheory/forecast/commit/73013ef37eef48a735c0de714dd763c278cb08b4))

* ci: mkdir with parent directories ([`16679ac`](https://github.com/agritheory/forecast/commit/16679ac5cbcab0b8c6e9788ed3e19ab87577449e))

* ci: create folder ([`42e2242`](https://github.com/agritheory/forecast/commit/42e224271cc27f85e9de69ab3ea18321143a7a00))

* ci: add debug ls ([`8f87c7d`](https://github.com/agritheory/forecast/commit/8f87c7dfa3c2853fdb566e8da1db719724f53246))

* ci: copy instead of move ([`92450e7`](https://github.com/agritheory/forecast/commit/92450e7b24bc8d825796a54952a9558727e1730d))

* ci: select all files ([`41fc915`](https://github.com/agritheory/forecast/commit/41fc91561f7300dedf3725fa2a7032c1f38f53d2))

* ci: move png files ([`c0fb036`](https://github.com/agritheory/forecast/commit/c0fb03653e9364a4a46daa159606c7a46f58597f))

* ci: remove comma ([`87089f3`](https://github.com/agritheory/forecast/commit/87089f3f1232a9ec3d58ad0da3ba848e1ab7fb20))

* ci: export pngs too ([`c80e068`](https://github.com/agritheory/forecast/commit/c80e0685d7f2fe88fefdd8978683e7ad426dca2b))

* ci: embed images ([`f466c8a`](https://github.com/agritheory/forecast/commit/f466c8ac9b03c4a67df4dc0c40ce1e4270c1ae03))

* ci: export md, not html ([`d1cfb75`](https://github.com/agritheory/forecast/commit/d1cfb75d19fa194224f2d6630698f4aa8ecb5a19))

* ci: update branch ([`7e98298`](https://github.com/agritheory/forecast/commit/7e9829880e66000d8442302de751805805f64c63))

* ci: add output-dir to nbconvert ([`658ad91`](https://github.com/agritheory/forecast/commit/658ad917f5563a906fa5f805269f70520d993e27))

* ci: fix flag typo ([`5a76395`](https://github.com/agritheory/forecast/commit/5a76395ab19e76a8129ca1f76c82870423a41f15))

* ci: add notebook conversion workflow ([`2f602de`](https://github.com/agritheory/forecast/commit/2f602de3e93a1b1bf6512e00f9e84927594dea91))

### Documentation

* docs: Automatic commit of updated Jupyter notebook ([`76b4c29`](https://github.com/agritheory/forecast/commit/76b4c29a390e9ef56aa85e62f08cc7f7831f4d92))

* docs: Automatic commit of updated Jupyter notebook ([`d02d832`](https://github.com/agritheory/forecast/commit/d02d832a0d2fe9555f5a22024d7385c7bf006e3a))

* docs: Automatic commit of updated Jupyter notebook ([`90ec3a0`](https://github.com/agritheory/forecast/commit/90ec3a045ef1295712b62fe451f4c2e6d83f23b0))

* docs: Automatic commit of updated Jupyter notebook conversions ([`0498ddb`](https://github.com/agritheory/forecast/commit/0498ddba014b170e589024d052a605086f366f78))

* docs: export to markdown instead of HTML ([`86001fc`](https://github.com/agritheory/forecast/commit/86001fccd968ca94c6dbebaddc47b94049ae1e6f))

* docs: Automatic commit of updated Jupyter notebook conversions ([`b4b6506`](https://github.com/agritheory/forecast/commit/b4b650666c9b86f1c0c2f5c2f9c726da52f329f0))

### Features

* feat: remove stub for cal month, quarter, inclusive end date is default ([`476517e`](https://github.com/agritheory/forecast/commit/476517e29fcde2039476586da2379435a3b6b377))

* feat: update for custom days, labels ([`5453196`](https://github.com/agritheory/forecast/commit/5453196ce972a0c6e167bc54bf2594053f58789b))

### Testing

* test: add tests for full coverage ([`ed1a65c`](https://github.com/agritheory/forecast/commit/ed1a65c6ee227b43f0e4ec83f422d22c148d03dc))

* test: add custom date format for labels using start date test ([`4cfc0de`](https://github.com/agritheory/forecast/commit/4cfc0de1b5fbad635f2a6680d805e855f3fc2ae3))

* test: update for weekly, biweekly change, add labels ([`b242e33`](https://github.com/agritheory/forecast/commit/b242e330da31422174b030b792c974bbaf2382f0))

### Unknown

* Merge pull request #9 from agritheory/date_binning

feat: add date binning functionality ([`7e6b6bb`](https://github.com/agritheory/forecast/commit/7e6b6bbe60b2989436393637c46c53497c8927e3))

* Merge branch 'main' into date_binning ([`a57b14f`](https://github.com/agritheory/forecast/commit/a57b14f329dbca685252fd0588a562cf604c6ca1))

* Merge pull request #14 from agritheory/tox_ci

ci: lint and test with tox, add py sem release ([`416b836`](https://github.com/agritheory/forecast/commit/416b83608188e87e28d09f53cf118b4ce7e51ebe))

* Merge branch 'main' into tox_ci ([`087ea69`](https://github.com/agritheory/forecast/commit/087ea6932c12cff121a11dca53196309212ef753))

* Merge branch 'main' into tox_ci ([`b0160de`](https://github.com/agritheory/forecast/commit/b0160deb9bbadfdd99ecc560e56e41646d3e7846))

* Merge branch 'main' into date_binning ([`3387eb0`](https://github.com/agritheory/forecast/commit/3387eb0906fb52a2b119fc7710157c41fa9cf3a4))

* Merge pull request #17 from agritheory/export_to_markdown

ci: export md, not html ([`061f009`](https://github.com/agritheory/forecast/commit/061f009aa9bc739ea990548a5d6f9797e99b13fd))

* Merge pull request #16 from agritheory/export_to_markdown

CI: rename job ([`9f7ded0`](https://github.com/agritheory/forecast/commit/9f7ded0e91b061664ba944e740145d7db506e563))

* CI: rename job ([`84119c7`](https://github.com/agritheory/forecast/commit/84119c7e8e35b0a18dd963b0d8eedd5dde64fe83))

* Merge pull request #15 from agritheory/export_to_markdown

docs: export to markdown instead of HTML ([`5e0ae51`](https://github.com/agritheory/forecast/commit/5e0ae5171c1cf9257d7586098b39c119ac3c2594))

* Merge pull request #13 from agritheory/jupyter_to_html

ci: convert Jupyter notebooks to html ([`eafa949`](https://github.com/agritheory/forecast/commit/eafa9496357fb544c1b750cc11f4e9eb7073ef38))


## v0.1.0 (2024-08-09)

### Bug Fixes

* fix: update dependencies ([`def6f9a`](https://github.com/agritheory/forecast/commit/def6f9af7f4d4c4070d899c8db4d7f86913a64cd))

* fix: data length not always 12 in linear_smoothing and exponential_smoothing ([`64dcaa8`](https://github.com/agritheory/forecast/commit/64dcaa8f72e384696613dd41b200528761facad8))

### Build System

* build: add builds based on correct spelling ([`d173c30`](https://github.com/agritheory/forecast/commit/d173c300b648e520f66f11d982877766c15d5107))

### Chores

* chore: fix variable names ([`2dd27b3`](https://github.com/agritheory/forecast/commit/2dd27b35ca71127a137b5e0b6a4243d46ee11559))

* chore: spell approximation correctly ([`454d7a9`](https://github.com/agritheory/forecast/commit/454d7a9a2f4cd1247a2c527c62210186456d0755))

* chore: reduce python version and clean imports to support 3.6.1+ ([`38f9d91`](https://github.com/agritheory/forecast/commit/38f9d91ca54f07b7758d4f40fc7c99d6ba3c9541))

* chore: update project dependencies ([`a4ed0f7`](https://github.com/agritheory/forecast/commit/a4ed0f75c6de6f7ed1c04593b14ba0a2cf5b94bb))

### Features

* feat: class implementation and tests ([`9f73faf`](https://github.com/agritheory/forecast/commit/9f73faf01706cc9d4799b9f6bf14a2d4cbbd11e1))

* feat: add method 12 plots ([`a98971e`](https://github.com/agritheory/forecast/commit/a98971e10aee5e812ae3fc0279e550de3bb77e37))

* feat: add method 12 ([`31fbeae`](https://github.com/agritheory/forecast/commit/31fbeae2e76149f3022f1fd6778039e1f2a0f01c))

* feat: code clean-up for methods 6-11 ([`7ade79b`](https://github.com/agritheory/forecast/commit/7ade79b4cd6e47df0ca48120e72f90cf45659f7e))

* feat: code clean-up for methods 1-6 ([`e96ed9d`](https://github.com/agritheory/forecast/commit/e96ed9d3dfc253e0c7a5482af60e38377654427e))

* feat: start method 12 ([`85ed3c5`](https://github.com/agritheory/forecast/commit/85ed3c57857bbbf0d794a1768bc75504c9672ccb))

* feat: add method 11 exponential smoothing ([`a5fd0a2`](https://github.com/agritheory/forecast/commit/a5fd0a212dec3d0749fb08f14bc2862196915fae))

* feat: add method 10 linear smoothing ([`e9b884a`](https://github.com/agritheory/forecast/commit/e9b884a4ccda75612eba7aa44170b84e573bffda))

* feat: update to ignore Jupyter/Ipython notebook checkpoint files ([`b9ff7b6`](https://github.com/agritheory/forecast/commit/b9ff7b6378265049971b8aef37f0c769b421ad96))

* feat: add methods 7-9 2nd deg poly, flexible, and weighted moving avg ([`4d9226d`](https://github.com/agritheory/forecast/commit/4d9226db0c95d1ab7e50126498eac2858d78b4f0))

* feat: add method 6 least squares regression example ([`6994d78`](https://github.com/agritheory/forecast/commit/6994d78b18e52b770417428f7492cc41546cdf5c))

* feat: start forecast method calc example notebook ([`5105dcb`](https://github.com/agritheory/forecast/commit/5105dcb9e3256c25afcac8ac2db4cdff2aa68fd5))

### Testing

* test: fix test for zero data ([`c3755cb`](https://github.com/agritheory/forecast/commit/c3755cb88a8ea21262b866f11c0823b6fea5ecac))

### Unknown

* Merge pull request #11 from agritheory/fix-deps

fix: update dependencies ([`4b9f9ba`](https://github.com/agritheory/forecast/commit/4b9f9ba33b8368bb0e02002b1f76255c9fd5a130))

* tests: add pytest tests for Period ([`3d7aeb4`](https://github.com/agritheory/forecast/commit/3d7aeb4ab883107ff841d57c31d69fd65e69aa5c))

* wip: refactor Period class definition to module, import to notebook ([`2ad92e5`](https://github.com/agritheory/forecast/commit/2ad92e533d737d73f9c9b9780c1b8e1e4fe8a728))

* wip: add contextvars for week start day, refactor loops, error handling ([`95c3e44`](https://github.com/agritheory/forecast/commit/95c3e44323ec42107c1d2dc8c3bc001a5b3bd0fb))

* wip: add financial redistribution functionality ([`6446c15`](https://github.com/agritheory/forecast/commit/6446c15419c5e8895fc8f2521d18303a07d42d70))

* wip: add error handling, change default periodicity to ISO Weeks, make framework neutral ([`9cbc792`](https://github.com/agritheory/forecast/commit/9cbc792ada9940ef9948a65eff404de9b09dacfb))

* wip: add bin conversion functionality ([`0f09d55`](https://github.com/agritheory/forecast/commit/0f09d55656e27d871da03668539450f44646ddf8))

* wip: start of date binning functionality ([`e042695`](https://github.com/agritheory/forecast/commit/e042695e0dce3d2981cd34ba610d23c294af6262))

* Merge pull request #7 from agritheory/decimal_refactor

Decimal refactor ([`53dc149`](https://github.com/agritheory/forecast/commit/53dc149d80548d0c0a387f5cce78160651a1b3f0))

* Changed to use Decimal datatype. ([`5b88591`](https://github.com/agritheory/forecast/commit/5b88591772e1e30cd3ecf2c346b2386c1e9c13bc))

* Changed to use Decimal datatype. Removed use of numpy. ([`23e0720`](https://github.com/agritheory/forecast/commit/23e072002ae0bb0527d99224fa66e3ad180f98c8))

* feat/wip: add default value api for null data ([`fc4599f`](https://github.com/agritheory/forecast/commit/fc4599f659583bb0edd4da860b8e8e51c4777bd8))

* dist: add distpackages to repo ([`0841d8a`](https://github.com/agritheory/forecast/commit/0841d8a13beeba474eb9c8e5ae19e0fee9990cb7))

* Merge pull request #4 from agritheory/develop

Add Class implementation and tests ([`cb8b0dd`](https://github.com/agritheory/forecast/commit/cb8b0dd9974a0022b95c1739b8fd2a15847afce6))

* Merge pull request #1 from HKuz/main

Add notebook laying out forecast method calculations ([`a50c608`](https://github.com/agritheory/forecast/commit/a50c608b856e21b86ae2ee2bcd222653b59213d4))

* initial commit ([`4d1cd6f`](https://github.com/agritheory/forecast/commit/4d1cd6fc61ad77ac77b786292348a3df97ab56ce))
