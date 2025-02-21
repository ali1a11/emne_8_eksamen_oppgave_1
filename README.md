# Eksamen Oppgave 1 API Løsning

Dette prosjektet implementerer et enkelt API for produktstyring med en MySQL-database og NGINX som en reverse proxy. Arkitekturen følger en mikrotjenestebasert tilnærming, med tre hovedtjenester:

---

## 📌 Arkitektur og Konfigurasjon

Struktur
oppgave_1/
├── docker-compose.yml
├── api/
│    ├── app.py
│    ├── Dockerfile
│    ├── requirements.txt
├── db/
│    ├── database_setup.sql
│    ├── Dockerfile
├── nginx/
│    ├── Dockerfile
│    ├── nginx.conf

Løsningen består av tre hovedtjenester som kjører i separate Docker-containere:

### 1️⃣ Flask API (web)
   - Et Flask-basert RESTful API som kommuniserer med MySQL-databasen for å hente produktinformasjon.
   - API-et eksponerer endepunkter for å hente en liste over produkter, hente ett produkt etter ID, og utføre en helse-sjekk.


#### 🔗 Endepunkter:
- **`GET /api/products`** – Henter en liste over alle produkter.
- **`GET /api/products/{id}`** – Henter detaljer for et spesifikt produkt basert på ID.
- **`GET /api/health`** – Returnerer en helsesjekk for API-et.

### 2️⃣ MySQL Database (db)
   - En MySQL-container som inneholder databasen `product_db` og lagrer produktinformasjon.
   - Databasen initieres ved hjelp av en `database_setup.sql`-fil, som oppretter tabeller og setter inn testdata.

#### 🛠 MySQL-konfigurasjon:
- **Database:** `product_db`
- **Bruker:** `product-api`
- **Passord:** `securepass`

### 3️⃣ Nginx Reverse Proxy (nginx)
   - Fungere som en reverse proxy for API-et, og videresender innkommende forespørsler til Flask-applikasjonen som kjører inne i `eksamen_api`-containeren.
   - Gir lastbalansering og forbedrer sikkerheten ved å skjule direkte tilgang til API-tjenesten.

#### 🔄 Proxy-konfigurasjon:
- `http://localhost/api/products` rutes til Flask API-et via Nginx.

---
## Prosjektoppsett
For å komme i gang med prosjektet, følg disse stegene:

Klon depotet:
   ```bash
   git clone <repository-url>
   cd <project-directory>

---

## 🚀 Starte og Stoppe Tjenestene

### 1️⃣ Bygg og start tjenestene
```bash
docker-compose up --build -d
```

### 2️⃣ Sjekk om containerne kjører
```bash
docker-compose ps
```

### 3️⃣ Stoppe tjenestene
```bash
docker-compose down
```

---

## 🔄 Hvordan Løsningen Samhandler

✔️ **Flask API** håndterer HTTP-forespørsler og kommuniserer med MySQL-databasen.
✔️ **MySQL Database** lagrer og leverer produktdata.
✔️ **Nginx** fungerer som en mellommann, som sikrer skalerbarhet og sikkerhet.

---

## ⚙️ Konfigurasjon

### 🐳 Docker Compose
Prosjektet er konfigurert med docker-compose og inkluderer:

web: Flask API-tjeneste.

db: MySQL databasetjeneste.

nginx: NGINX reverse proxy-tjeneste.

Hver tjeneste bygges ved hjelp av de respektive Dockerfilene som finnes i api, db og nginx-katalogene.


#### `docker-compose.yml`
```yaml
version: '3'
services:
  web:
    build: ./api
    container_name: eksamen_api
    environment:
      - DATABASE_URL=mysql://product-api:securepass@db:3306/product_db
    depends_on:
      - db
    networks:
      - eksamen_net
    expose:
      - "5000"

  db:
    build: ./db
    container_name: eksamen_db
    environment:
      - MYSQL_ROOT_PASSWORD=securepass
      - MYSQL_DATABASE=product_db
      - MYSQL_USER=product-api
      - MYSQL_PASSWORD=securepass
    volumes:
      - mysql_data:/var/lib/mysql
      - ./db/database_setup.sql:/docker-entrypoint-initdb.d/database_setup.sql
    networks:
      - eksamen_net
    expose:
      - "3306"

  nginx:
    build: ./nginx
    container_name: eksamen_nginx
    ports:
      - "80:80"
    depends_on:
      - web
    networks:
      - eksamen_net

volumes:
  mysql_data:

networks:
  eksamen_net:
    driver: bridge
```

## 🛠 Testing av API

Når tjenestene kjører, kan du teste API-et med **curl** eller **Postman**.

### 📋 Hent liste over produkter
```bash
curl http://localhost/api/products
```

### 🔍 Hent spesifikt produkt (ID 1)
```bash
curl http://localhost/api/products/1
```

### 💡 Helsesjekk
```bash
curl http://localhost/api/health
```

---

## 🔎 Feilsøking

Sjekk logger ved feil:
```bash
docker-compose logs web
docker-compose logs db
docker-compose logs nginx
```

---

## 🛠 Teknologier brukt
- **Flask** – Python web-rammeverk.
- **SQLAlchemy** – ORM for MySQL.
- **MySQL** – Databaseløsning.
- **Nginx** – Reverse proxy.
- **Docker Compose** – Orkestrering av containere.

---

