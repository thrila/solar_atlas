import { useRef, useEffect, useState } from "react";
import { useInput } from "../hooks/useInput";
import { ExternalEndpoints } from "../external_services/endpoints";
import SearchIcon from "/src/assets/search.svg?react";
import SettingsIcon from "/src/assets/settings.svg?react";
import { useMap } from "./MapContext";
import type { SolarEstimation, TitleBarProps } from "../types/index";

export default function TitleBar({
  setShowPanel,
  setLocationSolarInfo,
  setLoading,
}: TitleBarProps) {
  const initialPanel = 5;
  const initialPower = 330; // in watts

  const map = useMap();
  const [suggestions, setSuggestions] = useState([]);
  const [searchInput, resetSearchInput] = useInput("");
  const [powerInput] = useInput(initialPower);
  const [panelInput] = useInput(initialPanel);
  const inputRef = useRef<HTMLInputElement>(null);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    inputRef.current?.focus(); // Autofocus on mount
  }, []);

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (searchInput.value.length > 3) {
        ExternalEndpoints.getLocationSuggestion(searchInput.value).then((data) => {
          if (data) setSuggestions(data);
        });
      }
    }, 300); // debounce
    return () => clearTimeout(timeout);
  }, [searchInput.value]);

  const handleSubmit = async (location: string, power: number, numberOfPanels: number) => {
    setShowPanel(() => true);
    setLoading(() => true);
    resetSearchInput();
    setSuggestions([]);
    setOpen(false);
    const { lat, lon } = await ExternalEndpoints.getCoordinatesWithName(location);
    if (map) {
      map.flyTo({
        center: [lon, lat],
        zoom: 10,
        essential: true,
      });
    }
    const test = await ExternalEndpoints.getSolarData({
      lon,
      lat,
      power,
      numberOfPanels,
    });
    setLocationSolarInfo(test);
    console.log(test);
    setLoading(() => false);
  };

  const handleFocus = () => setShowPanel(() => false);
  const renderAdvanced = () => setOpen(() => !open);

  useEffect(() => {
    if (!map) return;

    const handleClick = async (e) => {
      setLoading(true);
      setShowPanel(true);
      const { lng, lat } = e.lngLat;
      map.flyTo({ center: [lng, lat], zoom: 5, essential: true });
      const data = await ExternalEndpoints.getSolarData({
        lon: lng,
        lat,
        power: powerInput.value,
        numberOfPanels: panelInput.value,
      });
      setLocationSolarInfo(data);
      setLoading(false);
    };

    map.on("click", handleClick);
    return () => map.off("click", handleClick);
  }, [map, powerInput.value, panelInput.value]);

  return (
    <header className="w-full absolute top-0 z-10">
      <div
        className={`flex flex-row items-start md:items-center space-x-2 
  w-full md:w-[24rem] 
  justify-center md:justify-start 
  border border-[#2A2B30] bg-[rgba(29,30,34,0.6)] text-white 
  px-4 mx-auto md:ml-0 md:mr-auto my-1 rounded-xl 
  transition-all duration-500 ease-in-out 
  ${open ? "opacity-100 py-3" : "opacity-90 py-2"}`}
      >
        <div className="">
          <div className="relative w-full transition-all duration-300 ease-in-out">
            {/* 🔍 Search Form */}
            <form
              className="flex flex-col space-y-4"
              onSubmit={(e) => {
                e.preventDefault();
                handleSubmit(searchInput.value, powerInput.value, panelInput.value);
              }}
            >
              {/* Search Bar */}
              <div className="flex rounded-full overflow-hidden bg-[#1D1E22] border border-[#2A2B30] shadow-[inset_0_0_1px_#00000066]">
                <input
                  {...searchInput}
                  type="search"
                  onFocus={handleFocus}
                  ref={inputRef}
                  placeholder="Search..."
                  aria-label="Search"
                  className="flex-1 bg-transparent px-4 py-2 text-[#CFCFCF] placeholder-[#888888] placeholder:italic outline-none placeholder:text-sm"
                />
                <button
                  type="submit"
                  title="Search"
                  aria-label="Submit search"
                  className="flex items-center justify-center cursor-pointer px-4 bg-[#1D1E22] hover:stroke-[#8FFFE0] transition-colors hover:animate-wiggle"
                >
                  <SearchIcon size={24} strokeWidth={1.5} color="#CFCFCF" />
                </button>
              </div>

              {/*  Advanced Inputs */}
              {open && (
                <div className="flex space-x-4">
                  <input
                    {...panelInput}
                    type="number"
                    step="any"
                    placeholder="no of solar panels"
                    className="w-full bg-[#1D1E22] border border-[#2A2B30] text-[#CFCFCF] px-4 py-2 placeholder:italic rounded-full outline-none placeholder:text-xs"
                  />
                  <input
                    {...powerInput}
                    type="number"
                    step="any"
                    placeholder="power per panel (W)"
                    className="w-full bg-[#1D1E22] border border-[#2A2B30] text-[#CFCFCF] px-4 py-2 placeholder:italic rounded-full outline-none placeholder:text-xs"
                  />
                </div>
              )}
            </form>

            {/*  Suggestions Dropdown (outside the form) */}
            {suggestions.length > 0 && (
              <ul className="absolute left-0 right-0 z-50 mt-1 rounded-md bg-[#1D1E22] border border-[#2C2C35] bg-[rgba(29,30,34,0.6)] text-sm text-[#CFCFCF]">
                {suggestions.map((item, idx) => (
                  <li
                    key={idx}
                    className="px-4 py-2 cursor-pointer hover:bg-[#2A2B30] border-t border-[#2C2C35]"
                    onClick={() => handleSubmit(item.name, powerInput.value, panelInput.value)}
                  >
                    {item.display_name}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <div className="flex justify-center py-2">
          <button onClick={renderAdvanced} title="Advanced">
            <SettingsIcon
              size={24}
              strokeWidth={1.5}
              color="#CFCFCF"
              className="transition-all duration-300 hover:stroke-[#8FFFE0] hover:rotate-45"
            />
          </button>
        </div>
      </div>
    </header>
  );
}
