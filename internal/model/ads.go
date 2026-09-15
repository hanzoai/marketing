package model

import (
	"github.com/hanzoai/commerce/models/types/currency"
)

// AdIntegration links an entity to the ad hierarchy.
type AdIntegration struct {
	AdId         string `json:"AdId,omitempty"`
	AdConfigId   string `json:"AdConfigId,omitempty"`
	AdSetId      string `json:"AdSetId,omitempty"`
	AdCampaignId string `json:"AdCampaignId,omitempty"`
}

func (a *AdIntegration) GetAdId() string         { return a.AdId }
func (a *AdIntegration) GetAdConfigId() string    { return a.AdConfigId }
func (a *AdIntegration) GetAdSetId() string       { return a.AdSetId }
func (a *AdIntegration) GetAdCampaignId() string  { return a.AdCampaignId }

// Status represents the lifecycle state of an ad entity.
type Status string

const (
	PendingStatus Status = "pending"
	RunningStatus Status = "running"
	StoppedStatus Status = "stopped"
)

// FacebookAdTypePlacements configures which Facebook ad types and placements to use.
type FacebookAdTypePlacements struct {
	// Link Click Ads
	// Recommended image size: 1,200 x 628 pixels
	// Ad copy text: 90 characters
	// Headline: 25 characters
	// Link Description: 30 characters
	//
	// Supported placements:
	// Right Column
	// Desktop Newsfeed
	// Mobile Newsfeed
	// Audience Network
	// Instagram
	DoLinkClickAds bool `json:"doLinkClickAds"`

	// Video Ads
	// Ad copy text: 90 characters
	// Aspect ratios supported: 16:9 to 9:16
	// File size: up to 4 GB max
	// Continuous looping available
	// Video can be as long as 120 min., but most top-performing videos are 15-30 seconds
	//
	// Supported placements:
	// Desktop Newsfeed
	// Mobile Newsfeed
	// Audience Network
	// Instagram
	DoVideoAds bool `json:"doVideoAds"`

	// Boosted Page Posts
	// Recommended image size: 1,200 x 628 pixels
	// Ad copy text: unlimited
	// Headline: 25 characters
	// Link Description: 30 characters
	//
	// Supported placements:
	// Desktop Newsfeed
	// Mobile Newsfeed
	// Audience Network
	// Instagram
	DoBoostedPagePosts bool `json:"doBoostedPagePosts"`

	// ... more here:
	// https://adespresso.com/guides/facebook-ads-beginner/facebook-ads-types/

	// Placements
	DoRightColumn     bool `json:"doRightColumn"`
	DoDesktopNewsfeed bool `json:"doDesktopNewsfeed"`
	DoMobileNewsfeed  bool `json:"doMobileNewsfeed"`
	DoAudienceNetwork bool `json:"doAudienceNetwork"`
	DoInstagram       bool `json:"doInstagram"`
}

// StatsWeCareAbout tracks key ad performance metrics.
// add some functionality to fetch these values from counters
type StatsWeCareAbout struct {
	Clicks      int64          `json:"clicks" datastore:"-"`
	Impressions int64          `json:"impressions" datastore:"-"`
	Conversions int64          `json:"conversions" datastore:"-"`
	TotalSpend  currency.Cents `json:"totalSpend" datastore:"-"`
	Currency    currency.Type  `json:"currency" datastore:"-"`
}
