# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com) and
this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [Unreleased]
[Unreleased]: https://github.com/althonos/ffpb/compare/v0.4.1...HEAD


## [v0.4.1] - 2021-02-13
[v0.4.1]: https://github.com/althonos/ffpb/compare/v0.4.0...v0.4.1

### Fixed
- Unneeded decoding in main loop causing codec issues ([#22](https://github.com/althonos/ffpb/issues/22)).


## [v0.4.0] - 2021-01-13
[v0.4.0]: https://github.com/althonos/ffpb/compare/v0.3.0...v0.4.0

### Added
-   Support for Windows platform ([#21](https://github.com/althonos/ffpb/pull/21)).

### Removed
- [sh](https://pypi.org/project/sh) dependency.


## [v0.3.0] - 2020-08-15
[v0.3.0]: https://github.com/althonos/ffpb/compare/v0.2.0...v0.3.0

### Added
-   Option to change progress bar class in `ffpb.main`.

### Fixed
- Decoding error caused by missing encoding in `ffpb.main` ([#17](https://github.com/althonos/ffpb/issues/17)).


## [v0.2.0] - 2019-04-29
[v0.2.0]: https://github.com/althonos/ffpb/compare/v0.1.3...v0.2.0

### Added
- Python 3.7 as an explicitly supported version.

### Fixed
- Incorrect decoding of filenames caused by [`chardet`](https://pypi.org/project/chardet/).


## [v0.1.3] - 2019-04-06
[v0.1.3]: https://github.com/althonos/ffpb/compare/v0.1.2...v0.1.3

### Fixed
- `ffpb.main` not using given `argv` argument ([#12](https://github.com/althonos/ffpb/pull/12)).


## [v0.1.2] - 2018-09-12
[v0.1.2]: https://github.com/althonos/ffpb/compare/v0.1.1...v0.1.2

### Fixed
- `ffpb` crashing on non-video input/output ([#8](https://github.com/althonos/ffpb/issues/8)).


## [v0.1.1] - 2018-09-11
[v0.1.1]: https://github.com/althonos/ffpb/compare/v0.1.0...v0.1.1

### Fixed
- `README.rst` not rendering properly on [PyPI](https://pypi.org/project/ffpb).


## [v0.1.0] - 2018-09-11
[v0.1.0]: https://github.com/althonos/ffpb/compare/dacd42a...v0.1.0

Initial release.
