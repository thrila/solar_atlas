import SearchIcon from "/src/assets/search.svg?react";
import SunIcon from "/src/assets/sun.svg?react";
import PopupPortal from "./PopupPortal";
import InfoBlock from "./InfoBlock";

type SolarEstimate = {
  location: string;
  daily_solar_irradiance: number; // e.g., 5.78 kWh/m²/day
  sunlight_hours_per_day: number; // e.g., 9
  azimuth_angle: number; // e.g., 180°
  tilt_angle: number; // e.g., same as latitude
  lat: number;
  lon: number;
  number_of_panels: number;
  output_power: number; // total daily output (kWh/day)
  power_per_household_annually: number; // in kWh/year
  national_energy_demand_annually: number; // in kWh/year
  carbon_saved_annually: number; // in kg CO₂/year
  carbon_intensity: number; // in g CO₂ / kWh
  average_household_size: string; // keep as string if raw from dataset
  kWh_per_person: number; // personal avg consumption/year
  population: number;
};

const EnergyInfo = ({ data, loading }: { data: SolarEstimate; loading: boolean }) => {
  return (
    <div className="w-full max-w-xl flex flex-col justify-start rounded-2xl border border-[#2C2C35] bg-[rgba(26,26,31,0.9)] p-5 text-[#EDEDED] backdrop-blur-md shadow-sm space-y-5">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-medium tracking-tight text-white">Nigeria Solar Summary</h2>
        <span className="text-xs text-[#8FFFE0] border border-[#2C2C35] bg-[#1A1A1F] px-2 py-0.5 rounded-md">
          {loading ? (
            <span className="animate-pulse">•••</span>
          ) : (
            `${(data.output_power / 30).toFixed(0)} kWh/mo`
          )}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm text-[#B0B0B5]">
        <InfoBlock
          label="System Size"
          value={
            loading
              ? ""
              : `${(data.output_power / 1000).toFixed(2)} kW (${data.number_of_panels} panels)`
          }
          loading={loading}
        />
        <InfoBlock
          label="Annual Output"
          value={loading ? "" : `${data.output_power * 365} kWh`}
          loading={loading}
        />
        <InfoBlock
          label="Sunlight"
          value={loading ? "" : `${data.sunlight_hours_per_day} hrs/day`}
          loading={loading}
        />
        <InfoBlock
          label="Irradiance"
          value={loading ? "" : `${data.daily_solar_irradiance} kWh/m²/day`}
          loading={loading}
        />
        <InfoBlock
          label="Azimuth"
          value={loading ? "" : `${data.azimuth_angle}°`}
          loading={loading}
        />
        <InfoBlock
          label="Tilt Angle"
          value={loading ? "" : `${data.tilt_angle.toFixed(1)}°`}
          loading={loading}
        />
        <InfoBlock
          label="Power/Household"
          value={loading ? "" : `${data.power_per_household_annually.toFixed(0)} kWh/year`}
          loading={loading}
        />
        <InfoBlock
          label="National Demand"
          value={loading ? "" : `${(data.national_energy_demand_annually / 1e9).toFixed(1)} B kWh`}
          loading={loading}
        />
        <InfoBlock
          label="Carbon Saved"
          value={loading ? "" : `${(data.carbon_saved_annually / 1000).toFixed(2)} tons CO₂/year`}
          loading={loading}
        />
      </div>

      <div className="border-t border-[#2C2C35] pt-3 text-sm">
        <div className="flex items-center gap-2">
          <SunIcon
            size={10}
            strokeWidth={1.5}
            color="#CFCFCF"
            className="transition-colors duration-300 hover:stroke-[#8FFFE0]"
          />
          <span className="text-[#CFCFCF]">
            {loading ? (
              <span className="animate-pulse">Calculating CO₂ savings…</span>
            ) : (
              `${(data.carbon_saved_annually / 1000).toFixed(2)} tons CO₂/year saved`
            )}
          </span>
        </div>
        {!loading && (
          <p className="text-xs text-[#777] ml-6">
            ≈ {(data.carbon_saved_annually / 21).toFixed(0)} trees planted or{" "}
            {(data.carbon_saved_annually * 0.868).toFixed(0)} mi not driven
          </p>
        )}
      </div>
    </div>
  );
};

export default EnergyInfo;
