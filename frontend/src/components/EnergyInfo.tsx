import SunIcon from "/src/assets/sun.svg?react";
import InfoBlock from "./InfoBlock";
import type { SolarEstimation } from "../types/index";

const EnergyInfo = ({ data, loading }: { data: SolarEstimation; loading: boolean }) => {
  return (
    <div className="w-full max-w-xl flex flex-col justify-start rounded-2xl border border-[#2C2C35] bg-[rgba(26,26,31,0.9)] p-5 text-[#EDEDED] backdrop-blur-md shadow-sm space-y-5">
      <div className="flex items-center justify-between">
        {loading ? (
          <span className="animate-pulse">••••••</span>
        ) : (
          <h2 className="text-sm font-medium tracking-tight text-white">
            {`${data.location} Solar Summary`}
          </h2>
        )}
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
