import pandas as pd
import requests
import json
import os
from requests.auth import HTTPBasicAuth

org = "gtechnos"
token = "8ec07ZcR2DQf619Ckg8hGCCjqo2LeNnOHIgJPLLtoHieVQQGBHHxJQQJ99BCACAAAAAZg6lNAAASAZDO1Vba"
email = "gabrielmartins@grupotechnos.com.br"

def listar_projetos_azure_devops(org, token, email):
    url = f"https://dev.azure.com/{org}/_apis/projects?api-version=7.1"

    response = requests.get(
                            url,
                            auth=HTTPBasicAuth(email, token),
                            headers={'Content-Type': 'application/json'}
                            )

    if response.status_code == 200:
        projetos = response.json().get("value", [])
        projetos_i = [{"id": projeto["id"], "name": projeto["name"]} for projeto in projetos]

        return projetos_i
    else:
        print(f"Deu ruim na hora de listar projetos: {response.status_code}: {response.text}")
        return []

def listar_itens_azure_devops(org, proj, token, email):
    url2 = f"https://dev.azure.com/{org}/{proj}/_apis/wit/wiql?api-version=7.1"

    query = {
        "query": """
        SELECT [System.Id] 
        FROM workitemLinks 
        WHERE ([Source].[System.WorkItemType] = 'Epic') 
        AND ([System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Reverse') 
        AND ([Target].[System.WorkItemType] = 'User Story') 
        MODE (DoesNotContain)
        """
    }

    response2 = requests.post(
                            url2,
                            json=query,
                            auth=HTTPBasicAuth(email, token),
                            headers={'Content-Type':'application/json'}
                            )

    if response2.status_code == 200:
        print("Deu bom!")
        dados = response2.json()

        return dados

    else:
        print(f"Deu ruim na hora de pegar os work items:{response2.text}")
        return []


lista_projetos = listar_projetos_azure_devops(org, token, email)
nome_projetos = [projeto["name"] for projeto in lista_projetos]

lista_itens = listar_itens_azure_devops(org, "Business%20Intelligence", token, email)

print(lista_projetos)
print(nome_projetos)
print(lista_itens)