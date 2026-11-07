import flet as ft
import db 
# für real-time updaten
import time       
import threading  

import os

def main(page: ft.Page):
    page.title = "Gemeinsame Einkaufsliste"
    page.window_width = 400  
    page.window_height = 700

    eingabefeld = ft.TextField(hint_text="Was brauchen wir?", expand=True)
    artikel_liste_ui = ft.Column() 

    def lade_liste():
        artikel_liste_ui.controls.clear() 
        
        daten = db.start() 
        
        for eintrag in daten:
            item_name = eintrag['item']
            
            zeile = ft.Row([
                ft.Text(item_name, expand=True),
                ft.IconButton(
                    # GEÄNDERT: Großes I bei Icons
                    icon=ft.Icons.DELETE_OUTLINE, 
                    icon_color="red",
                    on_click=lambda e, name=item_name: loeschen_klick(name)
                )
            ])
            artikel_liste_ui.controls.append(zeile)
            
        page.update() 

    def hinzufuegen_klick(e):
        neuer_artikel = eingabefeld.value
        if neuer_artikel != "":
            db.addItem(neuer_artikel)  
            eingabefeld.value = ""     
            lade_liste()               

    def loeschen_klick(item_name):
        db.delete(item_name) 
        lade_liste()         

    def auto_aktualisierung():
            while True:
                time.sleep(3)  # Pausiert für 3 Sekunden
                lade_liste()   # Lädt die Liste neu

    # GEÄNDERT: Heißt jetzt nur noch ft.Button
    add_button = ft.Button("Hinzufügen", on_click=hinzufuegen_klick)

    # NEU: Startet den Hintergrund-Thread, der unendlich läuft
    hintergrund_aufgabe = threading.Thread(target=auto_aktualisierung, daemon=True)
    hintergrund_aufgabe.start()

    page.add(
        ft.Row([eingabefeld, add_button]),
        artikel_liste_ui
    )

    lade_liste()
    
# Fragt den Server nach seinem Port. Wenn wir lokal testen, nimmt er 8550.
port = int(os.environ.get("PORT", 8550))

# App als Webserver starten
ft.run(main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)



'''# Startet die App als Webserver in deinem Heim-WLAN (Flet 1.0 Syntax)
ft.run(main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8550)'''