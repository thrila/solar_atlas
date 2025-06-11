import SearchIcon from "/src/assets/search.svg?react";
import SunIcon from "/src/assets/sun.svg?react";
import PopupPortal from "./PopupPortal";

type SolarEstimate = {
  location: string; // e.g., "Austin, TX"
  monthlyConsumption: number; // in kWh, e.g., 800
  annualConsumption: number; // in kWh/year, e.g., 9600
  systemSizeKw: number; // e.g., 6.65
  panelCount: number; // e.g., 19
  roofSpaceM2: number; // e.g., 32
  annualOutputKwh: number; // e.g., 9700
  costBeforeIncentives: number; // e.g., 19950
  costAfterIncentives: number; // e.g., 13965
  paybackYears: number; // e.g., 9.5
  electricityRate: number; // e.g., 0.15
  co2SavedTonsPerYear: number; // e.g., 3.9
  treesEquivalent: number; // e.g., 97
  milesNotDriven: number; // e.g., 9360
  sunlightHoursPerDay?: number; // optional: e.g., 5.3
};

const EnergyInfo = (Data: SolarEstimate) => {
  return (
    <PopupPortal>
      <div className="w-full max-w-xl rounded-2xl border border-[#2C2C35] bg-[rgba(26,26,31,0.9)] p-5 text-[#EDEDED] backdrop-blur-md shadow-sm space-y-5">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-medium tracking-tight text-white">Austin Solar Summary</h2>
          {/*NOTE: Add title tags to the data spans   */}
          <span className="text-xs text-[#8FFFE0] border border-[#2C2C35] bg-[#1A1A1F] px-2 py-0.5 rounded-md">
            800 kWh/mo
          </span>
        </div>

        <div className="grid grid-cols-2 gap-3 text-sm text-[#B0B0B5]">
          <div
            className="space-y-0.5"
            aria-label="System size: 6.65 kilowatts with 19 panels"
            title="System size: 6.65 kW (19 panels)"
          >
            <p className="text-[#777] text-xs">System Size</p>
            <p className="text-[#EDEDED] font-medium">6.65 kW (19 panels)</p>
          </div>
          <div
            className="space-y-0.5"
            aria-label="Annual Output: 9,700 kWh"
            title="Annual Output: 9,700 kWh"
          >
            <p className="text-[#777] text-xs">Annual Output</p>
            <p className="text-[#EDEDED] font-medium">9,700 kWh</p>
          </div>
          <div className="space-y-0.5" aria-label="Roof Space: 32 m²" title="Roof Space: 32 m²">
            <p className="text-[#777] text-xs">Roof Space</p>
            <p className="text-[#EDEDED] font-medium">32 m²</p>
          </div>
          <div
            className="space-y-0.5"
            aria-label="Sunlight: 5.3hrs/day"
            title="Sunlight: 5.3hrs/day"
          >
            <p className="text-[#777] text-xs">Sunlight</p>
            <p className="text-[#EDEDED] font-medium">5.3 hrs/day</p>
          </div>
          <div className="space-y-0.5" aria-label="Est. Cost: $19,950" title="Est. Cost: $19,950">
            <p className="text-[#777] text-xs">Est. Cost</p>
            <p className="text-[#EDEDED] font-medium">$19,950</p>
            <p className="text-xs text-[#666]">→ $13,965 after ITC</p>
          </div>
          <div
            className="space-y-0.5"
            aria-label="Payback: 9–10 yrs @ $0.15/kWh"
            title="Payback: 9–10 yrs @ $0.15/kWh"
          >
            <p className="text-[#777] text-xs">Payback</p>
            <p className="text-[#EDEDED] font-medium">9–10 yrs @ $0.15/kWh</p>
          </div>
        </div>

        <div className="border-t border-[#2C2C35] pt-3 text-sm">
          <div className="flex items-center gap-2">
            <SunIcon
              size={10}
              strokeWidth={1.5}
              color="#CFCFCF"
              className="transition-colors duration-300 hover:stroke-[#8FFFE0]"
            />
            <span className="text-[#CFCFCF]">3.9 tons CO₂/year saved</span>
          </div>
          <p className="text-xs text-[#777] ml-6">≈ 97 trees planted or 9,360 mi not driven</p>
        </div>
      </div>
    </PopupPortal>
  );
};

export default EnergyInfo;
