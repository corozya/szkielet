# Analiza: TASK_9 — Alternatywny flow zamówienia z opisem zamiast projektowania

**Data analizy:** 2026-04-26  
**Status:** READY FOR ARCHITECT REVIEW  
**Zatwierdzono przez:** UX Designer + Product Owner

---

## 📋 KONTEKST ZADANIA

Klienci nie chcą lub nie potrafią korzystać z kreatora haftu. Potrzebują możliwości:
1. Dodania do koszyka bez projektowania
2. Wpisania opisu swoich życzeń dotyczących haftu
3. Przechowywania tego opisu w zamówieniu i mailu potwierdzającym

**Strona testowa:** https://reczniki-haftowane.pl/products/duzy-i-maly-w-koszu (production)

---

## ✅ STATUS WDROŻENIA

### Zrobione
- Frontend ma już taby `Projektuj haft` / `Opisz zamówienie` w kreatorze.
- `CustomNotesTab` istnieje i zapisuje `custom_notes` do store.
- `WizzardPanelTabs` ma `role="tablist"`, `role="tab"`, `aria-selected`, `aria-controls` oraz obsługę `ArrowLeft` / `ArrowRight` / `Home` / `End`.
- Przy przełączaniu tabów pokazuje się toast `✓ Dane zostały zachowane`.
- Strona produktu otwiera kreator z kontekstem istniejącego itemu z koszyka, jeśli produkt już tam jest.
- Po zapisie zmian pokazuje się toast z akcjami `Tak` / `Nie`.
- CTA w koszyku zostało ujednolicone do `AKTUALIZUJ ZAMÓWIENIE`.
- Button edycji w koszyku ma prostsze `Edytuj`.
- Backend ma walidację `configuration.custom_notes` oraz cast `configuration` na array.
- Snapshot zamówienia zachowuje `custom_notes`.
- Email potwierdzający pokazuje instrukcje klienta.
- Filament pokazuje `Instrukcje klienta` przy itemach zamówienia.

### Do zweryfikowania przez Architekta
- Czy obecny toast z akcjami `Tak` / `Nie` jest wystarczający względem briefu UX.
- Czy etykiety CTA w koszyku i na produkcie są zgodne z oczekiwanym copy.
- Czy należy wykonać dodatkowy smoke test w przeglądarce na produkcie i koszyku.

### Odpowiedzi Architekta (2026-04-26)
- **Toast `✓ Zmiany zapisane! Wróć do koszyka?` (Tak/Nie)**: **TAK, wystarczający jako MVP**. Warunek: `Tak` prowadzi do koszyka, `Nie` tylko zamyka toast (bez dodatkowych modali).
- **Copy/CTA**:
  - **Koszyk**: `AKTUALIZUJ ZAMÓWIENIE` — **OK** (edycja istniejącego itemu).
  - **Strona produktu**: CTA `ZAPROJEKTUJ I ZAMÓW` — **OK** jako wejście do kreatora.
  - **Kreator otwarty ze strony produktu**: gdy produkt **już jest w koszyku**, zapis musi działać jak **update** (bez duplikowania pozycji) i pokazywać label **`Aktualizuj zamówienie`**.
- **Smoke test**: **TAK, wymagany** (produkt → kreator (taby + zapis) → koszyk → checkout → email → Filament).

### Braki / ryzyka (Architect)
- **Ryzyko duplikacji pozycji przy edycji z produktu**: obecnie zapis w kreatorze używa `addItem(...)` (dodaje nową pozycję). Dla scenariusza “produkt już w koszyku” potrzebny jest “update flow” (np. add+remove starej pozycji) lub osobny endpoint update.

### Kolejny krok (Architect) — właściciel: Frontend Developer
- **Cel**: domknąć flow “produkt już w koszyku” (update zamiast duplikacji) + poprawny label CTA w kreatorze.
- **Propozycja implementacji (bez zmian API)**: przy edycji z produktu wykonać **addItem(newSnapshot)** + **removeItem(oldItemId)** (z rollbackiem jeśli remove się nie uda).
- **AC**:
  - [ ] Zapis z produktu dla itemu już w koszyku **nie zwiększa** liczby pozycji (brak duplikatu).
  - [ ] CTA w kreatorze pokazuje **`Aktualizuj zamówienie`** gdy produkt był już w koszyku.
  - [ ] Smoke test przechodzi end-to-end (w tym email i Filament).

