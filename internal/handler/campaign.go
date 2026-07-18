package handler

import (
	"fmt"
	"math"
	"strconv"
	"time"

	"github.com/zap-proto/zip"

	"github.com/hanzoai/commerce/util/json/http"
	"github.com/hanzoai/commerce/util/rest"
	"github.com/hanzoai/marketing/internal/model"
)

type ProgressRes struct {
	Progress float64 `json:"progress"`
}

func RouteCampaign(router zip.Router, args ...zip.Handler) {
	api := rest.New(model.Campaign{})

	api.GET("/:campaignid/progress", func(c *zip.Ctx) error {
		// hardcoded for Stoned
		now := time.Now()
		startDate := time.Date(2016, time.November, 21, 0, 0, 0, 0, time.UTC)
		endDate := time.Date(2016, time.November, 24, 0, 0, 0, 0, time.UTC)
		daysTotal := endDate.Sub(startDate).Hours() / 24
		days := now.Sub(startDate).Hours() / 24
		daysComplete := days / daysTotal

		startPct := 40.0

		progress := math.Min(startPct+((100.0-startPct)*daysComplete), 99.9)
		// Go has no math.Round, sadly
		f, _ := strconv.ParseFloat(fmt.Sprintf("%.2f", progress), 64)
		return http.Render(c, 200, ProgressRes{f})
	})

	api.Route(router, args...)
}
