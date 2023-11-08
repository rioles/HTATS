from services.room_service.paginator import index_range, Paginator
import unittest

class TestIndexRange(unittest.TestCase):
    def test_index_range_1(self):
        self.assertEquals(index_range(1, 10), (0,10))
        
    def test_index_range_2(self):
        self.assertEquals(index_range(2, 10), (10,20))
    
    def test_index_range_3(self):
        self.assertEquals(index_range(5, 10), (40,50))

class TestGetPage(unittest.TestCase):
    def setUp(self):
        # Create a sample dataset for testing
        self.dataset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.paginator = Paginator(self.dataset)
     
    def test_valid_page(self):
        # Test when requesting a valid page
        page = self.paginator.get_page(page=2, page_size=3)
        self.assertEqual(page, [4, 5, 6])   
    
    def test_empty_page(self):
        # Test when requesting a page beyond the dataset
        page = self.paginator.get_page(page=4, page_size=5)
        self.assertEqual(page, [])

    def test_large_page_size(self):
        # Test when requesting a page with a larger page_size than dataset size
        page = self.paginator.get_page(page=1, page_size=20)
        self.assertEqual(page, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        
    def test_page_zero(self):
        # Test when requesting a page with page=0
        with self.assertRaises(AssertionError):
            self.paginator.get_page(page=0, page_size=5)
            
    def test_negative_page(self):
        # Test when requesting a negative page number
        with self.assertRaises(AssertionError):
            self.paginator.get_page(page=-1, page_size=5)

    def test_negative_page_size(self):
        # Test when requesting a negative page_size
        with self.assertRaises(AssertionError):
            self.paginator.get_page(page=1, page_size=-5)

    def test_invalid_page_type(self):
        # Test when passing a non-integer page number
        with self.assertRaises(AssertionError):
            self.paginator.get_page(page="invalid", page_size=5)

    def test_invalid_page_size_type(self):
        # Test when passing a non-integer page_size
        with self.assertRaises(AssertionError):
            self.paginator.get_page(page=1, page_size="invalid")
            
class TestPaginator(unittest.TestCase):

    def setUp(self):
        # Create a sample dataset for testing
        self.dataset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.paginator = Paginator(self.dataset)

    def assertIsDict(self, obj):
        self.assertIsInstance(obj, dict, f"Expected a dictionary, but got {type(obj)}")

    def test_get_hyper_default(self):
        # Test get_hyper with default parameters
        hyper = self.paginator.get_hyper()
        self.assertIsDict(hyper)

        expected_hyper = {
            "page_size": 10,
            "page": 1,
            "data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "next_page": None,
            "prev_page": None,
            "total_pages": 1,
        }
        self.assertEqual(hyper, expected_hyper)

    def test_get_hyper_with_extra_info(self):
        # Test get_hyper with extra_info provided
        extra_info = {"key": "value"}
        hyper = self.paginator.get_hyper(extra_info=extra_info, key_name="custom_info")
        self.assertIsDict(hyper)

        expected_hyper = {
            "page_size": 10,
            "page": 1,
            "data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "next_page": None,
            "prev_page": None,
            "total_pages": 1,
            "custom_info": extra_info,
        }
        self.assertEqual(hyper, expected_hyper)

    def test_get_hyper_custom_page(self):
        # Test get_hyper with a custom page number
        hyper = self.paginator.get_hyper(page=2)
        self.assertIsDict(hyper)

        expected_hyper = {
            "page_size": 0,
            "page": 2,
            "data": [],
            "next_page": None,
            "prev_page": 1,
            "total_pages": 1,
        }
        self.assertEqual(hyper, expected_hyper)
  

if __name__=='__main__':
    unittest.main()