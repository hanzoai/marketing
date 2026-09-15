package engine

import (
	"github.com/hanzoai/commerce/datastore"
	"github.com/hanzoai/commerce/models/multi"
	"github.com/hanzoai/marketing/internal/model"
)

// Create dispatches campaign creation to the appropriate engine.
func Create(db *datastore.Datastore, ci CreateInput) (cmpgn *model.AdCampaign, err error) {
	co := CreateOutput{
		nil,
		[]interface{}{},
	}

	switch ci.Engine {
	default:
		if co, err = (DemoEngine{}.Create(db, ci)); err != nil {
			return nil, err
		}
	}

	return co.AdCampaign, multi.Create(co.Entities)
}
