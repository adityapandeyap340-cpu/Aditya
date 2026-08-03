import mysql.connector
import matplotlib.pyplot as plt

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root@2403",
        database="Fashion_store"
    )

    if conn.is_connected():
        print("Connected Successfully to MySQL")

    cur = conn.cursor()

    while True:

        print("\n========== FASHION STORE MENU ==========")
        print("1. Add Record")
        print("2. Delete Record")
        print("3. Update Record")
        print("4. Display Records")
        print("5. Graphical Representation")
        print("6. Exit")

        choice = int(input("\nEnter your choice (1-6): "))

        # ---------------- ADD RECORD ----------------
        if choice == 1:

            pid = input("Enter Product ID: ")
            pname = input("Enter Product Name: ")
            brand = input("Enter Brand Name: ")
            price = int(input("Enter Price: "))

            sql = """
            INSERT INTO store
            (Product_id, Product_name, Brand_name, Price)
            VALUES (%s, %s, %s, %s)
            """

            values = (pid, pname, brand, price)

            cur.execute(sql, values)
            conn.commit()

            print("Record Added Successfully.")

        # ---------------- DELETE RECORD ----------------
        elif choice == 2:

            cur.execute("SELECT * FROM store")
            rows = cur.fetchall()

            print("\n========== CURRENT RECORDS ==========\n")

            for row in rows:
                print(row)

            pid = input("\nEnter Product ID to Delete: ")

            ch = input("Are you sure (Y/N): ")

            if ch.upper() == "Y":
                cur.execute(
                    "DELETE FROM store WHERE Product_id=%s",
                    (pid,)
                )

                conn.commit()

                print("Record Deleted Successfully.")

            else:
                print("Delete Cancelled.")

        # ---------------- UPDATE RECORD ----------------
        elif choice == 3:

            cur.execute("SELECT * FROM store")
            rows = cur.fetchall()

            print("\n========== CURRENT RECORDS ==========\n")

            for row in rows:
                print(row)

            pid = input("\nEnter Product ID to Update: ")

            pname = input("Enter New Product Name: ")
            brand = input("Enter New Brand Name: ")
            price = int(input("Enter New Price: "))

            sql = """
            UPDATE store
            SET Product_name=%s,
                Brand_name=%s,
                Price=%s
            WHERE Product_id=%s
            """

            values = (pname, brand, price, pid)

            cur.execute(sql, values)
            conn.commit()

            print("Record Updated Successfully.")

        # ---------------- DISPLAY RECORD ----------------
        elif choice == 4:

            cur.execute("SELECT * FROM store")
            rows = cur.fetchall()

            print("\n========== PRODUCT LIST ==========\n")

            print("{:<12} {:<20} {:<20} {:<10}".format(
                "Product ID",
                "Product Name",
                "Brand Name",
                "Price"
            ))

            print("-" * 70)

            for row in rows:
                print("{:<12} {:<20} {:<20} {:<10}".format(
                    row[0],
                    row[1],
                    row[2],
                    row[3]
                ))

        # ---------------- BAR GRAPH ----------------
        elif choice == 5:

            cur.execute("SELECT Product_name, Price FROM store")
            rows = cur.fetchall()

            if len(rows) == 0:
                print("No records found.")

            else:

                product = []
                price = []

                for row in rows:
                    product.append(row[0])
                    price.append(row[1])

                plt.figure(figsize=(8,5))
                plt.bar(product, price)

                plt.title("Product Price Bar Graph")
                plt.xlabel("Product Name")
                plt.ylabel("Price")
                plt.grid(axis="y")

                plt.show()

        # ---------------- EXIT ----------------
        elif choice == 6:

            print("Thank You!")
            break

        else:
            print("Invalid Choice.")

    cur.close()
    conn.close()

except mysql.connector.Error as err:
    print("Database Error:", err)

except ValueError:
    print("Please enter a valid number.")
