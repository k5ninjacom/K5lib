"""
Alustava suunnitelma project objectista.
- ajatus on että objecti annetaan parametrina projecti kontekstin vaativille funktio kutsuille.
- Objetktin kentät:
  - projectToken
  - projectId
  - region (koska projeckti on regioonan alla)
  - mitä muuta ?
- Käyttö:
 - get project token muutetaan kutsuksi joka palauttaa project objecktin projectToken sijaan
 - muutetaan kaikki functio kutsut käyttämään project objectia erillisten kenttien sijaan
 - kuuluu todennäköisesti authenticate alle ..

"""