---

## 🔍 Weryfikacja po pracy Codex (Architect, 2026-04-26)

### Stan wdrożenia (kod)
- **Backend**: walidacja `configuration.custom_notes` + snapshot do `OrderItem.configuration` + email + Filament + API cart zwraca `configuration` — **OK**.
- **Frontend**: taby (A11y) + `CustomNotesTab` + GA4 `tab_switched` + zachowanie danych przy przełączaniu — **OK**.

### Blokery / co dalej
- ~~Repo app `apps/reczniki-haftowane/` ma lokalne zmiany (8 plików) nieobjęte commitami~~ — **zamknięte**.
  - **Commit**: `apps/reczniki-haftowane@47095f9` — `feat(frontend): update task 9 wizard flow and cart edit labels`
  - Zakres: update-flow (add+remove dla edycji istniejącego itemu) + toast “✓ Zmiany zapisane! Wróć do koszyka?” + dopięcie A11y/tabów i copy.

### Następny krok (właściciel: Frontend Developer) — „merge-ready”
- [ ] Wykonać smoke test:
  - [ ] Produkt → kreator → tab “Opisz zamówienie” → zapis → koszyk (bez duplikacji pozycji)
  - [ ] Checkout → mail potwierdzający pokazuje instrukcje
  - [ ] Filament → widoczna kolumna “Instrukcje klienta”
- [ ] Po smoke teście: oznaczyć TASK_9 jako **DONE**.

---

## ✅ SPECYFIKACJA — FRONTEND

### Flow:

**1. Strona produktu — Button "ZAPROJEKTUJ I ZAMÓW":**
- Jeśli produkt **NIE w koszyku** → dodaj + otwórz kreator
- Jeśli produkt **JUŻ w koszyku** → otwórz kreator z jego kontekstem (brak modal-u)

**2. Kreator — Krok 1 — Dwa taby do przełączania:**

| Element | Szczegóły |
|---------|-----------|
| **Tab 1** | "Projektuj haft" (default) — normalny kreator |
| **Tab 2** | "Opisz zamówienie" — textarea do instrukcji |
| **Dane** | Zachowują się przy przełączaniu (projekty + opis) |
| **Help text** | Pod tab-ami: "Możesz przełączać między tabami bez utraty danych. Wybierz sposób który ci pasuje." |

**3. Tab "Opisz zamówienie" — Textarea:**

| Pole | Wartość |
|------|---------|
| **Label** | "Dodatkowe instrukcje (opcjonalnie)" |
| **Placeholder** | "Np. Rozmiar, kolor, haft, kolor nici, napis..." |
| **Help text** | "Czujesz się zagubiony? Użyj kreatora powyżej — każdy klik tworzy projekt automatycznie." |
| **Max długość** | 1000 znaków |
| **Obowiązkowy** | NIE — opcjonalny |

**4. Button — kontekstowy:**

| Kontekst | Label | Akcja |
|----------|-------|-------|
| Produkt nowy | "Dodaj do koszyka" | Dodaj + feedback |
| Produkt w koszyku | "Aktualizuj zamówienie" | Aktualizuj + feedback |

**5. Po kliknięciu button-u:**
- Aktualizuj item w koszyku (z projektem + opisem, jeśli są)
- Toast: "✓ Zmiany zapisane! Wróć do koszyka?" (buttons: "Tak" / "Nie")
- Kreator się zamyka
- (Opcjonalnie) Pokaż "Chcesz dodać kolejny item?"

**6. Edycja z koszyka:**
- Button "Edytuj" przy itemu w koszyku
- Otwiera kreator z kontekstem tego itemu (ładuje ostatnią wersję projektu/opisu)
- Button label: "Edytuj projekt" (jeśli ma projekt) / "Edytuj zamówienie" (jeśli ma opis)

**7. GA4 Tracking:**
```javascript
gtag('event', 'tab_switched', {
  which_tab: 'designer' || 'description',
  product_id: 123
})
```

