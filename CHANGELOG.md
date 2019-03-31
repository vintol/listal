# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

------------
## [1.2.1] - 2018-01-27
### Added
- Capability for handling https protocol.
### Deprecated
- Forcing usage of http protocol because ssl certificate issues
### Security
- HTTPS certificate is not verified.


---------
## [1.2.0] - 2018-11-21
### Added
- Stop scraping at a perticular image
- Start from or finish at a perticular page no.
### Changed
- Report Broken links.
### Fixed
- Error handling exception when http timeout

-------
## [1.1.0] - 2017-03-29

### Added
- Downloader always checks if files are already downloaded and skips them.
- Errors are categorized for better understanding of bugs.
- Checks for broken links.

----
## [1.0.0] - 2016-11-10
First Stable release.
### Added
- Can now get images from `image` lists.
- Support for command-line Arguments.
- Added a progress bar.
- Download resume capability.

### Changed
- Instead of entering the name of the person you enter the profile url.
- Downloader is now a seperate script rather then an option.
- Links are placed in a file in working dir; Instead of creating a seperate directory inside the working directory.
- No interactive input; instead command line args are accepted.

### Removed
- Option to download images is removed from main file.

------
## [0.1.0] - 2016-04-20
This is the first public release. **Pre Release**

### Added
- Retrives the links of of all photos from any `person` profile on `listal.com`.
- Also, can download the photos from the retrived links using mulitple threads.
