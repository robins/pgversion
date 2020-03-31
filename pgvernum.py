# This script allows working with Postgres Version Numbers and tries
# to provide basic modules around it. It provides functions to:

# 1) Conversion - For e.g. getPGVerNumFromString() is a function that
#    converts any Postgres version string (for e.g. v9.3.14) to
#    corresponding version Number - i.e. 90314

# 2) Validity - For e.g. IsValidPGVersion() allows validity checks. It also
#    takes care of the new Version numbering system in effect since v10+

# 3) Parsing - For e.g. PargePGVersion()

# 4) Auto-Correction - For e.g. appendMinorVersionIfRequired()

# 5) Historical Info
#    For e.g. getVerReleasedDate() - returns Version release date
#             IsVerReleasedAfter() - Whether Ver X was released before Y

# Original Source: https://github.com/robins/pgversion/blob/master/pgvernum.py


# Sample runs
# -----------
# >py pgvernum.py 9.3.14
# 90314
# >py pgvernum.py 9.6.1
# 90601
# >py pgvernum.py 10.0
# 100000
# >py pgvernum.py 10.14
# 100014
# >py pgvernum.py 11.1
# 110001

# Sample runs for the Unit Tests
#>py test_pgvernum.py
#................
#----------------------------------------------------------------------
#Ran 16 tests in 0.006s
#
#OK

import sys
import re
from datetime import datetime

debug_level = 0
default_debug_level = 1

