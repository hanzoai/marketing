package model

import (
	"github.com/hanzoai/commerce/datastore"
	"github.com/hanzoai/commerce/models/mixin"
	"github.com/hanzoai/orm"
)

func init() { orm.Register[AdCampaign]("adcampaign") }

type Engine string

const (
	DemoEngineType Engine = "demo"
)

type FacebookAdCampaign struct{}

type AdCampaign struct {
	mixin.Model[AdCampaign]
	FacebookAdCampaign
	StatsWeCareAbout

	Name   string `json:"name"`
	Engine Engine `json:"engine"`
	Status Status `json:"status"`
}

func (a AdCampaign) GetAdConfigSearchFieldAndIds() (string, []string) {
	return "AdCampaignId", []string{a.Id()}
}

func (a AdCampaign) GetAdSetSearchFieldAndIds() (string, []string) {
	return "AdCampaignId", []string{a.Id()}
}

func (a AdCampaign) GetAdSearchFieldAndIds() (string, []string) {
	return "AdCampaignId", []string{a.Id()}
}

func (a AdCampaign) GetHeadlineSearchFieldAndIds() (string, []string) {
	return "AdCampaignId", []string{a.Id()}
}

func (a AdCampaign) GetCopySearchFieldAndIds() (string, []string) {
	return "AdCampaignId", []string{a.Id()}
}

func (a AdCampaign) GetMediaSearchFieldAndIds() (string, []string) {
	return "AdCampaignId", []string{a.Id()}
}

func NewAdCampaign(db *datastore.Datastore) *AdCampaign {
	a := new(AdCampaign)
	a.Init(db)
	a.Status = PendingStatus
	return a
}

func QueryAdCampaign(db *datastore.Datastore) datastore.Query {
	return db.Query("adcampaign")
}
