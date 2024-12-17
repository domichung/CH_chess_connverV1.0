import Sys_reedom

Sys_reedom.initialize_json()
input_amount = int(input("輸入金額: "))
code = Sys_reedom.generate_redeem_code(input_amount)
print(f"生成的兌換碼: {code}")