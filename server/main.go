package main

import (
	"database/sql"
	"log"
	"net/http"
	"os"

	_ "modernc.org/sqlite"
)

func openDB() *sql.DB {
	db, err := sql.Open("sqlite", "chrimbus.db")
	if err != nil {
		log.Fatal(err)
	}
	_, err = db.Exec(`
		CREATE TABLE IF NOT EXISTS patterns (
			id INTEGER PRIMARY KEY,
			animation TEXT NOT NULL,
			pi_claimed_at DATETIME
		)
	`)
	if err != nil {
		log.Fatal(err)
	}
	return db
}

func pattern(apiKey string) http.HandlerFunc {
	return func(w http.ResponseWriter, req *http.Request) {
		reqKey := req.Header.Get("Authorization")
		if reqKey != "Bearer "+apiKey {
			w.WriteHeader(http.StatusUnauthorized)
			return
		}
		w.WriteHeader(http.StatusCreated)
	}
}

func main() {
	apiKey := os.Getenv("CHRIMBUS_API_KEY")
	db := openDB()
	defer db.Close()

	mux := http.NewServeMux()

	mux.HandleFunc("POST /pattern/{$}", pattern(apiKey))
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
