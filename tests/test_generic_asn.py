import unittest
from asn.generic_asn import GenericASN
from asn.utils import U7, U8, U16


class TestGenericASNGenPack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        GenericASN.TAG = b'\x8A'

    def test_pack_none(self):
        self.assertEqual(GenericASN.generic_pack(None), b'\x8A\x00')

    def test_pack_0_extra_min(self):
        self.assertEqual(GenericASN.generic_pack(b'a'), b'\x8A\x01a')

    def test_pack_0_extra_max(self):
        self.assertEqual(GenericASN.generic_pack(b'a' * (U7 - 1)), b'\x8A\x7F' + (b'a' * (U7 - 1)))

    def test_pack_1_extra_min(self):
        self.assertEqual(GenericASN.generic_pack(b'a' * U7), b'\x8A\x81\x80' + (b'a' * U7))

    def test_pack_1_extra_max(self):
        self.assertEqual(GenericASN.generic_pack(b'a' * (U8 - 1)), b'\x8A\x81\xFF' + (b'a' * (U8 - 1)))

    def test_pack_2_extra_min(self):
        self.assertEqual(GenericASN.generic_pack(b'a' * U8), b'\x8A\x82\x01\x00' + (b'a' * U8))

    def test_pack_2_extra_max(self):
        self.assertEqual(GenericASN.generic_pack(b'a' * (U16 - 1)), b'\x8A\x82\xFF\xFF' + (b'a' * (U16 - 1)))

    def test_pack_wrong_extra(self):
        self.assertRaises(ValueError, GenericASN.generic_pack, b'a' * U16)


class TestGenericASNGetASN(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        GenericASN.TAG = b'\x86'

    def test_unpack_wrong_tag(self):
        self.assertRaises(TypeError, GenericASN.generic_unpack, b'\x87\x00')

    def test_unpack_missing_size(self):
        self.assertRaises(ValueError, GenericASN.generic_unpack, b'\x86')

    def test_unpack_smaller_size(self):
        self.assertRaises(ValueError, GenericASN.generic_unpack, b'\x86\x03\xFF\xFF')

    def test_unpack_bigger_size(self):
        self.assertRaises(ValueError, GenericASN.generic_unpack, b'\x86\x03\xFF\xFF\xFF\xFF')

    def test_unpack_extra_length(self):
        length = U7 + 1
        string = b'a' * length

        actual = GenericASN.generic_unpack(b'\x86\x81\x81' + string)
        expected = (length, string)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()