package model

import (
	"errors"

	"github.com/hanzoai/commerce/datastore"
)

// Relationship interfaces for ad entities.

type BelongsToAdCampaign interface {
	GetAdCampaignId() string
}

type BelongsToAdSet interface {
	GetAdSetId() string
}

type BelongsToAdConfig interface {
	GetAdConfigId() string
}

type BelongsToAd interface {
	GetAdId() string
}

type HasAdSets interface {
	GetAdSetSearchFieldAndIds() (string, []string)
}

type HasAdConfigs interface {
	GetAdConfigSearchFieldAndIds() (string, []string)
}

type HasAds interface {
	GetAdSearchFieldAndIds() (string, []string)
}

type HasHeadlines interface {
	GetHeadlineSearchFieldAndIds() (string, []string)
}

type HasCopies interface {
	GetCopySearchFieldAndIds() (string, []string)
}

type HasMedias interface {
	GetMediaSearchFieldAndIds() (string, []string)
}

// Relationship interfaces for copy/media parent entities.

type BelongsToParentCopy interface {
	GetParentCopyId() string
}

type BelongsToParentMedia interface {
	GetParentMediaId() string
}

// Sentinel errors for missing relationships.

var (
	NoAdCampaignFound  = errors.New("No AdCampaign Found")
	NoAdConfigFound    = errors.New("No AdConfig Found")
	NoAdSetFound       = errors.New("No AdSet Found")
	NoAdFound          = errors.New("No Ad Found")
	NoParentCopyFound  = errors.New("No Parent Copy Found")
	NoParentMediaFound = errors.New("No Parent Media Found")
)

// Ad-hierarchy query helpers.

func GetAdCampaign(db *datastore.Datastore, h BelongsToAdCampaign) (*AdCampaign, error) {
	if id := h.GetAdCampaignId(); id == "" {
		return nil, NoAdCampaignFound
	} else {
		a := NewAdCampaign(db)
		err := a.GetById(id)
		return a, err
	}
}

func GetAdSet(db *datastore.Datastore, h BelongsToAdSet) (*AdSet, error) {
	if id := h.GetAdSetId(); id == "" {
		return nil, NoAdSetFound
	} else {
		a := NewAdSet(db)
		err := a.GetById(id)
		return a, err
	}
}

func GetAdConfig(db *datastore.Datastore, h BelongsToAdConfig) (*AdConfig, error) {
	if id := h.GetAdConfigId(); id == "" {
		return nil, NoAdConfigFound
	} else {
		a := NewAdConfig(db)
		err := a.GetById(id)
		return a, err
	}
}

func GetAd(db *datastore.Datastore, h BelongsToAd) (*Ad, error) {
	if id := h.GetAdId(); id == "" {
		return nil, NoAdFound
	} else {
		a := NewAd(db)
		err := a.GetById(id)
		return a, err
	}
}

func GetAdSets(db *datastore.Datastore, h HasAdSets) ([]*AdSet, error) {
	field, keys := h.GetAdSetSearchFieldAndIds()
	results := make([]*AdSet, 0)
	part := make([]*AdSet, 0)
	for _, key := range keys {
		if _, err := QueryAdSet(db).Filter(field+"=", key).GetAll(&part); err != nil {
			return nil, err
		}
		results = append(results, part...)
	}
	return results, nil
}

func GetAdConfigs(db *datastore.Datastore, h HasAdConfigs) ([]*AdConfig, error) {
	field, keys := h.GetAdConfigSearchFieldAndIds()
	results := make([]*AdConfig, 0)
	part := make([]*AdConfig, 0)
	for _, key := range keys {
		if _, err := QueryAdConfig(db).Filter(field+"=", key).GetAll(&part); err != nil {
			return nil, err
		}
		results = append(results, part...)
	}
	return results, nil
}

func GetAds(db *datastore.Datastore, h HasAds) ([]*Ad, error) {
	field, keys := h.GetAdSearchFieldAndIds()
	results := make([]*Ad, 0)
	part := make([]*Ad, 0)
	for _, key := range keys {
		if _, err := QueryAd(db).Filter(field+"=", key).GetAll(&part); err != nil {
			return nil, err
		}
		results = append(results, part...)
	}
	return results, nil
}

func GetCopies(db *datastore.Datastore, h HasCopies) ([]*Copy, error) {
	field, keys := h.GetCopySearchFieldAndIds()
	results := make([]*Copy, 0)
	part := make([]*Copy, 0)
	for _, key := range keys {
		if _, err := QueryCopy(db).Filter("Type=", ContentType).Filter(field+"=", key).GetAll(&part); err != nil {
			return nil, err
		}
		results = append(results, part...)
	}
	return results, nil
}

func GetHeadlines(db *datastore.Datastore, h HasHeadlines) ([]*Copy, error) {
	field, keys := h.GetHeadlineSearchFieldAndIds()
	results := make([]*Copy, 0)
	part := make([]*Copy, 0)
	for _, key := range keys {
		if _, err := QueryCopy(db).Filter("Type=", HeadlineType).Filter(field+"=", key).GetAll(&part); err != nil {
			return nil, err
		}
		results = append(results, part...)
	}
	return results, nil
}

func GetMedias(db *datastore.Datastore, h HasMedias) ([]*Media, error) {
	field, keys := h.GetMediaSearchFieldAndIds()
	results := make([]*Media, 0)
	part := make([]*Media, 0)
	for _, key := range keys {
		if _, err := QueryMedia(db).Filter(field+"=", key).GetAll(&part); err != nil {
			return nil, err
		}
		results = append(results, part...)
	}
	return results, nil
}

// Copy/Media parent query helpers.

func GetParentCopy(db *datastore.Datastore, h BelongsToParentCopy) (*Copy, error) {
	if id := h.GetParentCopyId(); id == "" {
		return nil, NoParentCopyFound
	} else {
		m := NewCopy(db)
		err := m.GetById(id)
		return m, err
	}
}

func GetParentMedia(db *datastore.Datastore, h BelongsToParentMedia) (*Media, error) {
	if id := h.GetParentMediaId(); id == "" {
		return nil, NoParentMediaFound
	} else {
		m := NewMedia(db)
		err := m.GetById(id)
		return m, err
	}
}

// Copy-specific query helpers (duplicate from copy/util, kept for backward compat).

func GetCopiesForParent(db *datastore.Datastore, h HasCopies) ([]*Copy, error) {
	field, keys := h.GetCopySearchFieldAndIds()
	results := make([]*Copy, 0)
	part := make([]*Copy, 0)
	for _, key := range keys {
		if _, err := QueryCopy(db).Filter(field+"=", key).GetAll(&part); err != nil {
			return nil, err
		}
		results = append(results, part...)
	}
	return results, nil
}

// Media-specific query helpers (duplicate from media/util, kept for backward compat).

func GetMediasForParent(db *datastore.Datastore, h HasMedias) ([]*Media, error) {
	field, keys := h.GetMediaSearchFieldAndIds()
	results := make([]*Media, 0)
	part := make([]*Media, 0)
	for _, key := range keys {
		if _, err := QueryMedia(db).Filter(field+"=", key).GetAll(&part); err != nil {
			return nil, err
		}
		results = append(results, part...)
	}
	return results, nil
}
