package main

import (
	"database/sql"
	"log"
	"net/http"

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

func pattern(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(http.StatusCreated)
}

func main() {
	db := openDB()
	defer db.Close()

	mux := http.NewServeMux()

	mux.HandleFunc("POST /pattern/{$}", pattern)
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
