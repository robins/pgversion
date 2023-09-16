
import pgvernum as v
# sys.path.append('pgvernum.py') pgvernum

print()
print("Accepts argument as int. For e.g. isValidPGVersion(11.1) -", v.isReleasedPGVersion(11.1))
print("Accepts argument as string. For e.g. isValidPGVersion('11.1') -", v.isReleasedPGVersion('11.1'))

print()
print("Accepts old Postgres version number system - For e.g. isValidPGVersion('9.6.1') -", v.isValidPGVersion('9.6.1'))

print()
print("Check if Postgres version is valid. For e.g. isValidPGVersion('10.14') -", v.isValidPGVersion('10.14'))
print("... and even when technically valid, confirm if a version was ever released. For e.g. was v9.7.1 ever released? ", v.isReleasedPGVersion('9.7.1'))

print()
print("Extract Major version from a Postgres version. For e.g. getMajorPGVersion('14.2') -", v.getMajorPGVersion('14.2'))

print()
print("Extract Minor version from a Postgres version. For e.g. getMinorPGVersion('14.2') -", v.getMinorPGVersion('14.2'))

print()
print("Attempt to modify input to create a valid postgres version. For e.g. appendMinorVersionIfRequired(10) -", v.appendMinorVersionIfRequired(10))

print()
print("Convert Postgres version string to Postgres Version Number. For e.g. getPGVerNumFromString('9.6.1') -", v.getPGVerNumFromString("9.6.1"))

print()
print("Get Release Date for Postgres Version. For e.g. getVerReleaseDate('10.1') -", v.getVerReleaseDate("10.1"))

print()
print("Compare release dates of two Postgres versions. For e.g. IsVerReleasedAfter('12.14', '15.1')",v.IsVerReleasedAfter('12.14', '15.1'))
print("... in other words, v12.14 was released *after* v15.1")
print()
