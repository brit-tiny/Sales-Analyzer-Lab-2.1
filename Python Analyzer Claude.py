import csv

class SalesAnalyzer:
	"""
	A class to analyze sales data from a CSV file.
	
	This class provides methods to load sales data, calculate total revenue,
	and identify the top-selling product based on total revenue.
	"""
	
	def __init__(self, filename):
		"""
		Initialize the SalesAnalyzer with a CSV file.
		
		Args:
			filename (str): Path to the CSV file containing sales data.
				The CSV must have 'product_name', 'price', and 'quantity' columns.
		"""
		self.filename = filename
		self.data = []
	
	def load_data(self):
		"""
		Load sales data from the CSV file into memory.
		
		Returns:
			list: A list of dictionaries where each dictionary represents a row
				from the CSV file with product information.
		
		Raises:
			FileNotFoundError: If the CSV file does not exist.
		"""
		try:
			self.data = []
			with open(self.filename, mode='r') as file:
				csv_reader = csv.DictReader(file)
				for row in csv_reader:
					try:
						# Validate and convert data types
						product = row['product_name']
						price = float(row['price'])
						quantity = int(row['quantity'])
						self.data.append({
							'product_name': product,
							'price': price,
							'quantity': quantity
						})
					except ValueError:
						print(f"Warning: Invalid data in row - price or quantity is not a valid number. Row: {row}")
						continue
					except KeyError as e:
						print(f"Warning: Missing column {e} in row: {row}")
						continue
			return self.data
		except FileNotFoundError:
			print(f"Error: The file '{self.filename}' was not found. Please check the file path and try again.")
			return []
	
	def calculate_total_sales(self):
		"""
		Calculate the total sales revenue from all products.
		
		Returns:
			float: The sum of (price * quantity) for all products in the data.
				Returns 0.0 if no data is loaded.
		"""
		if not self.data:
			self.load_data()
		
		total = sum(item['price'] * item['quantity'] for item in self.data)
		return total
	
	def find_top_product(self):
		"""
		Find the product with the highest total revenue.
		
		Returns:
			tuple: A tuple containing (product_name, revenue) where product_name
				is the name of the top-selling product and revenue is its total
				revenue (price * quantity). Returns (None, 0.0) if no data is available.
		"""
		if not self.data:
			self.load_data()
		
		if not self.data:
			return None, 0.0
		
		top_product = max(
			self.data,
			key=lambda item: item['price'] * item['quantity']
		)
		
		top_revenue = top_product['price'] * top_product['quantity']
		return top_product['product_name'], top_revenue

if __name__ == "__main__":
	sales_data_file = 'Python Sales'
	
	# Create an instance of the SalesAnalyzer
	analyzer = SalesAnalyzer(sales_data_file)
	
	# Load the data
	analyzer.load_data()
	
	# Calculate total sales
	total_sales = analyzer.calculate_total_sales()
	print(f"Total sales from {sales_data_file}: ${total_sales:.2f}")
	
	# Find and display top-selling product
	print("\n" + "="*50)
	top_product, top_revenue = analyzer.find_top_product()
	if top_product is not None:
		print(f"Top-Selling Product: {top_product}")
		print(f"Total Revenue: ${top_revenue:.2f}")
	else:
		print("No valid product data found.")
	print("="*50)