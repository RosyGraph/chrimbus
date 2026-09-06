package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestPattern(t *testing.T) {
	tests := []struct {
		name   string
		auth   string
		status int
	}{
		{
			name:   "unauthorized",
			status: http.StatusUnauthorized,
		},
		{
			name:   "authorized",
			auth:   "Bearer secret",
			status: http.StatusCreated,
		},
		{
			name:   "invalid key",
			auth:   "Bearer wrong",
			status: http.StatusUnauthorized,
		},
	}

	handler := pattern("secret")

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodPost, "/pattern/", nil)
			req.Header.Set("Authorization", tt.auth)

			rec := httptest.NewRecorder()

			handler(rec, req)

			if rec.Code != tt.status {
				t.Fatalf("want %d, got %d", tt.status, rec.Code)
			}
		})
	}
}
