# Data Flow Diagram — Wishlist API

```mermaid
flowchart LR
  subgraph Client[Trust Boundary: Client Devices]
    U[User Browser]
    Admin[Admin Panel]
  end

  subgraph Edge[Trust Boundary: Edge / Public]
    GW(API Gateway / FastAPI)
  end

  subgraph Core[Trust Boundary: Core Services]
    AUTH[Auth Service]
    WISH[Wish Service]
    LOG[Observability Pipeline]
  end

  subgraph Data[Trust Boundary: Data Stores]
    TOK[(Token Store)]
    DB[(Wishlist DB)]
    BAK[(Backup Storage)]
  end

  EXT_EMAIL[Notification Service]

  U -->|F1: HTTPS login/signup| GW
  Admin -->|F2: HTTPS admin actions| GW
  GW -->|F3: Auth requests| AUTH
  AUTH -->|F4: Issue tokens / verify| TOK
  GW -->|F5: CRUD wishes| WISH
  WISH -->|F6: Read/Write wishes| DB
  WISH -->|F7: Audit events| LOG
  LOG -->|F8: Alerts/metrics| Admin
  DB -->|F9: Nightly snapshot| BAK
  WISH -->|F10: Optional notifications| EXT_EMAIL
```

- Потоки F1–F10 используются в таблицах STRIDE и RISKS.
- Trust boundaries: `Client` (не доверяем устройствам), `Edge` (интернет-экспонированный слой), `Core` (приложение), `Data` (стойкое хранилище и бэкапы).
- Все меж-границы каналы выполняются по TLS внутри VPN/Priv network.
```