verReleaseDates = {
  '12.2'    : '2020-02-13',
  '12.1'    : '2019-11-14',
  '12.0'    : '2019-10-03',
  '11.7'    : '2020-02-13',
  '11.6'    : '2019-11-14',
  '11.5'    : '2019-08-08',
  '11.4'    : '2019-06-20',
  '11.3'    : '2019-05-09',
  '11.2'    : '2019-02-14',
  '11.1'    : '2018-11-08',
  '11.0'    : '2018-10-18',
  '10.12'   : '2020-02-13',
  '10.11'   : '2019-11-14',
  '10.10'   : '2019-08-08',
  '10.9'    : '2019-06-20',
  '10.8'    : '2019-05-09',
  '10.7'    : '2019-02-14',
  '10.6'    : '2018-11-08',
  '10.5'    : '2018-08-09',
  '10.4'    : '2018-05-10',
  '10.3'    : '2018-03-01',
  '10.2'    : '2018-02-08',
  '10.1'    : '2017-11-09',
  '10.0'    : '2017-10-05',
  '9.6.17'  : '2020-02-13',
  '9.6.16'  : '2019-11-14',
  '9.6.15'  : '2019-08-08',
  '9.6.14'  : '2019-06-20',
  '9.6.13'  : '2019-05-09',
  '9.6.12'  : '2019-02-14',
  '9.6.11'  : '2018-11-08',
  '9.6.10'  : '2018-08-09',
  '9.6.9'   : '2018-05-10',
  '9.6.8'   : '2018-03-01',
  '9.6.7'   : '2018-02-08',
  '9.6.6'   : '2017-11-09',
  '9.6.5'   : '2017-08-31',
  '9.6.4'   : '2017-08-10',
  '9.6.3'   : '2017-05-11',
  '9.6.2'   : '2017-02-09',
  '9.6.1'   : '2016-10-27',
  '9.6.0'   : '2016-09-29',
  '9.5.21'  : '2020-02-13',
  '9.5.20'  : '2019-11-14',
  '9.5.19'  : '2019-08-08',
  '9.5.18'  : '2019-06-20',
  '9.5.17'  : '2019-05-09',
  '9.5.16'  : '2019-02-14',
  '9.5.15'  : '2018-11-08',
  '9.5.14'  : '2018-08-09',
  '9.5.13'  : '2018-05-10',
  '9.5.12'  : '2018-03-01',
  '9.5.11'  : '2018-02-08',
  '9.5.10'  : '2017-11-09',
  '9.5.9'   : '2017-08-31',
  '9.5.8'   : '2017-08-10',
  '9.5.7'   : '2017-05-11',
  '9.5.6'   : '2017-02-09',
  '9.5.5'   : '2016-10-27',
  '9.5.4'   : '2016-08-11',
  '9.5.3'   : '2016-05-12',
  '9.5.2'   : '2016-03-31',
  '9.5.1'   : '2016-02-11',
  '9.5.0'   : '2016-01-07',
  '9.4.26'  : '2020-02-13',
  '9.4.25'  : '2019-11-14',
  '9.4.24'  : '2019-08-08',
  '9.4.23'  : '2019-06-20',
  '9.4.22'  : '2019-05-09',
  '9.4.21'  : '2019-02-14',
  '9.4.20'  : '2018-11-08',
  '9.4.19'  : '2018-08-09',
  '9.4.18'  : '2018-05-10',
  '9.4.17'  : '2018-03-01',
  '9.4.16'  : '2018-02-08',
  '9.4.15'  : '2017-11-09',
  '9.4.14'  : '2017-08-31',
  '9.4.13'  : '2017-08-10',
  '9.4.12'  : '2017-05-11',
  '9.4.11'  : '2017-02-09',
  '9.4.10'  : '2016-10-27',
  '9.4.9'   : '2016-08-11',
  '9.4.8'   : '2016-05-12',
  '9.4.7'   : '2016-03-31',
  '9.4.6'   : '2016-02-11',
  '9.4.5'   : '2015-10-08',
  '9.4.4'   : '2015-06-12',
  '9.4.3'   : '2015-06-04',
  '9.4.2'   : '2015-05-22',
  '9.4.1'   : '2015-02-05',
  '9.4.0'   : '2014-12-18',
  '9.3.25'  : '2018-11-08',
  '9.3.24'  : '2018-08-09',
  '9.3.23'  : '2018-05-10',
  '9.3.22'  : '2018-03-01',
  '9.3.21'  : '2018-02-08',
  '9.3.20'  : '2017-11-09',
  '9.3.19'  : '2017-08-31',
  '9.3.18'  : '2017-08-10',
  '9.3.17'  : '2017-05-11',
  '9.3.16'  : '2017-02-09',
  '9.3.15'  : '2016-10-27',
  '9.3.14'  : '2016-08-11',
  '9.3.13'  : '2016-05-12',
  '9.3.12'  : '2016-03-31',
  '9.3.11'  : '2016-02-11',
  '9.3.10'  : '2015-10-08',
  '9.3.9'   : '2015-06-12',
  '9.3.8'   : '2015-06-04',
  '9.3.7'   : '2015-05-22',
  '9.3.6'   : '2015-02-05',
  '9.3.5'   : '2014-07-24',
  '9.3.4'   : '2014-03-20',
  '9.3.3'   : '2014-02-20',
  '9.3.2'   : '2013-12-05',
  '9.3.1'   : '2013-10-10',
  '9.3.0'   : '2013-09-09',
  '9.2.24'  : '2017-11-09',
  '9.2.23'  : '2017-08-31',
  '9.2.22'  : '2017-08-10',
  '9.2.21'  : '2017-05-11',
  '9.2.20'  : '2017-02-09',
  '9.2.19'  : '2016-10-27',
  '9.2.18'  : '2016-08-11',
  '9.2.17'  : '2016-05-12',
  '9.2.16'  : '2016-03-31',
  '9.2.15'  : '2016-02-11',
  '9.2.14'  : '2015-10-08',
  '9.2.13'  : '2015-06-12',
  '9.2.12'  : '2015-06-04',
  '9.2.11'  : '2015-05-22',
  '9.2.10'  : '2015-02-05',
  '9.2.9'   : '2014-07-24',
  '9.2.8'   : '2014-03-20',
  '9.2.7'   : '2014-02-20',
  '9.2.6'   : '2013-12-05',
  '9.2.5'   : '2013-10-10',
  '9.2.4'   : '2013-04-04',
  '9.2.3'   : '2013-02-07',
  '9.2.2'   : '2012-12-06',
  '9.2.1'   : '2012-09-24',
  '9.2.0'   : '2012-09-10',
  '9.1.24'  : '2016-10-27',
  '9.1.23'  : '2016-08-11',
  '9.1.22'  : '2016-05-12',
  '9.1.21'  : '2016-03-31',
  '9.1.20'  : '2016-02-11',
  '9.1.19'  : '2015-10-08',
  '9.1.18'  : '2015-06-12',
  '9.1.17'  : '2015-06-04',
  '9.1.16'  : '2015-05-22',
  '9.1.15'  : '2015-02-05',
  '9.1.14'  : '2014-07-24',
  '9.1.13'  : '2014-03-20',
  '9.1.12'  : '2014-02-20',
  '9.1.11'  : '2013-12-05',
  '9.1.10'  : '2013-10-10',
  '9.1.9'   : '2013-04-04',
  '9.1.8'   : '2013-02-07',
  '9.1.7'   : '2012-12-06',
  '9.1.6'   : '2012-09-24',
  '9.1.5'   : '2012-08-17',
  '9.1.4'   : '2012-06-04',
  '9.1.3'   : '2012-02-27',
  '9.1.2'   : '2011-12-05',
  '9.1.1'   : '2011-09-26',
  '9.1.0'   : '2011-09-12',
  '9.0.23'  : '2015-10-08',
  '9.0.22'  : '2015-06-12',
  '9.0.21'  : '2015-06-04',
  '9.0.20'  : '2015-05-22',
  '9.0.19'  : '2015-02-05',
  '9.0.18'  : '2014-07-24',
  '9.0.17'  : '2014-03-20',
  '9.0.16'  : '2014-02-20',
  '9.0.15'  : '2013-12-05',
  '9.0.14'  : '2013-10-10',
  '9.0.13'  : '2013-04-04',
  '9.0.12'  : '2013-02-07',
  '9.0.11'  : '2012-12-06',
  '9.0.10'  : '2012-09-24',
  '9.0.9'   : '2012-08-17',
  '9.0.8'   : '2012-06-04',
  '9.0.7'   : '2012-02-27',
  '9.0.6'   : '2011-12-05',
  '9.0.5'   : '2011-09-26',
  '9.0.4'   : '2011-04-18',
  '9.0.3'   : '2011-01-31',
  '9.0.2'   : '2010-12-16',
  '9.0.1'   : '2010-10-04',
  '9.0.0'   : '2010-09-20',
  '8.4.22'  : '2014-07-24',
  '8.4.21'  : '2014-03-20',
  '8.4.20'  : '2014-02-20',
  '8.4.19'  : '2013-12-05',
  '8.4.18'  : '2013-10-10',
  '8.4.17'  : '2013-04-04',
  '8.4.16'  : '2013-02-07',
  '8.4.15'  : '2012-12-06',
  '8.4.14'  : '2012-09-24',
  '8.4.13'  : '2012-08-17',
  '8.4.12'  : '2012-06-04',
  '8.4.11'  : '2012-02-27',
  '8.4.10'  : '2011-12-05',
  '8.4.9'   : '2011-09-26',
  '8.4.8'   : '2011-04-18',
  '8.4.7'   : '2011-01-31',
  '8.4.6'   : '2010-12-16',
  '8.4.5'   : '2010-10-04',
  '8.4.4'   : '2010-05-17',
  '8.4.3'   : '2010-03-15',
  '8.4.2'   : '2009-12-14',
  '8.4.1'   : '2009-09-09',
  '8.4.0'   : '2009-07-01',
  '8.3.23'  : '2013-02-07',
  '8.3.22'  : '2012-12-06',
  '8.3.21'  : '2012-09-24',
  '8.3.20'  : '2012-08-17',
  '8.3.19'  : '2012-06-04',
  '8.3.18'  : '2012-02-27',
  '8.3.17'  : '2011-12-05',
  '8.3.16'  : '2011-09-26',
  '8.3.15'  : '2011-04-18',
  '8.3.14'  : '2011-01-31',
  '8.3.13'  : '2010-12-16',
  '8.3.12'  : '2010-10-04',
  '8.3.11'  : '2010-05-17',
  '8.3.10'  : '2010-03-15',
  '8.3.9'   : '2009-12-14',
  '8.3.8'   : '2009-09-09',
  '8.3.7'   : '2009-03-16',
  '8.3.6'   : '2009-02-02',
  '8.3.5'   : '2008-11-03',
  '8.3.4'   : '2008-09-22',
  '8.3.3'   : '2008-06-12',
  '8.3.1'   : '2008-03-17',
  '8.3.0'   : '2008-02-04',
  '8.2.23'  : '2011-12-05',
  '8.2.22'  : '2011-09-26',
  '8.2.21'  : '2011-04-18',
  '8.2.20'  : '2011-01-31',
  '8.2.19'  : '2010-12-16',
  '8.2.18'  : '2010-10-04',
  '8.2.17'  : '2010-05-17',
  '8.2.16'  : '2010-03-15',
  '8.2.15'  : '2009-12-14',
  '8.2.14'  : '2009-09-09',
  '8.2.13'  : '2009-03-16',
  '8.2.12'  : '2009-02-02',
  '8.2.11'  : '2008-11-03',
  '8.2.10'  : '2008-09-22',
  '8.2.9'   : '2008-06-12',
  '8.2.7'   : '2008-03-17',
  '8.2.6'   : '2008-01-07',
  '8.2.5'   : '2007-09-17',
  '8.2.4'   : '2007-04-23',
  '8.2.3'   : '2007-02-07',
  '8.2.2'   : '2007-02-05',
  '8.2.1'   : '2007-01-08',
  '8.2.0'   : '2006-12-05',
  '8.1.23'  : '2010-12-16',
  '8.1.22'  : '2010-10-04',
  '8.1.21'  : '2010-05-17',
  '8.1.20'  : '2010-03-15',
  '8.1.19'  : '2009-12-14',
  '8.1.18'  : '2009-09-09',
  '8.1.17'  : '2009-03-16',
  '8.1.16'  : '2009-02-02',
  '8.1.15'  : '2008-11-03',
  '8.1.14'  : '2008-09-22',
  '8.1.13'  : '2008-06-12',
  '8.1.11'  : '2008-01-07',
  '8.1.10'  : '2007-09-17',
  '8.1.9'   : '2007-04-23',
  '8.1.8'   : '2007-02-07',
  '8.1.7'   : '2007-02-05',
  '8.1.6'   : '2007-01-08',
  '8.1.5'   : '2006-10-16',
  '8.1.4'   : '2006-05-23',
  '8.1.3'   : '2006-02-14',
  '8.1.2'   : '2006-01-09',
  '8.1.1'   : '2005-12-12',
  '8.1.0'   : '2005-11-08',
  '8.0.26'  : '2010-10-04',
  '8.0.25'  : '2010-05-17',
  '8.0.24'  : '2010-03-15',
  '8.0.23'  : '2009-12-14',
  '8.0.22'  : '2009-09-09',
  '8.0.21'  : '2009-03-16',
  '8.0.20'  : '2009-02-02',
  '8.0.19'  : '2008-11-03',
  '8.0.18'  : '2008-09-22',
  '8.0.17'  : '2008-06-12',
  '8.0.15'  : '2008-01-07',
  '8.0.14'  : '2007-09-17',
  '8.0.13'  : '2007-04-23',
  '8.0.12'  : '2007-02-07',
  '8.0.11'  : '2007-02-05',
  '8.0.10'  : '2007-01-08',
  '8.0.9'   : '2006-10-16',
  '8.0.8'   : '2006-05-23',
  '8.0.7'   : '2006-02-14',
  '8.0.6'   : '2006-01-09',
  '8.0.5'   : '2005-12-12',
  '8.0.4'   : '2005-10-04',
  '8.0.3'   : '2005-05-09',
  '8.0.2'   : '2005-04-07',
  '8.0.1'   : '2005-01-31',
  '8.0.0'   : '2005-01-19',
  '7.4.30'  : '2010-10-04',
  '7.4.29'  : '2010-05-17',
  '7.4.28'  : '2010-03-15',
  '7.4.27'  : '2009-12-14',
  '7.4.26'  : '2009-09-09',
  '7.4.25'  : '2009-03-16',
  '7.4.24'  : '2009-02-02',
  '7.4.23'  : '2008-11-03',
  '7.4.22'  : '2008-09-22',
  '7.4.21'  : '2008-06-12',
  '7.4.19'  : '2008-01-07',
  '7.4.18'  : '2007-09-17',
  '7.4.17'  : '2007-04-23',
  '7.4.16'  : '2007-02-05',
  '7.4.15'  : '2007-01-08',
  '7.4.14'  : '2006-10-16',
  '7.4.13'  : '2006-05-23',
  '7.4.12'  : '2006-02-14',
  '7.4.11'  : '2006-01-09',
  '7.4.10'  : '2005-12-12',
  '7.4.9'   : '2005-10-04',
  '7.4.8'   : '2005-05-09',
  '7.4.7'   : '2005-01-31',
  '7.4.6'   : '2004-10-22',
  '7.4.5'   : '2004-08-18',
  '7.4.4'   : '2004-08-16',
  '7.4.3'   : '2004-06-14',
  '7.4.2'   : '2004-03-08',
  '7.4.1'   : '2003-12-22',
  '7.4.0'   : '2003-11-17',
  '7.3.21'  : '2008-01-07',
  '7.3.20'  : '2007-09-17',
  '7.3.19'  : '2007-04-23',
  '7.3.18'  : '2007-02-05',
  '7.3.17'  : '2007-01-08',
  '7.3.16'  : '2006-10-16',
  '7.3.15'  : '2006-05-23',
  '7.3.14'  : '2006-02-14',
  '7.3.13'  : '2006-01-09',
  '7.3.12'  : '2005-12-12',
  '7.3.11'  : '2005-10-04',
  '7.3.10'  : '2005-05-09',
  '7.3.9'   : '2005-01-31',
  '7.3.8'   : '2004-10-22',
  '7.3.7'   : '2004-08-16',
  '7.3.6'   : '2004-03-02',
  '7.3.5'   : '2003-12-03',
  '7.3.4'   : '2003-07-24',
  '7.3.3'   : '2003-05-22',
  '7.3.2'   : '2003-02-04',
  '7.3.1'   : '2002-12-18',
  '7.3.0'   : '2002-11-27',
  '7.2.8'   : '2005-05-09',
  '7.2.7'   : '2005-01-31',
  '7.2.6'   : '2004-10-22',
  '7.2.5'   : '2004-08-16',
  '7.2.4'   : '2003-01-30',
  '7.2.3'   : '2002-10-01',
  '7.2.2'   : '2002-08-23',
  '7.2.1'   : '2002-03-21',
  '7.2.0'   : '2002-02-04',
  '7.1.3'   : '2001-08-15',
  '7.1.2'   : '2001-05-11',
  '7.1.1'   : '2001-05-05',
  '7.1.0'   : '2001-04-13',
  '7.0.3'   : '2000-11-11',
  '7.0.2'   : '2000-06-05',
  '7.0.1'   : '2000-06-01',
  '7.0.0'   : '2000-05-08',
  '6.5.3'   : '1999-10-13',
  '6.5.2'   : '1999-09-15',
  '6.5.1'   : '1999-07-15',
  '6.5.0'   : '1999-06-09',
  '6.4.2'   : '1998-12-20',
  '6.4.1'   : '1998-12-18',
  '6.4.0'   : '1998-10-30',
  '6.3.2'   : '1998-04-07',
  '6.3.1'   : '1998-03-23',
  '6.3.0'   : '1998-03-01',
  '6.2.1'   : '1997-10-17',
  '6.2.0'   : '1997-10-02',
  '6.1.1'   : '1997-07-22',
  '6.1.0'   : '1997-06-08',
  '6.0.0'   : '1997-01-29',
  '1.09'    : '1996-11-04',
  '1.02'    : '1996-08-01',
  '1.01'    : '1996-02-23',
  '1.0'     : '1995-09-05',
  '0.03'    : '1995-07-21',
  '0.02'    : '1995-05-25',
  '0.01'    : '1995-05-01'
}

