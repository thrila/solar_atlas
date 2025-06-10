import { useRef, useEffect } from "react";
import { useInput } from "../hooks/useInput";
import SearchIcon from "/src/assets/search.svg?react";
import SettingsIcon from "/src/assets/settings.svg?react";
import UserIcon from "/src/assets/user.svg?react";
import { useMap } from "./MapContext";

export default function TitleBar() {
  const map = useMap();
  const [searchInput, resetSearchInput] = useInput("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus(); // Autofocus on mount
  }, []);

  const handleSubmit = async (location: string) => {
    const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${location}`);
    const data = await res.json();
    if (data.length > 0 && map) {
      const { lat, lon } = await data[0];
      map.flyTo({
        center: [parseFloat(lon), parseFloat(lat)],
        zoom: 10,
        essential: true,
      });
    }
    resetSearchInput();
  };
  return (
    <header className="w-full absolute top-0 z-10">
      <div className="flex flex-row items-center space-x-2 w-[99%] bg-[rgba(29,30,34,0.6)] text-white px-4 py-2 rounded-xl my-1 mx-auto">
        <form
          className="flex w-80 rounded-full overflow-hidden bg-[#1D1E22] border border-[#2A2B30] shadow-[inset_0_0_1px_#00000066]"
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
            className="flex items-center justify-center cursor-pointer px-4 bg-[#1D1E22] hover:stroke-[#8FFFE0] transition-colors"
          >
            {/*NOTE: add cursor focus */}
            <SearchIcon
              size={24}
              strokeWidth={1.5}
              color="#CFCFCF"
              className="transition-colors duration-300 hover:stroke-[#8FFFE0]"
            />
          </button>
        </form>
        <div>
          {/*NOTE: onclick, make icon turn 360 */}
          <SettingsIcon
            size={24}
            strokeWidth={1.5}
            color="#CFCFCF"
            className="transition-colors duration-300 hover:stroke-[#8FFFE0]"
          />
        </div>

        <div className="  rounded-full bg-red">
          <UserIcon
            size={24}
            strokeWidth={1.5}
            color="#CFCFCF"
            className="transition-colors duration-300 hover:stroke-[#8FFFE0]"
          />
        </div>
      </div>
    </header>
  );
}
