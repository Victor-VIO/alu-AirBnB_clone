#!/usr/bin/python3
from models import storage
from models.user import User

# Create a new user
user1 = User()
user1.email = "user1@example.com"
user1.password = "password123"
user1.first_name = "John"
user1.last_name = "Doe"
user1.save()
print(f"Created user: {user1}")

# Create another user
user2 = User()
user2.email = "user2@example.com"
user2.password = "secret456"
user2.first_name = "Jane"
user2.last_name = "Smith"
user2.save()
print(f"Created user: {user2}")

# Show all users
print("\nAll users:")
all_users = storage.all()
for key, user in all_users.items():
    if key.startswith("User."):
        print(user)
