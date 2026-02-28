package handler

import (
	"github.com/gin-gonic/gin"

	"github.com/hanzoai/commerce/util/router"
)

// Register wires all marketing HTTP routes onto the given router group.
func Register(r router.Router, args ...gin.HandlerFunc) {
	RouteMarketing(r, args...)
	RouteCampaign(r, args...)
}
