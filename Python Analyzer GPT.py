import csv


class SalesAnalyzer:
	"""Utility to analyze sales data from a CSV file.

	The analyzer expects a CSV file with at least the columns
	'product_name', 'price', and 'quantity'. Instantiate with the
	CSV filename and call the instance methods to load data and
	compute metrics.
	"""

	def __init__(self, filename):
		"""Initialize the analyzer with a CSV filename.

		Args:
			filename (str): Path to the CSV file to analyze.
		"""
		self.filename = filename
		self.data = []

	def load_data(self):
		"""Load CSV rows into memory as a list of dictionaries.

		Returns:
			list: The list of row dictionaries read from the CSV.
		"""
		with open(self.filename, mode='r', newline='') as f:
			reader = csv.DictReader(f)
			self.data = [row for row in reader]
		return self.data

	def calculate_total_sales(self):
		"""Calculate the total sales (price * quantity) for all rows.

		If data has not been loaded yet this method will call
		`load_data()` internally.

		Returns:
			float: Total sales value.
		"""
		if not self.data:
			self.load_data()

		total = 0.0
		for row in self.data:
			price = float(row['price'])
			quantity = int(row['quantity'])
			total += price * quantity
		return total

	def find_top_product(self):
		"""Find the product with the highest total revenue.

		If data has not been loaded yet this method will call
		`load_data()` internally. Handles FileNotFoundError and ValueError
		with informative error messages.

		Returns:
			tuple|None: A tuple `(product_name, revenue)` for the top
			product, or `None` if no products are present or on error.
		"""
		try:
			if not self.data:
				self.load_data()

			totals = {}
			for row_num, row in enumerate(self.data, start=1):
				try:
					name = row.get('product_name') or row.get('product') or 'Unknown'
					price = float(row['price'])
					quantity = int(row['quantity'])
					totals[name] = totals.get(name, 0.0) + price * quantity
				except ValueError as e:
					print(f"Warning: Invalid data in row {row_num}: {row}. Error: {e}. Skipping this row.")
					continue

			if not totals:
				print("Warning: No valid products found in the data.")
				return None

			top_product = max(totals.items(), key=lambda x: x[1])
			return top_product
		except FileNotFoundError:
			print(f"Error: The file '{self.filename}' was not found.")
			print("Please ensure the CSV file exists in the current directory.")
			return None
		except KeyError as e:
			print(f"Error: Missing required column {e} in CSV file.")
			print("Expected columns: 'product_name' (or 'product'), 'price', 'quantity'")
			return None


if __name__ == "__main__":
	sales_data_file = 'Python Sales.csv'
	analyzer = SalesAnalyzer(sales_data_file)
	try:
		total_sales = analyzer.calculate_total_sales()
		print(f"Total sales from {sales_data_file}: ${total_sales:.2f}")
	except FileNotFoundError:
		print(f"Error: The file '{sales_data_file}' was not found.")
		print("Please ensure the CSV file exists in the current directory.")