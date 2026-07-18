package main

import (
	"context"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"

	luxlog "github.com/luxfi/log"
	"github.com/zap-proto/zip"
	zipmw "github.com/zap-proto/zip/middleware"

	"github.com/hanzoai/marketing/internal/config"
	"github.com/hanzoai/marketing/internal/handler"
)

func main() {
	cfg := config.Load()
	logger := luxlog.New("marketing")

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	// Canonical zip middleware pipeline — mirrors cmd/commerce cloud boot:
	// Recover → RequestID → Logger.
	app := zip.New(zip.Config{Logger: logger})
	app.Use(zipmw.Recover())
	app.Use(zipmw.RequestID())
	app.Use(zipmw.Logger(logger))

	// Health checks.
	app.Get("/", func(c *zip.Ctx) error { return c.String(200, "ok") })
	app.Get("/ping", func(c *zip.Ctx) error { return c.String(200, "pong") })

	// API routes — /v1 surface (no /api/ prefix).
	handler.Register(app.Group("/v1"))

	// zip's default transport is ZAP; marketing is an external HTTP/REST API,
	// so serve over the HTTP transport unless the operator pins a scheme.
	addr := cfg.HTTPAddr
	if !strings.Contains(addr, "://") {
		addr = "http://" + addr
	}

	listenErr := make(chan error, 1)
	go func() {
		logger.Info("marketing service listening", "addr", addr)
		if err := app.Listen(addr); err != nil {
			listenErr <- err
			stop()
		}
	}()

	<-ctx.Done()
	logger.Info("shutting down")
	shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := app.ShutdownWithContext(shutdownCtx); err != nil {
		logger.Error("shutdown", "err", err)
	}

	select {
	case err := <-listenErr:
		if err != nil {
			logger.Error("listen", "err", err)
			os.Exit(1)
		}
	default:
	}
}
