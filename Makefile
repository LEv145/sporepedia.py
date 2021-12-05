
.PHONY: mkinit
mkinit:
	mkinit sporepedia --black --nomods --relative > sporepedia/__init__.py
	mkinit sporepedia/api --black --nomods --relative > sporepedia/api/__init__.py