**8. Accessibility & Mobile:**
- **ARIA atrybuty:** role="tablist", role="tab", aria-selected, aria-controls
- **Keyboard:** Tab → przełącza; Arrow Left/Right → poprzedni/następny
- **Mobile:** Sticky tab-y (zawsze widoczne przy scrollowaniu)
- **Toast:** Przy przełączaniu tab-ów: "✓ Dane zostały zachowane"

---

## ✅ SPECYFIKACJA — BACKEND

### 1. Walidacja w AddCartItemRequest

**Wymóg:** 
```php
'configuration.custom_notes' => ['nullable', 'string', 'max:1000'],
```

**Sprawdzić:** Czy to już istnieje w `app/Http/Requests/Cart/AddCartItemRequest.php`

### 2. Model CartItem

**Wymóg:** Cast na configuration
```php
protected $casts = [
    'configuration' => 'array',
];
```

**Sprawdzić:** Czy CartItem.php ma to

### 3. Email Confirmation Template

**Lokalizacja:** `resources/views/emails/order-confirmation.blade.php` lub `app/Mail/OrderConfirmation.php`

**Co dodać:**
```blade
@if($order->items)
  @foreach($order->items as $item)
    <div>
      <h3>{{ $item->product->name }}</h3>
      
      @if($item->configuration['custom_notes'] ?? null)
        <div style="background-color: #f5f5f5; padding: 10px; border-left: 4px solid #8b6f47;">
          <strong>Twoje instrukcje:</strong><br>
          {{ $item->configuration['custom_notes'] }}
        </div>
      @endif
    </div>
  @endforeach
@endif
```

### 4. Filament Resource — OrderItem

**Lokalizacja:** `app/Filament/Resources/OrderItemResource.php`

**Co dodać — kolumna:**
```php
Tables\Columns\TextColumn::make('configuration.custom_notes')
    ->label('Instrukcje klienta')
    ->sortable()
    ->limit(100)
    ->tooltip(fn ($state) => $state),
```

### 5. API Resources

**Sprawdzić:**
- `app/Http/Resources/CartItemResource.php` — `configuration` widoczny
- `app/Http/Resources/OrderItemResource.php` — `configuration` widoczny (jeśli istnieje)

### 6. Order Snapshot

**Lokalizacja:** `app/Services/OrderService.php` lub `app/Http/Controllers/CheckoutController.php`

**Co sprawdzić:**
```php
$orderItem = OrderItem::create([
    'order_id' => $order->id,
    'configuration' => $cartItem->configuration, // ← snapshot!
    // ...
]);
```

---

## 📂 PLIKI DO ZMIANY

### Frontend:
- [ ] `frontend/src/components/products/ProductHero.jsx`
- [ ] `frontend/src/hooks/useProductPageLogic.js`
- [ ] Kreator — krok 1 (dodać taby)

### Backend:
- [ ] `backend/app/Http/Requests/Cart/AddCartItemRequest.php` (sprawdzić walidację)
- [ ] `backend/app/Models/CartItem.php` (sprawdzić cast)
- [ ] `resources/views/emails/order-confirmation.blade.php` (dodać custom_notes)
- [ ] `backend/app/Filament/Resources/OrderItemResource.php` (dodać kolumnę)
- [ ] `backend/app/Http/Resources/CartItemResource.php` (sprawdzić configuration)
- [ ] `backend/app/Services/OrderService.php` (sprawdzić snapshot)

---

## 🔄 COMMIT MESSAGES

### Frontend:
```text
feat(frontend): dodaj taby w kreatorze - projektuj haft lub opisz zamówienie

- Krok 1 kreatora: dwa taby "Projektuj haft" / "Opisz zamówienie"
- Tab "Opisz zamówienie" zawiera textarea do wpisania instrukcji
- Dane się zachowują przy przełączaniu między tabami
- Kontekstowy button: "Dodaj do koszyka" / "Aktualizuj zamówienie"
- GA4 tracking: event "tab_switched" z which_tab
- ARIA atrybuty dla accessibility
- Mobile: sticky tab-y
- Toast feedback przy zmianie tab-u

TASK_9: Alternatywny flow dla klientów bez chęci projektowania haftu

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

### Backend:
```text
feat(backend): dodaj custom_notes do zamówień i email confirmation