def dprint(s, debug = default_debug_level):
  if (debug_level >= debug):
    print (s)


# Returns 1 if the postgres version is valid
# It does not take (only) major versions. It would need to be appended with .0 to be considered valid
# It takes care of Version Number semantics differences before and after v10.0
def isValidPGVersion(_s, debug = default_debug_level):

  s= str(_s)
  # Old (v9.3.1) or New (v11.0) require at least 4 characters for
  # being a valid version string
  if (len(s)<4):
    dprint('Invalid Version String - Requires at least 4 characters - ' + s, debug)
    return 0

  if (re.match(r"^\.|.*\.$", s)):
    dprint("Invalid Version String. Shouldn't begin or end with period / dot (.) - " + s, debug)
    return 0

  # Fail if there are 2 or more adjacent dots (.)
  if (re.match(r".*[\.]{2,}", s)):
    dprint("Invalid Version String. There are 2+ adjacent periods / dots (.) - " + s, debug)
    return 0

  dots = s.count('.')

  # Fail if it has anything except numbers and dot (.)
  if (not re.match(r'^[0-9\.]*$', s)):
    dprint("Invalid Version String. Shouldn't have anything except numbers and period / dot (.) - " + s, debug)
    return 0

  # Fail if it has no dots. A Version requires both Major AND Minor
  # version to be present.
  #
  # There are other functions that act as fallback, that can convert
  # some Major Version strings to a valid Postgres Versions by appending
  # a ".0" minor version, but that is beyond scope of this function
  if (dots == 0):
    dprint("Invalid Version String. Should have both Major and Minor version - " + s, debug)
    return 0

  # Fail if it has more than 2 dots
  if (dots > 2):
    dprint("Invalid Version String. Has more than 2 periods / dots (.) - " + s, debug)
    return 0

  x = list(map(int, s.split('.', dots)))

  if (dots == 2):
    # v10+ should not have more than 1 dot
    if (x[0]>=10):
      dprint("Invalid Version String. v10+ shouldn't have more than one period / dot (.) - " + s, debug)
      return 0
    if (x[2] >= 100):
      dprint("Invalid Version String. Minor version should be less than 100 - " + s, debug)
      return 0
    if (x[1] >= 100):
      dprint("Invalid Version String. Right digit of Major version (9.x) should be <100 - " + s, debug)
      return 0

  if (dots == 1):
    # pre-v10 should have more than 1 dot
    if (x[0]<10):
      dprint("Invalid Version String. Should have both Major and Minor versions - " + s, debug)
      return 0
    if (x[1] >= 10000):
      dprint("Invalid Version String. Minor Version should be less than 10000 - " + s, debug)
      return 0

  return 1


