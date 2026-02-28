package model

import (
	"github.com/hanzoai/commerce/datastore"
	"github.com/hanzoai/commerce/models/mixin"
	"github.com/hanzoai/orm"
)

func init() { orm.Register[Ad]("ad") }

type FacebookAd struct{}

type Ad struct {
	mixin.Model[Ad]
	FacebookAd
	FacebookAdTypePlacements

	AdConfigId   string `json:"adConfigId"`
	AdSetId      string `json:"adSetId"`
	AdCampaignId string `json:"adCampaignId"`

	// For Caching Purposes
	Headline Copy  `json:"headline"`
	Copy     Copy  `json:"copy"`
	Media    Media `json:"media"`

	Status Status `json:"status"`
}

func (a Ad) GetAdConfigId() string {
	return a.AdConfigId
}

func (a Ad) GetAdSetId() string {
	return a.AdSetId
}

func (a Ad) GetAdCampaignId() string {
	return a.AdCampaignId
}

func (a Ad) GetHeadlineSearchFieldAndIds() (string, []string) {
	return "AdId", []string{a.Id()}
}

func (a Ad) GetCopySearchFieldAndIds() (string, []string) {
	return "AdId", []string{a.Id()}
}

func (a Ad) GetMediaSearchFieldAndIds() (string, []string) {
	return "AdId", []string{a.Id()}
}

func NewAd(db *datastore.Datastore) *Ad {
	a := new(Ad)
	a.Init(db)
	a.Status = PendingStatus
	return a
}

func QueryAd(db *datastore.Datastore) datastore.Query {
	return db.Query("ad")
}
