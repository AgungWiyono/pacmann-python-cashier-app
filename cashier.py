import uuid
from typing import Dict, TypedDict


class TransactionRow(TypedDict):
    price: float
    qty: int


class Transaction:
    def __init__(self):
        self.id = uuid.uuid4()
        self.items: Dict[str, TransactionRow] = {}

    def show_items(self):
        """
        Show all items in transaction.
        """
        print("Item yang dibeli adalah: ", self.items)

    def add_item(self, name: str, qty: int, price: float):
        """
        Add new item along with quantity and price per item into transaction.

        Parameters
        ----------
        name : str
            Product's name.
        qty : int
            Product quantity to be inputted in transaction.
        price : float
            Product's unit price.
        """
        self.items[name] = {"price": price, "qty": qty}

    def update_item_name(self, old_name: str, new_name: str):
        """
        Update an item name inside transaction.

        Parameters
        ----------
        old_name : str
            Product's old name to be changed.
        new_name : str
            Product's new name.
        """
        data = self.items.pop(old_name, None)
        if not data:
            print("Item not found.")
            return
        self.items[new_name] = data

    def update_item_qty(self, name: str, qty: int):
        """
        Update an item quantity.

        Parameters
        ----------
        name : str
            Product name.
        qty : int
            New quantity.
        """
        data = self.items.get(name, None)
        if not data:
            print("Item not found.")
            return
        data["qty"] = qty

    def update_item_price(self, name: str, price: float):
        """
        Update item unit price.

        Parameters
        ----------
        name : str
            Product name.
        price : float
            New product unit price.
        """
        data = self.items.get(name, None)
        if not data:
            print("Item not found.")
            return
        data["price"] = price

    def delete_item(self, name: str):
        """
        Delete a product from transaction.

        Parameters
        ----------
        name : str
            Product name.
        """
        if name not in self.items:
            print("Item not found.")
            return
        del self.items[name]

    def check_order(self):
        """
        Menampilkan keseluruhan isi transaksi untuk dilakukan pengecekan
        oleh admin.
        """
        for key, value in self.items.items():
            price_total = value["price"] * value["qty"]
            text = f"{key} | {value['qty']} | {value['price']} | {price_total}"
            print(text)

    def total_price(self):
        """
        Menghitung total harga beserta diskon bila ada.
        """
        total_price = 0
        for value in self.items.values():
            price = value["price"] * value["qty"]
            total_price += price

        discounter = {500000: 0.9, 300000: 0.92, 200000: 0.95}
        for key in discounter:
            if total_price > key:
                total_price *= discounter[key]
                break

        print("Total harganya adalah: ", total_price)
        return total_price

    def reset_transaction(self):
        """
        Delete all inputted item.
        """
        self.items = {}
        print("Semua item berhasil didelete.")

    def print_order(self):
        print("Order ID ", self.id)
        self.check_order()
        self.total_price()
        print("Have a nice day!")


class TransactionRunner:
    def __init__(self):
        self.transaction = Transaction()
        self.update_dialog = {
            "name": (
                "Masukkan nama item yang baru",
                self.transaction.update_item_name,
                str,
            ),
            "qty": (
                "Masukkan kuantitas item yang baru",
                self.transaction.update_item_qty,
                int,
            ),
            "price": (
                "Masukkan harga item yang baru",
                self.transaction.update_item_price,
                float,
            ),
        }

    def ask_input(self, dialog: str, tipe: type = str) -> type:
        """
        Meminta input user dan memastikan tipe datanya sesuai.

        Parameters
        ----------
        dialog : str
            Dialog yang ditampilkan ke user
        tipe : type
            Tipe data yang diminta

        Returns
        -------
        type

        """
        while True:
            user_input = input(f"{dialog} :")
            try:
                tipe(user_input)
                return tipe(user_input)
            except Exception:
                print("Input tidak valid.")

    def check_item_existence(self, item_name: str) -> bool:
        """
        Mengecek apakah suatu item ada dalam transaksi.

        Parameters
        ----------
        item_name : str
            Nama item yang dicari

        Returns
        -------
        bool

        """
        if not self.transaction.items.get(item_name):
            print("Item tidak ditemukan.")
            print("Operasi dibatalkan.")
            return False
        return True

    def add_item(self):
        """
        Dialog wrapper untuk fungsi penambah item.
        """
        item_name = self.ask_input("Masukkan nama item")
        item_qty = self.ask_input("Masukkan kuantitas item", int)
        item_price = self.ask_input("Masukkan harga satuan item", float)

        self.transaction.add_item(item_name, item_qty, item_price)
        print(f"Item {item_name} berhasil diinput.")

    def delete_item(self):
        """
        Dialog wrapper untuk fungsi penghapus item.
        """
        item_name = self.ask_input("Masukkan nama item")
        is_valid = self.check_item_existence(item_name)
        if not is_valid:
            return

        self.transaction.delete_item(item_name)
        print(f"Item {item_name} berhasil dihapus.")

    def reset_transaction(self):
        """
        Dialog wrapper untuk fungsi reset transaksi.
        """
        self.transaction.reset_transaction()
        print("Transaksi berhasil direset.")

    def update_item(self, tipe: str):
        """
        Dialog wrapper untuk update item.

        Parameters
        ----------
        tipe : str
            Tipe perubahan [name|price|qty]
        """
        item_name = self.ask_input("Masukkan nama item yang ingin diubah")
        is_valid = self.check_item_existence(item_name)
        if not is_valid:
            return

        operation_data = self.update_dialog[tipe]
        new_input = self.ask_input(operation_data[0], operation_data[2])
        operation_data[1](item_name, new_input)
        print("Update berhasil")

    def show_actions(self):
        """
        Menampilkan daftar aksi yang ada.
        """
        actions = [
            "Menambahkan item baru",
            "Menghapus item",
            "Mengganti nama item",
            "Mengganti kuantitas item",
            "Mengganti harga item",
            "Reset transaksi",
            "Cek transaksi",
            "Hitung harga total",
            "Cetak transaksi",
        ]

        for index, value in enumerate(actions):
            print(f"{index+1}. {value}")

    def run(self):
        """
        Fungsi utama untuk menjalankan wrapper.
        """
        while True:
            self.show_actions()
            user_choice = input("Masukkan pilihan anda: ")

            if not user_choice.isdigit():
                print("Silakan masukkan nomor pilihan yang diinginkan")
                continue

            choice = int(user_choice)
            if choice < 1 or choice > 9:
                print("Silakan masukkan pilihan yang valid.")
                continue

            if choice == 1:
                self.add_item()
                print("")
            elif choice == 2:
                self.delete_item()
                print("")
            elif choice == 3:
                self.update_item("name")
                print("")
            elif choice == 4:
                self.update_item("qty")
                print("")
            elif choice == 5:
                self.update_item("price")
                print("")
            elif choice == 6:
                self.reset_transaction()
                print("")
            elif choice == 7:
                self.transaction.check_order()
                print("")
            elif choice == 8:
                self.transaction.total_price()
                print("")
            else:
                self.transaction.print_order()
                return


if __name__ == "__main__":
    runner = TransactionRunner()
    runner.run()
