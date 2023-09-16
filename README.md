# PGVersion
## Python functions for Postgres version strings

### Python library allows
- Validation of Postgres Version Strings
- Attempt auto-correction of minor versions
- Get Release Date information for a given Postgres Version
- Compare release dates of two versions
- Extract Major (or Minor) version from Version String
- Conversion of Postgres version string to version number (for e.g. v10.14 -> 100014)


## Functions
- `isValidPGVersion(s)`
- `isReleasedPGVersion(s)`
- `getMajorPGVersion(s)`
- `getMinorPGVersion(s)`
- `parsePGVersion(s)`
- `appendMinorVersionIfRequired(s)`
- `getPGVerNumFromString(s)`
- `getVerReleaseDate(ver)`
- `IsVerReleasedAfter(v1, v2)`


## Sample Output

```
PS C:\proj\pgversion> python .\main.py

Accepts argument as int. For e.g. isValidPGVersion(11.1) - True
Accepts argument as string. For e.g. isValidPGVersion('11.1') - True

Accepts old Postgres version number system - For e.g. isValidPGVersion('9.6.1') - True

Check if Postgres version is valid. For e.g. isValidPGVersion('10.14') - True
... and even when technically valid, confirm if a version was ever released. For e.g. was v9.7.1 ever released?  False

Extract Major version from a Postgres version. For e.g. getMajorPGVersion('14.2') - 14

Extract Minor version from a Postgres version. For e.g. getMinorPGVersion('14.2') - 2

Attempt to modify input to create a valid postgres version. For e.g. appendMinorVersionIfRequired(10) - 10.0

Convert Postgres version string to Postgres Version Number. For e.g. getPGVerNumFromString('9.6.1') - 90601

Get Release Date for Postgres Version. For e.g. getVerReleaseDate('10.1') - 2017-11-09

Compare release dates of two Postgres versions. For e.g. IsVerReleasedAfter('12.14', '15.1') True
... in other words, v12.14 was released *after* v15.1
```


## Testing
- 100+ tests for various functions
- Travis integration


### Sample Test Run
```
C:\proj\pgversion>coverage run test_pgversion.py
...................
----------------------------------------------------------------------
Ran 19 tests in 0.005s

OK
```
