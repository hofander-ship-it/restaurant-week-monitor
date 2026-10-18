# Restaurant Week Monitor — PWA na iPhone

## Co robi
- Dodawanie linków do postów/rolek Instagram (Szczecin lub Śląsk).
- Otwieranie postów do ręcznego polubienia z zalogowanego konta @hofander.
- Oznaczanie wpisów jako „Polubione”, „Pominięte”, „Do sprawdzenia”.
- Filtry, lokalna historia, eksport CSV/JSON i import JSON.
- Instalacja na ekranie początkowym iPhone'a, możliwość pracy z zapisanymi danymi offline.

## Czego nie robi
Nie wyszukuje automatycznie postów, nie loguje się do Instagrama i nie klika „Lubię to” za użytkownika. Nie wymaga hasła do Instagrama. Status „Polubione” to własne oznaczenie użytkownika, nie weryfikacja przez Instagram.

## Uruchomienie na iPhonie (zalecane: GitHub Pages)
1. Załóż konto GitHub i utwórz nowe publiczne repozytorium, np. `restaurant-week-monitor`.
2. Prześlij **zawartość** folderu `rw-pwa` do głównego katalogu repozytorium (index.html, app.js, sw.js, manifest.webmanifest, ikony).
3. W repozytorium otwórz Settings → Pages → Build and deployment → Deploy from a branch; wybierz `main` i `/ (root)`; zapisz.
4. Poczekaj na publikację. Adres będzie zwykle `https://TWOJ_LOGIN.github.io/restaurant-week-monitor/` (dokładny adres pokaże GitHub Pages).
5. Otwórz adres na iPhonie w Safari → Udostępnij → Dodaj do ekranu początkowego → Dodaj.
6. Otwórz RW Monitor z ekranu iPhone'a. Znalezione w Instagramie linki wklejaj w formularzu. Zaloguj się w aplikacji Instagram jako @hofander, aby ręcznie polubić post po otwarciu linku.

## Ważne
- Historia zapisana jest wyłącznie w pamięci przeglądarki tego iPhone'a (localStorage). Nie synchronizuje się między urządzeniami. Eksportuj JSON na kopię zapasową.
- Hostowanie w GitHub Pages udostępnia publicznie **kod aplikacji**, ale nie udostępnia Twoich lokalnych wpisów.
- Aby korzystać na wielu urządzeniach i automatycznie pobierać posty, konieczny byłby backend i zgodne z zasadami Instagram API źródło danych.
- Serwis Instagram może zmieniać sposób obsługi linków i hashtagów.

## Test lokalny na komputerze
`python3 -m http.server 8000` w folderze projektu, następnie `http://localhost:8000`.
