from operator import index

import pandas as pd
import requests
import json
import os

from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray
from requests.auth import HTTPBasicAuth

org = "gtechnos"
proj = "Business%20Intelligence"
token = "8ec07ZcR2DQf619Ckg8hGCCjqo2LeNnOHIgJPLLtoHieVQQGBHHxJQQJ99BCACAAAAAZg6lNAAASAZDO1Vba"
email = "gabrielmartins@grupotechnos.com.br"

url = f"https://dev.azure.com/{org}/{proj}/_apis/wit/wiql?api-version=7.1"

wiql_query = {
    "query": """
    SELECT [System.Id] 
    FROM workitemLinks 
    WHERE ([Source].[System.WorkItemType] = 'Epic') 
    AND ([System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Reverse') 
    AND ([Target].[System.WorkItemType] = 'User Story') 
    MODE (DoesNotContain)
    """
}

response = requests.post(
                        url,
                        json=wiql_query,
                        auth=HTTPBasicAuth(email, token),
                        headers={'Content-Type':'application/json'}
                         )

listaids = []

if response.status_code == 200:
    print("Deu bom")
    data = response.json()
    workitems = data.get("workItems", [])
    for item in workitems:
        listaids.append(item["id"])

else:
    print(f"Deu ruim: {response.text}")

strids = ",".join(map(str, listaids))
print(listaids)
print(strids)

url_workitems = f"https://dev.azure.com/{org}/{proj}/_apis/wit/workitems?ids={strids}&fields=System.Id,System.Title,System.State,Microsoft.VSTS.Scheduling.TargetDate,System.CreatedDate,System.ChangedDate,System.BoardColumn,System.Description&api-version=7.1"

response2 = requests.get(
                        url_workitems,
                        auth=HTTPBasicAuth(email, token),
                        headers={'Content-Type':'application/json'}
                        )

if response2.status_code == 200:
    print("Deu bom2")
    data2 = response2.json()
    df = pd.json_normalize(data2, 'value')
    df.to_excel(r"C:\Users\gabrielmartins\Desktop\Projeto de BI\Azure.xlsx", index=False)

else:
    print(f"Deu ruim2: {response2.text}")