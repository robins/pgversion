import unittest
import pgvernum

class TestMethods(unittest.TestCase):
  def test_getPGVerNumFromString(self):
    self.assertEqual(pgvernum.getPGVerNumFromString('9.3.14'), 90314)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.6.1'), 90601)
    self.assertEqual(pgvernum.getPGVerNumFromString('10.0'), 100000)
    self.assertEqual(pgvernum.getPGVerNumFromString('10.14'), 100014)
    self.assertEqual(pgvernum.getPGVerNumFromString('11.1'), 110001)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.3.14'), 90314)
    self.assertEqual(pgvernum.getPGVerNumFromString('11.9999'), 119999)

  def test_getPGVersionString_negatives(self):
    self.assertEqual(pgvernum.getPGVerNumFromString('9'), False)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.6'), False)
    self.assertEqual(pgvernum.getPGVerNumFromString('10'), False)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.3.1.1'), False)
    self.assertEqual(pgvernum.getPGVerNumFromString('10.1.1'), False)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.3.1a'), False)
    self.assertEqual(pgvernum.getPGVerNumFromString('10.1b'), False)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.3.99'), False)
    self.assertEqual(pgvernum.getPGVerNumFromString('9.99.1'), False)

  def test_isValidPGVersion_negatives(self):
    self.assertEqual(pgvernum.isValidPGVersion(''), False)
    self.assertEqual(pgvernum.isValidPGVersion('a'), False)
    self.assertEqual(pgvernum.isValidPGVersion('a.a'), False)
    self.assertEqual(pgvernum.isValidPGVersion('a.a.a'), False)
    self.assertEqual(pgvernum.isValidPGVersion('.'), False)
    self.assertEqual(pgvernum.isValidPGVersion('..'), False)
    self.assertEqual(pgvernum.isValidPGVersion('...'), False)
    self.assertEqual(pgvernum.isValidPGVersion('1'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.4'), False)
    self.assertEqual(pgvernum.isValidPGVersion('.9.4'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.4.'), False)
    self.assertEqual(pgvernum.isValidPGVersion('94'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.4.4.4'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.4.4.4.4'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9b.2.4'), False)
    self.assertEqual(pgvernum.isValidPGVersion('b9.2.12'), False)
    self.assertEqual(pgvernum.isValidPGVersion('b.2.2'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.b2.12'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.2b.12'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.b.12'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.2.b12'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.2.12b'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.2.b'), False)
    self.assertEqual(pgvernum.isValidPGVersion('-9.3.1'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.-3.1'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.3.-1'), False)
    self.assertEqual(pgvernum.isValidPGVersion('11.1.1'), False)
    self.assertEqual(pgvernum.isValidPGVersion('11.1.'), False)
    self.assertEqual(pgvernum.isValidPGVersion('.11.1'), False)
    self.assertEqual(pgvernum.isValidPGVersion('11.1a'), False)
    self.assertEqual(pgvernum.isValidPGVersion('11.a1'), False)
    self.assertEqual(pgvernum.isValidPGVersion('11.a'), False)
    self.assertEqual(pgvernum.isValidPGVersion('11a.1'), False)
    self.assertEqual(pgvernum.isValidPGVersion('a11.1'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9..'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9..1'), False)
    self.assertEqual(pgvernum.isValidPGVersion('11..'), False)
    self.assertEqual(pgvernum.isValidPGVersion('11.'), False)
    self.assertEqual(pgvernum.isValidPGVersion('11.10000'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.6.100'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.7.10'), False)
    self.assertEqual(pgvernum.isValidPGVersion('9.100.10'), False)
    self.assertEqual(pgvernum.isValidPGVersion('#'), False)

  def test_isValidPGVersion_positives(self):
    self.assertEqual(pgvernum.isValidPGVersion('9.3.0'), True)
    self.assertEqual(pgvernum.isValidPGVersion('11.1'), True)

  def test_isReleasedPGVersion_positives(self):
    self.assertEqual(pgvernum.isReleasedPGVersion('9.3.0'), True)
    self.assertEqual(pgvernum.isReleasedPGVersion('11.1'), True)

  def test_isReleasedPGVersion_negatives(self):
    self.assertEqual(pgvernum.isReleasedPGVersion(''), False)
    self.assertEqual(pgvernum.isReleasedPGVersion('10.24'), False)

  def test_getMajorPGVersion_positives(self):
    self.assertEqual(pgvernum.getMajorPGVersion('9.3'), 9.3)
    self.assertEqual(pgvernum.getMajorPGVersion('9.3.0'), 9.3)
    self.assertEqual(pgvernum.getMajorPGVersion('11.1'), 11)
    self.assertEqual(pgvernum.getMajorPGVersion('11.0'), 11)
    self.assertEqual(pgvernum.getMajorPGVersion('11'), 11)

  def test_getMajorPGVersion_negatives(self):
    self.assertEqual(pgvernum.getMajorPGVersion('9'), False)
    self.assertEqual(pgvernum.getMajorPGVersion('11.2.2'), False)
    self.assertEqual(pgvernum.getMajorPGVersion('a'), False)

  def test_getMinorPGVersion_positives(self):
    self.assertEqual(pgvernum.getMinorPGVersion('9.3.0'), False)
    self.assertEqual(pgvernum.getMinorPGVersion('11.1'), True)

  def test_getMinorPGVersion_negatives(self):
    self.assertEqual(pgvernum.getMinorPGVersion('9.3'), False)
    self.assertEqual(pgvernum.getMinorPGVersion('11'), False)

  def test_parsePGVersion_positives(self):
    self.assertEqual(pgvernum.parsePGVersion('9.3.0'), [9.3, 0])
    self.assertEqual(pgvernum.parsePGVersion('11.1'), [11,1])

  def test_parsePGVersion_negatives(self):
    self.assertEqual(pgvernum.parsePGVersion('9.3'), False)
    self.assertEqual(pgvernum.parsePGVersion('11'), False)

  def test_appendMinorVersionIfRequired_positives(self):
    self.assertEqual(pgvernum.appendMinorVersionIfRequired('9.3'), '9.3.0')
    self.assertEqual(pgvernum.appendMinorVersionIfRequired('11'), '11.0')

  def test_appendMinorVersionIfRequired_negatives(self):
    self.assertEqual(pgvernum.appendMinorVersionIfRequired('9.3.2'), '9.3.2')
    self.assertEqual(pgvernum.appendMinorVersionIfRequired('11.1a'), '11.1a')

  def test_convToYYYYMMDD(self):
    self.assertEqual(pgvernum.convToYYYYMMDD('2023-02-01'), 20230201)

  def test_getVerReleaseDate_positives(self):
    self.assertEqual(pgvernum.getVerReleaseDate('12.1'), '2019-11-14')
    self.assertEqual(pgvernum.getVerReleaseDate('12.0'), '2019-10-03')
    self.assertEqual(pgvernum.getVerReleaseDate('10.1'), '2017-11-09')

  def test_getVerReleaseDate_negatives(self):
    self.assertEqual(pgvernum.getVerReleaseDate('12.100'), '0')
    self.assertEqual(pgvernum.getVerReleaseDate('12.'), '0')
    self.assertEqual(pgvernum.getVerReleaseDate('12.a'), '0')
    self.assertEqual(pgvernum.getVerReleaseDate('1232'), '0')
    self.assertEqual(pgvernum.getVerReleaseDate('-1'), '0')

  def test_IsVerReleasedAfter_positives(self):
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '11.5'), True)
    self.assertEqual(pgvernum.IsVerReleasedAfter('9.4.23', '9.5.15'), True)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.0', '12.1'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '11.6'), False)

  def test_IsVerReleasedAfter_negatives(self):
    self.assertEqual(pgvernum.IsVerReleasedAfter('121', '12.0'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('121', '120'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '120'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '13.1'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', 'a'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', ''), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '#'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '.'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '..'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('12.1', '...'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('a', '12.0'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('', '12.0'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('.', '12.0'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('..', '12.0'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('...', '12.0'), False)
    self.assertEqual(pgvernum.IsVerReleasedAfter('#', '12.0'), False)

if __name__ == '__main__':
  unittest.main(failfast=True)