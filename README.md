# 🧠 Aji-Memo – Zewnętrzna pamięć AI przez REST API (GET)

System **Aji-Memo** to zewnętrzna pamięć kontekstowa, która może być wykorzystywana przez modele językowe (np. ChatGPT) za pomocą prostych zapytań HTTP typu `GET`. Dzięki temu LLM może zapisywać i odczytywać informacje w zewnętrznym systemie bez konieczności stosowania złożonych integracji (np. pluginów czy function calling). 

---

## 🧩 Stos technologiczny

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend:** [Next.js](https://nextjs.org/)
- **Baza danych:** PostgreSQL (np. z JSONB) lub SQLite
- **Vector DB (opcjonalnie):** FAISS / Qdrant / Chroma

---

## 🎯 Główne założenia

- Komunikacja przez `GET` z parametrami w `query string`.
- Token, `uid` i `namespace` w URL.
- Obsługa tagów (`tags=ustawienia,preferencje`) do grupowania pamięci.
- Możliwość przeszukiwania pamięci (tekstowo lub po tagach).
- LLM może odczytywać i zapisywać dane kontekstowe bez pluginów.

---

## 🔑 Parametry identyfikacyjne

| Parametr     | Wymagany | Domyślna wartość       | Uwagi |
|--------------|----------|-------------------------|-------|
| `token`      | ✅ tak   | —                       | Klucz autoryzacyjny |
| `uid`        | ✅ tak   | —                       | Użytkownik lub identyfikator sesji |
| `namespace`  | ⛔ opcjonalny | `namespace = uid`     | Pozwala grupować pamięć per firma/zespół |
| `tags`       | ⛔ opcjonalny | `[]`                  | Lista tagów oddzielona przecinkami |

---

## 📎 Przykłady wywołań

### Zapis pamięci z tagami
```
GET /memory/save?
  uid=jm-sky&
  namespace=jm-sky&
  token=abc123z&
  text=Uzytkownik+lubi+ciemny+motyw&
  tags=preferencje,ui
```

### Wyszukiwanie po tagu
```
GET /memory/query?
  uid=jm-sky&
  token=abc123z&
  tags=preferencje
```

### Wyszukiwanie pełnotekstowe
```
GET /memory/query?
  uid=jm-sky&
  token=abc123z&
  query=ciemny+motyw
```

---

## ⚠️ Uwagi bezpieczeństwa

- Tokeny w URL mogą wyciekać do logów lub historii.
- GET służy wyłącznie do ułatwienia dostępu z AI (dla ludzi używaj POST).
- Zabezpiecz API: krótkoterminowe tokeny, ograniczenia IP, zakres UID/token, dedykowana domena.

---

## ✅ Rekomendacje

- Endpoint `/memory/save-by-get` jako uproszczony interfejs tylko dla LLM.
- Pełne API (`POST`, `PATCH`, `DELETE`) dla użytkowników lub panelu.
- Możliwość przeszukiwania po tagach + fuzzy search + data sort.

---
