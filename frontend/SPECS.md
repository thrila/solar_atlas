### Color Schemes
| Role               | Color Name  | Hex       | Notes                           |
| ------------------ | ----------- | --------- | ------------------------------- |
| **Primary Accent** | Orchid Pink | `#D68FD6` | Soft neon pop for buttons/icons |
| **Secondary**      | Soft Aqua   | `#8FFFE0` | Cool counterpoint, hover states |
| **Background UI**  | Gunmetal    | `#1D1E22` | Panels/sidebar bg (matches map) |
| **Text/Main UI**   | Fog Gray    | `#CFCFCF` | Clean, readable on dark         |
| **Highlight/CTA**  | Coral Dust  | `#FF6B6B` | Warming tone for emotional cues |


Use translucent backgrounds (rgba) for map overlays and modals:
rgba(29,30,34, 0.7) + backdrop-filter: blur(10px) = sleek glassy UI.


### Icons
Use feather icons
with size: 24px 
     Stroke width: 1.5
     Color: #CFCFCF

Austin Solar Estimate
For an average usage of 800 kWh/month, you'll need:

⚡ ~19 panels (6.65 kW system)
🌞 Produces ~9,700 kWh/year (~810/month)
📦 Roof area: ~32 m²
💵 Estimated cost: $13,965 (after 30% ITC)
📉 Payback: ~9–10 years at $0.15/kWh
🌍 Saves 3.9 tons CO₂/year (~97 trees or 9,360 miles)
Austin gets ~5.3 full sun hours/day. Data is based on NREL averages.




### app flow
- user clicks or searches a location (or better still ask users for their location.)
  - the user can choose to enter the amount of electricity he wants or better still use the default which is fetched from the average kwh/year of a household in his country
  - the sidepanel with info shows, while data loads its does the text pulsy thing
  - eventually it fetches and displays the data
  - say the user is location curious and he enters another location, the sidebar is already out and will just display the data he needs

when we click the suggested name, the power and panel number isnt used
