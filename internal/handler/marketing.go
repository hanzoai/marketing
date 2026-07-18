package handler

import (
	"github.com/zap-proto/zip"

	"github.com/hanzoai/commerce/datastore"
	"github.com/hanzoai/commerce/middleware"
	"github.com/hanzoai/commerce/util/json"
	"github.com/hanzoai/commerce/util/json/http"
	"github.com/hanzoai/commerce/util/permission"
	"github.com/hanzoai/commerce/util/rest"
	"github.com/hanzoai/marketing/internal/engine"
	"github.com/hanzoai/marketing/internal/model"
)

func RouteMarketing(router zip.Router, args ...zip.Handler) {
	adminRequired := middleware.TokenRequired(permission.Admin)
	namespaced := middleware.Namespace()

	api := router.Group("marketing")
	api.Use(adminRequired)

	api.Post("", adminRequired, namespaced, create)

	rest.New(model.AdCampaign{}).Route(api)
	rest.New(model.AdConfig{}).Route(api)
	rest.New(model.AdSet{}).Route(api)
	rest.New(model.Ad{}).Route(api)
}

func create(c *zip.Ctx) error {
	org := middleware.GetOrganization(c)
	db := datastore.New(org.Namespaced(c.Context()))

	req := engine.CreateInput{}

	// Decode request body to create new campaign
	if err := json.DecodeBytes(c.Body(), &req); err != nil {
		return http.Fail(c, 400, "Failed decode request body", err)
	}

	cmpgn, err := engine.Create(db, req)
	if err != nil {
		return http.Fail(c, 400, "Failed to create campaign", err)
	}
	return http.Render(c, 201, cmpgn)
}
