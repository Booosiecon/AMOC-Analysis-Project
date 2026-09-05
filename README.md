# AMOC Analysis Assignment2

> 📊 Data analysis for physical oceanography - Geostrophic transport and relating AMOC series


## Project Structure
```
amoc-analysis/
├── venv1/                     # venv environment
├── notebooks/                 # Jupyter notebooks for analysis
│   ├── Assignment1.ipynb           
│   └──  Assignment2.ipynb
├── amoc_analysis/             # Analysis for assignment1
│   ├── _init_.py
│   ├── data.py                
│   ├── analysis.py            
│   └── plotting.py            
├── correlation_trends/        # Analysis for assignment2
│   ├── _init_.py
│   ├── correlation.py
│   ├── data_io.py
│   ├── geostrophy.py
│   ├── seasonal.py
│   ├── trends.py
│   ├── plotting.py
│   └── simple_cal.py          # calculation and report functions
├── figures/
├── tests/                     
│   ├── test_data.py           
│   ├── test_analysis.py 
│   ├── test_correlation.py
│   ├── test_geostrophy.py
│   ├── test_seasonal.py
│   ├── test_trends.py      
│   └── test_plotting.py       
├── data/                      
├── pyproject.toml             # Package configuration
├── requirements.txt           
├── GETTING_STARTED.md  
├── INSTRUCTIONS.md         
└── writeup.md                 # write-up
```


---

## 📊 Data | ts_gridded.nc

The assignment uses boundary hydrography data from the RAPID-MOCHA array at 26°N. Data will be automatically downloaded when you run the analysis functions. Because of the bad internet connection, sometimes the download fails. The dataset includes:

- **Time series / Period**: 2004-present (depending on the run)
- **Variables**: Boundary potential temperature and salinity profiles (`TEMP_`, `PSAL`) at the Western and Eastern boundaries on pressure coordinates.
- **Resolution**: Gridded depth/pressure profiles used for thermal wind calculation.
- **Units**: Practical Salinity Unit (PSU) for salinity, degrees Celsius (°C) for temperature, dbar/m for pressure.


---

## 📚 Useful Resources

- [RAPID-MOCHA Array](https://rapid.ac.uk/rapidmoc)
- [Xarray Documentation](https://xarray.pydata.org/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Physical Oceanography Concepts](https://www.whoi.edu/know-your-ocean/)

