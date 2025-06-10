import { useState } from "react";

export const useInput = <T extends string | number>(initialValue: T) => {
  const [value, setValue] = useState<T>(initialValue);
  return [
    {
      value,
      onChange: (e: React.ChangeEvent<HTMLInputElement>) => setValue(e.target.value as T),
    },
    () => setValue(initialValue),
  ] as const;
};
