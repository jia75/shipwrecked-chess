all: bld/quadchess.zip

bld/quadchess.zip: src/main.py src/manifest.json src/logo.pbm
	cd src && zip ../bld/quadchess.zip main.py manifest.json logo.pbm
