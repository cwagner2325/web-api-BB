import os

print("Sample runs for RESTful API")

print("\nInput:")
print("curl -X POST http://localhost:3000/guid/09118F5A6C7811EDBD4F88E9FE733593 -H 'Content-Type: application/json' -d '{\"user\": \"Cayden\"}'")

os.system("curl -X POST http://localhost:3000/guid/09118F5A6C7811EDBD4F88E9FE733593 -H 'Content-Type: application/json' -d '{\"user\": \"Cayden\"}'")

print("\n\nInput:")
print("curl -X POST http://localhost:3000/guid -H 'Content-Type: application/json' -d '{\"expire\": 111111111111, \"user\": \"Andrew\"}'")

os.system("curl -X POST http://localhost:3000/guid -H 'Content-Type: application/json' -d '{\"expire\": 111111111111, \"user\": \"Andrew\"}'")

print("\n\nInput:")
print("curl -X POST http://localhost:3000/guid/09118F5A6C7811EDBD4F88E9FE733593 -H 'Content-Type: application/json' -d '{\"user\": \"Updated Name\"}'")

os.system("curl -X POST http://localhost:3000/guid/09118F5A6C7811EDBD4F88E9FE733593 -H 'Content-Type: application/json' -d '{\"user\": \"Updated Name\"}'")

print("\n\nInput:")
print("curl http://localhost:3000/guid/09118F5A6C7811EDBD4F88E9FE733593")

os.system("curl http://localhost:3000/guid/09118F5A6C7811EDBD4F88E9FE733593")

print("\n\nInput:")
print("curl -X DELETE http://localhost:3000/guid/09118F5A6C7811EDBD4F88E9FE733593")

os.system("curl -X DELETE http://localhost:3000/guid/09118F5A6C7811EDBD4F88E9FE733593")

print("\n\Display all contents of database (Just for debugging purposes):")
print("curl http://localhost:3000/")

os.system("curl http://localhost:3000/")

