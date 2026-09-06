package main

import (
	"log"
	"net/http"
)

func pattern(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(http.StatusCreated)
}

func main() {
	mux := http.NewServeMux()

	mux.HandleFunc("POST /pattern/{$}", pattern)
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
