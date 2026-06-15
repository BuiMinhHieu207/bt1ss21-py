"""
MoMo Wallet Simulation

Author: Student
Description:
CLI application that simulates MoMo wallet operations.
"""

import logging
import os
import re


logging.basicConfig(
    filename="momo_transactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class InvalidAmountError(Exception):
    """Raised when transaction amount is invalid."""


class InsufficientBalanceError(Exception):
    """Raised when wallet balance is insufficient."""


class Wallet:
    """Represents a MoMo wallet."""

    HIGH_VALUE_LIMIT = 10_000_000

    def __init__(self):
        """Initialize wallet with zero balance."""
        self.balance = 0

    def deposit(self, amount):
        """
        Deposit money into wallet.

        Args:
            amount (int): Amount to deposit.

        Raises:
            InvalidAmountError: If amount <= 0.
        """
        if amount <= 0:
            raise InvalidAmountError(
                f"Attempted to process {amount} VND."
            )

        self.balance += amount

        logging.info(
            "Deposit successful: +%s VND. Current Balance: %s",
            amount,
            self.balance
        )

    def transfer(self, phone_number, amount):
        """
        Transfer money to another wallet.

        Args:
            phone_number (str): Receiver phone number.
            amount (int): Transfer amount.

        Raises:
            InvalidAmountError
            InsufficientBalanceError
        """
        if amount <= 0:
            raise InvalidAmountError(
                f"Attempted to process {amount} VND."
            )

        if amount > self.balance:
            raise InsufficientBalanceError(
                f"Attempted to transfer {amount} VND "
                f"with balance {self.balance} VND."
            )

        if amount >= self.HIGH_VALUE_LIMIT:
            logging.warning(
                "High value transaction detected: "
                "%s VND to %s",
                amount,
                phone_number
            )

        self.balance -= amount

        logging.info(
            "Transfer successful: -%s VND to %s. "
            "Current Balance: %s",
            amount,
            phone_number,
            self.balance
        )

    def get_balance(self):
        """
        Return current balance.

        Returns:
            int
        """
        logging.info(
            "Balance checked. Current Balance: %s",
            self.balance
        )

        return self.balance


def format_currency(amount):
    """
    Format currency with comma separator.

    Args:
        amount (int)

    Returns:
        str
    """
    return f"{amount:,}"


def validate_phone(phone_number):
    """
    Validate Vietnamese phone number.

    Args:
        phone_number (str)

    Returns:
        bool
    """
    return bool(re.fullmatch(r"\d{10}", phone_number))


def display_menu():
    """Display CLI menu."""
    print("\n========== VÍ MOMO GIẢ LẬP ==========")
    print("1. Nạp tiền vào ví")
    print("2. Chuyển tiền")
    print("3. Xem số dư hiện tại")
    print("4. Thoát chương trình")
    print("====================================")


def deposit_menu(wallet):
    """
    Handle deposit operation.

    Args:
        wallet (Wallet)
    """
    print("\n--- NẠP TIỀN VÀO VÍ ---")

    while True:
        try:
            amount = int(input("Nhập số tiền cần nạp: "))

            wallet.deposit(amount)

            print(
                f"\nNạp tiền thành công: "
                f"+{format_currency(amount)} VND"
            )

            print(
                f"Số dư hiện tại: "
                f"{format_currency(wallet.balance)} VND"
            )
            break

        except ValueError:
            print("Lỗi: Vui lòng nhập số tiền hợp lệ.")

            logging.error(
                "ValueError: Invalid numeric input for deposit."
            )

        except InvalidAmountError as error:
            print("Lỗi: Số tiền giao dịch phải lớn hơn 0.")

            logging.error(
                "InvalidAmountError: %s",
                error
            )


def transfer_menu(wallet):
    """
    Handle transfer operation.

    Args:
        wallet (Wallet)
    """
    print("\n--- CHUYỂN TIỀN ---")

    phone_number = input(
        "Nhập số điện thoại người nhận: "
    ).strip()

    if not validate_phone(phone_number):
        print("Lỗi: Số điện thoại phải gồm 10 chữ số.")
        return

    try:
        amount = int(
            input("Nhập số tiền cần chuyển: ")
        )

        wallet.transfer(phone_number, amount)

        print(
            f"\nChuyển tiền thành công tới "
            f"số điện thoại {phone_number}."
        )

        print(
            f"Số tiền đã chuyển: "
            f"{format_currency(amount)} VND"
        )

        print(
            f"Số dư còn lại: "
            f"{format_currency(wallet.balance)} VND"
        )

    except ValueError:
        print("Lỗi: Vui lòng nhập số tiền hợp lệ.")

        logging.error(
            "ValueError: Invalid numeric input for transfer."
        )

    except InvalidAmountError as error:
        print("Lỗi: Số tiền giao dịch phải lớn hơn 0.")

        logging.error(
            "InvalidAmountError: %s",
            error
        )

    except InsufficientBalanceError as error:
        print(
            "\nGiao dịch thất bại: "
            "Số dư của bạn không đủ."
        )

        print(
            f"Số dư hiện tại: "
            f"{format_currency(wallet.balance)} VND"
        )

        logging.error(
            "InsufficientBalanceError: %s",
            error
        )


def show_balance(wallet):
    """
    Display current balance.

    Args:
        wallet (Wallet)
    """
    balance = wallet.get_balance()

    print("\n--- SỐ DƯ VÍ MOMO ---")

    print(
        f"Số dư hiện tại: "
        f"{format_currency(balance)} VND"
    )


def show_transaction_history():
    """Display log history."""
    log_file = "momo_transactions.log"

    print("\n--- LỊCH SỬ GIAO DỊCH ---")

    if not os.path.exists(log_file):
        print(
            "Chưa có lịch sử giao dịch nào "
            "trong hệ thống."
        )
        return

    with open(
        log_file,
        "r",
        encoding="utf-8"
    ) as file:
        content = file.read()

        if content.strip():
            print(content)
        else:
            print(
                "Chưa có lịch sử giao dịch nào "
                "trong hệ thống."
            )


def main():
    """Application entry point."""
    wallet = Wallet()

    while True:
        display_menu()

        choice = input(
            "\nChọn chức năng (1-4): "
        ).strip()

        if choice == "1":
            deposit_menu(wallet)

        elif choice == "2":
            transfer_menu(wallet)

        elif choice == "3":
            show_balance(wallet)

        elif choice == "4":
            print(
                "\nCảm ơn bạn đã sử dụng dịch vụ."
            )

            logging.info("System shutdown")
            break

        else:
            print(
                "Lựa chọn không hợp lệ. "
                "Vui lòng chọn lại."
            )


if __name__ == "__main__":
    main()
