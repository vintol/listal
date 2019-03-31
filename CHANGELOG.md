# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

------------
## [Upcoming Release]

-------

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
