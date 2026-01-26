# ARt Viewer - PINUS Hack 2026

An augmented reality web application that allows users to visualize artwork in their physical space using their smartphone camera.

## Team: Pinusoverclock

**Track 4: AI for Virtual Viewing & Decision Support**

## Quick Start

### 1. Print the Hiro Marker

You need a physical marker for the AR to work. Print or display this marker on your screen:

![Hiro Marker](https://raw.githubusercontent.com/AR-js-org/AR.js/master/data/images/hiro.png)

You can also download it here: [Hiro Marker PDF](https://github.com/AR-js-org/AR.js/blob/master/data/images/hiro.png)

### 2. Open the App

Visit the live demo: **[Your GitHub Pages URL will be here]**

Or run locally:
```bash
# Clone the repository
git clone https://github.com/ImNuza/pinusoverclock.git
cd pinusoverclock

# Start a local server (Python)
python3 -m http.server 8000

# Or use Node.js
npx serve .
```

Then open `http://localhost:8000` on your phone (must be on same WiFi network).

### 3. Point Your Camera

1. Open the app on your smartphone
2. Allow camera access when prompted
3. Point your camera at the Hiro marker
4. The 3D artwork will appear on the marker!

## Features

- **AR Artwork Visualization**: See 3D artwork models in your real environment
- **Multiple Artworks**: Switch between different artwork models
- **Mobile-First**: Designed for smartphone browsers
- **No App Install**: Works directly in Safari (iOS) or Chrome (Android)

## Project Structure

```
pinusoverclock/
├── index.html          # Main AR application
├── models/             # 3D model files (.glb)
│   └── decor_wall.glb  # Decor wall artwork
├── markers/            # AR marker images
└── README.md           # This file
```

## Technology Stack

- **A-Frame**: Web VR/AR framework
- **AR.js**: Augmented reality library for the web
- **glTF/GLB**: 3D model format

## Browser Compatibility

| Browser | Status |
|---------|--------|
| Safari (iOS) | ✅ Supported |
| Chrome (Android) | ✅ Supported |
| Chrome (Desktop) | ⚠️ Limited (no AR) |
| Firefox | ⚠️ Limited |

## Team Members

| Name | Role |
|------|------|
| Nuza | Project Lead, UX/Pitch |
| Matthew | Business Logic, Demo Video |
| Michael | Lead Developer |
| Bryan | Frontend Developer |
| Noah | Backend, AI Integration |

## Development

### Adding New Artwork Models

1. Export your 3D model as `.glb` format
2. Place the file in the `models/` directory
3. Add a new asset in `index.html`:
   ```html
   <a-asset-item id="new-model" src="models/new_model.glb"></a-asset-item>
   ```
4. Add a button to switch to the new model

### Converting FBX to GLB

If you have FBX files, convert them using:
```bash
# Using FBX2glTF
./FBX2glTF -b -i input.fbx -o output
```

## Troubleshooting

**Camera not working?**
- Make sure you're using HTTPS or localhost
- Check that camera permissions are granted

**Model not appearing?**
- Ensure the marker is well-lit and flat
- Keep the marker fully visible in frame
- Check browser console for errors

**Model too big/small?**
- Adjust the `scale` attribute in the `<a-entity>` tag

## License

MIT License - PINUS Hack 2026

## Acknowledgments

- PINUS Hack 2026 Organizers
- Manus & Xtremax (Sponsors)
- AR.js Community
