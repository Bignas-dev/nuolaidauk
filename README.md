# Nuolaidauk

Programėlė, kuri turi visų prekybos centrų nuolaidines programėles

## Build Android APK

### Method 1: Using Google Colab (Recommended)

1. Open the `build_apk_colab.ipynb` notebook in Google Colab
2. Follow the instructions in the notebook to build and download the APK

### Method 2: Using GitHub Actions

1. Push your code to GitHub
2. Go to the Actions tab in your GitHub repository
3. Run the "Build Android APK" workflow
4. Download the APK from the workflow artifacts

### Method 3: Using Buildozer Locally

Prerequisites:
- Python 3.11+
- Buildozer

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip build-essential git python3 python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev

# Generate icons
uv run data/generate_icon.py

# Build the APK
buildozer android debug
```

## Palaikomos programėlės

- [x] Iki
- [x] Senukai
- [ ] Maxima
- [ ] Lidl
- [ ] Rimi
- [ ] Norfa
- [ ] Norfa Vaistine
- [ ] ePromo
- [ ] Viada
- [ ] Circle K
- [ ] Eurovaistine
- [ ] IKEA
- [ ] McDonalds
- [ ] Drogas
- [ ] Benu Vaistine
- [ ] Gintarine
- [ ] Pigu.lt
- [ ] Ermitazas
- [ ] Cili Pica
- [ ] Mumbo
- [ ] Aibe 
- [ ] Elektromarkt
- [ ] Avon
- [ ] Bikuva
- [ ] Camelia Vaistine
- [ ] Cia
- [ ] Douglas
- [ ] Eurokos
- [ ] Gruste
- [ ] Express Market
- [ ] JYSK
- [ ] Koops
- [ ] Kubas
- [ ] Ogmina
- [ ] Oriflame
- [ ] PEPCO
- [ ] Promo
- [ ] Ramuneles Vaistine
- [ ] Vynoteka
- [ ] Thomas Phillips
- [ ] Silas
- [ ] Tau
- [ ] Batu Kalnas
- [ ] 
