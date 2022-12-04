from cashier import Transaction

transaction = Transaction()
print("Menambahkan ayam goreng dan pasta gigi.")
transaction.add_item("Ayam Goreng", 2, 20000)
transaction.add_item("Pasta Gigi", 3, 15000)
result = {
    "Ayam Goreng": {"qty": 2, "price": 20000},
    "Pasta Gigi": {"qty": 3, "price": 15000},
}
assert transaction.items == result, "Fungsi add_item bermasalah"

print("Menghapus item ayam goreng.")
transaction.delete_item("Ayam Goreng")
result.pop("Ayam Goreng")
assert transaction.items == result, "Fungsi delete_item bermasalah"

print("Menghapus semua item.")
transaction.reset_transaction()
assert transaction.items == {}, "Fungsi reset_transaction bermasalah"

transaction.add_item("Ayam Goreng", 2, 20000)
transaction.add_item("Pasta Gigi", 3, 15000)
transaction.check_order()
assert transaction.total_price() == 85000, "Fungsi total_price bermasalah"
