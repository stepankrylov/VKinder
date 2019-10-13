import unittest
import user
import find

class TestVKinder(unittest.TestCase):

    def test_user(self):
        res = user.user(
                        '88aaa557781ffd1325cb745fbb65127b38b16b3675584745562891825e6375f108f60eb6c6d6ea93d4315', 
                        '126882190'
                        )
        self.assertEqual(res[1] - res[0], res[1])

if __name__ == '__main__':
    unittest.main()