import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

# STEP 1
df_boston = """
 SELECT firstName, lastName
 FROM employees
 JOIN offices ON employees.officeCode = offices.officeCode
 WHERE offices.city = 'Boston'
"""
df_boston = pd.read_sql(df_boston, conn)
print(df_boston)

# STEP 2
df_zero_emp = """
SELECT offices.officeCode, COUNT(employees.employeeNumber) AS total_employees
FROM offices
LEFT JOIN employees USING (officeCode)
GROUP BY offices.officeCode
HAVING total_employees = 0
"""
df_zero_emp = pd.read_sql(df_zero_emp, conn)
print(df_zero_emp)

# STEP 3
df_employee = """
 SELECT firstName, lastName, city, state
 FROM employees
 LEFT JOIN offices USING (officeCode)
 ORDER BY firstName, lastName
"""
df_employee = pd.read_sql(df_employee, conn)
print(df_employee)

# STEP 4
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
df_contacts = pd.read_sql(df_contacts, conn)
print(df_contacts)

# STEP 5
df_payment = """
 SELECT contactFirstName, contactLastName, amount, paymentDate
 FROM customers
 JOIN payments USING (customerNumber)
 ORDER BY CAST(amount AS FLOAT) DESC
"""
df_payment = pd.read_sql(df_payment, conn)
print(df_payment)

# STEP 6
df_credit = """
 SELECT employeeNumber, 
        firstName, 
        lastName,
        COUNT(customers.customerNumber) AS total_customers
 FROM employees
 JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
 GROUP BY employees.employeeNumber
 HAVING AVG(customers.creditLimit) > 90000
 ORDER BY total_customers DESC
"""
df_credit = pd.read_sql(df_credit, conn)
print(df_credit)

# STEP 7
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
df_product_sold = pd.read_sql(df_product_sold, conn)
print(df_product_sold)

# STEP 8
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
df_total_customers = pd.read_sql(df_total_customers, conn)
print(df_total_customers)

# STEP 9
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
df_customers = pd.read_sql(df_customers, conn)
print(df_customers)

# STEP 10
df_under_20 = """
 SELECT DISTINCT employeeNumber, firstName, lastName, offices.city, offices.officeCode
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
ORDER BY lastName, firstName
"""
df_under_20 = pd.read_sql(df_under_20, conn)
print(df_under_20)

conn.close()