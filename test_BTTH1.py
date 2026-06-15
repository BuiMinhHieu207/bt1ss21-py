import unittest

from BTTH1 import (
    Wallet,
    InvalidAmountError,
    InsufficientBalanceError
)


class TestWallet(unittest.TestCase):
    """Unit tests for Wallet class."""

    def setUp(self):
        """Create test wallet."""
        self.wallet = Wallet()

    def test_deposit_success(self):
        """Test successful deposit."""
        self.wallet.deposit(500000)

        self.assertEqual(
            self.wallet.balance,
            500000
        )

    def test_transfer_insufficient_balance(self):
        """
        Test transfer with insufficient balance.
        """
        with self.assertRaises(
            InsufficientBalanceError
        ):
            self.wallet.transfer(
                "0987654321",
                100000
            )

    def test_invalid_amount(self):
        """
        Test invalid deposit amount.
        """
        with self.assertRaises(
            InvalidAmountError
        ):
            self.wallet.deposit(-50000)


if __name__ == "__main__":
    unittest.main()
