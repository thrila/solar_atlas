declare module "*.svg?react" {
  import * as React from "react";
  interface SVGRProps extends React.SVGProps<SVGSVGElement> {
    size?: number;
    color?: string;
    strokeWidth?: number;
  }
  const ReactComponent: React.FunctionComponent<SVGRProps>;
  export default ReactComponent;
}
