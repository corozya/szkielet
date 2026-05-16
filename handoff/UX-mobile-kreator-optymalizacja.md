# Zadanie: Optymalizacja UX Kreatora na urządzeniach mobilnych

## Status: Do analizy / wdrożenia
**Priorytet:** Wysoki
**Autor:** Agent UX (Gemini)

## Opis problemu
Przeprowadzona analiza procesu projektowania ręcznika na małych ekranach (375x812) wykazała, że obecny interfejs oparty na długim, przewijanym widoku utrudnia personalizację. Użytkownik traci z oczu podgląd produktu podczas dokonywania wyborów, co zmusza go do ciągłego scrollowania.

## Ważne: Spójność RWD (Responsive Design Integrity)
**Kluczowe zastrzeżenie:** Wszystkie poniższe zmiany dotyczą wyłącznie widoku mobilnego (ekrany < 1024px). Implementacja NIE MOŻE wpływać na układ desktopowy, gdzie obecny dwukolumnowy układ i stałe panele są pożądane.

## Zidentyfikowane problemy i rozwiązania UX

### 1. Eliminacja stanu pustego (Color-First Approach) - PRIORYTET
*   **Problem:** Na starcie podgląd jest często szary/pusty (wireframe).
*   **Rekomendacja:** Wprowadzenie **domyślnego koloru** (np. Ecru/Biały) lub wymuszenie wyboru koloru bazowego zestawu na "dzień dobry".
*   **Zysk:** Natychmiastowa wizualizacja gotowego produktu.

### 2. Dynamika interfejsu: Auto-collapsing Panels
*   **Problem:** Wybór opcji (np. wzoru) na długiej liście zasłania podgląd.
*   **Rekomendacja:** Kliknięcie w konkretny wzór, kolor lub nić powinno **automatycznie zwijać/chować** panel wyboru, odsłaniając pełny podgląd ręcznika.
*   **Zysk:** Użytkownik od razu widzi efekt swojej decyzji w dużej skali.

### 3. Optymalizacja nawigacji "Wróć do zestawu"
*   **Problem:** Duży przycisk "Wróć do zestawu" wewnątrz sekcji edycji zabiera cenną przestrzeń.
*   **Rekomendacja:** Usunięcie dużego bloku przycisku. Przeniesienie akcji powrotu do **dolnego paska nawigacji** (obok zakładek) lub pozostawienie jej w formie dyskretnej ikony w nagłówku.
*   **Zysk:** Czysty interfejs i więcej miejsca na podgląd haftu.

### 4. Sticky Bottom Navigation (Tabs)
*   **Problem:** Zakładki (Wzory, Nici, Tekst) uciekają podczas przewijania.
*   **Rekomendacja:** Przyklejenie paska zakładek do dolnej krawędzi ekranu (Sticky Bottom Bar).
*   **Zysk:** Natychmiastowy dostęp do wszystkich kategorii edycji z dowolnego punktu.

### 5. Optymalizacja listy wzorów i wyszukiwarka
*   **Problem:** Setki wzorów na telefonie uniemożliwiają sprawne przeglądanie.
*   **Rekomendacja:** Dodanie pola wyszukiwania oraz horyzontalnych kategorii nad siatką wzorów.
*   **Zysk:** Drastyczne skrócenie czasu personalizacji.

### 6. Interakcja z klawiaturą (Visual Viewport)
*   **Problem:** Klawiatura zasłania pole tekstowe i podgląd.
*   **Rekomendacja:** Automatyczne windowanie pola tekstowego i miniatury podglądu nad otwartą klawiaturę systemową.

### 7. Interaktywne Podpowiedzi (Contextual Tips)
*   **Problem:** Przycisk "Przejdź do zakładki" w chmurkach podpowiedzi (tips) nie zawsze precyzyjnie kieruje użytkownika do miejsca akcji.
*   **Rekomendacja:** 
    *   Kliknięcie w przycisk wewnątrz podpowiedzi musi automatycznie **aktywować odpowiednią zakładkę** (np. "Wzory") i rozwinąć panel wyboru.
    *   Przycisk powinien mieć dynamiczną nazwę, np. "Wybierz wzór teraz" zamiast ogólnego "Przejdź do zakładki".
*   **Zysk:** Skrócenie ścieżki użytkownika (User Journey) i eliminacja dezorientacji.

## Sugerowane kroki wdrożeniowe
1.  **UX Priority:** Wdrożenie domyślnego koloru i auto-zwijania paneli (mobile-only).
2.  **UI Refactor:** Przeniesienie zakładek i przycisku powrotu do stałego paska na dole ekranu (mobile-only).
3.  **Functional Add:** Dodanie wyszukiwarki wzorów (dostępna na wszystkich urządzeniach).

---
*Dokument wygenerowany automatycznie podczas audytu UX. Wszystkie zalecenia powinny być testowane w trybie mobilnym Playwright przed wdrożeniem na produkcję.*
