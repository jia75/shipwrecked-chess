all: bld/quadchess.zip

bld/quadchess.zip: src/main.py src/manifest.json
	cd src && zip ../bld/quadchess.zip main.py manifest.json
