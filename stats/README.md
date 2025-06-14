[Data Source for family size by country](https://www.un.org/development/desa/pd/data/household-size-and-composition?utm_source=chatgpt.com)
[Data source for total population of countries](https://population.un.org/wpp/downloads?folder=Standard%20Projections&group=Most%20used)
[Data for total population of countries](https://data.worldbank.org/indicator/SP.POP.TOTL) --- will probably use this
[Data source for energy consumption per country](https://data.worldbank.org/indicator/EG.USE.ELEC.KH.PC)


First off, we want to find how much electricity a family uses in different countries around the world
After that, We will find The daily sun duration of places around the world, the sun entensity,and use a fixed solar panel size(the user can enter the solar panel they have)
with this data we will compute how many kw of electricity the customers unit will generate, or how much gear they will need to generate a specific Kw

### To annual family use per country:
household_kWh = kWh_per_person * avg_household_size








# Note 
> i know that some countries could be using more energy and stuff but for now i just want to see how many panels they will need to match their current supply

- I used the 2022 year column because it has the right amount of valid cells and is the most recent full column
- Also assumes that entities that use electricity use it at an average each month  / day(we know this is not true)



Author: Thrila (@nino_da_creator)
My project: Solar Atlas
Email: ifeanyichukwundubuizu@gmail.com
