package model

import (
	"github.com/hanzoai/commerce/datastore"
	"github.com/hanzoai/commerce/models/mixin"
	"github.com/hanzoai/orm"
)

func init() { orm.Register[Media]("media") }

type MediaType string
type MediaUsage string

const (
	ImageType MediaType = "image"
	VideoType MediaType = "video"
)

const (
	AdUsage      MediaUsage = "ad"
	ProductUsage MediaUsage = "product"
	UnknownUsage MediaUsage = "unknown"
)

type Media struct {
	mixin.Model[Media]

	Type MediaType `json:"type"`
	URI  []byte    `json:"uri"`

	ParentMediaId string `json:"parentMediaId,omitempty"`

	// Only for filters and searches, don't rely on this after you get it out
	// of the db. Always check m.ParentMediaId != "".
	IsParent bool `json:"isParent"`

	// Only for filters and searches, don't rely on this after you get it out
	// of the db. Usage is based on which ids(below) are set, always call
	// m.DetermineUsage() to get the correct usage.
	Usage MediaUsage `json:"usage"`

	// Just start adding usage ids here

	// This is for ads
	AdIntegration
	ProductId string `json:"productId,omitempty"`
}

func (m Media) Fork() *Media {
	m2 := NewMedia(m.Datastore())

	m2.AdIntegration = m.AdIntegration
	m2.Type = m.Type
	m2.URI = m.URI
	m2.ParentMediaId = m.Id()
	m2.IsParent = false
	m2.Usage = m.Usage
	m2.ProductId = m.ProductId

	return m2
}

func (m *Media) DetermineUsage() MediaUsage {
	u := UnknownUsage
	if m.AdId != "" {
		u = AdUsage
	} else if m.ProductId != "" {
		u = ProductUsage
	}

	m.Usage = u
	return u
}

func (m *Media) Load(ps []datastore.Property) (err error) {
	// Ensure we're initialized
	m.MediaDefaults()

	// Load supported properties
	return datastore.LoadStruct(m, ps)
}

func (m *Media) Save() (ps []datastore.Property, err error) {
	// Serialize unsupported properties
	m.DetermineUsage()
	m.IsParent = m.ParentMediaId != ""

	// Save properties
	return datastore.SaveStruct(m)
}

func (m Media) GetParentMediaId() string {
	return m.ParentMediaId
}

func (m Media) GetMediaSearchFieldAndIds() (string, []string) {
	return "ParentMediaId", []string{m.Id()}
}

func (m *Media) MediaDefaults() {
	m.Type = ImageType
	m.Usage = UnknownUsage
	m.IsParent = false
}

func NewMedia(db *datastore.Datastore) *Media {
	a := new(Media)
	a.Init(db)
	a.MediaDefaults()
	return a
}

func QueryMedia(db *datastore.Datastore) datastore.Query {
	return db.Query("media")
}
