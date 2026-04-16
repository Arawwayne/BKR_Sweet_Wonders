dictt = {
    'sos': "lala"
}

try:
    employees = dictt.get("employees", [])
    if employees == []:
        employees = dictt.get("sos")
except:
    pass

print(employees)