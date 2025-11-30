fullname = input("Ismingiz va familiyangizni kiriting: ")
age = input("Yoshingizni kiriting: ")

email = input("Email manzilingizni kiriting: ")
address = input("Yashash manzilingizni kiriting: ")
barchasi = input("Barcha foydalanuvchilarni korish uchun 'show' ni yozing: ")
user_data = {
    "fullname": fullname,
    "age": age,
    "email": email,
    "address": address
}

if barchasi.lower == 'show':
    print("\nFoydalanuvchi ma'lumotlari:")
    print(f"To'liq ismi: {user_data['fullname']}")
    print(f"Yoshi: {user_data['age']}")
    print(f"Email: {user_data['email']}")
    print(f"Manzil: {user_data['address']}")