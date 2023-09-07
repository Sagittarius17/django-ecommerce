import sqlite3

# def inspect_and_fix_invalid_foreign_keys(conn):
#     c = conn.cursor()

#     # Check if any ShippingAddress row has an invalid Customer reference.
#     c.execute('''
#         SELECT id, customer_id
#         FROM ecommerce_shippingaddress
#         WHERE customer_id NOT IN (SELECT id FROM ecommerce_customer);
#     ''')
#     problematic_rows = c.fetchall()

#     for row in problematic_rows:
#         print(f"Found problematic row with id {row[0]} pointing to non-existent customer id {row[1]}.")

#     # You can delete these rows, or update them. For now, I'll show the delete option:
#     c.execute('''
#         DELETE FROM ecommerce_shippingaddress
#         WHERE customer_id NOT IN (SELECT id FROM ecommerce_customer);
#     ''')

#     print(f"Deleted {c.rowcount} problematic rows from ecommerce_shippingaddress.")

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

table_name = input("Enter table name: ")
# id = input("Enter id: ")

# if table_name == "ecommerce_shippingaddress":
#     inspect_and_fix_invalid_foreign_keys(conn)

# Delete all rows from table
# c.execute(f'DELETE FROM {table_name} WHERE ID = {id};')
# print(f'We have deleted {c.rowcount} records from the table {table_name}.')




# Let's say you want to copy the record with id = 1 from source_table to destination_table
record_id = input("Enter id: ")

# Fetch the record from the source_table
c.execute(f'SELECT * FROM {table_name} WHERE id = ?', (record_id,))
record = c.fetchone()

if record:
    # Insert the fetched record into the destination_table
    placeholders = ', '.join(['?'] * len(record))
    c.execute(f'INSERT INTO ecommerce_customer VALUES ({placeholders})', record)
    conn.commit()
    print(f"Record with id {record_id} copied successfully!")
else:
    print(f"No record found with id {record_id} in source_table.")

# Commit the changes to db			
conn.commit()
# Close the connection
conn.close()
