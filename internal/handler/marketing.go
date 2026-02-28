package handler

import (
	"github.com/gin-gonic/gin"

	"github.com/hanzoai/commerce/datastore"
	"github.com/hanzoai/commerce/middleware"
	"github.com/hanzoai/commerce/util/json"
	"github.com/hanzoai/commerce/util/json/http"
	"github.com/hanzoai/commerce/util/permission"
	"github.com/hanzoai/commerce/util/rest"
	"github.com/hanzoai/commerce/util/router"
	"github.com/hanzoai/marketing/internal/engine"
	"github.com/hanzoai/marketing/internal/model"
)

func RouteMarketing(router router.Router, args ...gin.HandlerFunc) {
	adminRequired := middleware.TokenRequired(permission.Admin)
	namespaced := middleware.Namespace()

	api := router.Group("marketing")
	api.Use(adminRequired)

	api.POST("", adminRequired, namespaced, create)

	rest.New(model.AdCampaign{}).Route(api)
	rest.New(model.AdConfig{}).Route(api)
	rest.New(model.AdSet{}).Route(api)
	rest.New(model.Ad{}).Route(api)
}

func create(c *gin.Context) {
	org := middleware.GetOrganization(c)
	db := datastore.New(org.Namespaced(c))

	req := engine.CreateInput{}

	// Decode response body to create new user
	if err := json.Decode(c.Request.Body, &req); err != nil {
		http.Fail(c, 400, "Failed decode request body", err)
		return
	}

	if cmpgn, err := engine.Create(db, req); err != nil {
		http.Fail(c, 400, "Failed to create campaign", err)
		return
	} else {
		http.Render(c, 201, cmpgn)
	}
}