# Return (only) the Major version when given a Valid Postgres Version
def getMajorPGVersion(v):
  s=appendMinorVersionIfRequired(v)
  if (not isValidPGVersion(s)):
    return -1

  dots = s.count('.')
  x = list(map(int, s.split('.', dots)))

  # This is pre-v10
  if (dots == 2):
    return float(str(x[0]) + "." + str(x[1]))
  # This is v10+
  elif (dots == 1):
    return int(x[0])

  # We shouldn't reach here. Something went wrong
  return -2


# Return (only) the Minor version when given a Valid Postgres Version
def getMinorPGVersion(s):
  if (not isValidPGVersion(s)):
    return -1

  dots = s.count('.')
  x = list(map(int, s.split('.', dots)))

  # This is pre-v10
  if (dots == 2):
    return x[2]
  # This is v10+
  elif (dots == 1):
    return x[1]

  # We shouldn't reach here. Something went wrong
  return -2


# Returns a dict of [Major, Minor] if provided a valid PG Version
def parsePGVersion(s):

  if (not isValidPGVersion(s)):
    return -1

  Maj = getMajorPGVersion(s)
  Min = getMinorPGVersion(s)

  if (Maj >= 0):
    if (Min >= 0):
      return [Maj, Min]

  return -1


# Attempt to append a .0 at the end of the Version passed to check if passes isValidPGVersion()
def appendMinorVersionIfRequired(s):

  if (not isValidPGVersion(s)):
    attempt1 = s + ".0"
    if (isValidPGVersion(attempt1)):
      # Additionally also check whether we already have this in the lookup list.
      # This is a best-effort function and unlike in IsValidPGVersion() we can
      # rely on the release date list and fail if it doesn't exist there.
      # This avoids some scenarios such as v1.1 becomes v.1.1.0, which is wrong.
      if (attempt1 in verReleaseDates):
        return attempt1

  return s


