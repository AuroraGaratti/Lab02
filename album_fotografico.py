def carica_da_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            righe = file.readlines()
            album=[]
            for riga in righe[1:]:
                if riga.strip()=="":
                    continue
                chiave=riga.split(",")
                codice = chiave[0].strip()
                titolo = chiave[1].strip()
                autore = chiave[2].strip()
                mese = int(chiave[3].strip())
                anno = int(chiave[4].strip())
                foto = {"codice": codice, "titolo": titolo, "autore": autore, "mese": mese,"anno":anno}
            #apertura file e lettura per righe, estrazione singoli valori e creazione dizionario foto
                anno_trovato = False
                for sezione in album:
                    if anno == sezione[0]:
                        sezione[1].append(foto)
                        anno_trovato=True
                        break
                if not anno_trovato:
                        album.append([anno,[foto]])
                #album è suddiviso in sezioni-anno, cerco in tutte sezioni album se nell'index 0 ho il valore anno
                # della foto già esistente e nel caso aggiungo foto a lista di foto che corrisponde a index 1 della
                # sezione, se non trovo nulla creo nuova sezione aggiungo nuova lista nell'alb
        return album
    except FileNotFoundError:
        print("File non trovato")
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):

    for sezione in album:
        for fotografia in sezione[1]:
            if codice == fotografia["codice"]:
                return None
    #doppio for per cercare per ogni sezione e per ogni foto nella sezione se il codice è gia esistente
    #rispetto quello appena inserito
    if mese<1 or mese>12:
        return None
    #valori mese ammessi
    foto = {"codice": codice, "titolo": titolo, "autore": autore, "mese": mese, "anno": anno}
    try:
        with open(file_path,"a",encoding="utf-8")as file:
            file.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
    except FileNotFoundError:
        return None
    #aggiunta della foto nel file nel caso non fosse scattato None sopra
    for sezione in album:
        if anno == sezione[0]:
            sezione[1].append(foto)
            return foto
    #ricerca nelle sezioni dell'anno inserito, se è già esistente aggiungo foto alla lista di foto nella sezione
    album.append([anno,[foto]])
    return foto
    #se l'anno inserito non esistesse creo nuova sezione da inserire nell'album

def cerca_foto(album, codice):

    for sezione in album:
        for fotografia in sezione[1]:
            if codice == fotografia["codice"]:
                foto=f"{fotografia['codice']}, {fotografia['titolo']}, {fotografia['autore']}, {fotografia['mese']}, {fotografia['anno']}"
                return foto
    #doppio ciclo for prima dividendo le sezioni e poi ciclo for degli elementi lista foto, che è index 1 della sezione,
    #se trovo codice corrispondente a quello in input fermo ciclo e restituisco dati della foto
    return None
    #se ciclo non trova alcun codice corrispondente allora resituisco None

def elenco_foto_anno_per_titolo(album, anno):
    lista_foto=[]
    for sezione in album:
        if anno == sezione[0]:
            for fotografia in sezione[1]:
                lista_foto.append(fotografia["titolo"])
            lista_foto.sort()
            return lista_foto
    #creo lista foto vuota, ora itero su tutte le sezioni e controllo di ognuna index 0 e vedo se ano corrisponde
    #a quello in input, se corrisponde itero la lista foto che corrisponde a index 1 della sezione e inserisco titoli
    #foto nella lista_foto vuota e a fine ciclo ordina i titoli
    return None

def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break


        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
