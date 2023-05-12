import React from "react";
import Image from "react-bootstrap/Image";

import Logo from "../../assets/image/search-flat.png";

export default function Header() {
  return (
    <div className="header">
      <span>I</span>
      <Image src={Logo} width={73} height={73} roundedCircle />
      <span>U</span>
    </div>
  );
}
