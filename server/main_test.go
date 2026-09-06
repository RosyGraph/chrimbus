package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestPatternUnauthorized(t *testing.T) {
	handler := pattern("secret")

	req := httptest.NewRequest(http.MethodPost, "/pattern/", nil)
	rec := httptest.NewRecorder()

	handler(rec, req)
	want := http.StatusUnauthorized
	got := rec.Code

	if got != want {
		t.Fatalf("want %d, got %d", want, got)
	}
}
