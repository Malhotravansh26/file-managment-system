import streamlit as st
from hello import Bank


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Simple Bank App",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Welcome to Streamlit Bank")


# ---------------- SIDEBAR ----------------
menu = st.sidebar.selectbox(
    "Choose Action",
    [
        "Create Account",
        "Deposit",
        "Withdraw",
        "Show Details",
        "Update Info",
        "Delete Account"
    ]
)


# =========================================================
# CREATE ACCOUNT
# =========================================================

if menu == "Create Account":

    st.subheader("🆕 Create New Account")

    name = st.text_input("Your Name")
    age = st.number_input(
        "Your Age",
        min_value=0,
        max_value=150,
        step=1
    )
    email = st.text_input("Your Email")
    pin = st.text_input(
        "4-digit PIN",
        type="password",
        max_chars=4
    )

    if st.button("Create Account", type="primary"):

        if not name or not email or not pin:
            st.warning("⚠️ Please fill all fields.")

        elif not pin.isdigit():
            st.error("❌ PIN must contain only digits.")

        elif len(pin) != 4:
            st.error("❌ PIN must contain exactly 4 digits.")

        elif age < 18:
            st.error("❌ You must be 18 or above.")

        else:

            user, msg = Bank.create_account(
                name,
                int(age),
                email,
                pin
            )

            if user:

                st.success(msg)

                # IMPORTANT:
                # Your Bank class uses "accountNo", NOT "accountNo."
                st.info(
                    f"🏦 Your Account Number: {user['accountNo']}"
                )

                st.warning(
                    "⚠️ Please save your account number safely."
                )

            else:
                st.error(msg)


# =========================================================
# DEPOSIT
# =========================================================

elif menu == "Deposit":

    st.subheader("💰 Deposit Money")

    acc_no = st.text_input("Account Number")

    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4
    )

    amount = st.number_input(
        "Amount",
        min_value=1,
        step=1
    )

    if st.button("Deposit", type="primary"):

        if not acc_no or not pin:
            st.warning("⚠️ Please enter Account Number and PIN.")

        elif not pin.isdigit():
            st.error("❌ PIN must contain only digits.")

        elif len(pin) != 4:
            st.error("❌ PIN must contain exactly 4 digits.")

        else:

            success, msg = Bank.deposit(
                acc_no,
                int(pin),
                int(amount)
            )

            if success:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ {msg}")


# =========================================================
# WITHDRAW
# =========================================================

elif menu == "Withdraw":

    st.subheader("💸 Withdraw Money")

    acc_no = st.text_input("Account Number")

    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4
    )

    amount = st.number_input(
        "Amount",
        min_value=1,
        step=1
    )

    if st.button("Withdraw", type="primary"):

        if not acc_no or not pin:
            st.warning("⚠️ Please enter Account Number and PIN.")

        elif not pin.isdigit():
            st.error("❌ PIN must contain only digits.")

        elif len(pin) != 4:
            st.error("❌ PIN must contain exactly 4 digits.")

        else:

            success, msg = Bank.withdraw(
                acc_no,
                int(pin),
                int(amount)
            )

            if success:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ {msg}")


# =========================================================
# SHOW DETAILS
# =========================================================

elif menu == "Show Details":

    st.subheader("👤 Account Details")

    acc_no = st.text_input("Account Number")

    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4
    )

    if st.button("Show Details", type="primary"):

        if not acc_no or not pin:
            st.warning("⚠️ Please enter Account Number and PIN.")

        elif not pin.isdigit():
            st.error("❌ PIN must contain only digits.")

        elif len(pin) != 4:
            st.error("❌ PIN must contain exactly 4 digits.")

        else:

            user = Bank.find_user(
                acc_no,
                int(pin)
            )

            if user:

                # Don't display PIN
                safe_user = user.copy()
                safe_user.pop("pin", None)

                st.success("✅ Account found!")

                st.write("### Account Information")

                st.write(
                    f"**Name:** {safe_user.get('name', 'N/A')}"
                )

                st.write(
                    f"**Age:** {safe_user.get('age', 'N/A')}"
                )

                st.write(
                    f"**Email:** {safe_user.get('email', 'N/A')}"
                )

                st.write(
                    f"**Account Number:** {safe_user.get('accountNo', 'N/A')}"
                )

                st.write(
                    f"**Balance:** ₹{safe_user.get('balance', 0)}"
                )

            else:
                st.error("❌ No account found.")


# =========================================================
# UPDATE INFO
# =========================================================

elif menu == "Update Info":

    st.subheader("✏️ Update Your Information")

    acc_no = st.text_input("Account Number")

    pin = st.text_input(
        "Current PIN",
        type="password",
        max_chars=4
    )

    name = st.text_input("New Name (Optional)")

    email = st.text_input("New Email (Optional)")

    new_pin = st.text_input(
        "New PIN (Optional)",
        type="password",
        max_chars=4
    )

    if st.button("Update Information", type="primary"):

        if not acc_no or not pin:
            st.warning(
                "⚠️ Account Number and Current PIN are required."
            )

        elif not pin.isdigit():
            st.error("❌ Current PIN must contain only digits.")

        elif len(pin) != 4:
            st.error("❌ Current PIN must contain exactly 4 digits.")

        elif new_pin and (
            not new_pin.isdigit() or len(new_pin) != 4
        ):
            st.error("❌ New PIN must contain exactly 4 digits.")

        else:

            success, msg = Bank.update_user(
                acc_no,
                int(pin),
                name if name else None,
                email if email else None,
                new_pin if new_pin else None
            )

            if success:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ {msg}")


# =========================================================
# DELETE ACCOUNT
# =========================================================

elif menu == "Delete Account":

    st.subheader("🗑️ Delete Account")

    st.warning(
        "⚠️ This action is permanent. Your account will be deleted."
    )

    acc_no = st.text_input("Account Number")

    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4
    )

    confirm = st.checkbox(
        "I understand that this account will be permanently deleted."
    )

    if st.button("Delete Account", type="primary"):

        if not confirm:
            st.warning("⚠️ Please confirm account deletion.")

        elif not acc_no or not pin:
            st.warning("⚠️ Please enter Account Number and PIN.")

        elif not pin.isdigit():
            st.error("❌ PIN must contain only digits.")

        elif len(pin) != 4:
            st.error("❌ PIN must contain exactly 4 digits.")

        else:

            success, msg = Bank.delete_user(
                acc_no,
                int(pin)
            )

            if success:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ {msg}")