import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
import os


def init_database():
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employee (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            employee_surname TEXT NOT NULL,
            employee_cell_number TEXT,
            employee_email TEXT UNIQUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_surname TEXT NOT NULL,
            customer_cell_number TEXT,
            customer_email TEXT,
            billing_address TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            product_price REAL NOT NULL,
            product_quantity INTEGER NOT NULL DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT NOT NULL,
            product_name TEXT NOT NULL,
            sale_total REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()


class PersonManager(ABC):
    def __init__(self, db_name='store.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
    
    @abstractmethod
    def insert_person(self, **kwargs):
        pass
    
    @abstractmethod
    def remove_person(self, person_id):
        pass
    
    @abstractmethod
    def display_all(self):
        pass


class EmployeeManager(PersonManager):
    def insert_person(self, name, surname, cell_number, email):
        try:
            self.cursor.execute('''
                INSERT INTO Employee (employee_name, employee_surname, employee_cell_number, employee_email)
                VALUES (?, ?, ?, ?)
            ''', (name, surname, cell_number, email))
            self.conn.commit()
            print(f"Employee {name} {surname} added successfully!")
            return True
        except sqlite3.IntegrityError:
            print("Error: Email already exists!")
            return False
        except Exception as e:
            print(f"Error adding employee: {e}")
            return False
    
    def remove_person(self, employee_id):
        try:
            self.cursor.execute("DELETE FROM Employee WHERE employee_id = ?", (employee_id,))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                print(f"Employee ID {employee_id} removed successfully!")
                return True
            else:
                print("Employee not found!")
                return False
        except Exception as e:
            print(f"Error removing employee: {e}")
            return False
    
    def display_all(self):
        try:
            self.cursor.execute("SELECT * FROM Employee")
            employees = self.cursor.fetchall()
            
            if not employees:
                print("No employees found!")
                return
            
            print("\n" + "="*80)
            print(f"{'ID':<5} {'Name':<15} {'Surname':<15} {'Cell Number':<15} {'Email':<20}")
            print("="*80)
            for emp in employees:
                print(f"{emp[0]:<5} {emp[1]:<15} {emp[2]:<15} {emp[3] if emp[3] else 'N/A':<15} {emp[4] if emp[4] else 'N/A':<20}")
            print("="*80)
        except Exception as e:
            print(f"Error displaying employees: {e}")


class CustomerManager(PersonManager):
    def insert_person(self, name, surname, cell_number, email, billing_address):
        try:
            self.cursor.execute('''
                INSERT INTO Customer (customer_name, customer_surname, customer_cell_number, customer_email, billing_address)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, surname, cell_number, email, billing_address))
            self.conn.commit()
            print(f"Customer {name} {surname} added successfully!")
            return True
        except Exception as e:
            print(f"Error adding customer: {e}")
            return False
    
    def remove_person(self, customer_id):
        try:
            self.cursor.execute("DELETE FROM Customer WHERE customer_id = ?", (customer_id,))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                print(f"Customer ID {customer_id} removed successfully!")
                return True
            else:
                print("Customer not found!")
                return False
        except Exception as e:
            print(f"Error removing customer: {e}")
            return False
    
    def display_all(self):
        try:
            self.cursor.execute("SELECT * FROM Customer")
            customers = self.cursor.fetchall()
            
            if not customers:
                print("No customers found!")
                return
            
            print("\n" + "="*100)
            print(f"{'ID':<5} {'Name':<15} {'Surname':<15} {'Cell':<15} {'Email':<20} {'Billing Address':<25}")
            print("="*100)
            for cust in customers:
                print(f"{cust[0]:<5} {cust[1]:<15} {cust[2]:<15} {cust[3] if cust[3] else 'N/A':<15} "
                      f"{cust[4] if cust[4] else 'N/A':<20} {cust[5] if cust[5] else 'N/A':<25}")
            print("="*100)
        except Exception as e:
            print(f"Error displaying customers: {e}")


class Store:
    def __init__(self, db_name='store.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
    
    def add_product(self, name, price, quantity):
        try:
            self.cursor.execute('''
                INSERT INTO Product (product_name, product_price, product_quantity)
                VALUES (?, ?, ?)
            ''', (name, price, quantity))
            self.conn.commit()
            print(f"Product '{name}' added successfully!")
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
    
    def remove_product(self, product_id):
        try:
            self.cursor.execute("DELETE FROM Product WHERE product_id = ?", (product_id,))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                print(f"Product ID {product_id} removed successfully!")
                return True
            else:
                print("Product not found!")
                return False
        except Exception as e:
            print(f"Error removing product: {e}")
            return False
    
    def update_product(self, product_id, name=None, price=None, quantity=None):
        try:
            updates = []
            params = []
            
            if name:
                updates.append("product_name = ?")
                params.append(name)
            if price is not None:
                updates.append("product_price = ?")
                params.append(price)
            if quantity is not None:
                updates.append("product_quantity = ?")
                params.append(quantity)
            
            if not updates:
                print("No updates provided!")
                return False
            
            params.append(product_id)
            query = f"UPDATE Product SET {', '.join(updates)} WHERE product_id = ?"
            self.cursor.execute(query, params)
            
            if self.cursor.rowcount > 0:
                self.conn.commit()
                print(f"Product ID {product_id} updated successfully!")
                return True
            else:
                print("Product not found!")
                return False
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
    
    def display_products(self):
        try:
            self.cursor.execute("SELECT * FROM Product")
            products = self.cursor.fetchall()
            
            if not products:
                print("No products found!")
                return
            
            print("\n" + "="*70)
            print(f"{'ID':<5} {'Product Name':<25} {'Price':<15} {'Quantity':<10}")
            print("="*70)
            for prod in products:
                status = " (OUT OF STOCK)" if prod[3] == 0 else ""
                print(f"{prod[0]:<5} {prod[1]:<25} R{prod[2]:<14.2f} {prod[3]}{status}")
            print("="*70)
        except Exception as e:
            print(f"Error displaying products: {e}")
    
    def sell_product(self, product_id, quantity_to_sell):
        try:
            
            self.cursor.execute("SELECT product_name, product_price, product_quantity FROM Product WHERE product_id = ?", 
                              (product_id,))
            product = self.cursor.fetchone()
            
            if not product:
                print("Product not found!")
                return False
            
            name, price, available_qty = product
            
            
            if available_qty <= 0:
                print(f"Error: Product '{name}' is out of stock!")
                return False
            
            if available_qty < quantity_to_sell:
                print(f"Error: Insufficient quantity! Available: {available_qty}, Requested: {quantity_to_sell}")
                return False
            
            
            sale_total = price * quantity_to_sell
            sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            
            new_quantity = available_qty - quantity_to_sell
            self.cursor.execute("UPDATE Product SET product_quantity = ? WHERE product_id = ?", 
                              (new_quantity, product_id))
            
            
            self.cursor.execute('''
                INSERT INTO Sales (sale_date, product_name, sale_total)
                VALUES (?, ?, ?)
            ''', (sale_date, name, sale_total))
            
            self.conn.commit()
            print(f"Sale successful! Sold {quantity_to_sell} x {name} for R{sale_total:.2f}")
            return True
            
        except Exception as e:
            print(f"Error processing sale: {e}")
            return False
    
    def display_sales(self):
        try:
            self.cursor.execute("SELECT * FROM Sales ORDER BY sale_date DESC")
            sales = self.cursor.fetchall()
            
            if not sales:
                print("No sales recorded!")
                return
            
            print("\n" + "="*70)
            print(f"{'Sale ID':<8} {'Date':<20} {'Product':<25} {'Total':<10}")
            print("="*70)
            for sale in sales:
                print(f"{sale[0]:<8} {sale[1]:<20} {sale[2]:<25} R{sale[3]:<9.2f}")
            print("="*70)
        except Exception as e:
            print(f"Error displaying sales: {e}")


def main():
    init_database()
    
    emp_manager = EmployeeManager()
    cust_manager = CustomerManager()
    store = Store()
    
    while True:
        print("\n" + "="*50)
        print("       STORE MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Employee Management")
        print("2. Customer Management") 
        print("3. Product Management")
        print("4. Sales Management")
        print("5. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            employee_menu(emp_manager)
        elif choice == '2':
            customer_menu(cust_manager)
        elif choice == '3':
            product_menu(store)
        elif choice == '4':
            sales_menu(store)
        elif choice == '5':
            print("Thank you for using Store Management System. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1-5.")

def employee_menu(emp_manager):
    while True:
        print("\n--- EMPLOYEE MANAGEMENT ---")
        print("1. Add Employee")
        print("2. Remove Employee")
        print("3. Display All Employees")
        print("4. Back to Main Menu")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            name = input("Enter first name: ")
            surname = input("Enter surname: ")
            cell = input("Enter cell number: ")
            email = input("Enter email: ")
            emp_manager.insert_person(name, surname, cell, email)
            
        elif choice == '2':
            emp_id = input("Enter employee ID to remove: ")
            if emp_id.isdigit():
                emp_manager.remove_person(int(emp_id))
            else:
                print("Invalid ID!")
                
        elif choice == '3':
            emp_manager.display_all()
            
        elif choice == '4':
            break
        else:
            print("Invalid choice!")

def customer_menu(cust_manager):
    while True:
        print("\n--- CUSTOMER MANAGEMENT ---")
        print("1. Add Customer")
        print("2. Remove Customer")
        print("3. Display All Customers")
        print("4. Back to Main Menu")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            name = input("Enter first name: ")
            surname = input("Enter surname: ")
            cell = input("Enter cell number: ")
            email = input("Enter email: ")
            address = input("Enter billing address: ")
            cust_manager.insert_person(name, surname, cell, email, address)
            
        elif choice == '2':
            cust_id = input("Enter customer ID to remove: ")
            if cust_id.isdigit():
                cust_manager.remove_person(int(cust_id))
            else:
                print("Invalid ID!")
                
        elif choice == '3':
            cust_manager.display_all()
            
        elif choice == '4':
            break
        else:
            print("Invalid choice!")

def product_menu(store):
    while True:
        print("\n--- PRODUCT MANAGEMENT ---")
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Update Product")
        print("4. Display All Products")
        print("5. Back to Main Menu")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            name = input("Enter product name: ")
            try:
                price = float(input("Enter price: "))
                qty = int(input("Enter quantity: "))
                store.add_product(name, price, qty)
            except ValueError:
                print("Invalid price or quantity!")
                
        elif choice == '2':
            prod_id = input("Enter product ID to remove: ")
            if prod_id.isdigit():
                store.remove_product(int(prod_id))
            else:
                print("Invalid ID!")
                
        elif choice == '3':
            prod_id = input("Enter product ID to update: ")
            if not prod_id.isdigit():
                print("Invalid ID!")
                continue
            
            print("Leave blank if you don't want to update that field")
            name = input("New name: ") or None
            price_input = input("New price: ")
            price = float(price_input) if price_input else None
            qty_input = input("New quantity: ")
            qty = int(qty_input) if qty_input else None
            
            store.update_product(int(prod_id), name, price, qty)
                
        elif choice == '4':
            store.display_products()
            
        elif choice == '5':
            break
        else:
            print("Invalid choice!")

def sales_menu(store):
    while True:
        print("\n--- SALES MANAGEMENT ---")
        print("1. Sell Product")
        print("2. Display Sales History")
        print("3. Back to Main Menu")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            store.display_products()
            prod_id = input("Enter product ID to sell: ")
            if not prod_id.isdigit():
                print("Invalid ID!")
                continue
            
            try:
                qty = int(input("Enter quantity to sell: "))
                if qty <= 0:
                    print("Quantity must be greater than 0!")
                    continue
                store.sell_product(int(prod_id), qty)
            except ValueError:
                print("Invalid quantity!")
                
        elif choice == '2':
            store.display_sales()
            
        elif choice == '3':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()