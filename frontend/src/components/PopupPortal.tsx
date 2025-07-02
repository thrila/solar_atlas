import { createPortal } from "react-dom";

interface Props {
  children: React.ReactNode;
}

export default function PopupPortal({ children }: Props) {
  const popupEl = document.getElementById("popup-root");
  if (!popupEl) return null;

  return createPortal(children, popupEl);
}
