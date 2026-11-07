import os
from supabase import create_client, Client


# supabase API aufrufen mit meinen Daten:
url: str = "https://votbgrjdgafnswzoredm.supabase.co"
key: str = "sb_publishable_0pN3AOWc7iDKmW-VcZbFSg_csFGpnib"

supabase: Client = create_client(url, key)




#Funktionen

def start():
    response = supabase.table('liste').select('*').execute()
    return response.data



#Die eigentliche Liste mit den gefundenen Datenbank-Einträgen versteckt sich in der Eigenschaft .data.
def vorhanden(ItemName):
    response = supabase.table('liste').select('*').eq('item', ItemName).execute()

    if not response.data:
        return False
    else:
        return True


#supabase.table('liste').insert({"item": "Apfel"}).execute()
def addItem(ItemName):
    schon_da = vorhanden(ItemName)

    if not schon_da:
        supabase.table('liste').insert({"item": ItemName}).execute()
    else:
        print("Das item ist bereits vorhanden")


# Item löschen
# supabase.table('liste').delete().eq('id', 15).execute()

def delete(ItemName):
    supabase.table('liste').delete().eq('item', ItemName).execute()