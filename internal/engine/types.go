package engine

import (
	"github.com/hanzoai/commerce/datastore"
	"github.com/hanzoai/marketing/internal/model"
)

type AdConfigParams struct {
	model.AdConfig

	Headlines []model.Copy  `json:"headlines"`
	Copies    []model.Copy  `json:"copies"`
	Medias    []model.Media `json:"medias"`
}

type CreateInput struct {
	model.AdCampaign

	AdConfigs []AdConfigParams `json:"adConfigs"`
}

type CreateOutput struct {
	AdCampaign *model.AdCampaign
	Entities   []interface{}
}

// Runnable defines the interface for marketing engines.
type Runnable interface {
	Create(*datastore.Datastore, CreateInput) (CreateOutput, error)

	StartAdCampaign(*model.AdCampaign) error
	StopAdCampaign(*model.AdCampaign) error

	StartAdSet(*model.AdSet) error
	StopAdSet(*model.AdSet) error

	StartAd(*model.Ad) error
	StopAd(*model.Ad) error

	Next(*model.AdCampaign, *model.AdConfig, *model.AdSet, *model.Ad) error
}
