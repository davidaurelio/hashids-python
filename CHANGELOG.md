# Changelog

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [1.3.1] - 2020-07-26
### Fixed

Python requirement changed to `>=2.7`

## 1.3.0 - 2020-07-26

### Added
- Test for short alphabet

### Changed
- Changes the list of tested Python versions to the currently active versions: 2.7, 3.5–3.8, and pypy2/3.
- Build changed from `setup.py` to `pyproject.toml`
- Changelog format changed to *[Keep a Changelog].*

### Fixed
- Deprecation warnings for `encrypt`/`decrypt`


## 1.2.0 - 2017-01-06
### Changed
  - performance optimizations (Jakub Kramarz)
  - version classifiers (Patrick Mézard)

## 1.1.0 - 2015-03-31
### Added
  - add encode_hex() / decode_hex()

## 1.0.3 - 2015-02-26
### Changed
  - remove dependency to `future`

## 1.0.2 - 2015-01-15
### Changed
  - compatibility with JS version 1.0.x

## 1.0.1 - 2014-06-19
### Changed
  - only decode hashids if the re-encoded result equals the input

## 1.0.0 - 2014-04-21
### Changed
  - compatibility with JS version 0.3.x

## 0.8.4 - 2014-02-04
### Changed
  - Make setup.py compatible with older python versions

## [0.8.3] - 2013-06-02
Added
  - initial release, compatible with JS version 0.1.x


[1.3.0]: https://github.com/davidaurelio/hashids-python/compare/1.3.0...1.3.1
[1.3.0]: https://github.com/davidaurelio/hashids-python/compare/1.2.0...1.3.0
[1.2.0]: https://github.com/davidaurelio/hashids-python/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/davidaurelio/hashids-python/compare/1.0.3...1.1.0
[1.0.3]: https://github.com/davidaurelio/hashids-python/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/davidaurelio/hashids-python/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/davidaurelio/hashids-python/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/davidaurelio/hashids-python/compare/0.8.4...1.0.0
[0.8.4]: https://github.com/davidaurelio/hashids-python/compare/0.8.3...0.8.4
[0.8.3]: https://github.com/davidaurelio/hashids-python/releases/tag/v0.8.3
[Keep a Changelog]: https://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: https://semver.org/spec/v2.0.0.html
