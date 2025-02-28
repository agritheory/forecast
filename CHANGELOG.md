# CHANGELOG


## v0.5.0 (2025-02-28)

### Continuous Integration

- Add poetry pre-commands for tox envs
  ([`231b205`](https://github.com/agritheory/forecast/commit/231b205a133894b0986dfa7a2f92f9632c0a1a4f))

- Move jupyter dependencies to dev deps
  ([`0b52862`](https://github.com/agritheory/forecast/commit/0b52862114b5d7c0ec0d9939e2b2af4d7b9d2680))

- Update lock
  ([`8a07267`](https://github.com/agritheory/forecast/commit/8a07267734db07ed5ec3ea87e7e276ee1625f102))

- Update version_variables name to capture version in __init__
  ([`1794307`](https://github.com/agritheory/forecast/commit/17943074a9eff0b2b3fc35ddd8b44f42d9d1286d))

### Documentation

- Add notebook with date binning examples
  ([`0f51a07`](https://github.com/agritheory/forecast/commit/0f51a07a880a7a14f3cd5fbbf48a9103493a075d))

- Automatic commit of updated Jupyter notebook
  ([`092c0c6`](https://github.com/agritheory/forecast/commit/092c0c66b0effdc97650e775403e370988707433))

- Automatic commit of updated Jupyter notebook
  ([`36dbbf5`](https://github.com/agritheory/forecast/commit/36dbbf57e50b31d5957cf815806efd8a0e1ba4dd))

- Automatic commit of updated Jupyter notebook
  ([`b452250`](https://github.com/agritheory/forecast/commit/b4522503b17d60f102531843905bcd4871b9b422))

- Update for fiscal weeks periodicity
  ([`da7b19f`](https://github.com/agritheory/forecast/commit/da7b19f72a5e49f0621f83857c8934a6ef8ec892))

### Features

- Add fiscal years periodicity
  ([`5484cb4`](https://github.com/agritheory/forecast/commit/5484cb481badf2510ce5627c57d3e4ffb3a0920c))

- Change custom_period default to 1
  ([`435bc27`](https://github.com/agritheory/forecast/commit/435bc27802144b60e422275f0ac365b523a3a4b0))

### Refactoring

- Include number of weeks in ISO Month labels
  ([`2cbc996`](https://github.com/agritheory/forecast/commit/2cbc996f180508fb02ba63eb7929b80287b10d3c))

- Use ISO week patterns for non-standard periods
  ([`0443df7`](https://github.com/agritheory/forecast/commit/0443df7af952acee2ba51a3c8e9312751a45e85a))

### Testing

- Add fiscal weeks tests
  ([`2445095`](https://github.com/agritheory/forecast/commit/2445095d1b7fe5c8fdd5c68fe40536b6cc3a9f1e))

- Add ISO Month test W05 through 18 months
  ([`bd1aba5`](https://github.com/agritheory/forecast/commit/bd1aba57971d0a826ef2ac36846b365b2d24ae99))

- Update tests for new periodicities
  ([`d02f4cf`](https://github.com/agritheory/forecast/commit/d02f4cf8d9073fa5faeda5736f0f01a2add203aa))


## v0.4.0 (2024-11-13)

### Bug Fixes

- Sum in seasonality calc if different-length data
  ([`fa95df2`](https://github.com/agritheory/forecast/commit/fa95df213f880f3375debe91cdf8a24b583ec6eb))

### Features

- Add user-defined forecast period to all methods
  ([`d91adb2`](https://github.com/agritheory/forecast/commit/d91adb2e3554bd3072ec6bdc6f0f533b5c4a8941))

### Testing

- Add missing data test
  ([`bf85311`](https://github.com/agritheory/forecast/commit/bf853115620070b77ff487dd2870942165bcdb7c))


## v0.3.0 (2024-11-13)

### Documentation

- Add overall explanation, more detail for alpha/beta
  ([`e6e766b`](https://github.com/agritheory/forecast/commit/e6e766b209657347f6f5c9af425b487622915200))

- Automatic commit of updated Jupyter notebook
  ([`4a23ca0`](https://github.com/agritheory/forecast/commit/4a23ca07ffe727bdae0f9670a6b95311e84aba23))

- Forecast length and slicing if need less
  ([`9df41cc`](https://github.com/agritheory/forecast/commit/9df41ccaab1541ee95380421299f6c68d9c872bd))

- Update for user-provided number of forecast periods
  ([`70982f0`](https://github.com/agritheory/forecast/commit/70982f0bd5d2126898329b1b17c9525a1f078fe6))


## v0.2.0 (2024-10-29)

### Bug Fixes

- Wip to fix off by one errors, add docstrings, catch errors
  ([`ed6a739`](https://github.com/agritheory/forecast/commit/ed6a739bb925caf8f0202d8d885e8477786360c7))

### Chores

- Add copyright, fix typing
  ([`f1c972f`](https://github.com/agritheory/forecast/commit/f1c972f5485f79920d6dea54c9b7a003be69b1ae))

- Black formatting
  ([`49dcc01`](https://github.com/agritheory/forecast/commit/49dcc014444bc804eae1f3889e270d69292beb46))

- Black formatting
  ([`2be78c3`](https://github.com/agritheory/forecast/commit/2be78c3ebac7337dbb597b516730ed7fcde0baf1))

- Bump pytest version to avoid attribute error
  ([`d74e8ef`](https://github.com/agritheory/forecast/commit/d74e8ef97d1e58b2f4bdc4a7bdf361df3b2c9722))

- Fix flake8 errors
  ([`344c292`](https://github.com/agritheory/forecast/commit/344c292379794b3471e2253c803252cc770ba132))

- Fix linting errors
  ([`f308ccc`](https://github.com/agritheory/forecast/commit/f308ccc1d200b468ed103ee3fbac41b78572c9cf))

- Fix variable names
  ([`2dd27b3`](https://github.com/agritheory/forecast/commit/2dd27b35ca71127a137b5e0b6a4243d46ee11559))

- Ignore .python-version
  ([`b7ace56`](https://github.com/agritheory/forecast/commit/b7ace56f434bd88791003021b2f7c25ae0fc8ff1))

- Remove .python-version as tracked file
  ([`a2cdba4`](https://github.com/agritheory/forecast/commit/a2cdba4756161f51b047b74212154bf01907bbd1))

- Remove commented old error tests
  ([`179f8f1`](https://github.com/agritheory/forecast/commit/179f8f102a096e4bdf88970175da976a43537919))

- Remove date binning testing notebook (moved to pytests)
  ([`2059caa`](https://github.com/agritheory/forecast/commit/2059caa5726218da726e1c1acf129b069110667b))

- Remove html docs
  ([`ebd30cb`](https://github.com/agritheory/forecast/commit/ebd30cba48808cc7dc8cf8783d406770918852d5))

- Rename notebook for clarity
  ([`e663f62`](https://github.com/agritheory/forecast/commit/e663f6217497b9929028821caeee5451844ef283))

- Restructure directory so date binning in forecast app folder
  ([`0ad9cef`](https://github.com/agritheory/forecast/commit/0ad9cefce75a948a36d7b0102dc5ecc8666efe4b))

- Update pre-commit
  ([`6a38c3e`](https://github.com/agritheory/forecast/commit/6a38c3ed2a9da524771f40416db55f828d314444))

### Continuous Integration

- Add black options
  ([`526e006`](https://github.com/agritheory/forecast/commit/526e006af2ecd88fc676fc59fde1a2a2af560c41))

- Add debug ls
  ([`8f87c7d`](https://github.com/agritheory/forecast/commit/8f87c7dfa3c2853fdb566e8da1db719724f53246))

- Add debug statement
  ([`73013ef`](https://github.com/agritheory/forecast/commit/73013ef37eef48a735c0de714dd763c278cb08b4))

- Add linting config
  ([`5958e6d`](https://github.com/agritheory/forecast/commit/5958e6d398a9ca2be379ed7bfa1464f794ae118c))

- Add notebook conversion workflow
  ([`2f602de`](https://github.com/agritheory/forecast/commit/2f602de3e93a1b1bf6512e00f9e84927594dea91))

- Add output-dir to nbconvert
  ([`658ad91`](https://github.com/agritheory/forecast/commit/658ad917f5563a906fa5f805269f70520d993e27))

- Add pre-commit
  ([`2ff893d`](https://github.com/agritheory/forecast/commit/2ff893dfdf6d032d468575e563583df8f333ec25))

- Add pre-commit and formatting config
  ([`86ca718`](https://github.com/agritheory/forecast/commit/86ca7181e2943e0f65c13a0db8b94e43172aea2a))

- Add pytest coverage
  ([`e3be4c9`](https://github.com/agritheory/forecast/commit/e3be4c97622c3807543dcd16e769f6d0b662b288))

- Add python 3.11 to ci
  ([`b98f425`](https://github.com/agritheory/forecast/commit/b98f4250459f192ce656031bdc684b6abb9c8998))

- Add python 3.12, use for linting
  ([`1890d7b`](https://github.com/agritheory/forecast/commit/1890d7bfb5227c874d7ee949365a3c791e68d418))

- Add tox for tests, linting, python semantic release
  ([`7b3dbd0`](https://github.com/agritheory/forecast/commit/7b3dbd0bd7a358218b711c0b290e2daa4e3242cf))

- Change pipe to >
  ([`f73b7f2`](https://github.com/agritheory/forecast/commit/f73b7f2107f13b0fa869b9dc269938dbff2da46d))

- Check for coverage file before running comment step
  ([`730702b`](https://github.com/agritheory/forecast/commit/730702bb4534f740f197883e362ca9022fb6e2ba))

- Copy instead of move
  ([`92450e7`](https://github.com/agritheory/forecast/commit/92450e7b24bc8d825796a54952a9558727e1730d))

- Create folder
  ([`42e2242`](https://github.com/agritheory/forecast/commit/42e224271cc27f85e9de69ab3ea18321143a7a00))

- Don't bother moving files
  ([`4da25c5`](https://github.com/agritheory/forecast/commit/4da25c5cdfe4e4966d050576ee282bbf090fa28c))

- Embed images
  ([`f466c8a`](https://github.com/agritheory/forecast/commit/f466c8ac9b03c4a67df4dc0c40ce1e4270c1ae03))

- Expand permissions for coverage comment
  ([`672b634`](https://github.com/agritheory/forecast/commit/672b6348609a9931ebc236f778cab47da0eea3dd))

- Export md, not html
  ([`d1cfb75`](https://github.com/agritheory/forecast/commit/d1cfb75d19fa194224f2d6630698f4aa8ecb5a19))

- Export pngs too
  ([`c80e068`](https://github.com/agritheory/forecast/commit/c80e0685d7f2fe88fefdd8978683e7ad426dca2b))

- Fix flag typo
  ([`5a76395`](https://github.com/agritheory/forecast/commit/5a76395ab19e76a8129ca1f76c82870423a41f15))

- Install poetry, add black linting
  ([`807808a`](https://github.com/agritheory/forecast/commit/807808ad0a88d89a2063682ec6cf23d61e190a2f))

- Mkdir with parent directories
  ([`16679ac`](https://github.com/agritheory/forecast/commit/16679ac5cbcab0b8c6e9788ed3e19ab87577449e))

- More debug statements
  ([`6317b65`](https://github.com/agritheory/forecast/commit/6317b65ba1217676a51cfbbafc8ad56a87aefe7e))

- Move png files
  ([`c0fb036`](https://github.com/agritheory/forecast/commit/c0fb03653e9364a4a46daa159606c7a46f58597f))

- Remove comma
  ([`87089f3`](https://github.com/agritheory/forecast/commit/87089f3f1232a9ec3d58ad0da3ba848e1ab7fb20))

- Remove unsupported redirection chars from tox commands
  ([`924e4a7`](https://github.com/agritheory/forecast/commit/924e4a73d99afdfa1eaf3a6168a1e52fa098d882))

- Rename workflow
  ([`c33096e`](https://github.com/agritheory/forecast/commit/c33096eea8e2a59ec6b8f8f2a9f2d9fd816b7a52))

- Select all files
  ([`41fc915`](https://github.com/agritheory/forecast/commit/41fc91561f7300dedf3725fa2a7032c1f38f53d2))

- Update branch
  ([`7e98298`](https://github.com/agritheory/forecast/commit/7e9829880e66000d8442302de751805805f64c63))

- Update pytest cov command
  ([`a6d32f8`](https://github.com/agritheory/forecast/commit/a6d32f89b7cc7938ba967a18b291d3c4a4b0ae49))

### Documentation

- Add Forecast example, use len of data vs hardcodes
  ([`04eaf6c`](https://github.com/agritheory/forecast/commit/04eaf6cc57d29ea19c81fe00c67db55db7f6e3af))

- Automatic commit of updated Jupyter notebook
  ([`76b4c29`](https://github.com/agritheory/forecast/commit/76b4c29a390e9ef56aa85e62f08cc7f7831f4d92))

- Automatic commit of updated Jupyter notebook
  ([`d02d832`](https://github.com/agritheory/forecast/commit/d02d832a0d2fe9555f5a22024d7385c7bf006e3a))

- Automatic commit of updated Jupyter notebook
  ([`90ec3a0`](https://github.com/agritheory/forecast/commit/90ec3a045ef1295712b62fe451f4c2e6d83f23b0))

- Automatic commit of updated Jupyter notebook conversions
  ([`0498ddb`](https://github.com/agritheory/forecast/commit/0498ddba014b170e589024d052a605086f366f78))

- Automatic commit of updated Jupyter notebook conversions
  ([`b4b6506`](https://github.com/agritheory/forecast/commit/b4b650666c9b86f1c0c2f5c2f9c726da52f329f0))

- Export to markdown instead of HTML
  ([`86001fc`](https://github.com/agritheory/forecast/commit/86001fccd968ca94c6dbebaddc47b94049ae1e6f))

### Features

- Add function to calculate seasonality factors
  ([`38b5a94`](https://github.com/agritheory/forecast/commit/38b5a94ba79b2ee451199500d5b483eb51fecf7f))

- Remove stub for cal month, quarter, inclusive end date is default
  ([`476517e`](https://github.com/agritheory/forecast/commit/476517e29fcde2039476586da2379435a3b6b377))

- Update for custom days, labels
  ([`5453196`](https://github.com/agritheory/forecast/commit/5453196ce972a0c6e167bc54bf2594053f58789b))

### Testing

- Add custom date format for labels using start date test
  ([`4cfc0de`](https://github.com/agritheory/forecast/commit/4cfc0de1b5fbad635f2a6680d805e855f3fc2ae3))

- Add tests for full coverage
  ([`ed1a65c`](https://github.com/agritheory/forecast/commit/ed1a65c6ee227b43f0e4ec83f422d22c148d03dc))

- Test errors, fix off-by-one output, add seasonality
  ([`daf8cd6`](https://github.com/agritheory/forecast/commit/daf8cd6a64d9a429fb4c604bcff0a22f6614fe47))

- Update for weekly, biweekly change, add labels
  ([`b242e33`](https://github.com/agritheory/forecast/commit/b242e330da31422174b030b792c974bbaf2382f0))


## v0.1.0 (2024-08-09)

### Bug Fixes

- Data length not always 12 in linear_smoothing and exponential_smoothing
  ([`64dcaa8`](https://github.com/agritheory/forecast/commit/64dcaa8f72e384696613dd41b200528761facad8))

- Update dependencies
  ([`def6f9a`](https://github.com/agritheory/forecast/commit/def6f9af7f4d4c4070d899c8db4d7f86913a64cd))

### Build System

- Add builds based on correct spelling
  ([`d173c30`](https://github.com/agritheory/forecast/commit/d173c300b648e520f66f11d982877766c15d5107))

### Chores

- Reduce python version and clean imports to support 3.6.1+
  ([`38f9d91`](https://github.com/agritheory/forecast/commit/38f9d91ca54f07b7758d4f40fc7c99d6ba3c9541))

- Spell approximation correctly
  ([`454d7a9`](https://github.com/agritheory/forecast/commit/454d7a9a2f4cd1247a2c527c62210186456d0755))

- Update project dependencies
  ([`a4ed0f7`](https://github.com/agritheory/forecast/commit/a4ed0f75c6de6f7ed1c04593b14ba0a2cf5b94bb))

### Features

- Add method 10 linear smoothing
  ([`e9b884a`](https://github.com/agritheory/forecast/commit/e9b884a4ccda75612eba7aa44170b84e573bffda))

- Add method 11 exponential smoothing
  ([`a5fd0a2`](https://github.com/agritheory/forecast/commit/a5fd0a212dec3d0749fb08f14bc2862196915fae))

- Add method 12
  ([`31fbeae`](https://github.com/agritheory/forecast/commit/31fbeae2e76149f3022f1fd6778039e1f2a0f01c))

- Add method 12 plots
  ([`a98971e`](https://github.com/agritheory/forecast/commit/a98971e10aee5e812ae3fc0279e550de3bb77e37))

- Add method 6 least squares regression example
  ([`6994d78`](https://github.com/agritheory/forecast/commit/6994d78b18e52b770417428f7492cc41546cdf5c))

- Add methods 7-9 2nd deg poly, flexible, and weighted moving avg
  ([`4d9226d`](https://github.com/agritheory/forecast/commit/4d9226db0c95d1ab7e50126498eac2858d78b4f0))

- Class implementation and tests
  ([`9f73faf`](https://github.com/agritheory/forecast/commit/9f73faf01706cc9d4799b9f6bf14a2d4cbbd11e1))

- Code clean-up for methods 1-6
  ([`e96ed9d`](https://github.com/agritheory/forecast/commit/e96ed9d3dfc253e0c7a5482af60e38377654427e))

- Code clean-up for methods 6-11
  ([`7ade79b`](https://github.com/agritheory/forecast/commit/7ade79b4cd6e47df0ca48120e72f90cf45659f7e))

- Start forecast method calc example notebook
  ([`5105dcb`](https://github.com/agritheory/forecast/commit/5105dcb9e3256c25afcac8ac2db4cdff2aa68fd5))

- Start method 12
  ([`85ed3c5`](https://github.com/agritheory/forecast/commit/85ed3c57857bbbf0d794a1768bc75504c9672ccb))

- Update to ignore Jupyter/Ipython notebook checkpoint files
  ([`b9ff7b6`](https://github.com/agritheory/forecast/commit/b9ff7b6378265049971b8aef37f0c769b421ad96))

### Testing

- Fix test for zero data
  ([`c3755cb`](https://github.com/agritheory/forecast/commit/c3755cb88a8ea21262b866f11c0823b6fea5ecac))
