# Screen Frame and Bezel Tolerances

Got the calipers out and measured the 10.1" Waveshare display module to start modeling the front bezel.

## Screen measurements
- Outer glass frame: 235.0mm wide x 150.0mm tall
- Active display area: 217.0mm x 136.0mm
- Total panel depth: 6.8mm (including the controller PCB on the back)
- DSI ribbon connector location: centered on the lower edge, needs a 22mm x 4mm pass-through slot so the flat flex cable doesn't get pinched against the frame

## 3D print tolerances (PETG)
- Added +0.4mm total clearance on the inner pocket (235.4mm x 150.4mm x 7.2mm deep). PETG tends to shrink a tiny bit and corners can pull in, so without that margin the glass would get wedged or crack when tightening screws.
- Face bezel overlap: 5mm rim around the active area to hold the glass firmly in place while hiding the raw display borders.

## Mounting with M3 heat-set inserts
- Putting 4 mounting bosses on the back of the bezel corners.
- Hole size: 4.2mm diameter x 6.0mm deep for standard M3 x 4mm brass inserts.
- Sunk with a soldering iron set to 230C so the brass melts cleanly into the plastic without creating a bulge on the front face.

## Angle test
Tested cardboard mockups at 60, 65, and 75 degrees.
- 75 degrees was too upright, felt like looking at a wall and had bad reflection from the desk lamp.
- 60 degrees took up too much desk depth.
- 65 degrees is the sweet spot: perfectly perpendicular to your eyes when sitting ~50cm away, and keeps the whole desk footprint under 140mm deep.
