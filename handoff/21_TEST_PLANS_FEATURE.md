# 21_TEST_PLANS_FEATURE

**Status:** Do realizacji (Planowanie zakończone)
**Primary Agent:** Claude
**Priorytet:** Średni (po Rundzie 1 integracji)

Implementacja funkcji "Plany Testów" — pozwala klientom zdefiniować scenariusz testowania (np. "Testy procesu zakupowego") i zbierać feedback z testów w tym scenariuszu.

---

## Cel

Klient definiuje krótki opis planu testów na poziomie projektu. Testers widzi dostępne plany w extension i może przypisać feedback do planu. Admin widzi feedback pogrupowany po planach.

---

## Architektura

### Backend

**Model: `TestPlan`**
```php
- id (PK)
- project_id (FK)
- name: string (np. "Testy procesu zakupowego")
- description: text (długi opis scenariusza)
- is_active: boolean (domyślnie: true)
- created_at, updated_at
```

**Relacje:**
- `TestPlan belongsTo Project`
- `TestPlan hasMany FeedbackReport`
- `FeedbackReport belongsTo TestPlan` (nullable)

**Migration:**
- `2026_04_XX_XXXXXX_create_test_plans_table.php`
- Foreign key do `projects.id` z `onDelete('cascade')`

**Controller: `AdminTestPlanController`**
- `index(Project $project)` — lista planów projektu
- `store(Request $request, Project $project)` — utwórz plan
- `update(Request $request, TestPlan $plan)` — edytuj plan (name, description, is_active)
- `destroy(TestPlan $plan)` — usuń plan

**Routes:**
```php
Route::middleware(['auth', 'client_access', 'role:admin'])->prefix('dashboard')->group(function () {
    Route::get('/projects/{project}/test-plans', [AdminTestPlanController::class, 'index'])->name('dashboard.test-plans.index');
    Route::post('/projects/{project}/test-plans', [AdminTestPlanController::class, 'store'])->name('dashboard.test-plans.store');
    Route::put('/test-plans/{plan}', [AdminTestPlanController::class, 'update'])->name('dashboard.test-plans.update');
    Route::delete('/test-plans/{plan}', [AdminTestPlanController::class, 'destroy'])->name('dashboard.test-plans.destroy');
});
```

**API endpoint (dla extension):**
```php
Route::get('/api/v1/projects/{projectId}/test-plans/active', [TestPlanController::class, 'activeByProject']);
// Response: [{ id, name, description }, ...]
```

---

### Frontend — Dashboard

**Nowa strona: `/dashboard/projects/{id}/test-plans`**

`resources/js/Pages/Projects/TestPlans/Index.jsx`

Funkcjonalność:
- Lista aktywnych + nieaktywnych planów
- Przycisk "+ Nowy plan"
- Dla każdego planu: nazwa, opis, toggle is_active, edit, delete
- Form modal: nazwa (required, max 255) + opis (textarea, optional)

Layout: Card-based, podobnie do strony Integracje

---

### Frontend — Extension

**Modyfikacja: `src/popup.js`**

Przy wysyłaniu feedback:
1. Pobierz aktywne plany: `GET /api/v1/projects/{projectId}/test-plans/active`
2. Jeśli plany istnieją → pokaż dropdown "Plan (optional)" przed wysłaniem
3. Wysłanie:
```json
{
  "project_id": 123,
  "title": "...",
  "description": "...",
  "test_plan_id": 456,  // nullable
  "metadata": {...},
  "screenshot": "...",
  ...
}
```

**UI:** Dropdown pojawia się pod polem opisem, przed przyciskiem "Wyślij"

---

### Frontend — Dashboard Feedback

**Modyfikacja: `resources/js/Pages/Feedback/Show.jsx`**

Jeśli feedback ma `test_plan_id`:
```jsx
<Card>
  <Card.Body>
    <p className="text-sm text-gray-500">Plan testów</p>
    <p className="text-white font-semibold">{feedback.test_plan.name}</p>
    {feedback.test_plan.description && (
      <p className="text-gray-400 text-sm mt-1">{feedback.test_plan.description}</p>
    )}
  </Card.Body>
</Card>
```

**Modyfikacja: `resources/js/Pages/Feedback/Index.jsx` (lista)**

Dodać filter po planach (jeśli istnieją plany w projekcie)

---

## DoD

### Backend
- [ ] Model `TestPlan` z relacją do `Project` i `FeedbackReport`
- [ ] Migration `create_test_plans_table`
- [ ] `AdminTestPlanController` z CRUD
- [ ] Routes zarejestrowane
- [ ] API endpoint `/api/v1/projects/{projectId}/test-plans/active`
- [ ] `FeedbackController` — validacja i zapis `test_plan_id`

### Frontend — Dashboard
- [ ] Nowa strona `/dashboard/projects/{id}/test-plans`
- [ ] Lista planów z toggle is_active
- [ ] Form (modal lub inline) do tworzenia/edytowania
- [ ] Przycisk delete z potwierdzeniem
- [ ] Link z Dashboard do strony testPlans (opcjonalnie)

### Frontend — Extension
- [ ] Pobieranie aktywnych planów po zmianicy `project_id`
- [ ] Dropdown w popup.js
- [ ] Wysłanie `test_plan_id` w feedback payload
- [ ] Draft dla `test_plan_id` w `browser.storage.local`

### Frontend — Feedback Views
- [ ] `Feedback/Show.jsx` — wyświetlanie planu
- [ ] `Feedback/Index.jsx` — filter po planach (opcjonalnie)

### Testy
- [ ] E2E: Admin tworzy plan, widzi go w extension, tester zgłasza feedback z planem, admin widzi

---

## Uwagi implementacyjne

1. **Porządek:** Backend first (model, migration, controller, API), potem frontend dashboard, potem extension
2. **Walidacja:** `name` required, max 255; `description` optional, max 2000
3. **Bezpieczeństwo:** Admin może edytować/usuwać tylko plany jego projektu (middleware `client_access`)
4. **Feedback stale:** Jeśli plan zostanie usunięty, feedback może pozostać (nullable FK)
5. **Extension:** Pobieranie planów powinno być cached (aby nie robić API call przy każdym otwarciu)

---

## Oś czasu sugerowana

- **Backend:** 2-3h (model + migration + controller + API)
- **Dashboard:** 1-2h (strona, form, CRUD UI)
- **Extension:** 1-2h (dropdown, draft, wysłanie)
- **Feedback views:** 30-45min (wyświetlanie, filter)
- **Testy:** 30-45min

**Razem:** ~6-8 godzin pracy pełnoetatowej
