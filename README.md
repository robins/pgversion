# PGVersion

![Coverage](https://api.travis-ci.org/robins/getRDSUpgradePath.svg?branch=master)

Python library for Postgres Versions that allow:
- Validation of Postgres Version Strings
- Auto-Correct
  - Engine Minor Version Number
- Tune verbosity levels, if required
- Dates
  - Get Release Date for a given Postgres Version
  - Compare release dates of two versions v1 and v2
- Parsing
  - Get Major / Minor as dict[]
  - Extract only Major (or Minor) version from Version String
- Conversion
  - Convert PG Version String to PG Version Number (for e.g. v10.14 -> 100014)


## Testing
- 100+ tests for various functions
- Travis integration (pending)


### Testing Postgres Version Number generation
```
>coverage run test_pgvernum.py
....
----------------------------------------------------------------------
Ran 4 tests in 0.002s

OK
```