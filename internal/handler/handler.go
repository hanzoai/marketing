package handler

import (
	"github.com/zap-proto/zip"
)

// Register wires all marketing HTTP routes onto the given router group.
func Register(r zip.Router, args ...zip.Handler) {
	RouteMarketing(r, args...)
	RouteCampaign(r, args...)
}
