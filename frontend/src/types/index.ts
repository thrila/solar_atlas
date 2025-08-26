export type TitleBarProps = {
  setShowPanel: React.Dispatch<React.SetStateAction<boolean>>;
  setLocationSolarInfo: React.Dispatch<React.SetStateAction<SolarEstimation>>;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
};

export type SolarDataType = {
  long: number;
  lat: number;
  power: number;
  numberOfPanels: number;
};

export type Suggestion = {
  name: string;
  display_name: string;
};

export type SolarEstimation = {
  location: string;
  daily_solar_irradiance: number;
  sunlight_hours_per_day: number;
  azimuth_angle: number;
  tilt_angle: number;
  lat: number;
  lon: number;
  number_of_panels: number;
  output_power: number;
  power_per_household_annually: number;
  national_energy_demand_annually: number;
  carbon_saved_annually: number;
  carbon_intensity: number;
  average_household_size: string;
  kWh_per_person: number;
  population: number;
};
