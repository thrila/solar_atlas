import { useRef, useEffect, useState } from "react";
import { useInput } from "../hooks/useInput";
import { ExternalEndpoints } from "../external_services/endpoints";
import SearchIcon from "/src/assets/search.svg?react";
import SettingsIcon from "/src/assets/settings.svg?react";
import UserIcon from "/src/assets/user.svg?react";
import { useMap } from "./MapContext";

export default function TitleBar() {
  const map = useMap();
  const [suggestions, setSuggestions] = useState([]);
  const [searchInput, resetSearchInput] = useInput("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus(); // Autofocus on mount
  }, []);

  useEffect(() => {
    console.log(searchInput.value);
    const timeout = setTimeout(() => {
      if (searchInput.value.length > 3) {
        ExternalEndpoints.getLocationSuggestion(searchInput.value).then((data) => {
          if (data) setSuggestions(data);
        });
      }
    }, 300); // debounce
    return () => clearTimeout(timeout);
  }, [searchInput.value]);

  const handleSubmit = async (location: string) => {
    const { lat, lon } = await ExternalEndpoints.getCoordinatesWithName(location);
    if (map) {
      map.flyTo({
        center: [lon, lat],
        zoom: 10,
        essential: true,
      });
    }
    resetSearchInput();
  };

  return (
    <header className="w-full absolute top-0 z-10">
      <div className="flex flex-row items-center space-x-2 w-[99%] border border-[#2A2B30] bg-[rgba(29,30,34,0.6)] text-white px-4 py-2 rounded-xl my-1 mx-auto">
        <div className="relative w-80">
          <form
            className="flex rounded-full overflow-hidden bg-[#1D1E22] border border-[#2A2B30] shadow-[inset_0_0_1px_#00000066]"
            onSubmit={(e) => {
              e.preventDefault();
              handleSubmit(searchInput.value);
            }}
          >
            <input
              {...searchInput}
              type="search"
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
          </form>

          {/* 🔽 Suggestions Dropdown */}
          {suggestions.length > 0 && (
            <ul className="absolute left-0 right-0 z-50 mt-1 rounded-md bg-[#1D1E22] border border-[#2C2C35] bg-[rgba(29,30,34,0.6)] text-sm text-[#CFCFCF]">
              {suggestions.map((item, idx) => (
                <li
                  key={idx}
                  className="px-4 py-2 cursor-pointer hover:bg-[#2A2B30]  border-t border-[#2C2C35]"
                  onClick={() => handleSubmit(item.name)}
                >
                  {item.display_name}
                </li>
              ))}
            </ul>
          )}
        </div>
        <div>
          {/*NOTE: onclick, make icon turn 360 */}
          <SettingsIcon
            title="Search"
            size={24}
            strokeWidth={1.5}
            color="#CFCFCF"
            className="transition-all duration-300 hover:stroke-[#8FFFE0] hover:rotate-45"
          />
        </div>
      </div>
    </header>
  );
}
