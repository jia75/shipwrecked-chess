all: bld/quadchess.zip

bld/quadchess.zip: src/main.py src/manifest.json
	zip bld/quadchess.zip src/main.py src/manifest.json
