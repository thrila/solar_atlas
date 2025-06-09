import { createPortal } from "react-dom";

interface Props {
  children: React.ReactNode;
  lngLat: [number, number];
}

export default function PopupPortal({ children, lngLat }: Props) {
  const popupEl = document.getElementById("popup-root");
  if (!popupEl) return null;

  return createPortal(
    <div
      style={{
        position: "absolute",
        left: `${lngLat[0]}px`,
        top: `${lngLat[1]}px`,
        background: "white",
        border: "1px solid #ccc",
        padding: "8px",
        borderRadius: "4px",
        zIndex: 20,
      }}
    >
      {children}
    </div>,
    popupEl,
  );
}
