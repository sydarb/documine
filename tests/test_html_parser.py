# tests/test_html_partitioner.py
import unittest
from documine.parser.html import HTMLParser
from documine.structures import Text, Title, List, Image, Link, Table

class TestHTMLPartitioner(unittest.TestCase):
    def test_partition(self):
        partitioner = HTMLParser()
        elements = partitioner.partition('tests/sample.html')
        self.assertIsInstance(elements, list)
        self.assertGreater(len(elements), 0)

        for element in elements:
            self.assertIsNotNone(element.content)
            self.assertIsNotNone(element.metadata)
            self.assertIsNotNone(element.metadata.order)
            print(f"Order: {element.metadata.order}, Type: {type(element).__name__}, Content: {element.content[:30]}")

    # Add more tests for specific cases

if __name__ == '__main__':
    unittest.main()
