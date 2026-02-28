package config

import "os"

// Config holds environment-based configuration for the marketing service.
type Config struct {
	HTTPAddr string
}

// Load reads configuration from environment variables with sensible defaults.
func Load() Config {
	c := Config{
		HTTPAddr: ":8002",
	}

	if v := os.Getenv("MARKETING_HTTP"); v != "" {
		c.HTTPAddr = v
	}

	return c
}
