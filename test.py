from unittest import TestCase
from code import get_annual_price, get_price

class TestGetAnnualPrice(TestCase):
	def test_get_annual_price_month(self):
		price = "£5.99(inc. VAT)Per Month"	
		actual = get_annual_price(price)
		expected = 5.99*12
		self.assertEqual(actual, expected)
	
	def test_get_annual_price_year(self):
		price = "£108.00  (inc. VAT) Per Year"
		actual = get_annual_price(price)
		expected = 108
		self.assertEqual(actual, expected)

class TestGetPrice(TestCase):
	def test_get_price_year(self):
		info = '<div class="package-price"><span class="price-big">£174.00</span><br/>(inc. VAT)<br/>Per Year<p style="color: red">Save £17.90 on the monthly price</p>'
		actual_price, actual_discount = get_price(info)
		expected_price = '£174.00  (inc. VAT) Per Year'
		expected_discount = 'Save £17.90 on the monthly price'
		self.assertEqual(expected_price, actual_price)
		self.assertEqual(expected_discount, actual_discount)