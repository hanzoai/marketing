package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"

	"github.com/hanzoai/marketing/internal/config"
	"github.com/hanzoai/marketing/internal/handler"
)

func main() {
	cfg := config.Load()

	gin.SetMode(gin.ReleaseMode)

	r := gin.New()
	r.Use(gin.Recovery())

	// Health check
	r.GET("/", func(c *gin.Context) { c.String(200, "ok") })
	r.GET("/ping", func(c *gin.Context) { c.String(200, "pong") })

	// API routes
	api := r.Group("/api/v1")
	handler.Register(api)

	srv := &http.Server{Addr: cfg.HTTPAddr, Handler: r}

	go func() {
		log.Printf("Marketing service listening on %s", cfg.HTTPAddr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %s", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("Shutting down...")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	srv.Shutdown(ctx)
}
