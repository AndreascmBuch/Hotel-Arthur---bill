Denne microservice genererer fakturaer baseret på bookingdata fra en separat bookingservice.

Funktioner og API'er:
Databaseforbindelse: get_db_connection() opretter en forbindelse til billing-databasen, og returnerer en fejlkode, hvis forbindelsen fejler.
Bestem Sæson: determine_season(checkin_date) identificerer sæsonen for booking baseret på check-in-måned, hvilket bruges til at beregne dagsprisen.
Beregn Opholdsdage: parse_dates(checkin, checkout) beregner antal opholdsdage for at udregne totalprisen.
API Endpoints:
Opdater fakturering (/bills/update/<booking_id>, POST): Denne API bruger ovenstående funktioner til at opdatere fakturaen. JSON-data fra forespørgslen, inkl. room_type, checkin, og checkout, valideres og parses. Totalprisen beregnes ud fra antal dage, dagspris og sæson. Fakturadata indsættes eller opdateres i billing-tabellen og returneres som JSON.

Hent alle fakturaer (/bills, GET): Henter alle fakturaer fra billing-tabellen, formatterer dem som JSON og returnerer dem.

Hent specifik faktura (/bills/<id>, GET): Finder en faktura baseret på ID. Returnerer JSON med fakturadata eller en fejlkode, hvis ID'et ikke findes.