# Get the PostgresVersionNum Integer from the Version String provided
# For e.g. v10.14 would return 100014
# More details: https://www.postgresql.org/docs/devel/runtime-config-preset.html#GUC-SERVER-VERSION-NUM
def getPGVerNumFromString(s):

  if (not isValidPGVersion(s)):
    return 0

  dots = s.count('.')

  x = list(map(int, s.split('.', dots)))

  if (x[0]>=10):
    versionnum = int(x[0]*10000)
    if (dots == 1):
      versionnum += x[1]
  else:
    versionnum = x[0]*10000 + (x[1]*100)
    if (dots ==2):
      versionnum += x[2]
  return versionnum


# Get the Release Date when a Postgres Version was released to the Community
# For e.g.: v12.2 was released on 13th Feb 2020
# So when '12.2' is passed, the function returns '2020-02-13'
# Sample Release URL: https://www.postgresql.org/about/news/2011/
def getVerReleasedDate(ver):
  global verReleaseDates

  if not isValidPGVersion(ver):
    return '0'

  if (ver in verReleaseDates):
    return verReleaseDates[ver]
  else:
    dprint('Release date unavailable for release: ' + ver)
  return '0'


# Convert date from YYYY-MM-DD to YYYYMMDD format
def convToYYYYMMDD(dt):
  return int(datetime.strptime(dt, '%Y-%m-%d').strftime('%Y%m%d'))


# Simple comparison function that returns 1 if v1 was released AFTER v2
# For e.g. IsVerReleasedAfter('10.12', '11.5') returns 1 (TRUE) owing to how Postgres Release numbering works.
def IsVerReleasedAfter(v1, v2):
  global verReleaseDates

  if not isValidPGVersion(v1):
    return 0

  if not isValidPGVersion(v2):
    return 0

  if (v1 in verReleaseDates) and (v2 in verReleaseDates):
    if (v1 in verReleaseDates) and (v2 in verReleaseDates):
      if (convToYYYYMMDD(verReleaseDates[v1])>convToYYYYMMDD(verReleaseDates[v2])):
        return 1
    else:
      dprint('Release date unavailable for release: ' + v2)
  else:
    dprint('Release date unavailable for release: ' + v1)

  return 0

def main(argv):
  if len(sys.argv) == 2:
    s = sys.argv[1]
  else:
    dprint('Invalid number of arguments - ' + str(len(sys.argv)), 0)
    exit()
  print (isValidPGVersion(s))

if (__name__ == '__main__'):
  main(sys.argv)

#getMajorPGVersion(sys.argv[1])