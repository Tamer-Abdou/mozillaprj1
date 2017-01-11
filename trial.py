from lxml import html
import requests
import re as regular_expression
import json

page = requests.get("https://reviewboard.mozilla.org/r/?sort=review_id&datagrid-id=datagrid-0&columns=review_id&show-closed=1&page=")
tree = html.fromstring(page.text)
print(tree)


tables = [tree.xpath('//table/tbody/tr[2]/td/center/center/font/table/tbody'),
          tree.xpath('//table/tbody/tr[5]/td/center/center/font/table/tbody')]

tabs = []

for table in tables:
    tab = []
    for row in table:
        for col in row:
            var = col.text_content()
            var = var.strip().replace(" ", "")
            var = var.split('\n')
            if regular_expression.match('^\d{4}$', var[0].strip()):
                tab_row = {}
                tab_row["href"] = var[0].strip()
                tab.append(tab_row)
    tabs.append(tab)

json_data = json.dumps(tabs)

output = open("output.txt", "w")
output.write(json_data)
output.close()