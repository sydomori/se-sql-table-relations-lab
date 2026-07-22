# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = """
 SELECT firstName, lastName, jobTitle
 FROM employees
 JOIN offices ON employees.officeCode = offices.officeCode
 WHERE offices.city = 'Boston'
"""
print (pd.read_sql(df_boston,conn))

# STEP 2
# Replace None with your code
df_zero_emp = """
SELECT offices.officeCode, COUNT(employees.employeeNumber) AS total_employees
FROM offices
LEFT JOIN employees USING (officeCode)
GROUP BY offices.officeCode
HAVING total_employees = 0
"""
print (pd.read_sql(df_zero_emp,conn))

# STEP 3
# Replace None with your code
df_employee = """
 SELECT firstName, lastName, city, state
 FROM employees
 LEFT JOIN offices USING (officeCode)
 ORDER BY firstName, lastName
"""
print (pd.read_sql(df_employee,conn))

# STEP 4
# Replace None with your code
df_contacts = """
 SELECT contactFirstName,
        contactLastName,
        phone,
        salesRepEmployeeNumber
 FROM customers
 LEFT JOIN orders USING (customerNumber)
 WHERE orders.customerNumber IS NULL
 ORDER BY contactLastName
"""
print (pd.read_sql(df_contacts,conn))

# STEP 5
# Replace None with your code
df_payment = """
 SELECT contactFirstName, contactLastName, amount, paymentDate
 FROM customers
 JOIN payments USING (customerNumber)
 ORDER BY CAST(amount AS FLOAT) DESC
"""
print (pd.read_sql(df_payment,conn))

# STEP 6
# Replace None with your code
df_credit = """
 SELECT employeeNumber, 
        firstName, 
        lastName,
        COUNT(customers.customerNumber) AS total_customers
 FROM employees
 JOIN customers ON employees.emploeeNumber = customers.salesRepEmployeeNumber
 GROUP BY employees.employeeNumber
 HAVING AVG(customers.creditLimit) > 90000
 ORDER BY total_customers DESC
"""

# STEP 7
# Replace None with your code
df_product_sold = """
 SELECT 
    productName,
    COUNT(orderdetails.orderNumber) AS numorders,
    SUM(orderdetails.quantityOrdered) AS totalunits
 FROM products
 JOIN orderdetails ON products.productCode = orderdetails.productCode
 GROUP BY products.productCode
 ORDER BY totalunits DESC
"""

# STEP 8
# Replace None with your code
df_total_customers = """
 SELECT 
    productName,
    products.productCode,
    COUNT(DISTINCT customers.customerNumber) AS numpurchasers
 FROM products
 JOIN orderdetails ON products.productCode = orderdetails.productCode
 JOIN orders ON orderdetails.orderNumber = orders.orderNumber
 JOIN customers ON orders.customerNumber = customers.customerNumber
 GROUP BY products.productCode
 ORDER BY numpurchasers DESC
"""

# STEP 9
# Replace None with your code
df_customers = """
 SELECT 
    offices.officeCode,
    offices.city,
    COUNT(customers.customerNumber) AS n_customers
 FROM offices
 LEFT JOIN employees ON offices.officeCode = employees.officeCode
 LEFT JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
 GROUP BY offices.officeCode
"""

# STEP 10
# Replace None with your code
df_under_20 = """
 SELECT DISTINCT employeeNumber, firstName, lastName, city, offices.officeCode
 FROM employees
 JOIN offices ON offices.officeCode = employees.officeCode
 JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
 JOIN orders ON customers.customerNumber = orders.customerNumber
 JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
 WHERE orderdetails.productCode IN (
    SELECT products.productCode
    FROM products
    JOIN orderdetails ON products.productCode = orderdetails.productCode
    JOIN orders ON orderdetails.orderNumber = orders.orderNumber
    JOIN customers ON orders.customerNumber = customers.customerNumber
    GROUP BY products.productCode
    HAVING COUNT(DISTINCT customers.customerNumber) < 20
)
"""
print (pd.read_sql(df_under_20,conn))

conn.close()
"""
SELECT products.productCode, productName, COUNT(DISTINCT customers.customerNumber) AS numpurchasers
 FROM products
 JOIN orderdetails ON products.productCode = orderdetails.productCode
 JOIN orders ON orderdetails.orderNumber = orders.orderNumber
 JOIN customers ON orders.customerNumber = customers.customerNumber
 GROUP BY products.productCode
 HAVING numpurchasers < 20

"""