import { createPortal } from "react-dom";

interface Props {
  children: React.ReactNode;
}

export default function PopupPortal({ children }: Props) {
  const popupEl = document.getElementById("popup-root");
  if (!popupEl) return null;

  return createPortal(
    <div
      style={{
        position: "absolute",
        right: `10px`,
        top: `100px`,
        zIndex: 20,
      }}
    >
      {children}
    </div>,
    popupEl,
  );
}
