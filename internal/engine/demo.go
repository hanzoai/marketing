package engine

import (
	"github.com/hanzoai/commerce/datastore"
	"github.com/hanzoai/marketing/internal/model"
)

type DemoEngine struct{}

func (d DemoEngine) Create(db *datastore.Datastore, ci CreateInput) (CreateOutput, error) {
	co := CreateOutput{}

	cmpgn := model.NewAdCampaign(db)
	co.AdCampaign = cmpgn
	co.Entities = []interface{}{cmpgn}

	for _, adcfgparams := range ci.AdConfigs {
		cfg := model.NewAdConfig(db)
		cfg.AdCampaignId = cmpgn.Id()
		cfg.FacebookAdTypePlacements = adcfgparams.FacebookAdTypePlacements

		co.Entities = append(co.Entities, cfg)

		as := model.NewAdSet(db)
		as.AdCampaignId = cmpgn.Id()
		as.AdConfigId = cfg.Id()

		co.Entities = append(co.Entities, as)

		for _, headline := range adcfgparams.Headlines {
			co.Entities = append(co.Entities, &headline)
			headline.Init(db)
			headline.AdCampaignId = cmpgn.Id()
			headline.AdConfigId = cfg.Id()
			headline.AdSetId = as.Id()
		}

		for _, cop := range adcfgparams.Copies {
			co.Entities = append(co.Entities, &cop)
			cop.Init(db)
			cop.AdCampaignId = cmpgn.Id()
			cop.AdConfigId = cfg.Id()
			cop.AdSetId = as.Id()
		}

		for _, med := range adcfgparams.Medias {
			co.Entities = append(co.Entities, &med)
			med.Init(db)
			med.Usage = model.AdUsage
			med.AdCampaignId = cmpgn.Id()
			med.AdConfigId = cfg.Id()
			med.AdSetId = as.Id()

			m := med.Fork()
			co.Entities = append(co.Entities, m)

			for _, headline := range adcfgparams.Headlines {
				headline.Init(db)
				h := headline.Fork()
				co.Entities = append(co.Entities, h)

				for _, cop := range adcfgparams.Copies {
					cop.Init(db)
					c := cop.Fork()
					co.Entities = append(co.Entities, c)

					a := model.NewAd(db)
					h.AdId = a.Id()
					c.AdId = a.Id()
					m.AdId = m.Id()

					a.AdCampaignId = cmpgn.Id()
					a.AdSetId = as.Id()
					a.AdConfigId = cfg.Id()
					a.Headline = *h
					a.Copy = *c
					a.Media = *m

					co.Entities = append(co.Entities, a)
				}
			}
		}
	}

	return co, nil
}

func (d DemoEngine) StartAdCampaign(*model.AdCampaign) error { return nil }
func (d DemoEngine) StopAdCampaign(*model.AdCampaign) error  { return nil }
func (d DemoEngine) StartAdSet(*model.AdSet) error           { return nil }
func (d DemoEngine) StopAdSet(*model.AdSet) error            { return nil }
func (d DemoEngine) StartAd(*model.Ad) error                 { return nil }
func (d DemoEngine) StopAd(*model.Ad) error                  { return nil }

func (d DemoEngine) Next(*model.AdCampaign, *model.AdConfig, *model.AdSet, *model.Ad) error {
	return nil
}
