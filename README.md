# Restaurant Week Monitor — wersja automatyczna

Monitor na iPhone, konto @hofander, Szczecin i Śląsk.

## Co jest automatyczne

GitHub Actions uruchamia co około 6 godzin skrypt `scripts/monitor.py`, który sprawdza publiczne wyniki Bing RSS pod kątem bezpośrednich linków do postów/reels Instagram. Znalezione linki zapisuje do `discovered.json`. Aplikacja przy otwarciu pobiera wyniki i dodaje nowe do lokalnej listy. Można też nacisnąć **Sprawdź nowe wyniki**.

**Ograniczenie:** publiczne wyszukiwarki indeksują tylko niewielką część Instagrama; możliwe jest 0 wyników. Nie jest to pełne monitorowanie hasztagów ani API Instagrama. Skrypt nie loguje się na Instagram, nie lajkuje i nie zbiera prywatnych danych. Oznaczenie „Polubione” to wyłącznie Twoja notatka.

## Aktualizacja istniejącego repozytorium

1. Otwórz `https://github.com/hofander-ship-it/restaurant-week-monitor/upload/main` w Safari.
2. Rozpakuj ZIP i prześlij **zawartość** paczki, zachowując folder `.github/workflows` i `scripts` (na iOS przesyłanie folderów bywa utrudnione). Alternatywnie użyj komputera albo edytora GitHub do stworzenia obu plików w folderach.
3. Zatwierdź zmiany w `main` (nadpisz pliki `index.html`, `app.js`, `sw.js`, `README.md`).
4. GitHub → repozytorium → Settings → Actions → General → Workflow permissions: **Read and write permissions** (jeśli dostępne; konieczne do automatycznego zapisu `discovered.json`).
5. Zakładka **Actions** → **Public post discovery** → **Run workflow** (pierwszy raz ręcznie). Następne uruchomienia są planowane co około 6 godzin, ale GitHub może je opóźniać.
6. Otwórz aplikację w Safari, odśwież, wybierz „Sprawdź nowe wyniki”.

Uwaga: na iPhonie GitHub web może nie zachować struktury folderów przy wielokrotnym wyborze plików. W razie potrzeby dodaj `scripts/monitor.py` i `.github/workflows/monitor.yml` przez GitHub **Add file → Create new file**, wpisując pełną ścieżkę.

## Prywatność

Historia polubień i pominięć jest przechowywana lokalnie w przeglądarce i nie synchronizuje się między urządzeniami. GitHub Pages i `discovered.json` są publiczne; nie umieszczaj w repozytorium haseł ani tokenów.
