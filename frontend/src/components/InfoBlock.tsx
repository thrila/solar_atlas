const InfoBlock = ({
  label,
  value,
  loading,
}: {
  label: string;
  value: string;
  loading: boolean;
}) => (
  <div className="space-y-0.5" title={value} aria-label={`${label}: ${value}`}>
    <p className="text-[#777] text-xs">{label}</p>
    <p
      className={`text-[#EDEDED] font-medium ${loading ? "animate-pulse bg-[#333] rounded h-4 w-24" : ""}`}
    >
      {loading ? "" : value}
    </p>
  </div>
);

export default InfoBlock;
