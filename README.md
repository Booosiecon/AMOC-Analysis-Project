# AMOC Analysis Assignment2

> 📈 Data analysis for physical oceanography - Geostrophic transport and relating AMOC series


## 📌 Project Structure
```
amoc-analysis/
├── notebooks/                 # Jupyter notebooks for analysis         
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
├── writeup.md                 # write-up
└── ⭐Assignment2_Report.pdf      # pdf version of writeup.md
```

## ✅ Aim

- Compute the 26°N UMO geostrophic transport, compare it with the official UMO product, and compute the correlation coefficient between calcualted UMO transport and the official UMO transport timeseries.

- Calculate and illustrate the monthly climatology of both the 26°N MOC and UMO transport series. Plot the raw and deseasonalised figures for both timeseries.

- Perform an autocorrelation with T* marked, fit a linear trend for both the 26°N MOC and UMO transports series, and find the significance based on $N_eff$.

- Match 2 series, 26°N MOC and 47°N MOC to show a cross-correlation analysis for after removing their seasonal cycles. Draw scatter plots at the peak lag for both raw and deseasonalised data. Evaluate the significance.

- Perform a depth sensitivity analysis for the 26°N UMO transport to assess the effect of different max depths on the integrated transport values.

---

## ⏳ Data 

1. `ts_gridded.nc`. Link: [rapid.ac.uk/data/gridded-mooring-data](https://rapid.ac.uk/data/gridded-mooring-data)

    - The gridded mooring data contains 5 vertical profiles, and all profiles comtain timeseries of 12-hourly temperature and salinity data gridded onto 20m intervals starting in Apr 2004.

2. `moc_transports.nc`. Link: [rapid.ac.uk/data/integrated-transports](https://rapid.ac.uk/data/integrated-transports)

    - 12-hourly, 10-days low pass filtered transport timeseries from Apr 2004 to Mar 2024.


---

## 📚 Useful Resources

- [RAPID-MOCHA Array](https://rapid.ac.uk/rapidmoc)
- [Xarray Documentation](https://xarray.pydata.org/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Physical Oceanography Concepts](https://www.whoi.edu/know-your-ocean/)