- Walidacja custom_notes: max 1000 znaków, opcjonalne
- Przechowywanie w OrderItem.configuration (snapshot ze CartItem)
- Email confirmation: wyświetl instrukcje klienta w sekcji item-u
- Filament: kolumna "Instrukcje klienta" w OrderItem resource
- API: custom_notes widoczny w CartItemResource

TASK_9: Opis zamówienia w email confirmation

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

---

## ✅ WERYFIKACJA (Architect)

Po ukończeniu pracy agentów:

1. **Frontend:**
   - [ ] Otwórz https://reczniki-haftowane.pl/products/duzy-i-maly-w-koszu (production)
   - [ ] Kliknij "ZAPROJEKTUJ I ZAMÓW"
   - [ ] Sprawdź czy są dwa taby na kroku 1
   - [ ] Przełącz między tabami — dane się zachowują?
   - [ ] Wpisz opis w textarea
   - [ ] Kliknij "Dodaj do koszyka" / "Aktualizuj zamówienie"
   - [ ] Sprawdź toast
   - [ ] Przejdź do koszyka — czy item ma opis?

2. **Backend:**
   - [ ] Utwórz zamówienie z custom notes
   - [ ] Sprawdź czy email ma instrukcje w sekcji item-u
   - [ ] Otwórz Filament — OrderItem Resource — czy kolumna "Instrukcje klienta" widoczna?
   - [ ] Sprawdź API: GET /api/cart — czy configuration.custom_notes widoczny?

3. **GA4:**
   - [ ] Przełącz tab-y — czy event "tab_switched" pojawia się w GA4?

4. **Mobile:**
   - [ ] Otwórz na mobile
   - [ ] Sprawdź czy tab-y są sticky (widoczne przy scrollowaniu)
   - [ ] Wpisz opis
   - [ ] Sprawdź czy textarea ma dobry rozmiar

---

## 📝 NOTATKI

- **Poprzednia implementacja:** Była oddzielnym button-em "Dodaj bez projektowania" + modal. Ta wersja integruje to w kreator (lepszy UX).
- **UX decyzja:** Taby na kroku 1 zamiast osobnej ścieżki — klient ma wybór zaraz po kliknięciu "ZAPROJEKTUJ I ZAMÓW".
- **Tracking:** GA4 event "tab_switched" pokaże który flow jest popularniejszy.
- **Email:** Custom notes będą widoczne dla klienta i support team w mailu — redukuje support tickets.

## ❓ Questions/Issues for Architect

1. Czy potwierdzasz, że dla tabów mamy trzymać standard ARIA: `Tab` przechodzi do/poza tablistą, a zmiana aktywnego taba odbywa się przez `ArrowLeft` / `ArrowRight` / `Home` / `End`?
2. Który jeden kodowy punkt ma być źródłem prawdy dla snapshotu `custom_notes` przy checkout: `OrderService`, `CheckoutController`, czy inny wspólny serwis?
3. Czy toast po zapisie ma zostać z akcjami `Tak` / `Nie`, czy trzeba go dopasować do dokładnego copy z briefu UX?

## ✅ Podsumowanie wykonania

- Flow na stronie produktu został dopięty tak, aby wykrywać istniejącą pozycję w koszyku dla tego samego produktu.
- Zapis z kreatora dla produktu już obecnego w koszyku działa jako update-flow: dodaje nową wersję, potem usuwa starą pozycję, z rollbackiem jeśli usuwanie się nie uda.
- CTA w kreatorze na stronie produktu pokazuje `Aktualizuj zamówienie`, gdy edytowany jest item z koszyka.
- Stan edycji jest czyszczony po zamknięciu kreatora i przy zmianie slug produktu.
- Nie udało się wykonać pełnego smoke testu w tym środowisku, bo repo aplikacji nie ma tu kompletu zależności runtime do uruchomienia linta/testów, a backendowy `php` nie jest dostępny.

---

## Status

**🔄 IN PROGRESS — Frontend Developer pracuje, Architekt ma zweryfikować i zdecydować co dalej**
